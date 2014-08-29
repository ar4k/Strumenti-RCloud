#!/bin/bash
#.
#. Realizzato da Rossonet s.c.a r.l.
#. Rilasciato con licenza GNU Affero General Public License
#. la licenza AGPL è disponibile qui: http://www.gnu.org/licenses/agpl-3.0.html
#.
#. Per informazioni ed eventuali contratti di supporto:
#. http://www.rossonet.com
#. andrea.ambrosini@rossonet.com
#
#. Rossonet s.c.a r.l. distributes this code under GNU Affero General Public License ( AGPLv3 )
#. All right not expressly granted are reserved.
#
#. Autore: Andrea Ambrosini
#. Contributi:	Davide Prato ( davide.prato@rossonet.com )
#.		Laura Baldassarri ( laura.baldassarri@rossonet.com )
#.		Gianni Ghedini ( gianni.ghedini@acantho.com )
#.
# Descrizione Prodotto:
#
#.
#. Questo script converte una macchina istanziata
#. da una ami S3 in una macchina XEN per OpenNebula
#. o DVD XEN
#.
#. Con la macchina XEN, che ha il filesystem permanente,
#. si può erogare servizio ai clienti in produzione su cloud privati.
#.
#. by Ambrosini - Rossonet s.c.a r.l.
#.
#. Carica sempre /etc/rossonet/ec2Account se presente
if [ -f /etc/rossonet/ec2Account ]
then
 source /etc/rossonet/ec2Account
else
 echo "/etc/rossonet/ec2Account Non esiste..."
fi
#.

# Carica le variabili per EC2

# Input da Utente e guida
cd /mnt
parametro1=$1

while [ "$nomemacchina" == ""  ]
do

nomemacchina=$parametro1

if [ "$nomemacchina" == ""  ]
then
	echo -n "Inserisci il nome del progetto con cui nominare la macchina ( help per la guida o uscita ): "
        read nomemacchina
fi

if [ "$nomemacchina" == "help" ]
then
nomemacchina=""
grep "#\." /opt/rossonet/dvd/$( basename $0 ) | sed "s/^#\.//"
exit 0
fi
#. -------------------------------------
#. Usare il comando uscita per terminare
#. ------------------------------------
if [ "$nomemacchina" == "uscita" ]
then
nomemacchina=""
exit 0
fi

done


NOME=$nomemacchina
#DESCRIZIONE="Server $nomemacchina copiato da $MATRICE ( $NOMEAMI )"
IMAGE='/mnt/disco-xen.bin'
XEN_MOUNT_POINT='/mnt/xen-mnt'

echo
echo "Crea il disco su filesystem..."
dd bs=1M count=10240 if=/dev/zero of=$IMAGE
echo
echo "Crea il mount point..."
mkdir -p $XEN_MOUNT_POINT
echo
echo "Formatta il disco..." 
mkfs.ext4 -F $IMAGE
echo
echo "Monta il disco..." 
mount  $IMAGE $XEN_MOUNT_POINT -o loop
echo
echo "Copia l'immagine sul disco..."
#make a local working copy
#rm -rf /mnt/tmp
#mkdir /mnt/tmp
echo "Inizio la copia. Attendere..."

#.
#. Spegne i servizi critici ( configurati in /etc/rossonet/serviziDaGestire.txt )
/opt/rossonet/spegniServizi.sh
#.

rsync -av --exclude=/etc/rossonet/*.rsyncremove --exclude=/root/.bash_history --exclude=/etc/rossonet/context.sh --exclude=/etc/rossonet/ec2Account --exclude=/etc/rossonet/ec2-cert.pem --exclude=/etc/rossonet/ec2-pk.pem --exclude=/home/*/.bash_history --exclude=/etc/ssh/ssh_host_* --exclude=/etc/ssh/moduli --exclude=/etc/udev/rules.d/*persistent-net.rules --exclude=/var/lib/ec2/* --exclude=/mnt/* --exclude=/proc/* --exclude=/tmp/* --exclude=/sys/* / $XEN_MOUNT_POINT >/dev/null

#
# Accende i servizi
#
/opt/rossonet/accendeServizi.sh
#

#clear out log files
cd $XEN_MOUNT_POINT/var/log
for i in `ls ./**/*`; do
  echo $i && echo -n> $i
done
# Ripristina i file Originale AMAZON
if [ -f $XEN_MOUNT_POINT/etc/fstab ]
then
 mv $XEN_MOUNT_POINT/etc/fstab $XEN_MOUNT_POINT/etc/fstab.bak
 cp /opt/rossonet/dvd/fstab $XEN_MOUNT_POINT/etc/fstab
fi

sync;sync
echo
echo "Smonta"
sleep 5
cd /mnt
umount $XEN_MOUNT_POINT
rm -rf $XEN_MOUNT_POINT
echo
echo "Crea la struttura della directory..."
destinazione="/mnt/xen/$nomemacchina"
if [ -e $destinazione ]
then
 rm -rf $destinazione
fi
cp -a /opt/rossonet/xen $destinazione
echo
echo "Sposta il disco..."
mv $IMAGE $destinazione/$nomemacchina.bin
echo
cd $destinazione
#qemu-img convert -c -f raw -O qcow2 $nomemacchina.bin $nomemacchina.qcow2
#rm -f $nomemacchina.bin
#echo "Crea il file tar..."
#tar -cf $nomemacchina.tar xen-$nomemacchina
bzip2 -9 $nomemacchina.bin
ln -s $nomemacchina.bin.bz2 ami.bin.bz2
cp -a /opt/rossonet/dvd/templateNebulizza/* $destinazione/
echo "Completato!"

exit 0
