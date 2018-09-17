#!/bin/bash

sed -i "s#aqt://[^\"]*#aqt://$(echo $AQUETI_SYSTEM_NAME)#g" /home/www/Homunculus/config.py
