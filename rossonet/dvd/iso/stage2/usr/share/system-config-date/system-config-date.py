#!/usr/bin/python2

## system-config-date - Program creates a user interface 
##             that allows the system time, system date,
##             time zone, and ntpd configuration to be easily set

## Copyright (C) 2001, 2002, 2003, 2005 Red Hat, Inc.
## Copyright (C) 2001, 2002, 2003 Brent Fox <bfox@redhat.com>
##                                Tammy Fox <tfox@redhat.com>
## Copyright (C) 2005 Nils Philippsen <nphilipp@redhat.com>

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import sys
import signal
import getopt

##
## I18N
##
import gettext
from rhpl.translate import _, N_
import rhpl.translate as translate
translate.textdomain ("system-config-date")

def showhelp ():
    sys.stderr.write (_("""Usage: system-config-date [options]
Enduser options:
-h|--help        Display this help message
Reserved options:
--page <page>    Display page <page>
"""))

def useGuiMode(page):
    try:
        import scdMainWindow
    except:
        #Starting the GUI failed, so let's start the text mode UI
        sys.stderr.write (_("Text mode interface is deprecated\n"))
        import time
        time.sleep (2)
        import timeconfig
        sys.exit(0)

    scdMainWindow.scdMainWindow(page).stand_alone()

if __name__ == "__main__":
    signal.signal (signal.SIGINT, signal.SIG_DFL)

    try:
        opts, rest = getopt.gnu_getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError, g:
        sys.stderr.write (gettext.gettext ("%s\n") % g)
        showhelp ()
        sys.exit (1)

    if rest:
        sys.stderr.write (_("option(s) '%s' not recognized\n") % ' '.join (rest))
        showhelp ()
        sys.exit (1)

    page = 0
    for opt, value in opts:
        if opt == '-h' or opt == '--help':
            showhelp ()
            sys.exit (0)
        if opt == "--page":
            page = int(value)

    useGuiMode(page)
