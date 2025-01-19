import re
import httpx
from bs4 import BeautifulSoup as bs

DATE_REGEX = r'\w+\s\d{1,2},\s\d{4}|\d{1,2}\s\w+\s\d{4}|\d{4}'

def get_italics_tag(tags):
    urls = [tag["href"] for tag in tags]
    return urls


def get_disney_urls(url):
    """
    Extracts URLs from italicized text within a wikitable on a Disney webpage.

    Args:
        url (str): The URL of the Disney webpage.

    Returns:
        list: A list of extracted URLs.
    """
    response = httpx.get(url)
    walt_disney_html = response.content
    walt_disney_bs = bs(walt_disney_html)
    # walt_disney_bs.prettify()
    # table = walt_disney_bs.find_all('table', {'class': 'wikitable sortable'})
    italics_tag = walt_disney_bs.select(".wikitable.sortable i a")
    urls = get_italics_tag(italics_tag)
    
    return urls

def remove_tags(soup):
    """
    Removes specific tags (sup and span) from a BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object to modify.
    """
    tags = soup.find_all(['sup', 'span'])
    for tag in tags:
        tag.decompose()


def replace_string(string):
    """
    Replaces a non-breaking space character with a regular space.

    Args:
        string (str): The string to modify.

    Returns:
        str: The modified string with non-breaking spaces replaced.
    """
    return string.replace('\xa0', ' ')


def find_html(row, tag = 'th'):
    """
    Finds text within a specified HTML tag (default: th) in a table row.

    Args:
        row (bs4.element.Tag): The table row element.
        tag (str, optional): The HTML tag to search for. Defaults to 'th'.

    Returns:
        str: The text content within the specified tag, or an empty string if not found.
    """
    return row.find(tag).get_text(' ', strip=True)


def get_field_data(row):
    """
    Extracts data from a table data cell (td), handling different content formats (lists, breaks).

    Args:
        row (bs4.element.Tag): The table row element containing the data cell.

    Returns:
        list or str: The extracted data, either a list of strings or a single string.
    """
    table_data = row.find('td')
    if table_data.find('li'):
        producers = [replace_string(producer.get_text(' ', strip=True))for producer in table_data.find_all('li')]
        return producers
    
    elif table_data.find('br'):
        return [text for text in table_data.stripped_strings]

    return replace_string(find_html(row, tag='td'))


def get_info_box(movies_bs):
    """ 
    Extract information from the infobox in the provided BeautifulSoup object.

    Args: 
        movies_bs (BeautifulSoup): A BeautifulSoup object containing the movie's HTML.

    Returns:
        dict: A dictionary containing the movie information extracted from the infobox.
      
    Raises:
        ValueError: If the infobox is not found. 
      """
    try:
        info_box = movies_bs.find(class_="infobox vevent")
        if not info_box:  # Check if info_box is found
            raise ValueError("Infobox not found")
        
        remove_tags(info_box)
        info_table = info_box.find_all('tr')

        movie_info = {}
        for index, row in enumerate(info_table):
            if index == 0:
                movie_info['Title'] = find_html(row)
            else:
                header = row.find('th')
                if header:
                    title = find_html(row)
                    data = get_field_data(row)
                    movie_info[title] = data
            
        return  movie_info
    
    except Exception as e:
        print(f"An error occurred in get_info_box: {e}")
        return {}

def clean_minutes(running_time):
    """ 
    Clean and convert running time to minutes.
    Args: 
        running_time (str or list): Running time as a \
            string or list of strings.

    Returns: 
        int or None: Running time in minutes, or None if not available or \
            an error occurs. 
    """
    try:
        if running_time == 'N/A':
            return None
        if isinstance(running_time, list):
            return int(running_time[0].split(' ')[0])
        
        return int(re.split("\s|\n", running_time)[0])
    
    except (ValueError, AttributeError) as e:
        print(f"An error occurred in clean_minutes: {e}")
        return None

def clean_date(value):
    """ 
    Clean and extract date from value. 
    Args: 
        value (list): A list containing date strings.

    Returns: 
        str or None: Cleaned date string, or None if an error occurs. 
        
    Raises: 
    IndexError: If an invalid index is accessed. 
    AttributeError: If a string method is called on a NoneType. 
    """
    try:
        if isinstance(value, list) and len(value) > 1:
            # Get release date for US
            value = value[1]
        else:
            value = value[0]

        string = re.search(DATE_REGEX, value).group()
        return string
    
    except (IndexError, AttributeError) as e:
        print(f"An error occurred in clean_date: {e}")
        return None

def get_movie_titles(movie_data):
    """ 
    Retrieve movie titles from movie data. 
    Args: 
        movie_data (list): A list of dictionaries containing movie information.

    Returns: 
        list: A list of movie titles, or 'N/A' if the title is not available. 
    """
    movie_titles = []
    for movie in movie_data: # Iterate through all movie data dictionaries
        title = movie.get('Title', 'N/A') # Get the title or return 'N/A' if not found
        movie_titles.append(title) # Append the title to the list

    return movie_titles


def get_rotten_tomoatoes_score(data, key='Ratings'):
    """ 
    Get Rotten Tomatoes score from the provided data dictionary. 
    Args: 
    data (dict): A dictionary containing movie information. 
    key (str): The key to access the ratings data (default is 'Ratings').

    Returns: 
        str or None: The Rotten Tomatoes rating value, or 
        None if not available or an error occurs. 
    """
 
    ratings = data.get(key, None) # Retrieve ratings with the specified key
    if ratings is None: # Check if ratings are not available
        return None
    
    for dict_ in ratings: # Loop through each rating dictionary
        rotten_tomoatoes_score = dict_.get('Source', None) # Get the source of the rating
        if rotten_tomoatoes_score == 'Rotten Tomatoes': # Check if the source is Rotten Tomatoes
            value = dict_.get('Value', None) # Return the Rotten Tomatoes rating value
            return value