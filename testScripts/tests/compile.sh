#!/bin/bash

LIST=`find . -type f -regex '.*?\.cpp' | sed "s/^..//"`

for script in $LIST
do
  out_name=${script::-4}
  g++ -pthread -w $script -o $out_name /usr/lib/libMantisAPI.so -lsqlite3
done