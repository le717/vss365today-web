import tweepy

from src.core.filters import create_proper_image_url
from src.core.helpers import load_env_vals
from src.core.tweets import add_word_to_db
# from src.core.emails.sender import send_emails


__all__ = ["Listener"]


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # Take out retweets
        if status.retweeted:
            return False

        # If we have media in our tweet, get a proper URL to it
        tweet_text = status.text
        if status.entities.get("media"):
            media = status.entities["media"]
            tweet_text = create_proper_image_url(
                tweet_text,
                media[0]["url"], media[0]["media_url_https"]
            )

        # Construct a dictionary with just the info we need
        tweet = {
            "date": status.created_at,
            "user_handle": f"@{status.author.screen_name}",
            "content": tweet_text,
            "url": "https://twitter.com/{}/status/{}".format(
                status.author.screen_name, status.id_str
            )
        }

        # Add the tweet to the database
        add_word_to_db(tweet)

        # TODO Kick off the emails
        # send_emails(tweet)
        return True

    def on_error(self, status_code):
        if status_code == 420:  # blaze it
            return False


class Listener:
    """@link {https://www.dataquest.io/blog/streaming-data-python/}"""
    def __init__(self):
        self.__api = None

        # Get the app settings for the Twitter secret keys
        config = load_env_vals()
        auth = tweepy.OAuthHandler(
            config["TWITTER_APP_KEY"],
            config["TWITTER_APP_SECRET"]
        )
        auth.set_access_token(
            config["TWITTER_KEY"],
            config["TWITTER_SECRET"]
        )
        self.__api = tweepy.API(auth)

    def start(self):
        stream_listener = StreamListener()
        stream = tweepy.Stream(auth=self.__api.auth, listener=stream_listener)
        # TODO I don't like having to hard-code the user IDs
        # http://gettwitterid.com/?user_name=SalnPage&submit=GET+USER+ID
        stream.filter(
            follow=["227230837", "2704693854"]
            # ,
            # track=["#vss365", "#prompt"]
        )
