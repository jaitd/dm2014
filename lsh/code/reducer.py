#!/usr/bin/env python

from __future__ import division
import numpy as np
import sys


def print_duplicates(videos):
    unique = np.unique(videos)
    for i in xrange(len(unique)):
        for j in xrange(i + 1, len(unique)):
            vid1 = np.fromstring(unique[i][1], dtype=np.int32, sep=" ")
            vid2 = np.fromstring(unique[j][1], dtype=np.int32, sep=" ")
            similarity = len(set(vid1).intersection(vid2)) / len(set(vid1).union(vid2))
            #print "vid1: ",
            #print unique[i][0]
            #print "vid2: ",
            #print unique[j][0]
            #print "similarity: ",
            #print similarity
            if similarity >= 0.85:
                print "%d\t%d" % (min(int(unique[i][0]), int(unique[j][0])), max(int(unique[i][0]), int(unique[j][0])))

last_key = None
key_count = 0
duplicates = []

for line in sys.stdin:
    line = line.strip()
    key, video_details = line.split("\t")

    video_id, shingles_string = video_details.split("|")

    if last_key is None:
        last_key = key

    if key == last_key:
            duplicates.append((int(video_id), shingles_string))
    else:
        # Key changed (previous line was k=x, this line is k=y)
        print_duplicates(duplicates)
        duplicates = [(int(video_id), shingles_string)]
        last_key = key

if len(duplicates) > 0:
    print_duplicates(duplicates)
