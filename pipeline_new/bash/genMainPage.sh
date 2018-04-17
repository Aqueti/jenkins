#!/bin/bash

DOC_HOME="/storage/Web/software/Documentation/acos"
WEBHOME="/storage/Web/repositories"
DATE=`date`
MASTER_FILE="$WEBHOME/index.html"
DEV_FILE="$WEBHOME/branches.html"
S3_DEST="s3://aqueti.operations/repositories"
BRANCH=$1

: '
if [ $BRANCH == "master" ]; then
   echo "Removing old documentation at $DOC_HOME"
   rm -r $DOC_HOME/*
   mkdir -p $DOC_HOME
   echo "Copying Documentation from `pwd` to $DOC_HOME"
   cp -r Documentation/* $DOC_HOME
   #rm -rf Documentation
else 
   echo "Not master branch. Branch is $BRANCH"
fi
'

echo "Copying all files to $WEBHOME"
mkdir -p $WEBHOME/$1/$2
cp -r * $WEBHOME/$1/$2

echo "Working in $WEBHOME"
cd $WEBHOME

echo "<html>" > $MASTER_FILE
echo "<title>Aqueti Testbed Release List ($DATE)</title>" >> $MASTER_FILE
echo "<body>" >> $MASTER_FILE

echo "<h1>Aqueti Testbed Release List ($DATE)</h1>" >> $MASTER_FILE

echo "<h3>Branches</h3>" >> $MASTER_FILE
cat $MASTER_FILE > $DEV_FILE

for directory in */ ; do
   rm latest

   echo "Generating content in $directory"
   cd $directory 
   DEST=index.html


   echo "Creating $DEST"
   echo "<html>" > $DEST
   echo "<title>$directory Releases</title>" >> $DEST
   echo "<body>" >> $DEST

   echo "<h1>Aqueti Testbed Releases for branch $directory</h1>" >> $DEST
   echo "<h2>Date: $DATE<h2>" >> $DEST

   for d in */ ; do
      if [[ $d == *"@"* ]];
      then
         rm -rf $d
      else 
         dirname=${d%/}
 
         echo "adding $dirname to $DEST"
         echo "<a href=\"$dirname/index.html\">$dirname</a><br>" >> $DEST
         last=$d
      fi
   done

   dirname=${directory%/}
   lastname=${last%/}

   rm -rf latest
   cp -r $lastname latest

   echo "<a href=\"latest/index.html\">latest</a><br>" >> $DEST
  

   echo "</body>" >> $DEST
   echo "</html>" >> $DEST

   cd ..

   echo "<a href=\"$dirname/index.html\">$directory</a><br>" >> $DEV_FILE

   if [[ $dirname == "master" || $dirname == "alpha" || $dirname == "beta" || $dirname == "release" ]]; 
   then 
      echo "<a href=\"$dirname/index.html\">$directory</a><br>" >> $MASTER_FILE
   fi
done

echo "A full list of builds is available at <a href=\"branches.html\">branches.html</a>" >> $MASTER_FILE

echo "<h1>Documentation</h1>" >> $MASTER_FILE
echo "The latest for documentation for the master branch is available at <a href=\"/software/Documentation/acos/annotated.html\">/software/Documentation/acos/annotated.html</a>" >> $MASTER_FILE

echo "</body>" >> $DEV_FILE
echo "</html>" >> $DEV_FILE
echo "</body>" >> $MASTER_FILE
echo "</html>" >> $MASTER_FILE
