#/bin/bash
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
#. Crea una macchina xen da una Ami Amazon
#. by Ambrosini Rossonet s.c.a r.l. http://www.rossonet.com
#. andrea.ambrosini@rossonet.com
#.

# Memorizza la cartella di chiamata e si posiziona
vecchiacartella=$( pwd )
cartella=$( dirname $0 )
cd $cartella

# Input da Utente e guida
parametro1=$1

while [ "$nomemacchina" == ""  ]
do

nomemacchina=$parametro1

if [ "$nomemacchina" == ""  ]
then
        echo -n "Nome Macchina XEN da istanziare ( help per la guida, uscita per uscire ): "
        read nomemacchina
fi

if [ "$nomemacchina" == "help" ]
then
nomemacchina=""
grep "#\." $0 | sed "s/^#\.//"
exit 0
fi

#. Usare il comando uscita per terminare
if [ "$nomemacchina" == "uscita" ]
then
nomemacchina=""
exit 0
fi

done
#.
#. I file devono essere posizionati nella directory dello script
#. come elencato:
#. 
#. - ami.ext3 = Immagine Macchina ( Per ottenere l'immagine da una macchina
#.				Amazon EC2 scaricarla con ec2-download-bundle
#.				e ricostruirla con ec2-unbundle	)
#. - initrd.img = RAM Disk XEN
#. - vmlinuz.bin = Kernel XEN
#.
#.

echo
echo
#. Crea il disco di ephemeral e la swap
#.
if [ -e ephemeral.ext3 ]
then
	echo "il disco ephemeral esiste"
else
	echo "Crea il disco ephemeral..."
	dd bs=1M count=147000 if=/dev/zero of=ephemeral.ext3
fi

echo
echo

if [ -e swap.img ]
then
	echo "il disco swap esiste"
else
	echo "Crea il disco swap..."
	dd bs=1M count=1024 if=/dev/zero of=swap.img
fi

echo
echo

#. Formatta in ext3 il disco ephemeral e
#. Prepara la partizione di swap
#.

echo "Prepara la partizione swap..."
mkswap swap.img

echo
echo

echo "Formatta il disco ephemeral..."
mkfs.ext3 -F ephemeral.ext3

#. Prepara la configurazione per XEN
#.
attuale=$( pwd | sed 's/\//\\\//g' )

echo "Copia il template virsh"
cp ami.xml $nomemacchina.xml

echo "Completa il template..."

sed --in-place "s/<nome-da-sostituire>/$nomemacchina/" $nomemacchina.xml
#sed --in-place "s/<kernel-da-sostituire>/$attuale\/vmlinuz.bin/" $nomemacchina.xml
#sed --in-place "s/<ramdisk-da-sostituire>/$attuale\/initrd.img/" $nomemacchina.xml
sed --in-place "s/<ephemeral-da-sostituire>/$attuale\/ephemeral.ext3/" $nomemacchina.xml
sed --in-place "s/<root-da-sostituire>/$attuale\/ami.ext4/" $nomemacchina.xml
sed --in-place "s/<swap-da-sostituire>/$attuale\/swap.img/" $nomemacchina.xml

#. Fa partire la macchina XEN
#.
echo
echo
echo "Crea il dominio XEN..."

virsh create $nomemacchina.xml

# Ritorna alla cartella chiamante

cd $vecchiacartella

exit 0

