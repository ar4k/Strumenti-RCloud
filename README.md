## strumenti-go

Script e template per gestire la piattaforma AR4K GO

Progetto di laboratorio per implementare AR4K Go
by Ambrosini (Rossonet s.c.a r.l.)

Per installare il pacchetto grails su OpenShift Origin:
rhc app create <name> jbossews-2.0 mysql-5.5 --from-code=http://repo.ar4k.eu/r/boot-go.git

Per installare un nuovo host OpenShift su EC2

1. Configurare una macchina base (pacchetti minimi) di CentOS6 x86_64
2. modificare /etc/rc.local aggiungendo:

      # Installa OpenShift
      cd /root
      wget http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/installaOpenShift.sh
      chmod +x installaOpenShift.sh
      /root/installaOpenShift.sh
      #

3. Avviare la macchina amazon con i parametro in user metadata

	<file di configurazione openshift>;<nome host>

per esempio:

http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/bottegaio.yml;master.nodi.bottegaio.net
http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/lachimera.yml;master.nodi.lachimera.net
http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/ar4k.yml;master.nodi.ar4k.net

Per i nostri test usiamo l'ami: 20140821-OpenShift-Template (ami-d6ae70a1)


Infine, per lanciare l'installazione da un KickStart di Anaconda su CentOS 6 x86_64
inserire il seguente parametro al grub del network cd o install cd:

ks=http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/go.ks

o

ks=http://go.rossonet.net/interno

o

ks=http://go.rossonet.net/esterno



Per creare una macchina virtuale XEN o KVM:

virt-install -n <nome macchina virtuale> -r 1600 --vcpus=1 --os-variant=rhel6 --paravirt -w bridge:xenbr0 --disk path=/opt/images/rossonet.img,size=16 -l http://mirror.centos.org/centos/6.5/os/x86_64/ -x "ks=http://go.rossonet.net/interno proxy=http://andrea.ambrosini:xxxxxxxx@proxyvip.adn.intra:8080 ip=10.10.21.76 netmask=255.255.255.240 dns=10.10.21.1 gateway=10.10.21.100" --os-type=linux

- l'opzione --paravirt funziona solo su macchine xen

il video demo è realizzato con questo comando su macchina locale:

virt-install -n openshift --ram 2048 --vcpus=1 --os-variant=rhel6 -w network:default --disk path=/mnt/rossonet.img,size=16 -l http://mirror.centos.org/centos/6.5/os/x86_64/ -x "ks=http://go.rossonet.net/interno proxy=http://localhost:3128" --os-type=linux


Il relativo file di configurazione di Apache

<VirtualHost *:80>
DocumentRoot /var/www/html
ServerName go.rossonet.net
Redirect /esterno http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/go.ks
Redirect /interno http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/internal.ks
</VirtualHost>

in EC2, su una macchina adeguata (ami-230b1b57):

bash <(curl -sL http://go.rossonet.net/ec2) http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/ar4k.yml master.nodi.ar4k.net

Per connessione IPA e creazione directory:
ipa-client-install --domain=ar4k.net -w <password on shot> --mkhomedir --enable-dns-updates -U
( con opzione -d per il debug )

MOLTI FILE SONO IN CACHE NELLE DIR RPM,JAR E TGZ se dovessero sparire dalla rete.
