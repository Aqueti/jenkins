#!/bin/bash

if [ $1 == "TX1" ]; then
  echo "TX1" > $HOME/tegra/tegra.txt 

  cam=102

  ssh nvidia@192.168.10.1 'pkill -9 acosd'
  ssh nvidia@192.168.10.1 'acosd -R acosdLog -C H264 -s 1 -vvv'
  sleep 1
elif [ $1 == "TX2" ]; then
  echo "TX2" > $HOME/tegra/tegra.txt 

  cam=103
  
  ssh nvidia@192.168.10.11 'pkill -9 acosd'
  ssh nvidia@192.168.10.11 'acosd -R acosdLog -C H264 -s 1 -vvv'
  sleep 1
fi

pkill -9 V2
V2 --cache-size 20000 --maxRecordingLength 3600 --tightPrefetch -p 24816 --numJpegDecompressors 16 --numH26XDecompressors 5 --prefetchSize 40 --force-gpu-compatibility --dir $HOME --camera $cam  1>/dev/null &
sleep 3

bin_dir=/home/jenkins/workspace/$2/testScripts/apitest/bin

LIST=`find $bin_dir -type f | perl -lne 'print if -B'`

for script in $LIST; do 
  $script --gtest_output="xml:results.xml"
done
