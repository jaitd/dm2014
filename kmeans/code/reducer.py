#!/usr/bin/env python2.7

import numpy as np
import sys
from scipy.spatial.distance import euclidean

CLUSTER_SIZE = 200
centers = np.random.rand(750)
counts = np.zeros(CLUSTER_SIZE)


def init_skmeans():
    # init the centers to random data points
    global centers
    for i in range(CLUSTER_SIZE - 1):
        centers = np.vstack([centers, np.random.rand(750)])


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
    init_skmeans()

    for line in sys.stdin:
        line = line.strip()
        key, data_string = line.split('\t')
        data_point = np.fromstring(data_string, dtype=np.float64, sep=" ")

        skmeans(data_point)

    for center in centers:
        value = ' '.join(str(x) for x in center)
        print value
