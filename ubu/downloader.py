"""
Downloader functions for UbuWeb content.

This module provides high-level functions for downloading content from UbuWeb,
including random downloads, full archive runs, and tweet-based downloads.
"""

from .models import Page, Work
from .constants import FILM_URL, DOWNLOAD_PATH
from .file_index import build_file_index, FileIndex
import random
import logging
import re
import requests

URL_REGEX_STRING = r"((http|https):\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"

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


def full_download_run(skip_existing=True):
    """
    Download all works from all artists in the film archive.
    
    This function iterates through all artists on the film index page
    and downloads all their available works. Errors are logged to transfers.log.
    
    Args:
        skip_existing: If True, build an index of existing files and skip them
    """
    # Build index of existing files if skip_existing is enabled
    file_index = None
    if skip_existing:
        logging.info("Building index of existing files...")
        file_index = build_file_index(DOWNLOAD_PATH)
        logging.info(f"Found {len(file_index)} existing files")
    
    page = Page()
    artists_page = page.get_artists(FILM_URL)
    
    stats = {
        'artists_processed': 0,
        'works_found': 0,
        'files_skipped': 0,
        'files_downloaded': 0,
        'errors': 0
    }
    
    for artist in artists_page:
        try:
            stats['artists_processed'] += 1
            logging.info(f"Processing artist: {artist.name}")
            
            artist_works = page.get_artist_works(artist)
            stats['works_found'] += len(artist_works)
            
            for work in artist_works:
                work.set_download_url(work.url)
                if work.download_url:
                    # Check if file exists in index
                    if file_index:
                        from urllib.parse import urlparse
                        url_parts = urlparse(work.download_url)
                        filename = url_parts.path.split("/")[-1]
                        
                        if file_index.has_file(filename):
                            logging.debug(f"Skipping existing file: {filename}")
                            stats['files_skipped'] += 1
                            continue
                    
                    # Download the file
                    try:
                        work.download_work()
                        stats['files_downloaded'] += 1
                    except Exception as e:
                        logging.error(f"Failed to download {work.name}", exc_info=True)
                        stats['errors'] += 1
                        
        except Exception as e:
            logging.error(f"Failed to process artist {artist.name if artist else 'unknown'}", exc_info=True)
            stats['errors'] += 1
    
    # Print summary
    print("\n" + "="*60)
    print("DOWNLOAD SUMMARY")
    print("="*60)
    print(f"Artists processed: {stats['artists_processed']}")
    print(f"Works found: {stats['works_found']}")
    print(f"Files skipped (already downloaded): {stats['files_skipped']}")
    print(f"Files downloaded: {stats['files_downloaded']}")
    print(f"Errors: {stats['errors']}")
    print("="*60)
    
    logging.info(f"Download complete: {stats}")


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
