#!/bin/bash

grep -lr -e "env.password = 'homunculus'" fabfile.py | xargs sed -i "s/env.password = 'homunculus'/env.password = 'DARPAaware'/g"

service ssh start

fab install_requirements

service supervisor start

fab pack_flask
fab install_flask
fab configure_supervisor

service dbus start
service avahi-daemon start

fab deploy

cp /tmp/install/homunculus.conf /etc/supervisor/conf.d/homunculus.conf
