## Clock.py - implements a simple text clock widget.
## Copyright (C) 2002, 2003 Red Hat, Inc.
## Copyright (C) 2002, 2003 Brent Fox <bfox@redhat.com>

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

import gtk
import gobject
import time

class Clock (gtk.HBox):
    def __init__(self, *args):
        gtk.HBox.__init__ (self)
        # always display clock left-to-right (#165109)
        self.set_direction(gtk.TEXT_DIR_LTR)
        self.interval = 1
        self.hour = gtk.Label("")
        self.minute = gtk.Label("")
        self.second = gtk.Label("")

        self.pack_start(self.hour, False)
        self.pack_start(gtk.Label(":"), False)
        self.pack_start(self.minute, False)
        self.pack_start(gtk.Label(":"), False)
        self.pack_start(self.second, False)

        times = time.localtime(time.time())
        self.setTime(times[3], times[4], times[5])

    def updateTime(self):
        times = time.localtime(time.time())
        self.setTime(times[3], times[4], times[5])
        return True
        
    def setTime(self, hour, minute, second):
        if hour < 10:
            hour = "0" + str(hour)

        if minute < 10:
            minute = "0" + str(minute)

        if second < 10:
            second = "0" + str(second)
            
        self.hour.set_text(str(hour))
        self.minute.set_text(str(minute))
        self.second.set_text(str(second))
        self.show_all()

    def setInterval(self, interval):
        self.interval = interval

    #def launch(self):
    #    return self

    def getTime(self):
        return self.hour.get_text(), self.minute.get_text(), self.second.get_text()
