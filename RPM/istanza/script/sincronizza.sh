#!/bin/bash
# Sincronizza il repository
if [ -f /var/lock/subsys/rsync_updates ]; then
    echo "Updates via rsync already running."
    exit 0
fi
if [ -d /var/www/html/rossonet/media/CentOS/5.9 ] ; then
    touch /var/lock/subsys/rsync_updates
    rsync  -avSHP --delete --exclude "local*" --exclude "isos" mirror.i3d.net::centos/5.9/ /var/www/html/rossonet/media/CentOS/5.9/
    /bin/rm -f /var/lock/subsys/rsync_updates
else
    echo "Target directory /var/www/html/rossonet/media/CentOS/5.9 not present."
    mkdir -p /var/www/html/rossonet/media/CentOS/5.9
fi
