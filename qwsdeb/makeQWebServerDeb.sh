#!/bin/bash

mkdir -p QWebServer/DEBIAN

CUR_DIR=`pwd`

DOCKERIMAGEPATH="${CUR_DIR}/QWebServer-image*.tar.gz"
mkdir -p QWebServer/tmp
cp $DOCKERIMAGEPATH QWebServer/tmp/
cp homunculusd.service QWebServer/tmp/
cp QView-0.1.0-x86_64.AppImage QWebServer/tmp/

VERSIONSTRING=2.0.5.5
DEBCONTROLFILE="Package: QWebServer
Version: $VERSIONSTRING
Maintainer: Aqueti
Architecture: amd64
Depends: docker-ce
Recommends: docker-compose (>= 1.23.1)
Description: The Aqueti SocketAPI Server"
echo "$DEBCONTROLFILE" > QWebServer/DEBIAN/control

cp ${CUR_DIR}/preinst QWebServer/DEBIAN/preinst
cp ${CUR_DIR}/postinst QWebServer/DEBIAN/postinst
cp ${CUR_DIR}/prerm QWebServer/DEBIAN/prerm
cp ${CUR_DIR}/postrm QWebServer/DEBIAN/postrm

dpkg-deb --build QWebServer
rm -rf QWebServer/
