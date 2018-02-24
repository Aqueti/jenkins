#!/bin/bash

last=`find $HOME/deb/$1/branches/$2/builds -type d -regex "./[0-9]+" | sed "s/^..//" | sort -n | tail -1`
dir="$HOME/deb/$1/branches/$2/builds/$last"

sudo dpkg -i $dir/mantisapi*.deb
sudo dpkg -i $dir/mantis_app*.deb
sudo dpkg -i $dir/mantis_agt*.deb

for i in {1..5} 11; do
  ssh nvidia@192.168.10.$i 'rm /home/nvidia/*.deb 2>/dev/null'
  scp $dir/aci*.deb nvidia@192.168.10.$i:./ 
  ssh nvidia@192.168.10.$i 'sudo dpkg -i /home/nvidia/aci*.deb'
done
