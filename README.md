# WEB SCRAPING AND DATA ANALYSIS

In this project is to generate data for Walt Disney movies I scraped the [Walt Disney Wikipedia](https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films) page and crawled to each movie to get infomation about the movie.

## SETUP

To Replicate this project do the following:
- Install conda or miniconda you can do that using the installation [guide](https://docs.anaconda.com/anaconda/install/)
- Create a new environment `conda create -n <environment_name>` this is to make sure you don't clash with any other dependencies you have from other programs
- Activate the created environment ` conda activate <environment_name>`
- Install dependencies
```bash
pip install -r requirements.txt
````

## Other Information

- You can check the data in [movie_dataset](https://github.com/codebasetwo/movie-scraper/tree/main/movie_datasets)
- You can run the script in [scraper folder](https://github.com/codebasetwo/movie-scraper/blob/main/scraper/web_scraper.py) To generate your own dataset for further cleaning

## Project Scope

The project covered the following:
- concurrency with asyncio, aiohtpp and httpx
- webscraping using beautiful soup
- data wrangling and cleaning pandas and python
- data analytics pandas and matplotlib
- making API requests

Ultimately you can create your own API by cleaning the data properly and hosting it on a web where people can retrieve information of disney movies.
