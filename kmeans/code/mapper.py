#!/usr/bin/env python2.7

import sys
import numpy as np
from scipy.spatial.distance import euclidean

CLUSTER_SIZE = 200
centers = np.random.rand(750)
counts = np.zeros(CLUSTER_SIZE)


def init_skmeans():
    # init the centers to random data points
    global centers
    for i in range(CLUSTER_SIZE - 1):
        centers = np.vstack([centers, np.random.uniform(low=-2, high=2, size=750)])


def skmeans(data_point):
    # sequential k-means
    global centers, counts

    min_index = 0
    min_distance = float("inf")

    for index, center in enumerate(centers):
        dist = euclidean(data_point, center)
        if dist < min_distance:
            min_distance = dist
            min_index = index

    counts[min_index] = counts[min_index] + 1

    centers[min_index] = centers[min_index] + ((1 / counts[min_index]) * (data_point - centers[min_index]))

if __name__ == "__main__":
    # for testing out averaging
    np.random.seed(seed=42)
    init_skmeans()

    for line in sys.stdin:
        line = line.strip()
        data_point = np.fromstring(line, dtype=np.float64, sep=" ")

        skmeans(data_point)

    for center in centers:
        val = ' '.join(str(x) for x in center)
        print '%s\t%s' % ('1', val)
