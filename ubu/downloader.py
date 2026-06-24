"""
Downloader functions for UbuWeb content.

This module provides high-level functions for downloading content from UbuWeb,
including random downloads, full archive runs, and tweet-based downloads.
"""

from .models import Page, Work
from .constants import FILM_URL
import random
import logging
import re
import requests

URL_REGEX_STRING = "((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s",
    filename="transfers.log",
    filemode="a"
)


def download_random_work_from(artists):
    """
    Download a random work from a random artist in the provided list.
    
    Args:
        artists: List of Artist objects
    """
    page = Page()
    r = len(artists)
    artist = artists[random.choice(range(r))]
    logging.debug(f"Artist is: {print(artist)}")
    artist_works = page.get_artist_works(artist)
    r = len(artist_works)
    work = artist_works[random.choice(range(r))]
    work.set_download_url(work.url)
    work.download_work()


def download_all_works_from(artist):
    """
    Download all works from a specific artist.
    
    Args:
        artist: Artist object
    """
    page = Page()
    artist_works = page.get_artist_works(artist)
    for work in artist_works:
        work.set_download_url(work.url)
        if work.download_url:
            work.download_work()


def full_download_run():
    """
    Download all works from all artists in the film archive.
    
    This function iterates through all artists on the film index page
    and downloads all their available works. Errors are logged to transfers.log.
    """
    page = Page()
    artists_page = page.get_artists(FILM_URL)
    for artist in artists_page:
        try:
            download_all_works_from(artist)
        except Exception as e:
            logging.error("Downloading work failed", exc_info=True)


def get_url_from_text(text):
    """
    Extract and resolve a URL from text (handles URL shorteners).
    
    Args:
        text: String containing a URL
        
    Returns:
        str: The resolved full URL
    """
    short_url_match = re.search(URL_REGEX_STRING, text)
    short_url = short_url_match.group(0)
    response = requests.get(short_url)
    return response.url


def download_from_tweet(tweet):
    """
    Extract URL from a tweet and download the associated work.
    
    Args:
        tweet: Tweet object with text attribute
    """
    print(tweet.text)
    url = get_url_from_text(tweet.text)
    work = Work()
    work.url = url
    work.download_work()
