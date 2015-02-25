# strumenti-go

Script e template per gestire la piattaforma AR4K GO, CentOS, OpenShift

###Progetto di laboratorio per implementare AR4K Go
###by Ambrosini (Rossonet s.c.a r.l.)
primo laboratorio con Gianni Ghedini c/o Acantho S.p.A.

##Sezione Script creazione iso Fedora

requisiti: (da completare)

uso:
(da root)
git clone https://github.com/rossonet/Strumenti-RCloud.git
cd kickstart/
./fedora-creaLive.sh fedora-client-rossonet.ks

L'immagine generata è un DVD Fedora live 21 con funzione di installazione.
E' possibile creare una chiavetta USB avviabile con la funzione di salvataggio dei dati utilizzando questa spin Rossonet. (https://fedorahosted.org/liveusb-creator/)

##Sezione Script Rossonet 

Nella cartella Rossonet sono presenti gli script bash per clonare il sistema sulle varie piattaforme virtuali
(da fare RPM e Repository yum)


##Sezione OpenShift

l'account host deve poter creare i servizi su se stesso in FREEIPA

Esempi parametri di configurazione per test:
https://github.com/rossonet/Strumenti-RCloud/blob/master/openshift/bottegaio.yml;master.nodi.bottegaio.net;<password otp>;0
https://github.com/rossonet/Strumenti-RCloud/blob/master/openshift/lachimera.yml;master.nodi.lachimera.net;<password otp>;1
https://github.com/rossonet/Strumenti-RCloud/blob/master/openshift/ar4k.yml;master.nodi.ar4k.net;<password otp>;1

Per installare da kickstart CentOS 6.x su architettura x86_64 utilizzare un media di installazione valido (http://isoredirect.centos.org/centos/6/isos/x86_64/ o, per PXE ecc..., leggere https://www.centos.org/docs/5/html/5.2/Installation_Guide/ )

Nella finestra di boot di GRUB selezionare l'installazione grafica o testuale, premere tab e aggiungere il seguente parametro:

ks=https://hc.rossonet.net/openshift oo_config=<file configurazione OO> oo_host=<nome host da creare> oo_otp=<password otp> oo_nat=<1>

o

ks=https://raw.githubusercontent.com/rossonet/Strumenti-RCloud/master/openshift/go.ks oo_config=<file configurazione OO> oo_host=<nome host da creare> oo_otp=<password otp> oo_nat=<0/1>

i parametri hanno il seguente significato:
- oo_config è il percorso del file di configurazione di oo-install (ess. https://github.com/rossonet/Strumenti-RCloud/blob/master/openshift/lachimera.yml)
- oo_host è il nome host del componente che si sta creando FQDN (ess. master.nodi.lachimera.net)
- oo_otp se presente prova la connessione alla piattaforma AR4K utilizzando la password temporanea (otp=one time password ; ess. F5ght4e)
- oo_nat se presente e se settato a uno permette la configurazione di macchine con indirizzo ip pubblico diverso dall'ip della scheda. Alcuni casi: macchine in AWS EC2 o in rete FastWeb con il nat. (ess. 1)  

La seguente linea di comando, data su un sistema host con KVM o XEN e virt-manager installato, crea una macchina virtuale con la configurazione del dominio lachimera.net (tra parentesi quadre le opzioni facoltative):

virt-install -n <nome macchina virtuale> -r 1600 --vcpus=1 --os-variant=rhel6 -w bridge:virbr0 --disk path=/mnt/rossonet.img,size=16 -l http://mirror.centos.org/centos/6.5/os/x86_64/ -x "ks=https://hc.rossonet.net/openshift oo_config=https://github.com/rossonet/Strumenti-RCloud/blob/master/openshift/lachimera.yml oo_host=master.nodi.lachimera.net [oo_otp=xxxxxx oo_nat=1 proxy=http://utente:xxxxxxxx@proxyvip.adn.intra:8080 ip=10.10.21.76 netmask=255.255.255.240 dns=10.10.21.1 gateway=10.10.21.100] " --os-type=linux [--paravirt]

l'opzione --paravirt funziona solo su macchine xen

Il relativo file di configurazione di Apache che risponde a hc.rossonet.name:
<VirtualHost *:443>
DocumentRoot /var/www/html
ServerName hc.rossonet.name
Redirect /openshift https://raw.githubusercontent.com/rossonet/Strumenti-RCloud/master/openshift/go.ks
Redirect /oo https://raw.githubusercontent.com/rossonet/Strumenti-RCloud/master/openshift/installaOpenShift.sh
</VirtualHost>


Per installare da console, da utente root, su una adeguata macchina CentOS 6.x x86_64 con un'installazione minima utilizzare il comando sotto; in EC2 usare l'ami ami-6bcd591c (https://console.aws.amazon.com/ec2/home?region=eu-west-1#launchAmi=ami-6bcd591c), entrare in root con la chive pem gestita con AWS EC2 e digitare: 

bash <(curl -sL https://hc.rossonet.name/oo) <file configurazione OO> <nome host da creare> <password otp> <opzione nat>

Per esempio:
bash <(curl -sL https://hc.rossonet.name/oo) https://github.com/rossonet/Strumenti-RCloud/blob/master/openshift/ar4k.yml master.nodi.ar4k.net password 1

- Per il significato dei parametri vedere sopra

è possibile passare i parametri anche aggiungendo un file /root/go.conf con i quattro valori in un'unica riga divisi dal carattere ";". Per esempio:
https://github.com/rossonet/Strumenti-RCloud/blob/master/openshift/lachimera.yml;master.nodi.lachimera.net;xxxxxxx;1

la stessa modalità di scrivere i parametri è valida in AWS EC2 per passare i parametri alla macchina dall'esterno. Usare il campo USER DATA in formato stringa. 
