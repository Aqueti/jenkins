#!/bin/bash

dir="$HOME/deb/apitest/lastSuccessful/archive"

sudo dpkg -i $dir/mantisapi*.deb
sudo dpkg -i $dir/mantis_app*.deb
sudo dpkg -i $dir/mantis_agt*.deb

for i in {1..5} 11; do
  ssh nvidia@192.168.10.$i 'rm /home/nvidia/*.deb 2>/dev/null'
  scp $dir/aci*.deb nvidia@192.168.10.$i:./ 
  ssh nvidia@192.168.10.$i 'sudo dpkg -i /home/nvidia/aci*.deb'
done
