#!/usr/bin/env python2.7

from __future__ import division
import numpy as np
import math
import operator
from scipy import linalg

# Global article vectors
articles = {}
articles_A = {}
articles_A_inv = {}
articles_b = {}

last_returned = -1
last_user_feature = None

#delta = 0.05
#alpha = 1 + np.sqrt(np.log(2 / delta) / 2)
alpha = 0.2


# Evaluator will call this function and pass the article features.
# Check evaluator.py description for details.
def set_articles(art):
    for key, value in art.iteritems():
        articles[key] = np.array(value, dtype=np.float64)


# This function will be called by the evaluator.
# Check task description for details.
def update(reward):
    global articles, articles_A, articles_A_inv, articles_b
    global last_user_feature, last_returned

    if reward == -1:
        return

    articles_A[last_returned] = articles_A[last_returned] + \
        last_user_feature.dot(last_user_feature.T)
    articles_A_inv[last_returned] = linalg.inv(articles_A[last_returned])

    articles_b[last_returned] = articles_b[last_returned] + \
        reward * last_user_feature


# This function will be called by the evaluator.
# Check task description for details.
def reccomend(timestamp, user_features, art):
    global articles, articles_A, articles_A_inv, articles_b
    global last_returned, last_user_feature

    p_ta = {}
    user_features = np.array([user_features]).T

    for article in art:
        if not article in articles_A:
            articles_A[article] = np.identity(6)
            articles_A_inv[article] = np.identity(6)
            articles_b[article] = np.array([np.zeros(6)]).T

        theta_hat = articles_A_inv[article].dot(articles_b[article])

        p_ta[article] = theta_hat.T.dot(user_features) + alpha * \
            math.sqrt(user_features.T.dot(articles_A_inv[article]).dot(user_features)[0][0])

    last_user_feature = user_features
    last_returned = max(p_ta.iteritems(), key=operator.itemgetter(1))[0]
    return last_returned
