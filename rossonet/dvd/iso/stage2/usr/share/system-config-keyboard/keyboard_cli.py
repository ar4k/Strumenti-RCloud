##
## keyboard_cli.py: command line keyboard configuration
##
## Copyright (C) 2003 Red Hat, Inc.
## Copyright (C) 2002, 2003 Brent Fox <bfox@redhat.com>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU Library Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import sys
import string
from rhpl.translate import _
import keyboard_backend
import rhpl.keyboard as keyboard

keyboardBackend = keyboard_backend.KeyboardBackend()

class childWindow:
    def usage(self):
        print _("""Usage: system-config-keyboard [--help] [--noui] [--text] [<keyboardtype>]
       --help            Print out this message.
       --noui            Run in command line mode.
       --text            Run in text interface mode.
       """)
               
        keys = self.kbdDict.keys()
        keys.sort()

        kbd_string = string.join(keys, ", ")
        print "      ", _("<keyboardtype> options are:"), kbd_string
        sys.exit(1)

    def __init__(self, kbdtype, help):
        self.kbd = keyboard.Keyboard()
        self.kbdDict = self.kbd.modelDict

        if help:
            self.usage()

        if kbdtype == []:
            print (_("You must specify a valid keyboard type."))
            print (_("Run 'system-config-keyboard --help' to see a list of keymaps."))
        else:
            keymapIsValid = 0
            keymap = None

            keys = self.kbdDict.keys()
            keys.sort()

            if kbdtype in keys:
                fullname, layout, model, variant, options = self.kbdDict[kbdtype]
                self.kbd.set(kbdtype)
                self.kbd.write()
                self.kbd.activate()
                keyboardBackend.modifyXconfig(fullname, layout, model, variant, options)
            else:
                print (_("'%s' is an invalid keymap.  Please run 'system-config-keyboard --help' "
                         "for a list of keymaps" % kbdtype))
