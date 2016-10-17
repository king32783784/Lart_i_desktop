#!/bin/sh
sleep 30
mount /dev/sda1 /mnt    
rm -rf /boot/grub
cp -rf /mnt/boot/grub /boot/grub
echo "iso install ok" >> /mnt/home/testiso.log
sleep 30
reboot
