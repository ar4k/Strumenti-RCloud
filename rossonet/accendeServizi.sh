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

# Spegne i servizi prima di costruire l'ami

HOME_ROSSONET=/opt/rossonet
cd $HOME_ROSSONET
for servizio in $( cat servizi.txt )
do
	echo "-----------------------------------"
	echo
	echo "Accendo il servizio $servizio ..."
	service $servizio start
done

exit 0



