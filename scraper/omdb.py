import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
import aiohttp
from pathlib import Path
from dotenv import load_dotenv
from tqdm.asyncio import tqdm_asyncio

from utils.utils import get_movie_titles
from utils.data_utils import load_pickle, save_pickle

load_dotenv()
# Get key from env file
OMDB_KEY = os.getenv('OMDB')

async def get_omdb_info(title: str, url: str='https://www.omdbapi.com' ):
    """
    Asynchronously fetch movie information from OMDB API for a given title.

    Parameters:
    title (str): The title of the movie to fetch information for.
    url (str): The OMDB API endpoint (default: 'https://www.omdbapi.com').

    Returns:
    dict: The JSON response containing movie information.
    """  
    params = {
      'apikey': OMDB_KEY,
      't': title
  }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            try:
                return await response.json()
            except aiohttp.ClientError as e:
                print(f'Fetching error for {title}: {e}')
                return {}


async def omdb_file(movie_data, path: Path='../movie_datasets/omdb_movies.pickle'):
    """
    Fetch OMDB information for a list of movies and save it to a pickle file.

    Parameters:
        movie_data (list): A list containing movie titles or data.
        path (Path): The path to save the pickle file \
        (default: '../movie_datasets/omdb_movies.pickle').

    """    
    # List of movie titles to fetch information for
    movie_titles = get_movie_titles(movie_data)

    # Use asyncio.gather to concurrently fetch information for each movie
    tasks = [get_omdb_info(title) for title in movie_titles]
    movie_infos = await tqdm_asyncio.gather(*tasks)

    # Save the fetched information to a pickle file using
    # a predefined function `save_pickle`
    save_pickle(path, movie_infos)

async def omdb_main(movie_data):
    """
    Main function to orchestrate fetching OMDB information and saving it.

    Parameters:
        movie_data (list): A list containing movie titles or data.
    """
    await omdb_file(movie_data)

if __name__ == "__main__":
    # Load the movie dataset using a predefined function `load_pickle`
    movie_data = load_pickle(Path('../movie_datasets/disney_movies.pickle'))
    asyncio.run(omdb_file(movie_data))

