##
## keyboard_tui.py: text mode mouse selection dialog
##
## Large parts of this file were taken from the anaconda
## text mode mouse configuration screen
##
## Brent Fox <bfox@redhat.com>
## Mike Fulbright <msf@redhat.com>
## Jeremy Katz <katzj@redhat.com>
##
## Copyright (C) 2002, 2003 Red Hat, Inc.
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


from snack import *
import rhpl.keyboard
import keyboard_backend

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
import locale
locale.setlocale(locale.LC_ALL, "")
translate.textdomain_codeset ("system-config-keyboard", locale.nl_langinfo(locale.CODESET))
translate.textdomain_codeset ("rhpl", locale.nl_langinfo(locale.CODESET))


keyboardBackend = keyboard_backend.KeyboardBackend()

class KeyboardWindow:
    def __call__(self, screen):
        self.kbd = rhpl.keyboard.Keyboard()
        self.kbd.read()
        self.kbdDict = self.kbd.modelDict
        
        self.kbdKeys = self.kbdDict.keys()
        self.kbdKeys.sort()

        bb = ButtonBar(screen, [_("OK"), _("Cancel")])
        t = TextboxReflowed(40, 
                _("Select the appropriate keyboard for the system."))
        l = Listbox(8, scroll = 1, returnExit = 0)
        self.l = l

        key = 0
        default = ""
        for kbd in self.kbdKeys:
            if kbd == self.kbd.get():
                default = kbd

            plainName = self.kbdDict[kbd][0]
            l.append(plainName, kbd)
            key = key + 1

        l.setCurrent(default)

        g = GridFormHelp(screen, _("Keyboard Selection"), "kbdtype", 1, 4)
        g.add(t, 0, 0)
        g.add(l, 0, 1, padding = (0, 1, 0, 1))
        g.add(bb, 0, 3, growx = 1)

        rc = g.runOnce()

        button = bb.buttonPressed(rc)

        if button == "cancel":
            return self.kbd, -1

        choice = l.current()

        self.kbd.set(choice)
        kbdData = self.kbdDict[choice]
        return self.kbd, kbdData


class childWindow:
    def __init__(self):
        screen = SnackScreen()

        DONE = 0

        while not DONE:
            kbd, rc = KeyboardWindow()(screen)
            if rc == -1:
                screen.finish()
                DONE = 1
            else:
                screen.finish()
                kbd.write()
                kbd.activate()
                fullname, layout, model, variant, options = rc                
                keyboardBackend.modifyXconfig(fullname, layout, model, variant, options)
                DONE = 1
                
