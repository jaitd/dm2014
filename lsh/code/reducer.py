#!/usr/bin/env python

import numpy as np
import sys


def print_duplicates(videos):
    unique = np.unique(videos)
    for i in xrange(len(unique)):
        for j in xrange(i + 1, len(unique)):
            print "%d\t%d" % (min(unique[i], unique[j]),
                              max(unique[i], unique[j]))

last_key = None
last_shingles = None
key_count = 0
duplicates = []

for line in sys.stdin:
    line = line.strip()
    key, video_details = line.split("\t")

    video_id, shingles_string = video_details.split("|")
    shingles = np.fromstring(shingles_string, dtype=np.int32, sep=" ")

    if last_key is None:
        last_key = key
        last_shingles = shingles

    if key == last_key:
        similarity = len(set(shingles).intersection(last_shingles)) / len(set(shingles).union(last_shingles))
        if similarity > 0.85:
            duplicates.append(int(video_id))
    else:
        # Key changed (previous line was k=x, this line is k=y)
        print_duplicates(duplicates)
        duplicates = [int(video_id)]
        last_key = key
        last_shingles = shingles

if len(duplicates) > 0:
    print_duplicates(duplicates)
