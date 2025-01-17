import re
import httpx
from bs4 import BeautifulSoup as bs

DATE_REGEX = r'\w+\s\d{1,2},\s\d{4}|\d{1,2}\s\w+\s\d{4}|\d{4}'

def get_italics_tag(tags):
    urls = [tag["href"] for tag in tags]
    return urls


def get_disney_urls(url):
    response = httpx.get(url)
    walt_disney_html = response.content
    walt_disney_bs = bs(walt_disney_html)
    # walt_disney_bs.prettify()
    # table = walt_disney_bs.find_all('table', {'class': 'wikitable sortable'})
    italics_tag = walt_disney_bs.select(".wikitable.sortable i a")
    urls = get_italics_tag(italics_tag)
    
    return urls

def remove_tags(soup):
    tags = soup.find_all(['sup', 'span'])
    for tag in tags:
        tag.decompose()


def replace_string(string):
    return string.replace('\xa0', ' ')


def find_html(row, tag = 'th'):
    return row.find(tag).get_text(' ', strip=True)


def get_field_data(row):
    table_data = row.find('td')
    if table_data.find('li'):
        producers = [replace_string(producer.get_text(' ', strip=True))for producer in table_data.find_all('li')]
        return producers
    
    elif table_data.find('br'):
        return [text for text in table_data.stripped_strings]

    return replace_string(find_html(row, tag='td'))


def get_info_box(movies_bs):
    
    info_box = movies_bs.find(class_="infobox vevent")
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

def clean_minutes(running_time):
    if running_time == 'N/A':
        return None
    if isinstance(running_time, list):
        return int(running_time[0].split(' ')[0])
    return int(re.split("\s|\n", running_time)[0])


def clean_date(value):
    if isinstance(value, list) and len(value) > 1:
        # Get release date for US
        value = value[1]
    else:
        value = value[0]

    string = re.search(DATE_REGEX, value).group()
    return string


def get_movie_titles(movie_data):
    movie_titles = []
    for movie in movie_data:
        title = movie.get('Title', 'N/A')
        movie_titles.append(title)

    return movie_titles