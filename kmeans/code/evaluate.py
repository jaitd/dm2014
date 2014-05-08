#!/usr/bin/env python

import logging
import sys

import numpy as np
from scipy.spatial.distance import euclidean

if __name__ == "__main__":
    mean = 0
    centers = np.array([])

    if not len(sys.argv) == 3:
        logging.error("Usage: evaluate.py test_data.txt "
                      "centers.txt")
        sys.exit(1)

    with open(sys.argv[2], "r") as clusters:
        centers = np.genfromtxt(clusters)

    with open(sys.argv[1], "r") as data:
        for datum in data:
            data_point = np.fromstring(datum, dtype=np.float64, sep=" ")

            min_distance = float("inf")

            for center in centers:
                dist = euclidean(data_point, center)
                if dist < min_distance:
                    min_distance = dist
            mean = mean + (min_distance ** 2)

    print("%f" % (float(mean) / 20000))
