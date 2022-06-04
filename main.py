# custom data models
from models import Artist, Work, Page
import random
from constants import *
import logging

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(message)s",
                    filename="transfers.log",
                    filemode="a"
        )

def download_random_work_from(artists):
    page = Page()
    r = len(artists)
    artist = artists[random.choice(range(r))]
    logging.debug(f"Artist is: {print(artist)}")
    artist_works = page.get_artist_works(artist)
    r = len(artist_works)
    work = artist_works[random.choice(range(r))]
    work.set_download_url(work)
    work.download_work()

def download_all_works_from(artist):
    logging.debug(f"Artist is: {print(artist)}")
    page = Page()
    artist_works = page.get_artist_works(artist)
    for work in artist_works:
        work.set_download_url(work)
        if work.download_url:
            work.download_work()

def main():
    page = Page()
    artists_page = page.get_artists(FILM_URL)
    for artist in artists_page:
        download_all_works_from(artist)
    # r = len(artists_page)
    # download_all_works_from(artists_page[random.choice(range(r))])
    # download_random_work_from(artists_page)
    # https://www.ubu.com/film/clarke_ornette.html
    # this index uses Javascript to render the link to media. the
    # streaming video uses a service called https://criticalcommons.org/embed?m=fwqF8eomo
    # which is not valid in youtube-dl
    # download_all_works_from(artists_page[215])

if __name__ == "__main__":
    main()
