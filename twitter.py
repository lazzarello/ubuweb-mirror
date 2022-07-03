import tweepy
import requests
import re
from os import environ

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_KEY_SECRET = environ['CONSUMER_KEY_SECRET']
BEARER_TOKEN = environ['BEARER_TOKEN']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']
username = "ubuweb"
url_regex_string = "((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"
client = tweepy.Client(BEARER_TOKEN)

def get_current_url(client, username):
    ubuweb_user = client.get_user(username=username)
    timeline = client.get_users_tweets(ubuweb_user.data.id, exclude=["retweets", "replies"],
                                       max_results=5, tweet_fields="id,text,created_at,attachments")
    tweets = timeline.data
    tweet_text = tweets[0].text
    short_url_match = re.search(url_regex_string, tweet_text)
    short_url = short_url_match.group(0)
    response = requests.get(short_url)
    return response.url

def get_urls(client, username, max_results=5):
    ubuweb_user = client.get_user(username=username)
    timeline = client.get_users_tweets(ubuweb_user.data.id, exclude=["retweets", "replies"],
                                       max_results=max_results, tweet_fields="id,text,created_at,attachments")
    tweets = timeline.data
    urls = []
    for tweet in tweets:
        tweet_text = tweet.text
        short_url_match = re.search(url_regex_string, tweet_text)
        short_url = short_url_match.group(0)
        response = requests.get(short_url)
        urls.append(response.url)
    return urls

def main():
    print(get_urls(client, username))

main()
