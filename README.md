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

Per i nostri test usiamo l'ami: 20140821-OpenShift-Template (ami-d6ae70a1)


Infine, per lanciare l'installazione da un KickStart di Anaconda su CentOS 6 x86_64
inserire il seguente parametro al grub del network cd o install cd:

ks=http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/go.ks

o

ks=http://go.rossonet.net/ks

Il relativo file di configurazione di Apache

<VirtualHost *:80>
DocumentRoot /var/www/html
ServerName go.rossonet.net
Redirect /ks http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/go.ks
</VirtualHost>


MOLTI FILE SONO IN CACHE NELLE DIR RPM,JAR E TGZ se dovessero sparire dalla rete.
