#!/bin/bash

BRANCH_NAME=$1

conts=`sudo docker images asis_${BRANCH_NAME}* --format "{{.Repository}}"`
e_conts=`echo ${conts}`

sudo docker save -o asis-image.tar ${e_conts}

sudo gzip asis-image.tar
