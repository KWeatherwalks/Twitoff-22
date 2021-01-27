"""SQLAlchemy models and utility functions for TwitOff"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


# User Table
class User(DB.Model):
    """Twitter Users corresponding to tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)  # id column
    name = DB.Column(DB.String, nullable=False)  # name column
    newest_tweet_id = DB.Column(DB.BigInteger)  # most recent tweet

    def __repr__(self):
        return f"<User: {self.name}>"


class Tweet(DB.Model):
    """Tweets corresponding to Users"""
    # Columns in the DB
    id = DB.Column(DB.BigInteger, primary_key=True)
    # tweet text column - allows for emojis/links
    text = DB.Column(DB.Unicode(300), nullable=False)
    # vectorized tweet
    vect = DB.Column(DB.PickleType, nullable=False)
    # user_id column (corresponding user)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        "user.id"), nullable=False)
    # Creates user link between tweets
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))

    def __repr__(self):
        return f"<Tweet: {self.text}>"
