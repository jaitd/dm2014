#!/bin/bash

hadoop dfs -rmr /user/hadoop-user/svm-output
hadoop jar /usr/local/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar -file /home/hadoop-user/dm2014/svm/code/mapper.py -mapper /home/hadoop-user/dm2014/svm/code/mapper.py -file /home/hadoop-user/dm2014/svm/code/reducer.py -reducer /home/hadoop-user/dm2014/svm/code/reducer.py -input /user/hadoop-user/svm/* -output /user/hadoop-user/svm-output

rm /home/hadoop-user/dm2014/svm/weights.txt
rm -r /home/hadoop-user/dm2014/svm/svm-output
hadoop dfs -get /user/hadoop-user/svm-output /home/hadoop-user/dm2014/svm
mv /home/hadoop-user/dm2014/svm/svm-output/part-00* /home/hadoop-user/dm2014/svm/weights.txt

python ./evaluate.py ../weights.txt ../test_data.txt ../test_labels.txt
