import tweepy
import requests
import re
from os import environ

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_KEY_SECRET = environ['CONSUMER_KEY_SECRET']
BEARER_TOKEN = environ['BEARER_TOKEN']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']
url_regex_string = "((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"

class Tweets:
    def __init__(self):
        self.consumer_key = CONSUMER_KEY
        self.consumer_key_secret = CONSUMER_KEY_SECRET
        self.access_token = ACCESS_TOKEN
        self.access_token_secret = ACCESS_TOKEN_SECRET
        self.bearer_token = BEARER_TOKEN
        self.client = tweepy.Client(BEARER_TOKEN)
        self.ubuweb_user = self.client.get_user(username="ubuweb")

    def get_current_url(self):
        timeline = self.client.get_users_tweets(self.ubuweb_user.data.id, exclude=["retweets", "replies"],
                                           max_results=5, tweet_fields="id,text,created_at,attachments")
        tweets = timeline.data
        tweet_text = tweets[0].text
        short_url_match = re.search(url_regex_string, tweet_text)
        short_url = short_url_match.group(0)
        response = requests.get(short_url)
        return response.url

'''
    def get_urls(self, client, user, max_results=5):
        timeline = client.get_users_tweets(user.data.id, exclude=["retweets", "replies"],
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

    def get_latest_tweet_id(self, client, user):
        return False 
'''
