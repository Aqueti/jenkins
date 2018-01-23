#!/bin/bash

find ./bin -type f | perl -lne 'print if -B' | xargs rm 2>/dev/null

if [ -z "$1" ]; then
	LIST=`find . -type f -regex '.*?\.cpp' | sed "s/^..//"`

	for script in $LIST
	do
	  out_name=${script::-4}
	  g++ -pthread -w $script -o ./bin/$out_name /usr/lib/libMantisAPI.so -lsqlite3
	done
else
	out_name=$1	
	g++ -pthread -w $1 -o ./bin/${out_name::-4} /usr/lib/libMantisAPI.so -lsqlite3	
fi

LIST=`find ./bin -type f -regex './[^.]+'` #| sed "s/^..//"

for script in $LIST
do
  $script
done