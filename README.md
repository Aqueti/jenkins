#Jenkins Rep
This repository provides tools to run the Aqueti testbed

#Notes
Changing dns info on tegra (https://devtalk.nvidia.com/default/topic/972446/resolv-conf-being-overwritten/):


As root:

cd /root
cp /boot/initrd ./initrd.gz
gzip -d initrd.gz
mkdir initDisk
cd initDisk
cpio -i <../initrd

vim etc/resolv.conf # make your changes here

find . | cpio --create --format='newc' >../newInitrd
cd ../
gzip newInitrd

mv /boot/initrd /boot/initrd_original
cp newInitrd.gz /boot/initrd
