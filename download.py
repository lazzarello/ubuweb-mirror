# https://realpython.com/beautiful-soup-web-scraper-python/
import requests
from bs4 import BeautifulSoup

FILM_URL = "https://www.ubu.com/film/index.html"
BASE_FILM_URL = "https://www.ubu.com/film/"
content_type = "artists"
download_path = "/home/lee/Videos/ubuweb"

def list_artists(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    tables = soup.find_all("table")
    links = tables[1].find_all("a")
    return links

artist_elements = list_artists(FILM_URL)
for artist in artist_elements:
    artist_name = artist.text.strip() 
    artist_url = artist["href"]
    print(f'Artist {artist_name} is at URL {BASE_FILM_URL+artist_url}')
