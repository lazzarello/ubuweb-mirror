# https://realpython.com/beautiful-soup-web-scraper-python/
# URL stuff
import requests
# Scraping the DOM
from bs4 import BeautifulSoup
# Progress bar
from tqdm import tqdm
# custom data models
from models import Artist, Work
import random
from constants import *

class Page:
    # can very likely abstract much of this into a single function
    def get_artists(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        tables = soup.find_all("table")
        links = tables[1].find_all("a")
        artists = []
        for artist in links:
            a = Artist()
            a.name = artist.text.strip() 
            a.url = BASE_FILM_URL + artist["href"]
            artists.append(a)
        # this convention removes the left nav bar links.
        artists.pop(0)
        return artists

    def get_artist_works(self, artist):
        page = requests.get(artist.url)
        soup = BeautifulSoup(page.content, "html.parser")
        tables = soup.find_all("table")
        links = tables[1].find_all("a")
        works = []
        for work in links:
            w = Work()
            w.name = work.text.strip()
            w.url = BASE_FILM_URL + work["href"]
            w.artist = artist
            works.append(w)
        # this convention removes the left nav bar links.
        for _ in range(2):
            works.pop(0)
        return works

if __name__ == "__main__":
    page = Page()
    artists_page = page.get_artists(FILM_URL)
    artist = artists_page[random.choice(range(100))]
    print(artist)
    artist_works = page.get_artist_works(artist)
    work = artist_works[0]
    work.get_work_movie(work)
    work.download_work()
