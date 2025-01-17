import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
import aiohttp
from pathlib import Path
from dotenv import load_dotenv

from utils.utils import get_movie_titles
from utils.data_utils import load_pickle

load_dotenv()
omdb_key = os.getenv('OMDB')
url = 'https://www.omdbapi.com/?'

async def get_omdb_info(title: str, url: str='https://www.omdbapi.com' ):
  params = {
      'apikey': omdb_key,
      't': title
  }
  async with aiohttp.ClientSession() as session:
      async with session.get(url, params=params) as response:
          return await response.json()


async def omdb_main(movie_data):
    # List of movie titles to fetch information for
    movie_titles = get_movie_titles(movie_data)

    # Use asyncio.gather to concurrently fetch information for each movie
    tasks = [get_omdb_info(title) for title in movie_titles]
    movie_infos = await asyncio.gather(*tasks)

    # Return the fetched information
    return movie_infos

if __name__ == "__main__":
    movie_data = load_pickle(Path('./movie_datasets/disney_movies.pickle'))
    asyncio.run(omdb_main(movie_data))   

