from dataclasses import dataclass, field
import requests
from bs4 import BeautifulSoup
from constants import *

@dataclass
class Artist:
    name: str = ""
    url: str = ""
    id: int = None
    description: str = None
    born: int = None

@dataclass
class Work:
    name: str = ""
    daterange: int = ""
    description: str = None
    url: str = None
    download_url: str = None
    # this doesn't work good for printing attributes
    artist = None

    def get_work_movie(self, work):
        page = requests.get(work.url)
        soup = BeautifulSoup(page.content, "html.parser")
        video = soup.find("div", class_="ubucontainer")
        if video is not None:
            moviename = video.find("a", id="moviename") 
            if moviename is not None:
                self.download_url = BASE_FILM_URL + moviename["href"]
        return work

    def download_work(self, url):
        response = requests.get(url, stream=True)
        url_parts = urlparse(url)
        path = url_parts.path.split("/")
        filename = DOWNLOAD_PATH + path[-1:][0]
        print(filename)
        # copypasta https://stackoverflow.com/questions/37573483/progress-bar-while-download-file-over-http-with-requests
        size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=size_in_bytes, unit='iB', unit_scale=True)
        with open(filename, "wb") as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        # maybe add an error condition here?
