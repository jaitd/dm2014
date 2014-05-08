#!/bin/bash

hadoop dfs -rmr /user/hadoop-user/kmeans-output
hadoop jar /usr/local/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar -file /home/hadoop-user/dm2014/kmeans/code/mapper.py -mapper /home/hadoop-user/dm2014/kmeans/code/mapper.py -file /home/hadoop-user/dm2014/kmeans/code/reducer.py -reducer /home/hadoop-user/dm2014/kmeans/code/reducer.py -input /user/hadoop-user/kmeans/* -output /user/hadoop-user/kmeans-output

rm -r /home/hadoop-user/kmeans-output
hadoop dfs -get /user/hadoop-user/kmeans-output /home/hadoop-user

./evaluate.py ../../../test.txt ../../../kmeans-output/part-00000
