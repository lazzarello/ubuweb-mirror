# https://realpython.com/beautiful-soup-web-scraper-python/
from dataclasses import dataclass, field
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from constants import *
# Progress bar
from tqdm import tqdm
from os.path import exists

@dataclass
class Artist:
    name: str = ""
    url: str = ""
    id: int = None
    description: str = None
    born: int = None
    broken: bool = False
    dmca: bool = False

@dataclass
class Work:
    name: str = ""
    daterange: int = ""
    description: str = None
    url: str = None
    download_url: str = None
    # this doesn't work good for printing attributes
    artist = None

    def set_download_url(self, work):
        page = requests.get(work.url)
        soup = BeautifulSoup(page.content, "html.parser")
        video = soup.find("div", class_="ubucontainer")
        # TODO: test downloaded file for a video type, if not call alternate download function
        # to use vimeo link via youtube-dl
        if video is not None:
            moviename = video.find("a", id="moviename") 
            if moviename is not None:
                self.download_url = BASE_FILM_URL + moviename["href"]
        return work

    def download_alternate_work(self, work):
        # we're here because the download link failed
        # There may be an alternative link to Vimeo, which we can download
        # via youtube-dl
        page = requests.get(work.url)
        soup = BeautifulSoup(page.content, "html.parser")
        video = soup.find("div", class_="ubucontainer")
        iframe = video.find("iframe")
        download_string = ["youtube-dl", iframe["src"]]
        return download_string

    def download_work(self):
        response = requests.get(self.download_url, stream=True)
        if response.url != ERROR_URL:
            url_parts = urlparse(self.download_url)
            path = url_parts.path.split("/")
            filename = DOWNLOAD_PATH + path[-1:][0]
            print(filename)
            # copypasta https://stackoverflow.com/questions/37573483/progress-bar-while-download-file-over-http-with-requests
            size_in_bytes = int(response.headers.get('content-length', 0))
            block_size = 1024
            progress_bar = tqdm(total=size_in_bytes, unit='iB', unit_scale=True)
            if exists(filename) is False:
                with open(filename, "wb") as file:
                    for data in response.iter_content(block_size):
                        progress_bar.update(len(data))
                        file.write(data)
                progress_bar.close()
            else:
                print('file exists, write a function to check for partial downloads')
        else:
            print("whoopsy daisy, no local download, need alternate download function")

class Page:
    def get_links(self, url):
        page = requests.get(url)
        if page.url != ERROR_URL:
            soup = BeautifulSoup(page.content, "html.parser")
            tables = soup.find_all("table")
            links = tables[1].find_all("a")
            return links
        else:
            print(f"server redirected to {ERROR_URL}")
            return ERROR_URL

    def get_artists(self, url):
        links = self.get_links(url)
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
        links = self.get_links(artist.url)
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
