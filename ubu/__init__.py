"""
UbuWeb Mirror - A Python module for archiving content from UbuWeb.

This module provides classes and functions to scrape, parse, and download
content from UbuWeb's film archive at https://ubuweb.com/film/index.html

Main Components:
    - Artist: Data class representing an artist in the archive
    - Work, FilmWork, SoundWork: Classes representing individual works
    - Page: Parser for extracting artists and works from HTML pages
    - download functions: High-level functions for downloading content

Example:
    >>> import ubu
    >>> page = ubu.Page()
    >>> artists = page.get_artists(ubu.FILM_URL)
    >>> ubu.download_all_works_from(artists[0])
"""

from .constants import (
    BASE_URL,
    FILM_URL,
    BASE_FILM_URL,
    DOWNLOAD_PATH,
    ERROR_URL,
    BROKEN_PAGES,
)

from .models import (
    Artist,
    Work,
    FilmWork,
    SoundWork,
    Page,
)

from .downloader import (
    download_random_work_from,
    download_all_works_from,
    full_download_run,
    get_url_from_text,
    download_from_tweet,
)

from .twitter import Tweets

__version__ = "0.1.0"
__all__ = [
    # Constants
    "BASE_URL",
    "FILM_URL",
    "BASE_FILM_URL",
    "DOWNLOAD_PATH",
    "ERROR_URL",
    "BROKEN_PAGES",
    # Models
    "Artist",
    "Work",
    "FilmWork",
    "SoundWork",
    "Page",
    # Downloader functions
    "download_random_work_from",
    "download_all_works_from",
    "full_download_run",
    "get_url_from_text",
    "download_from_tweet",
    # Twitter
    "Tweets",
]
