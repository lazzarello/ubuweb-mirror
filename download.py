# https://realpython.com/beautiful-soup-web-scraper-python/
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urlparse

BASE_URL = "https://www.ubu.com/"
FILM_URL = "https://www.ubu.com/film/index.html"
BASE_FILM_URL = "https://www.ubu.com/film/"
DOWNLOAD_PATH = "/home/lee/Videos/ubuweb/"
content_type = "artists"

def get_artists(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    tables = soup.find_all("table")
    links = tables[1].find_all("a")
    pages = []
    for artist in links:
        artist_name = artist.text.strip() 
        artist_url = BASE_FILM_URL + artist["href"]
        pages.append([artist_name, artist_url])
    # this convention removes the left nav bar links.
    pages.pop(0)
    return pages

def get_artist_page_links(name, url):
    # print(f"Name: {name}, URL: {url}")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    tables = soup.find_all("table")
    links = tables[1].find_all("a")
    works = []
    for work in links:
        work_name = work.text.strip()
        work_url = BASE_FILM_URL + work["href"]
        works.append([work_name, work_url])
    # this convention removes the left nav bar links.
    for _ in range(2):
        works.pop(0)
    return works

def get_work(name, url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    video = soup.find("div", class_="ubucontainer")
    # print(video)
    if video is not None:
        moviename = video.find("a", id="moviename") 
        return moviename

def download(url):
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

artist_pages = get_artists(FILM_URL)
artist_page_links = get_artist_page_links(artist_pages[0][0], artist_pages[0][1])
for work_page in artist_page_links[3:]:
    movie = get_work(work_page[0], work_page[1])
    if movie is not None:
        url = BASE_FILM_URL + movie["href"]
        print(url)
        download(url)

'''
for i in range(5):
    print(get_artist_page_links(artist_pages[i][0], artist_pages[i][1]))
'''
