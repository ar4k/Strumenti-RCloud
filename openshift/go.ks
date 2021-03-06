#Begin Kickstart Script
install
text
skipx

# Repository opensource utilizzati
url --url=http://mirror.centos.org/centos/6/os/x86_64
#repo --name=rossonet --baseurl=http://rossonet.rossonet.net/rossonet/rpmrossonet/x86_64
repo --name=updates --baseurl=http://mirror.centos.org/centos/6/updates/x86_64
repo --name=epel --baseurl=http://download.fedoraproject.org/pub/epel/6/x86_64

#rootpw openshift
rootpw --iscrypted $1$zVrqeWqd$dW4sWT90hcWdY/sqIxAB0/

# Localizzazione italiana
#lang en_US.UTF-8
#keyboard us
#timezone --utc America/New_York
lang it_IT
keyboard it
timezone --utc Europe/Rome
# fine localizzazione

services --enabled=ypbind,ntpd,network,logwatch
network --onboot yes --device eth0
firewall --service=ssh
authconfig --enableshadow --passalgo=sha512
selinux --enforcing

bootloader --location=mbr --driveorder=vda --append=" rhgb crashkernel=auto quiet console=ttyS0"

zerombr
clearpart --all --initlabel
firstboot --disable
reboot --eject

part /boot --fstype=ext4 --size=500
part pv.253002 --grow --size=1
volgroup vg_vm1 --pesize=4096 pv.253002
logvol / --fstype=ext4 --name=lv_root --vgname=vg_vm1 --grow --size=8192 --maxsize=51200
# versione con disco criptato
# logvol / --fstype=ext4 --name=lv_root --vgname=vg_vm1 --grow --size=8192 --maxsize=51200 --encrypted
logvol swap --name=lv_swap --vgname=vg_vm1 --grow --size=2048 --maxsize=2048

# versione con installazione da vnc
# vnc

%packages
@core
@server-policy
ntp
ntpdate
git
man
sudo
strace
vim-enhanced
wget
curl
@development
bind
java-devel
openssl
ruby
bc
quota
%end

%pre
cat /proc/cmdline >/tmp/ks.cmdline
%end

%post --nochroot
cp /etc/resolv.conf /mnt/sysimage/etc/resolv.conf
cp /tmp/ks.cmdline /mnt/sysimage/root/ks.cmdline
%end

%post --log=/root/anaconda-post.log

# During a kickstart you can tail the log file showing %post execution
# by using the following command:
#    tailf /mnt/sysimage/root/anaconda-post.log

# Log the command invocations (and not merely output) in order to make
# the log more useful.
set -x
echo
echo "#######################################"
echo "# configurazione post installazione   #"
echo "#######################################"
echo

for parametro in $(cat /root/ks.cmdline)
        do case "$parametro" in oo_*=*) eval $parametro;; esac
done

########################################################################

echo "$oo_config;$oo_host;$oo_otp;$oo_nat" > /root/go.conf

########################################################################

cat >> /etc/rc.local << ROSSONET_POST

# Post installazione AR4K
cd /root
wget https://raw.githubusercontent.com/rossonet/Strumenti-RCloud/master/openshift/installaOpenShift.sh
chmod +x installaOpenShift.sh
# Lo script genera di default il file /root/debug.log
# a secondo del tipo di installazione potrebbe essere necessario indirizzare l'output
# verso un'altra console
tail -F debug.log > /dev/tty1 &
/root/installaOpenShift.sh
killall tail &> /dev/null

ROSSONET_POST
%end

