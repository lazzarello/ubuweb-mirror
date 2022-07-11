# custom data models
from models import Page,Work
import random
from constants import *
import logging
from twitter import Tweets
from time import sleep
import polling
import re
import requests

URL_REGEX_STRING = "((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"
twitter_poll_freq = 3600
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
    work.set_download_url(work.url)
    work.download_work()

def download_all_works_from(artist):
    page = Page()
    artist_works = page.get_artist_works(artist)
    for work in artist_works:
        work.set_download_url(work.url)
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

def get_url_from_text(text):
    short_url_match = re.search(URL_REGEX_STRING, text)
    short_url = short_url_match.group(0)
    response = requests.get(short_url)
    return response.url

def download_from_tweet(tweet):
    print(tweet.text)
    url = get_url_from_text(tweet.text)
    work = Work()
    work.url = url
    work.download_work()

def main():
    t = Tweets()
    last_tweet = None
    while True:
        current_tweet = t.get_latest_tweet().data
        if last_tweet is None:
            last_tweet = current_tweet
            download_from_tweet(current_tweet)
        elif last_tweet.id == current_tweet.id:
            print("No new tweets")
        else:
            print(f"new tweet found! {current_tweet.data}")
            download_from_tweet(current_tweet)
            last_tweet = current_tweet
        sleep(twitter_poll_freq)

if __name__ == "__main__":
    main()
