"""Retrieve Tweets, embeddings, and add to database"""

from os import getenv

import spacy  # Vectorizes our tweets
import tweepy  # Allows us to interact with Twitter

from .models import DB, Tweet, User

# Twitter Developer API credentials
TWITTER_API_KEY = getenv("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = getenv("TWITTER_API_KEY_SECRET")

# Authenticate Twitter Developer
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)


def add_or_update_user(username):
    # Create user based on username passed into the function
    twitter_user = TWITTER.get_user(username)

    # If they exist then update that user, if we get something back
    # then instantiate a new user
    db_user = (User.query.get(twitter_user.id)) or User(
        id=twitter_user.id, name=username)

    # Add the user to database
    DB.session.add(db_user)

    tweets = twitter_user.timeline(
        count=200,
        exclude_replies=True,
        include_rts=False,
        tweet_mode="Extended"
    )  # list of tweets from "username"

    for tweet in tweets():
        # create tweet that will be added to DB
        db_tweet = Tweet(id=tweet.id, text=tweet.text)
        # append each tweet from 'username' to  username.tweets
        db_user.tweets.append(db_tweet)
        # Add db_tweet to Tweet DB
        DB.session.add(db_tweet)

    # commit changes to DB
    DB.session.commit()
