## strumenti-go

Script e template per gestire la piattaforma AR4K GO

Progetto di laboratorio per implementare AR4K Go
by Ambrosini (Rossonet s.c.a r.l.)

Esempi parametri di configurazione per test:
http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/bottegaio.yml;master.nodi.bottegaio.net;<password otp>;0
http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/lachimera.yml;master.nodi.lachimera.net;<password otp>;1
http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/ar4k.yml;master.nodi.ar4k.net;<password otp>;1

Per installare da kickstart CentOS 6.x su architettura x86_64 utilizzare un media di installazione valido (http://isoredirect.centos.org/centos/6/isos/x86_64/ o, per PXE ecc..., leggere https://www.centos.org/docs/5/html/5.2/Installation_Guide/ )

Nella finestra di boot di GRUB selezionare l'installazione grafica o testuale, premere tab e aggiungere il seguente parametro:

ks=http://go.rossonet.net/ks oo_config=<file configurazione OO> oo_host=<nome host da creare> oo_otp=<password otp> oo_nat=<1>

o

ks=http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/go.ks oo_config=<file configurazione OO> oo_host=<nome host da creare> oo_otp=<password otp> oo_nat=<0/1>

dove:
- oo_config è il percorso del file di configurazione di oo-install (ess. http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/lachimera.yml)
- oo_host è il nome host del componente che si sta creando FQDN (ess. master.nodi.lachimera.net)
- oo_otp se presente prova la connessione alla piattaforma AR4K utilizzando la password temporanea (otp=one time password ; ess. F5ght4e)
- oo_nat se presente e se settato a uno permette la configurazione di macchine con indirizzo ip pubblico diverso dall'ip della scheda. Alcuni casi: macchine in AWS EC2 o in rete FastWeb con il nat. (ess. 1)  

La seguente linea di comando, data su un sistema host con KVM o XEN e virt-manager installato, crea una macchina virtuale con la configurazione del dominio lachimera.net (tra parentesi quadre le opzioni facoltative):

virt-install -n <nome macchina virtuale> -r 1600 --vcpus=1 --os-variant=rhel6 -w bridge:virbr0 --disk path=/mnt/rossonet.img,size=16 -l http://mirror.centos.org/centos/6.5/os/x86_64/ -x "ks=http://go.rossonet.net/ks oo_config=http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/lachimera.yml oo_host=master.nodi.lachimera.net [oo_otp=xxxxxx oo_nat=1 proxy=http://utente:xxxxxxxx@proxyvip.adn.intra:8080 ip=10.10.21.76 netmask=255.255.255.240 dns=10.10.21.1 gateway=10.10.21.100] " --os-type=linux [--paravirt]

- l'opzione --paravirt funziona solo su macchine xen

Il relativo file di configurazione di Apache che risponde a go.rossonet.net:
################################################################
<VirtualHost *:80>
DocumentRoot /var/www/html
ServerName go.rossonet.net
Redirect /ks http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/go.ks
Redirect /installa  http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/installaOpenShift.sh
</VirtualHost>
################################################################


Per installare da console, da utente root, su una adeguata macchina CentOS 6.x x86_64 con un'installazione minima utilizzare il comando sotto; in EC2 usare l'ami ami-230b1b57, entrare in root con la chive pem gestita con AWS EC2 e digitare: 

bash <(curl -sL http://go.rossonet.net/installa) <file configurazione OO> <nome host da creare> <password otp> <opzione nat>

- Per il significato dei parametri vedere sopra

è possibile passare i parametri anche aggiungendo un file /root/go.conf con i quattro valori in un'unica riga divisi dal carattere ";". Per esempio:
http://repo.ar4k.eu/raw/strumenti-go.git/master/kickstart/lachimera.yml;master.nodi.lachimera.net;xxxxxxx;1

la stessa modalità di scrivere i parametri è valida in AWS EC2 per passare i parametri alla macchina dall'esterno. Usare il campo USER DATA in formato stringa. 
