"""
UbuWeb Mirror - Main entry point

This script can run in two modes:
1. Full archive download (commented out by default)
2. Twitter monitoring mode (default)

To run full download, uncomment the full_download_run() call in main().
"""

import ubu
from time import sleep

twitter_poll_freq = 3600  # 1 hour


def main():
    """
    Main function - monitors Twitter for new UbuWeb posts and downloads them.
    
    To run full archive download instead, comment out the Twitter code
    and uncomment: ubu.full_download_run()
    """
    # For full archive download, uncomment this:
    # ubu.full_download_run()
    
    # Twitter monitoring mode:
    t = ubu.Tweets()
    last_tweet = None
    while True:
        current_tweet = t.get_latest_tweet().data
        if last_tweet is None:
            last_tweet = current_tweet
            ubu.download_from_tweet(current_tweet)
        elif last_tweet.id == current_tweet.id:
            print("No new tweets")
        else:
            print(f"new tweet found! {current_tweet.data}")
            ubu.download_from_tweet(current_tweet)
            last_tweet = current_tweet
        sleep(twitter_poll_freq)


if __name__ == "__main__":
    main()
