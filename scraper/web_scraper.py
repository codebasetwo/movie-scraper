import os
import sys
import asyncio
from pathlib import Path
from tqdm.asyncio import tqdm_asyncio

import httpx
from bs4 import BeautifulSoup as bs
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_utils import save_json
from utils.utils import get_disney_urls, get_info_box


DEST_DIR = Path('movie_data/')
BASE_URL = 'https://en.wikipedia.org'
DISNEY_URL = 'https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films'

async def get_movie_content(url, client: httpx.AsyncClient, semaphore: asyncio.Semaphore):
    """
    Asynchronous function to fetch movie content from a given URL using an HTTP client
    and a semaphore for concurrency control.

    Parameters:
    url (str): The URL to fetch the movie content from.
    client (httpx.AsyncClient): The asynchronous HTTP client to make the requests.
    semaphore (asyncio.Semaphore): The semaphore to limit the number of concurrent requests.

    Returns:
    dict: A dictionary containing movie information, or None if an error occurs.
    """

    url = f'{BASE_URL}{url}'
    async with semaphore:
        try:
            response = await client.get(url, timeout=15,
                                        follow_redirects=True )
        except httpx.HTTPStatusError as e:
            print(f'HTTP error occurred: {e}')  # Log HTTP errors
            return None
        except httpx.RequestError as e:
            print(f'Request error occurred: {e}')  # Log request errors
            return None
        except asyncio.TimeoutError:
            print('Request timed out')  # Log timeout errors
            return None
        
    movie_html = response.content
    movie_bs = bs(movie_html)
    movie_info = None
    try:
        movie_info = get_info_box(movie_bs)
    except Exception as e:
        print(f'Error: {e} in extracting movie information')  # Log extraction errors     

    return movie_info


async def get_many_movie_content(urls):
    semaphore = asyncio.Semaphore(32)
    async with httpx.AsyncClient() as client:
        to_do = [get_movie_content(url, client, semaphore) for url in urls]
        results = await tqdm_asyncio.gather(*to_do)

    return results


def get_page_html(urls):
    """
    Synchronously runs the asynchronous function 
    to get movie content for multiple URLs.

    Parameters:
        urls (list): A list of URLs to fetch movie content from.

    Returns:
        list: A list of movie information dictionaries.
    """
    return asyncio.run(get_many_movie_content(urls))


def main():
    """
    Main function to fetch movie content from Disney
    URLs and print the results.

    Returns:
        list: A list of movie information dictionaries.
    """
    try:
        disney_urls = get_disney_urls(DISNEY_URL)
        results = get_page_html(disney_urls)
        print(f'Retrieved {len(results)} movies:')

    except Exception as e:
        print(f'Error in main: {e}')  # Log any errors that occur in the main function
        return []
            
    return results

# To run the script directly
if __name__ == '__main__':
    results = main()
    # Remove all None value from list
    result = list(filter(None, results))

    # Make a directory to store results
    DEST_DIR.mkdir(exist_ok=True)
    save_json(f'{DEST_DIR}/disney_movies.json', result)