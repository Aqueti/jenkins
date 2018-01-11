#!/bin/bash

LIST=`find . -type f -regex './[^.]+'` #| sed "s/^..//"

for script in $LIST
do
  $script
done

