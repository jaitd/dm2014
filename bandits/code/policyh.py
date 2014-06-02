#!/usr/bin/env python2.7

from __future__ import division
import math
import operator
import numpy as np
from scipy import linalg

# Global article vectors
articles = {}
articles_A = {}
articles_A_inv = {}
articles_B = {}
articles_b = {}

A_0 = np.identity(36)
A_0_inv = np.identity(36)
b_0 = np.array([np.zeros(6)]).T

last_returned = -1
last_user_feature = None
last_combined_feature = None

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
    global articles, articles_A, articles_B, articles_A_inv, articles_b
    global last_returned, last_user_feature, A_0, A_0_inv, b_0
    global last_combined_feature

    if reward == -1:
        return

    A_0 = A_0 + np.dot(articles_B[last_returned].T,
                       np.dot(articles_A_inv[last_returned],
                              articles_B[last_returned]))
    b_0 = b_0 + np.dot(articles_B[last_returned].T,
                       np.dot(articles_A_inv[last_returned],
                              articles_B[last_returned]))
    A_0_inv = linalg.inv(A_0)

    articles_A[last_returned] = articles_A[last_returned] + \
        last_user_feature.dot(last_user_feature.T)
    articles_A_inv[last_returned] = linalg.inv(articles_A[last_returned])

    articles_B[last_returned] = articles_B[last_returned] + \
        last_user_feature.dot(last_combined_feature.T)


# This function will be called by the evaluator.
# Check task description for details.
def reccomend(timestamp, user_features, art):
    global articles, articles_A, articles_B, articles_A_inv, articles_b
    global last_returned, last_user_feature, A_0, A_0_inv, b_0
    global last_combined_feature

    beta_hat = A_0_inv.dot(b_0)
    p_ta = {}
    user_features = np.array([user_features]).T

    for article in art:
        article_feature = np.array([articles[article]]).T
        z_ta = np.array([np.outer(user_features, article_feature).flatten()]).T

        if not article in articles:
            articles_A[article] = np.identity(6)
            articles_B[article] = np.zeros((36, 6))
            articles_b[article] = np.array([np.zeros(6)]).T

        theta_hat = np.dot(articles_A_inv[article],
                           articles_b[article] - np.dot(articles_B[article],
                                                        beta_hat))
        s_ta = np.dot(z_ta.T, np.dot(A_0_inv, z_ta)) - \
            2 * np.dot(z_ta.T,
                       np.dot(A_0_inv, np.dot(articles_B[article].T,
                                              np.dot(articles_A_inv[article],
                                                     user_features)))) + \
            np.dot(user_features.T,
                   np.dot(articles_A_inv[article],
                          user_features)) + \
            np.dot(user_features.T,
                   np.dot(articles_A_inv[article],
                          np.dot(articles_B[article],
                                 np.dot(A_0_inv,
                                        np.dot(articles_B[article].T,
                                               np.dot(articles_A_inv[article],
                                                      user_features))))))
        p_ta = np.dot(z_ta.T, beta_hat) + \
            np.dot(user_features.T, theta_hat) + \
            alpha * math.sqrt(s_ta)

    last_user_feature = user_features
    last_returned = max(p_ta.iteritems(), key=operator.itemgetter(1))[0]
    last_combined_feature = np.array([np.outer(user_features,
                                               article[last_returned]).flatten()]).T
    return last_returned
