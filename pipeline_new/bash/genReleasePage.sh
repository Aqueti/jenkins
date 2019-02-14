#!/bin/bash

BRANCH=$1
BUILD=$2

RELEASE_NOTES=`cat release_notes.txt`

echo "Building index.html for branch $BRANCH at `pwd`"

DATE=`date`
echo "<html>" > index.html
echo "<title>Aqueti ACOS build for branch $BRANCH - $BUILD  Release: ($DATE)</title>" >> index.html
echo "<body>" >> index.html
echo "<h1>Aqueti ACOS build for branch $BRANCH - $BUILD  Release: ($DATE)</h1>" >> index.html

echo "<h2>Packages</h2>" >> index.html

for item in *.deb; do
   echo "<a href=\"./$item\">$item</a><br>" >> index.html
done


echo "<h2>Release Notes</h2>" >> index.html
echo $RELEASE_NOTES >> index.html

echo "</body>" >> index.html
echo "</html>" >> index.html
