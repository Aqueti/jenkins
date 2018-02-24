#!/bin/bash

HOME="/home/jenkins"
dir="$HOME/deb_files"
dir2="$HOME/bin_files"

if ! [ -d $dir ]; then
  mkdir -p $dir
fi

if ! [ -d $dir2 ]; then
  mkdir -p $dir2
fi

rm $dir/* 2>/dev/null
cp *.deb $dir
cp jkns/testScripts/apitest/bin/* $dir2

sudo dpkg -i $dir/mantisapi*.deb
sudo dpkg -i $dir/mantis_app*.deb
sudo dpkg -i $dir/mantis_agt*.deb

for i in {1..5} 11; do
  ssh nvidia@192.168.10.$i 'rm /home/nvidia/*.deb 2>/dev/null'
  scp $dir/aci*.deb nvidia@192.168.10.$i:./ 
  ssh nvidia@192.168.10.$i 'sudo dpkg -i /home/nvidia/aci*.deb'
done
