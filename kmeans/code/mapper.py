#!/usr/bin/env python2.7

from __future__ import division

import sys
import numpy as np

BATCH_SIZE = 8000
count = 0
batch = np.array([])
CORESET_SIZE = 2000


def dist(x, y):
    return np.sum((x - y) ** 2)


def get_coreset(batch):
    global CORESET_SIZE

    weights = np.zeros(CORESET_SIZE)
    coreset = batch[np.random.choice(batch.shape[0],
                                     CORESET_SIZE, replace=False), :]

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
        value = str(weight) + ' '
        value = value + ' '.join(str(x) for x in point)
        print '%s\t%s' % (np.random.randint(100), value)


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
        CORESET_SIZE = int(count * 0.25)
        get_coreset(batch)
