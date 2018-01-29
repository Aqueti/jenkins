#!/bin/bash

if [ ! -d "../bin" ]; then
  mkdir ../bin
fi

find ../bin -type f | perl -lne 'print if -B' | xargs rm 2>/dev/null

if [ -z "$1" ]; then
	LIST=`find . -type f -regex '.*?\.cpp' | sed "s/^..//"`

	for script in $LIST
	do
	  out_name=${script::-4}
	  g++ -pthread -w $script ../src/tests.cpp -o ../bin/$out_name /usr/lib/libMantisAPI.so -lsqlite3 -I ../include
	done
else
	out_name=$1	
	g++ -pthread -w $1 ../src/tests.cpp -o ../bin/${out_name::-4} /usr/lib/libMantisAPI.so -lsqlite3 -I ../include	
fi

LIST=`find ../bin -type f -regex './[^.]+'` #| sed "s/^..//"

for script in $LIST
do
  $script
done