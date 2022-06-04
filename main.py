# custom data models
from models import Artist, Work, Page
import random
from constants import *

def download_first_from_random(artists):
    page = Page()
    r = len(artists)
    artist = artists[random.choice(range(r))]
    print(artist)
    artist_works = page.get_artist_works(artist)
    work = artist_works[0]
    work.set_work_url(work)
    work.download_work()
    
def main():
    page = Page()
    artists_page = page.get_artists(FILM_URL)
    download_first_from_random(artists_page)

if __name__ == "__main__":
    main()
