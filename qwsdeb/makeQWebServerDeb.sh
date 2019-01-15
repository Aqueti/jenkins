#!/bin/bash

mkdir -p QWebServer/DEBIAN

CUR_DIR=`pwd`

DOCKERIMAGEPATH="${CUR_DIR}/QWebServer-image*.tar.gz"
mkdir -p QWebServer/tmp
cp $DOCKERIMAGEPATH QWebServer/tmp/
cp homunculusd.service QWebServer/tmp/

VERSIONSTRING=2.0.5.5
DEBCONTROLFILE="Package: QWebServer
Version: $VERSIONSTRING
Maintainer: Aqueti
Architecture: amd64
Depends: docker-ce
Description: The Aqueti SocketAPI Server"
echo "$DEBCONTROLFILE" > QWebServer/DEBIAN/control

cp ${CUR_DIR}/postinst QWebServer/DEBIAN/postinst

dpkg-deb --build QWebServer
rm -rf QWebServer/
