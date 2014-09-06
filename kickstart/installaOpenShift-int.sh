#!/bin/bash

# Script di completamento della configurazione OpenShift
# by Ambrosini (Rossonet s.c.a r.l.)
# 
# da copiare in /root/ di un AMI EC2 con installazione CentOS 6.x x86_64
# SELinux deve essere attivo e l'installazione minima per evitare conflitti
# tra i pacchetti
# con i386 NON FUNZIONA
#
# Per installare lo script utilizare il seguente codice in /etc/rc.local

#	#!/bin/sh
#	#
#	# This script will be executed *after* all the other init scripts.
#	# You can put your own initialization stuff in here if you don't
#	# want to do the full Sys V style init stuff.
#	
#	touch /var/lock/subsys/local
#	
#	# set a random pass on first boot
#	if [ -f /root/firstrun ]; then
#	  dd if=/dev/urandom count=50|md5sum|passwd --stdin root
#	  passwd -l root
#	  # Installa OpenShift
#	  cd /root
#	  wget http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/installaOpenShift.sh
#	  chmod +x installaOpenShift.sh
#	  /root/installaOpenShift.sh
#	  #
#	  rm /root/firstrun
#	fi
#	
#	if [ ! -d /root/.ssh ]; then
#	  mkdir -m 0700 -p /root/.ssh
#	  restorecon /root/.ssh
#	fi
#	# Get the root ssh key setup
#	ReTry=0
#	while [ ! -f /root/.ssh/authorized_keys ] && [ $ReTry -lt 5 ]; do
#	  sleep 2
#	  curl -f http://169.254.169.254/latest/meta-data/public-keys/0/openssh-key > /root/.ssh/authorized_keys
#	  ReTry=$[Retry+1]
#	done
#	chmod 600 /root/.ssh/authorized_keys && restorecon /root/.ssh/authorized_keys
#	
#	

# Il file /root/firstrun permette il cambio della password al prossimo riavvio e poi si cancella
# Il disco deve essere almeno di 10GB

# Leggo il parametro EC2 della configurazione
#confUrl="http://rossonet.rossonet.net/indefero/index.php/p/go/source/file/master/CentOS6/ar4k.yml"
#hostName="go.nodi.ar4k.net"
confUrl=$(curl http://169.254.169.254/latest/user-data -o - | head -1 | grep -v '<?xml version="1.0" encoding="iso-8859-1"?>' | cut -d\; -f1)
hostName=$(curl http://169.254.169.254/latest/user-data -o - | head -1 | grep -v '<?xml version="1.0" encoding="iso-8859-1"?>' | cut -d\; -f2)
# eventuali parametri di configurazione vanno inseriti in /root/go.conf
# per i virtualizzatori con CDROM come parametro 
if [ -f /root/go.conf ]
then
	confUrl=$(cat /root/go.conf | cut -d\; -f1)
	hostName=$(cat /root/go.conf | cut -d\; -f2)
fi
#console="/dev/hvc0"
console="/root/debug.log"
dir_installazione="/root/openshift"

# Marca le macchine già installate
if [ -f /root/ar4k.mark ]
then
	echo "sistema installato precedentemente... esco." >> $console
	exit 0
else
	touch /root/ar4k.mark
fi

# Se le variabili non sono specificate lo script esce
if [ "$confUrl" == "" ]
then
	echo "Parametro url file di configurazione mancante" >> $console
	exit 1
fi
if [ "$hostName" == "" ]
then
	echo "Parametro url file di configurazione mancante" >> $console
	exit 1
fi

# Crea la directory
mkdir -p $dir_installazione
	
########################################################################

cat >> $console << ROSSONET_WELCOME

AR4K OpenShift Origin
Il sistema installerà un sistema CentOS 6.x con OpenShift origin.
per informazioni e supporto http://www.ar4k.eu

Installazione automatica creata da Rossonet s.c.a r.l.
per maggiori informazioni scrivere a origami@rossonet.com

ROSSONET_WELCOME

########################################################################

echo "Installo i pacchetti base mancanti" >> $console
yum install -y @server-policy ntp ntpdate git man sudo strace vim-enhanced wget curl @development bind java-devel openssl ruby bc java-1.7.0-openjdk java-1.7.0-openjdk-devel &>> $dir_installazione/yum.log

cd $dir_installazione

echo "Installo la JDK" >> $console
wget http://marx.rossonet.net/ar4k/jdk-7u67-linux-x64.rpm
yum localinstall -y  jdk-7u67-linux-x64.rpm &>> $dir_installazione/yum.log
## java ##
#alternatives --install /usr/bin/java java /usr/java/latest/jre/bin/java 200000
## javaws ##
#alternatives --install /usr/bin/javaws javaws /usr/java/latest/jre/bin/javaws 200000
## Install javac only if you installed JDK (Java Development Kit) package ##
#alternatives --install /usr/bin/javac javac /usr/java/latest/bin/javac 200000
#alternatives --install /usr/bin/jar jar /usr/java/latest/bin/jar 200000

# "Synchronize the system clock using NTP..."
echo "Sincronizza l'orologio del sistema..." >> $console
ntpdate clock.redhat.com
# "Synchronize the hardware clock to the system clock..."
hwclock --systohc

# Se la partizione è più grande, espande il filesystem
resize2fs /dev/xvde

# Setta quota in filesystem di root
sed -i 's/\(^.*\t\/ .*\)defaults\(.*$\)/\1defaults,usrquota\2/' /etc/fstab
mount -o remount /
quotacheck -f -cmug /

# Grab the IP address set during installation.
echo "Identifico la rete..." >> $console
cur_ip_addr="$(/sbin/ip addr show | awk '/inet .*global/ { split($2,a,"/"); print a[1]; }' | head -1)"
pub_ip_addr="$(curl rossonet.rossonet.net/myip.php 2> /dev/null | grep 'Current IP Address: ' | sed 's/Current IP Address: //')"
echo "ip privato:" >> $console
echo $cur_ip_addr >> $console
echo "ip pubblico:" >> $console
echo $pub_ip_addr >> $console
# add the IP to /etc/issue for convenience
echo "IP interfaccia durante l'installazione: ${cur_ip_addr} (${pub_ip_addr})" >> /etc/issue.net


# genera una chiave di installazione
echo "$(openssl rand -hex 3)" > $dir_installazione/chiave.txt
echo "Codice sicurezza AR4K:" >> /etc/issue.net
cat $dir_installazione/chiave.txt >> /etc/issue.net
# genera la password per OpenShift
echo "$(openssl rand -base64 8 | tr -dc _A-Z-a-z-0-9)" > $dir_installazione/OpenShift.pwd
password=$(cat $dir_installazione/OpenShift.pwd)
echo "Codice di sicurezza AR4K:" >> $console
cat $dir_installazione/chiave.txt >> $console
echo "Password OpenShift:" >> $console
cat $dir_installazione/OpenShift.pwd  >> $console

# "Installa OpenShift..."
echo "Scarico i file di configurazione e installazione di OpenShift" >> $console

cd $dir_installazione
curl -s $confUrl -o configurazione_OpenShift.yml
# corregge l'ip pubblico configurazione_OpenShift.yml
sed -i "s/<PUB_IP>/${cur_ip_addr}/g" configurazione_OpenShift.yml
sed -i "s/<PRI_IP>/${cur_ip_addr}/g" configurazione_OpenShift.yml
# assegna la password
sed -i "s/<PASSWORD>/${password}/g" configurazione_OpenShift.yml
curl -s https://install.openshift.com/ -o installazione_OpenShift.sh
chmod +x installazione_OpenShift.sh

# Configura l'host in /etc/hosts
echo "${cur_ip_addr}	${hostName}" >> /etc/hosts
# Configura hostname
sed -i "s/^HOSTNAME=.*$/HOSTNAME=${hostName}/" /etc/sysconfig/network
hostname ${hostName}
# Disabilita ipv6
cat >> /etc/sysctl.conf << SYSCTL
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
SYSCTL

cd $dir_installazione
# Scarico il tool diagnostico
wget https://raw.githubusercontent.com/openshift/origin-server/master/common/bin/oo-diagnostics
chmod +x oo-diagnostics

cd $dir_installazione

# Software utili allo sviluppo Rossonet/AR4K

echo "Installo Tomcat 7" >> $console
wget http://mirror.nohup.it/apache/tomcat/tomcat-7/v7.0.55/bin/apache-tomcat-7.0.55.tar.gz
tar -xzf apache-tomcat-7.0.55.tar.gz
#rm -f apache-tomcat-8.0.9.tar.gz
mv apache-tomcat-7.0.55 /opt/
ln -s /opt/apache-tomcat-7.0.55 /etc/alternatives/tomcat-7.0
ln -s /opt/apache-tomcat-7.0.55 /usr/share/tomcat7
wget  http://repo.ar4k.eu/raw/strumenti-go.git/master/jar/commons-logging-tomcat-juli.jar
cp commons-logging-tomcat-juli.jar /usr/share/tomcat7/bin/

echo "Installo Maven 3" >> $console
wget http://apache.fastbull.org/maven/maven-3/3.2.2/binaries/apache-maven-3.2.2-bin.tar.gz
tar -xzf apache-maven-3.2.2-bin.tar.gz
#rm -f apache-maven-3.2.2-bin.tar.gz
mv apache-maven-3.2.2 /opt/
ln -s /opt/apache-maven-3.2.2 /etc/alternatives/maven-3
ln -s /opt/apache-maven-3.2.2 /etc/alternatives/maven
ln -s /opt/apache-maven-3.2.2 /usr/share/java/apache-maven-3.0.3
echo -e 'export M2_HOME=/etc/alternatives/maven\nexport PATH=${M2_HOME}/bin:${PATH}'  > /etc/profile.d/maven.sh
source /etc/profile.d/maven.sh

echo "Installo Grails 2.4.3" >> $console
wget http://dist.springframework.org.s3.amazonaws.com/release/GRAILS/grails-2.4.3.zip
unzip grails-2.4.3.zip
#rm -f grails-2.4.3.zip
mv grails-2.4.3 /opt/
ln -s /opt/grails-2.4.3 /etc/alternatives/grails-2.4.3

echo "Installo Grails 2.3.6" >> $console
wget http://dist.springframework.org.s3.amazonaws.com/release/GRAILS/grails-2.3.6.zip
unzip grails-2.3.6.zip
#rm -f grails-2.3.6.zip
mv grails-2.3.6 /opt/
ln -s /opt/grails-2.3.6 /etc/alternatives/grails-2.3.6

echo "Installo JBoss 7" >> $console
wget http://download.jboss.org/jbossas/7.1/jboss-as-7.1.1.Final/jboss-as-7.1.1.Final.tar.gz
tar -xzf jboss-as-7.1.1.Final.tar.gz
#rm -f jboss-as-7.1.1.Final.tar.gz
mv  jboss-as-7.1.1.Final /opt/

git clone  https://github.com/openshift/jboss-as7-modules.git
cp -r jboss-as7-modules/mysql/modules/* /opt/jboss-as-7.1.1.Final/modules
cp -r jboss-as7-modules/mongodb/modules/* /opt/jboss-as-7.1.1.Final/modules
#rm -rf jboss-as7-modules

ln -s /opt/jboss-as-7.1.1.Final /etc/alternatives/jbossas-7

# Reset per i contesti SELinux
restorecon -r /opt/tomcat-8.0 /opt/apache-maven-3.2.2 /opt/grails-2.4.3 /opt/jboss-as-7.1.1.Final /etc/alternatives/tomcat-8.0 /etc/alternatives/maven-3.0 /etc/alternatives/grails-2.4.3 /etc/alternatives/jbossas-7 

# Installa il repository SCL
# per php54-php-pecl-memcache
yum install -y centos-release-SCL &>> $dir_installazione/yum.log

# Forza installazione delle cartucce con dipendenze JBOSS, MAVEN e TOMCAT
mkdir -p $dir_installazione/rpm
cd $dir_installazione/rpm
#wget https://mirror.openshift.com/pub/origin-server/release/4/rhel-6/packages/x86_64/openshift-origin-cartridge-jbosseap-2.19.1.1-1.el6.noarch.rpm
wget https://mirror.openshift.com/pub/origin-server/release/4/rhel-6/packages/x86_64/openshift-origin-cartridge-jbossas-1.26.1.1-1.el6.noarch.rpm
wget https://mirror.openshift.com/pub/origin-server/release/4/rhel-6/packages/x86_64/openshift-origin-cartridge-jbossews-1.25.3.1-1.el6.noarch.rpm
rpm -Uvh --nodeps openshift-origin-cartridge-jbossas-1.26.1.1-1.el6.noarch.rpm openshift-origin-cartridge-jbossews-1.25.3.1-1.el6.noarch.rpm

# Installa lista software
cat > $dir_installazione/lista_software.txt << LISTA
openshift-origin-cartridge-dependencies-optional-all
openshift-origin-cartridge-dependencies-recommended-all
ruby193-ruby-devel
ruby193-rubygem-zbxapi
ImageMagick-devel
ImageMagick
tomcat6
augeas
openshift-origin-cartridge-10gen-mms-agent
openshift-origin-cartridge-cron
openshift-origin-cartridge-diy
openshift-origin-cartridge-haproxy
openshift-origin-cartridge-jbossas
openshift-origin-cartridge-jbossews
openshift-origin-cartridge-jenkins
openshift-origin-cartridge-jenkins-client
openshift-origin-cartridge-mock
openshift-origin-cartridge-mock-plugin
openshift-origin-cartridge-mongodb
openshift-origin-cartridge-mysql
openshift-origin-cartridge-nodejs
openshift-origin-cartridge-perl
openshift-origin-cartridge-php
openshift-origin-cartridge-phpmyadmin
openshift-origin-cartridge-postgresql
openshift-origin-cartridge-python
openshift-origin-cartridge-ruby
openshift-origin-cartridge-switchyard
LISTA

cat > $dir_installazione/lista_software_post.txt << LISTAPOST
php54-php-mysqlnd
php54-php-gd
php54-php-imap
php54-php-mcrypt
php54-php-pgsql
php54-php-snmp
php54-php-soap
php54-php-pear
php-xml
php54-php-mbstring
rubygem-rdoc
telnet
LISTAPOST

#MariaDB-server
#MariaDB-devel
#openshift-origin-cartridge-mariadb
# esclusi per conflitto tra MariaDB-common-5.5.39-1.i386 e mysql-libs-5.1.73-3.el6_5.x86_64

echo "Installa tutte le dipendenze e aggiorna il sistema" >> $console
for pack in $( cat $dir_installazione/lista_software.txt )
do 
   yum install -y --skip-broken $pack &>> $dir_installazione/yum.log
done

yum update -y

cd $dir_installazione

echo "Inizio installazione OpenShift (dipende dal sistema, dura circa un'ora.)" >> $console
echo >> $console
echo "----------------" >> $console
tail -F /tmp/openshift-deploy.log >> $console &
./installazione_OpenShift.sh -w origin_deploy -c configurazione_OpenShift.yml --force > installazione_OpenShift.log
killall tail
echo "Fine del processo di installazione" >> $console

cd $dir_installazione

echo "Creo il file per installazione demo" >> $console
cat > demo.sh << DEMO
#!/bin/bash
# installa pacchetti basi trovati in internet
echo "dura parecchi minuti..."
rhc app create amq diy-0.1 --from-code=http://repo.ar4k.eu/r/openshift-activemq-example.git --no-git
rhc app create bootgo jbossews-2.0 mysql-5.5 --from-code=http://repo.ar4k.eu/r/boot-go.git --no-git
rhc app create wordpress php-5.4 mysql-5.5 --from-code=http://repo.ar4k.eu/r/openshift-wordpress-example.git --no-git
rhc app create sugarcrm php-5.4 mysql-5.5 --from-code=http://repo.ar4k.eu/r/openshift-sugarcrm-example.git --no-git
rhc app create owncloud php-5.4 mysql-5.5 cron-1.4 --from-code=http://repo.ar4k.eu/r/openshift-owncloud-example.git --no-git
rhc app create grails jbossews-2.0 mysql-5.5 --from-code=http://repo.ar4k.eu/r/openshift-grails-example.git --no-git
rhc app create git jbossews-1.0 --from-code=http://repo.ar4k.eu/r/openshift-gitblit-example.git --no-git
#rhc app create testfuse https://raw.github.com/jboss-fuse/fuse-openshift-cartridge/jboss-fuse-6.1.x-379/metadata/manifest.yml --no-git
#rhc app create testfuse2 https://raw.github.com/jboss-fuse/fuse-openshift-cartridge/master/metadata/manifest.yml --no-git
rhc app create testcakephp php-5.4 mysql-5.5 --from-code=git://github.com/openshift/cakephp-example.git --no-git
rhc app create testcroogo php-5.3 mysql-5.1 --from-code=https://github.com/openshift-quickstart/croogoExample.git --no-git
rhc app create testelgg php-5.3 mysql-5.1 --from-code=https://github.com/openshift-quickstart/elgg-openshift-quickstart.git --no-git
rhc app create testlimesurvey php-5.3 mysql-5.1 --from-code=https://github.com/openshift-quickstart/limesurvey-quickstart --no-git
rhc app create testmagento php-5.3 mysql-5.1 --from-code=https://github.com/openshift/magento-example --no-git
#rhc app create testpacman nodejs-0.10 --from-code=https://github.com/openshift-quickstart/pacman.git --no-git
rhc app create testpiwik php-5.4 mysql-5.5 --from-code=git://github.com/openshift/piwik-openshift-quickstart.git --no-git
rhc app create testplone diy-0.1 --from-code=https://github.com/openshift-quickstart/plone-openshift-quickstart.git --no-git
rhc app create testwwwhisper diy-0.1 --from-code=git://github.com/wrr/wwwhisper-openshift.git --no-git
rhc app create testredmine ruby-1.9 mysql-5.5 --from-code=git://github.com/openshift/openshift-redmine-quickstart.git --no-git
rhc app create testroundcube php-5.3 mysql-5.1 phpmyadmin --from-code=https://github.com/openshift-quickstart/roundcube-openshift-quickstart.git --no-git
rhc app create testopencart php-5.4 mysql-5.5 --from-code=git://github.com/Atriedes/openshift-opencart.git --no-git
rhc app create testtornado python-2.6 --from-code=git@github.com:ramr/openshift-tornado-websockets.git --no-git
rhc app create testdroolsplanner jbossas-7 --from-code=git://github.com/eschabell/openshift-droolsplanner.git --no-git
rhc app create testquake2 jbossas-7 --from-code=git://github.com/wshearn/openshift-quickstart-quake2.git --no-git
rhc app create testgeoserver jbossews-2.0 --from-code=https://github.com/thesteve0/geoserver-on-openshift.git --no-git
rhc app create testelasticsearch http://cartreflect-claytondev.rhcloud.com/github/ncdc/openshift-elasticsearch-cartridge --no-git
rhc app-create testzabbix -s http://zabbix-agrimm.rhcloud.com/build/manifest/master mysql-5.1 --no-git
DEMO
chmod +x demo.sh

cd $dir_installazione

# Corregge il dns
#sed -i "s/${cur_ip_addr}/${pub_ip_addr}/" /var/named/dynamic/*.db
service named restart

cat > /etc/cgconfig.conf << CGCONFIG
#
#  Copyright IBM Corporation. 2007
#
#  Authors: Balbir Singh <balbir@linux.vnet.ibm.com>
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of version 2.1 of the GNU Lesser General Public License
#  as published by the Free Software Foundation.
#
#  This program is distributed in the hope that it would be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See man cgconfig.conf for further details.
#
# By default, mount all controllers to /cgroup/<controller>

mount {
  cpuset  = /cgroup/cpuset;
  cpu = /cgroup/cpu;
  cpuacct = /cgroup/cpuacct;
  memory  = /cgroup/memory;
  devices = /cgroup/devices;
  freezer = /cgroup/freezer;
  net_cls = /cgroup/net_cls;
  blkio = /cgroup/blkio;
}

CGCONFIG

# Servizi da avviare automaticamente
/sbin/chkconfig cgconfig on
/sbin/chkconfig cgred on
/sbin/chkconfig oddjobd on
service cgconfig restart
service cgred restart
service oddjobd restart

# Installa i post pack
for pack in $( cat $dir_installazione/lista_software_post.txt )
do 
   yum install -y --skip-broken $pack &>> $dir_installazione/yum_post.log
done

# Patch per cartuccia Tomcat 7
file1=/usr/libexec/openshift/cartridges/jbossews/bin/setup
if [ -e $file1 ]
then 
	echo >> $file1
	echo "# Correzione bug by Ambrosini" >> $file1
	echo 'ln -sf ${SYSTEM_JBOSSEWS_DIR}/bin/commons-logging-tomcat-juli.jar ${OPENSHIFT_JBOSSEWS_DIR}/bin/commons-logging-tomcat-juli.jar' >> $file1
fi
# anche nella cache del nodo
file2=/var/lib/openshift/.cartridge_repository/redhat-jbossews/0.0.19/bin/setup
if [ -e $file2 ]
then
	echo >> $file2
	echo "# Correzione bug by Ambrosini" >> $file2
	echo 'ln -sf ${SYSTEM_JBOSSEWS_DIR}/bin/commons-logging-tomcat-juli.jar ${OPENSHIFT_JBOSSEWS_DIR}/bin/commons-logging-tomcat-juli.jar' >> $file2
fi

echo "Lancio la diagnostica.." >> $console
cd $dir_installazione
./oo-diagnostics &> diagnostica.log

exit 0
