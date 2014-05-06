#!/usr/bin/env python2.7

# for floating point division
from __future__ import division

import numpy as np
import sys

final_weights = [0] * 2001
count = 0

if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        key, weights_string = line.split("\t")

        weights = np.fromstring(weights_string, dtype=np.float64, sep=" ")

        # count the number of mappers
        # used to normalize the average weights
        count = count + 1
        # keep on adding weights from all the mappers to an array
        final_weights = [x + y for x, y in zip(final_weights, weights)]

    # normalize the weights
    final_weights = [x / count for x in final_weights]

    print "%s" % ' '.join(str(x) for x in final_weights)
