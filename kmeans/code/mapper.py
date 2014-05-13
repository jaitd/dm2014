#!/usr/bin/env python2.7

from __future__ import division

import sys
import numpy as np

BATCH_SIZE = 8000
count = 0
batch = np.array([])
#CORESET_SIZE = 2000


def dist(x, y):
    return np.sum((x - y) ** 2)


def init_coreset(batch):
    C = batch[np.random.choice(batch.shape[0], 1)]
    for _ in range(5):
        D2 = np.array([min([np.inner(c - p, c - p) for c in C])
                       for p in batch])
        probs = D2 / D2.sum()
        cumprobs = probs.cumsum()
        # setting it to 2 * 200 manually
        for i in range(2 * 200):
            r = np.random.rand()
            i = -1
            for j, p in enumerate(cumprobs):
                if r < 2 * 200 * p:
                    i = j
                    break
            C = np.vstack([C, batch[i]])
    return C


def get_coreset(batch):
    #global CORESET_SIZE

    #coreset = batch[np.random.choice(batch.shape[0],
    #                                 CORESET_SIZE, replace=False), :]
    coreset = init_coreset(batch)
    weights = np.zeros(coreset.shape[0])

    for point in batch:
        min_index = 4242
        min_dist = float("inf")
        for index, c in enumerate(coreset):
            d = dist(point, c)
            if d < min_dist:
                min_dist = d
                min_index = index
        weights[min_index] = weights[min_index] + 1

    for weight, point in zip(weights, coreset):
        #value = str(weight) + ' '
        #value = value + ' '.join(str(x) for x in point)
        #print '%s\t%s' % (np.random.randint(100), value)
        value = ' '.join(str(x) for x in point)
        if weight < 500:
            print '%s\t%s' % ('z' + str(weight), value)
        else:
            print '%s\t%s' % ('a' + str(weight), value)


if __name__ == "__main__":
    for line in sys.stdin:

        line = line.strip()
        data_point = np.fromstring(line, dtype=np.float64, sep=" ")

        if count == 0:
            batch = data_point
            count = count + 1
            continue

        if count < BATCH_SIZE:
            batch = np.vstack([batch, data_point])
            count = count + 1
        else:
            get_coreset(batch)
            count = 0
            batch = np.array([])

    if count != 0:
        #CORESET_SIZE = int(count * 0.4)
        get_coreset(batch)
