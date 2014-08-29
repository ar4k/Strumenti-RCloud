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

mkdir -p /opt/op
cd /opt/op
echo "Copia l'immagine di OP in /opt/op e rimuove l'originale"
cp -a /root/postinstall/op/* . && rm -rf /root/postinstall/op

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
#. Crea il disco di ephemeral e la swap
#.
if [ -e op.bin.bz2 ]
then
echo "Decomprime il disco op" 
/usr/bin/bzip2 -d op.bin.bz2
fi

echo "Installa i file di configurazione"
cp op /etc/xen/
mkdir -p /xen
mkdir -p /etc/webmin/servers
cp 134854405871090.serv /etc/webmin/servers/ 
cp centos6x.cfg /xen
ln -s /xen/centos6x.cfg /etc/xen/centos6x
ln -s /xen/centos6x.cfg /etc/xen/auto/centos6x.cfg
#ln -s /etc/xen/op /etc/xen/auto/op

if [ -e ephemeral.ext3 ]
then
	echo "il disco ephemeral esiste"
else
	echo "Crea il disco ephemeral..."
	dd bs=1M count=100352 if=/dev/zero of=ephemeral.ext3
fi
echo
if [ -e swap.img ]
then
	echo "il disco swap esiste"
else
	echo "Crea il disco swap..."
	dd bs=1M count=2048 if=/dev/zero of=swap.img
fi
echo
#. Formatta in ext3 il disco ephemeral e
#. Prepara la partizione di swap
#.
echo "Prepara la partizione swap..."
mkswap swap.img
echo
echo "Formatta il disco ephemeral..."
mkfs.ext3 -F ephemeral.ext3

cd $vecchiacartella

exit 0

