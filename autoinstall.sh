#!/bin/bash

# init ****************************************************
#if test -z "$part"; then
#    part=/dev/sda4
#fi
#
#if test -z "$isoftiso"; then
#    for iso in `ls *.iso`; do
#        if [[ $iso == isoft-desktop* ]]; then
#            isoftiso=$iso
#        fi
#    done
#fi
#
#if test -z "$part"; then
#    echo "partition is not specified! Exit now."
#    exit 1
#fi
#
#if test -z "$isoftiso"; then
#    echo "iso is not specified! Exit now."
#    exit 1
#fi
#
#if [ ! -f $isoftiso ]; then
#    echo "iso file is not exist."
#    exit 1
#fi
#
#partinfo=`ls -l $part | grep disk | grep ^b`
#if [[ ! -e $part && -n partinfo ]]; then
#    echo "partition is not exist."
#    exit 1
#fi
#
#echo $part
#echo $isoftiso
#
part=$1
isoftiso=$2
## prepare file system *************************************
sudo mkdir -p /tmp/inst
rootdir=/tmp/inst/rootdir
sudo mkdir -p $rootdir
#
sudo mkdir -p /tmp/inst/iso
sudo mkdir -p /tmp/inst/fs
sudo mkdir -p /tmp/inst/rt
sudo mount  -o loop $isoftiso /tmp/inst/iso
sudo mount /tmp/inst/iso/isoft/x86_64/root-image.fs.sfs /tmp/inst/fs
#
sudo mount /tmp/inst/fs/root-image.fs /tmp/inst/rt
sudo cp -f /tmp/inst/rt/usr/share/apps/dinstaller/postscript.tmpl /tmp/inst
sudo umount /tmp/inst/rt
#
## install *************************************************
echo 'start...' > /tmp/dins.log
#
## UUID="" TYPE="" PARTUUID=""
partinfo=`blkid $part`
partinfo=${partinfo#"${part}:"}
eval $partinfo
#
if test -z "$UUID"; then
    UUID=`uuidgen`
fi
#
## *** dd
echo 'dd operation...'
echo 'dd operation...' >> /tmp/dins.log
dd if=/tmp/inst/fs/root-image.fs of=$part bs=4k
sync
e2fsck -f -y $part
resize2fs -f $part
tune2fs $part -f -U $UUID

sudo umount /tmp/inst/fs
sudo umount /tmp/inst/iso

# *** postscript
sudo mount $part $rootdir
sudo mount -B /proc ${rootdir}/proc
sudo mount -B /sys ${rootdir}/sys
sudo mount -B /dev ${rootdir}/dev
sudo mount -B /run ${rootdir}/run
sudo mount -B /tmp ${rootdir}/tmp
 
sudo mkdir -p ${rootdir}/cur
sudo mount -B / ${rootdir}/cur
 
 # *** create fstab
echo 'create fstab...'
echo 'create fstab...' >> /tmp/dins.log

sudo sh -c "cat > ${rootdir}/etc/fstab << EOF
UUID=${UUID}          /          ext4          defaults          1          1
EOF"
 
# *** postscript
echo 'postscript...'
echo 'postscript...' >> /tmp/dins.log
 
sudo sh -c "cat > ${rootdir}/postscript.sh << EOF
#!/bin/bash
export LC_ALL=zh_CN.UTF-8
export LANG=zh_CN.UTF8
export GRUB_DEVICE=/dev/sda
export ROOT_DEVICE=$part
EOF"
sudo sh -c "cat /tmp/inst/postscript.tmpl >> ${rootdir}/postscript.sh"
sudo sed -i '/^systemctl enable firstboot/ d' ${rootdir}/postscript.sh

# begin 1
sudo sh -c "cat >> ${rootdir}/postscript.sh << EOF
localectl set-locale LANG=zh_CN.UTF-8
localectl --no-convert set-x11-keymap cn
timedatectl set-timezone Asia/Shanghai
useradd -U -G wheel,sys,video,audio,disk -m test
echo root:abc123 | chpasswd
echo test:abc123 | chpasswd
hostnamectl set-hostname test

xsession=/usr/share/xsessions
sddmconf=/etc/sddm.conf

if [ ! -c \\\$sddmconf ]; then
    sddm --example-config > \\\$sddmconf
fi

entry=\"[Desktop Entry]\n\"
entry+=\"Encoding=UTF-8\n\"
entry+=\"Type=XSession\n\"
entry+=\"Exec=/usr/bin/startkde\n\"
entry+=\"TryExec=/usr/bin/startkde\n\"
entry+=\"DesktopNames=KDE\n\"
entry+=\"Name=Plasma\n\"
entry+=\"Comment=Plasma by KDE\n\"
entry+=\"X-KDE-PluginInfo-Version=5.4.3\n\"
 
if [ ! -c \\\${xsession}/plasma.desktop ]; then
    echo -e \\\$entry > \\\${xsession}/plasma.desktop
fi
sed -i '/^Session=.*/d' \\\$sddmconf
sed -i '/^User=.*/d' \\\$sddmconf
sed -i '/^\\[Autologin\\]/a\\User=test' \\\$sddmconf
sed -i '/^User=test/a\\Session=/usr/share/xsessions/plasma.desktop' \\\$sddmconf

systemctl  enable sddm-plymouth
systemctl  start sddm-plymouth
EOF"
#end 1
 
sudo chmod 755 ${rootdir}/postscript.sh
sudo cp -f ${rootdir}/postscript.sh /tmp
sudo rm -f /tmp/postscript.log
sudo sh -c "chroot $rootdir /postscript.sh &> /tmp/postscript.log"
 
sudo umount ${rootdir}/cur
#sudo rm -rf ${rootdir}/cur
sudo umount ${rootdir}/proc
sudo umount ${rootdir}/sys/fs/fuse/connections
sudo umount ${rootdir}/sys
sudo umount ${rootdir}/dev
sudo umount ${rootdir}/run
sudo umount ${rootdir}/tmp
sudo umount $rootdir
 
sudo rm -rf /tmp/inst

