# custom data models
from models import Page
import random
from constants import *
import logging
from twitter import Tweets

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
    page = Page()
    artist_works = page.get_artist_works(artist)
    for work in artist_works:
        work.set_download_url(work)
        if work.download_url:
            work.download_work()

def full_download_run():
    page = Page()
    artists_page = page.get_artists(FILM_URL)
    for artist in artists_page:
        try:
            download_all_works_from(artist)
        except Exception as e:
            logging.error("Downloading work failed", exc_info=True)
    # r = len(artists_page)
    # download_all_works_from(artists_page[random.choice(range(r))])

def main():
    tw = Tweets()
    url = tw.get_current_url()
    print(url)
if __name__ == "__main__":
    main()
