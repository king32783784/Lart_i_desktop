#!/bin/sh
sleep 60
sudo mount /dev/sda1 /mnt    
sudo rm -rf /boot/grub
sudo cp -rf /mnt/boot/grub /boot/grub
sleep 60
sudo reboot
