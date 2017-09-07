#!/bin/bash

#remove any previous core files
rm core

if [ $# == 1 ]; then
   cmd="../INSTALL/bin/testATL -t $1"
else
   cmd="../INSTALL/bin/testATL"
fi


iters=0
pass=0
#Run 100 times
for i in `seq 1 1000`;
do 
   eval $cmd 2> error.log  > out$i.log 
   result=$?

   ((iters++))

   if [ $result == 0 ]
   then
      ((pass++))
      percent=$((100*pass/iters))
      echo "`date` - Test $i passed with code $result ($pass/$iters - $percent%)"
   elif [ $result == 1 ] 
   then
      percent=$((100*pass/iters))
      echo "`date` - Test $i failed with code $result ($pass/$iters - $percent%)"
#      exit 1
   else
      echo "`date` - Test $i error. Exiting with code $result"
      exit 1
   fi
done
