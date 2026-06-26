"""
Twitter monitoring script for UbuWeb updates.

This script monitors @ubuweb on Twitter and downloads new content as it's posted.
Requires Twitter API credentials in environment variables.

Usage:
    source environments  # Load Twitter API credentials
    python twitter_monitor.py
"""

import ubu
from time import sleep

twitter_poll_freq = 3600  # 1 hour


def main():
    """
    Main function - monitors Twitter for new UbuWeb posts and downloads them.
    """
    print("Starting Twitter monitoring for @ubuweb...")
    print(f"Poll frequency: {twitter_poll_freq} seconds ({twitter_poll_freq/3600:.1f} hours)")
    print()
    
    t = ubu.Tweets()
    last_tweet = None
    
    while True:
        try:
            current_tweet = t.get_latest_tweet().data
            
            if last_tweet is None:
                print(f"Initial tweet found: {current_tweet.text[:50]}...")
                last_tweet = current_tweet
                ubu.download_from_tweet(current_tweet)
            elif last_tweet.id == current_tweet.id:
                print("No new tweets")
            else:
                print(f"New tweet found! {current_tweet.text[:50]}...")
                ubu.download_from_tweet(current_tweet)
                last_tweet = current_tweet
                
        except Exception as e:
            print(f"Error: {e}")
            
        sleep(twitter_poll_freq)


if __name__ == "__main__":
    main()
