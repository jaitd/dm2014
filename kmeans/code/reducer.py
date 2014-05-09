#!/usr/bin/env python2.7

import numpy as np
import sys
from scipy.spatial.distance import euclidean

CLUSTER_SIZE = 200
centers = np.array([])
count = 0
counts = np.zeros(CLUSTER_SIZE)


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
    for line in sys.stdin:
        line = line.strip()
        key, data_string = line.split('\t')
        data_point = np.fromstring(data_string, dtype=np.float64, sep=" ")

        if count == 0:
            centers = data_point
            count = count + 1
        elif count < CLUSTER_SIZE:
            centers = np.vstack([centers, data_point])
            count = count + 1
        else:
            skmeans(data_point)

    for center in centers:
        value = ' '.join(str(x) for x in center)
        print value
