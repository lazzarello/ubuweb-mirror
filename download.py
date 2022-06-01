# from urllib import request
import requests
from bs4 import BeautifulSoup

FILM_URL = "https://www.ubu.com/film/index.html"
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
    print(artist.text.strip())
