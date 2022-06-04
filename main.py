# custom data models
from models import Artist, Work, Page
import random
from constants import *

def download_random_work_from(artists):
    page = Page()
    r = len(artists)
    artist = artists[random.choice(range(r))]
    print(artist)
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
    
def main():
    page = Page()
    artists_page = page.get_artists(FILM_URL)
    # download_random_work_from(artists_page)
    download_all_works_from(artists_page[0])

if __name__ == "__main__":
    main()
