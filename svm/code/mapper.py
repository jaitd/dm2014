#!/usr/bin/env python2.7

import sys

import numpy as np

from sklearn.linear_model.stochastic_gradient import SGDClassifier

# one classifier for the mapper
# this is the classifier on which we'll be running the partial_fit
classifier = SGDClassifier()

# batch size for the partial_fit
BATCH_SIZE = 50


# appended 1 to the original features for centering the data, the
# classifier also calculates the offset which is appended to
# the weights
def transform(x_original):
    return np.append(x_original, [1])


# run paritial_fit for the classifier with each picture
def train(y, features):
    classifier.partial_fit(features, y, classes=[1, -1])


if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        features = np.fromstring(line, dtype=np.float64, sep=" ")
        train([features[0]], features[1:])

    temp = classifier.coef_[0]
    # appending intercept to the calculated weights
    temp = np.append(temp, classifier.intercept_)

    value = ' '.join(str(x) for x in temp)

    print '%s\t%s' % ('1', value)
