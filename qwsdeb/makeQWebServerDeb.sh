#!/bin/bash

# create homunculus deb package directories
mkdir -p QWebServer/DEBIAN

CUR_DIR=`pwd`

# copy docker image file into directory
DOCKERIMAGEPATH="${CUR_DIR}/QWebServer-image*.tar.gz"
mkdir -p QWebServer/tmp
cp $DOCKERIMAGEPATH QWebServer/tmp/

# make debian control file
VERSIONSTRING="2.0.3.0"
DEBCONTROLFILE="Package: QWebServer
Version: $VERSIONSTRING
Maintainer: Aqueti
Architecture: amd64
Depends: aquetidaemon, docker-ce
Description: The Aqueti SocketAPI Server"
echo "$DEBCONTROLFILE" > QWebServer/DEBIAN/control


# copy postinst into deb package
cp ${CUR_DIR}/postinst QWebServer/DEBIAN/postinst


# make deb package (will output humunculusServer.deb)
dpkg-deb --build QWebServer

# remove homunculus directory
rm -rf QWebServer/
