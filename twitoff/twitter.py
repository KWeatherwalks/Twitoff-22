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

# Load Language Model
nlp = spacy.load('my_model')


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(username):

    try:
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

        # empty tweets list == false, non-empty tweets list == true
        if tweets:
            # update newest_tweet_id
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:

            # create an embedding for each tweet
            vectorized_tweet = vectorize_tweet(tweet.text)
            # create tweet that will be added to DB
            db_tweet = Tweet(id=tweet.id, text=tweet.text,
                             vect=vectorized_tweet)
            # append each tweet from 'username' to  username.tweets
            db_user.tweets.append(db_tweet)
            # Add db_tweet to Tweet DB
            DB.session.add(db_tweet)

    except Exception as e:
        print(f"Error processing {username}: {e}")
        raise e

    else:
        # commit changes to DB
        DB.session.commit()


def insert_example_users():
    # Usernames to propagate website
    usernames = ['KWeatherwalks', 'timnitGebru', 'DrIbram', 'StephStammel',
                 'kareem_carr', 'MsPackyetti', 'kjhealy', 'rajiinio']
    # Create users and add to database
    for user in usernames:
        add_or_update_user(user)
