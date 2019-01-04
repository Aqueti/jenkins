#!/bin/bash

mkdir -p Asis/DEBIAN

CUR_DIR=`pwd`

DOCKERIMAGEPATH="${CUR_DIR}/asis-image*.tar.gz"
mkdir -p Asis/tmp
cp $DOCKERIMAGEPATH Asis/tmp/
cp asisd.service Asis/tmp/
cp docker-compose.yml Asis/tmp/

VERSIONSTRING=3.0dev
DEBCONTROLFILE="Package: Asis
Version: $VERSIONSTRING
Maintainer: Aqueti
Architecture: amd64
Depends: aquetidaemon, docker-ce
Description: The Aqueti SocketAPI Server"
echo "$DEBCONTROLFILE" > Asis/DEBIAN/control

cp ${CUR_DIR}/postinst Asis/DEBIAN/postinst

dpkg-deb --build Asis

rm -rf Asis/
