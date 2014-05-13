#!/usr/bin/env python2.7

import numpy as np
import sys

CLUSTER_SIZE = 200
count = 0
centers = np.array([])
counts = np.zeros(CLUSTER_SIZE)


def dist(x, y):
    return np.sum((x - y) ** 2)


def skmeans(weight, point):
    # sequential k-means
    global centers, counts

    min_index = 0
    min_distance = float("inf")

    for index, center in enumerate(centers):
        d = weight * dist(point, center)
        if d < min_distance:
            min_distance = d
            min_index = index

    counts[min_index] = counts[min_index] + 1

    centers[min_index] = centers[min_index] + \
        ((1 / counts[min_index]) * (point - centers[min_index]))

if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        key, data_string = line.split('\t')
        data = np.fromstring(data_string, dtype=np.float64, sep=" ")

        if count == 0:
            #centers = data[1:]
            centers = data
            count = count + 1
            continue

        if count < CLUSTER_SIZE:
            #centers = np.vstack([centers, data[1:]])
            centers = np.vstack([centers, data])
            count = count + 1
        else:
            #skmeans(data[0], data[1:])
            skmeans(np.float64(key[1:]), data)

    for center in centers:
        value = ' '.join(str(x) for x in center)
        print value
