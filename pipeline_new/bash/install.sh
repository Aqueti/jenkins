#!/bin/bash

branch_name=$1
build_number=$2

#install

for i in {1..5}
do
  ssh nvidia@192.168.10.$i 'rm *.deb'
  scp aci*.deb AquetiDaemon-aarch64*.deb nvidia@192.168.10.$i
  ssh nvidia@192.168.10.$i 'sudo dpkg -i /home/nvidia/AquetiDaemon-aarch64*.deb'
  ssh nvidia@192.168.10.$i 'sudo dpkg -i /home/nvidia/aci*.deb'
done

sudo dpkg -i AquetiDaemon-x86_64*.deb

sudo docker pull aqueti:${branch_name}_${build_number}

# run

for i in {1..5}
do
  ssh nvidia@192.168.10.$i 'sudo service Aqueti-Daemon start'
done

sudo service Aqueti-Daemon start

sudo docker run -P --rm --network=host aqueti:${branch_name}_${build_number}
