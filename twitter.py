import tweepy
import requests
import re
from os import environ

URL_REGEX_STRING = "((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"

class Tweets:
    def __init__(self):
        self.consumer_key = environ['CONSUMER_KEY']
        self.consumer_key_secret = environ['CONSUMER_KEY_SECRET']
        self.access_token = environ['ACCESS_TOKEN']
        self.access_token_secret = environ['ACCESS_TOKEN_SECRET']
        self.bearer_token = environ['BEARER_TOKEN']
        self.client = tweepy.Client(self.bearer_token)
        self.ubuweb_user = self.client.get_user(username="ubuweb")
        self.last_tweets = [0]

    def get_timeline(self, max_results=5):
        timeline = self.client.get_users_tweets(self.ubuweb_user.data.id, exclude=["retweets", "replies"],
                                           max_results=max_results, tweet_fields="id,text,created_at,attachments")
        return timeline

    def get_current_url(self):
        timeline = self.get_timeline()
        tweets = timeline.data
        tweet_text = tweets[0].text
        short_url_match = re.search(URL_REGEX_STRING, tweet_text)
        short_url = short_url_match.group(0)
        response = requests.get(short_url)
        return response.url

    def get_urls(self, max_results=5):
        timeline = self.get_timeline(max_results)
        tweets = timeline.data
        urls = []
        for tweet in tweets:
            tweet_text = tweet.text
            short_url_match = re.search(URL_REGEX_STRING, tweet_text)
            short_url = short_url_match.group(0)
            response = requests.get(short_url)
            urls.append(response.url)
        return urls

    def get_latest_tweet(self):
        timeline = self.get_timeline() 
        tweets = timeline.data
        tweet_ids = []
        for tweet in tweets:
            tid = tweet.id
            tweet_ids.append(tid)
        tweet_ids.sort()
        if tweet_ids[-1] > self.last_tweets[-1]:
            tweet = self.client.get_tweet(tweet_ids[-1])
            self.last_tweets = tweet_ids
        else:
            # TODO: optimize this by returning the cached tweet from the previous run.
            # check if the library does this already, not sure.
            tweet = self.client.get_tweet(self.last_tweets[-1])
        return tweet
