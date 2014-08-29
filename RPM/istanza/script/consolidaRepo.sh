#!/bin/bash

# Repository Rossonet
echo "Ricrea la struttura del repositori i386"
createrepo --repo=Rossonet -s sha /var/www/html/rossonet/rpmrossonet/i386
echo "Ricrea la struttura del repositori x86_64"
createrepo --repo=Rossonet -s sha /var/www/html/rossonet/rpmrossonet/x86_64
