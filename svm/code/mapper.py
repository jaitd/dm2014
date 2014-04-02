#!/usr/bin/env python2.7

import sys

import numpy as np

from sklearn.linear_model.stochastic_gradient import SGDClassifier

# one classifier for the mapper
# this is the classifier on which we'll be running the partial_fit
classifier = SGDClassifier()


# This function has to either stay in this form or implement the
# feature mapping. For details refer to the handout pdf.
def transform(x_original):
    return np.append(x_original, [1])


def train(y, features):
    classifier.partial_fit(features, y, classes=[1, -1])


if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        features = np.fromstring(line, dtype=np.float64, sep=" ")
        train([features[0]], features[1:])

    temp = classifier.coef_[0]
    temp = np.append(temp, classifier.intercept_)

    value = ' '.join(str(x) for x in temp)

    print '%s\t%s' % ('1', value)
