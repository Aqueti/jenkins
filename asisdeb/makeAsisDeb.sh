#!/bin/bash

mkdir -p ASIS/DEBIAN

CUR_DIR=`pwd`

DOCKERIMAGEPATH="${CUR_DIR}/asis-image*.tar.gz"
mkdir -p ASIS/tmp
cp $DOCKERIMAGEPATH ASIS/tmp/
cp asisd.service ASIS/tmp/
cp docker-compose.yml ASIS/tmp/

VERSIONSTRING=3.0dev
DEBCONTROLFILE="Package: ASIS
Version: $VERSIONSTRING
Maintainer: Aqueti
Architecture: amd64
Depends: aquetidaemon, docker-ce
Description: The Aqueti SocketAPI Server"
echo "$DEBCONTROLFILE" > ASIS/DEBIAN/control

cp ${CUR_DIR}/postinst ASIS/DEBIAN/postinst

dpkg-deb --build ASIS

rm -rf ASIS/
