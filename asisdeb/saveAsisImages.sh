#!/bin/bash

sudo docker save -o asis-image_dev.tar asis_asis asis_janus asis_nginx
sudo gzip asis-image_dev.tar
