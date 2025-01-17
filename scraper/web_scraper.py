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
    url = f'{BASE_URL}{url}'
    async with semaphore:
        response = await client.get(url, timeout=15,
                                    follow_redirects=True )
    movie_html = response.content
    movie_bs = bs(movie_html)
    movie_info = None
    try:
        movie_info = get_info_box(movie_bs)
    except Exception as e:
        print(f'Error: {e} 1')     

    return movie_info


async def get_many_movie_content(urls):
    semaphore = asyncio.Semaphore(32)
    async with httpx.AsyncClient() as client:
        to_do = [get_movie_content(url, client, semaphore) for url in urls]
        results = await tqdm_asyncio.gather(*to_do)

    return results


def get_page_html(urls):
    return asyncio.run(get_many_movie_content(urls))


def main():
    disney_urls = get_disney_urls(DISNEY_URL)
    results = get_page_html(disney_urls)
    print(results, len(results))  
    return results

if __name__ == '__main__':
    results = main()
    result = list(filter(None, results))

    DEST_DIR.mkdir(exist_ok=True)
    save_json(f'{DEST_DIR}/disney_movies.json', result)