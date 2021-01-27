"""Prediction of Users based on Tweet Embeddings"""
import numpy as np
from sklearn.linear_model import LogisticRegression

from .models import User
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, hypo_tweet_text):
    """
    Determine who is more likely to tweet a hypothesized section of text.

    Example run: predict_user("elonmusk", "jackblack", "Gamestonks!!")
    Returns 0 (user0_name: "elonmusk") or (user1_name: "jackblack")
    """
    # Get users
    user0 = User.query.filter(User.name == user0_name).one()
    user1 = User.query.filter(User.name == user1_name).one()
    # Convert to embedding
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])
    # Stack embeddings to create one list of vects
    vects = np.vstack([user0_vects, user1_vects])
    # Get collection of labels same length as vects
    labels = np.concatenate(
        [np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])

    # Create Logistic Regression Model
    log_reg = LogisticRegression().fit(vects, labels)
    # Reassign hypothetical text to vectorized version
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    # Format hypo_tweet_vect and run prediction
    return log_reg.predict(np.array(hypo_tweet_vect).reshape(1, -1))
