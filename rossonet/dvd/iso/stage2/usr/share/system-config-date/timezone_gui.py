## timezone_gui.py - Program creates a user interface 
##             that allows the system time, system date,
##             time zone, and ntpd configuration to be easily set
## Copyright (C) 2001, 2002, 2003 Red Hat, Inc.
## Copyright (C) 2001, 2002, 2003 Brent Fox <bfox@redhat.com>
##                                Tammy Fox <tfox@redhat.com>
## Copyright (C) 2005             Nils Philippsen <nphilipp@redhat.com>

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
import sys
import scdMainWindow
from timezone_map_gui import TimezoneMap
from zonetab import ZoneTab

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
translate.textdomain ("system-config-date")

def timezone_widget_create (xml):
    folder = "/usr/share/system-config-date/"
    mappath = folder + "pixmaps/map1440.png"
    regionspath = folder + "regions"
    tzActionLabel = xml.get_widget ('tzActionLabel')
    default = scdMainWindow.timezoneBackend.getTimezoneInfo()[0]
    widget = TimezoneMap(ZoneTab (), default, map=mappath, regions=regionspath, tzActionLabel = tzActionLabel)
    widget.show_all ()
    return widget

custom_widgets = {'timezone_widget_create': timezone_widget_create}

class timezonePage (gtk.VBox):
    def __init__(self, xml):
        self.xml = xml
        self.mainVBox = self.xml.get_widget ("tz_vbox")
        self.timezone = scdMainWindow.timezoneBackend.getTimezoneInfo()
        self.default, self.asUTC, self.asArc = self.timezone

        self.tz = self.xml.get_widget ("tz")

        self.utcCheck = self.xml.get_widget ("utc_check")
        if self.asUTC == "true":
            self.utcCheck.set_active(True)
        else:
            self.utcCheck.set_active(False)
        
    def getVBox(self):
        return self.mainVBox

    def getSmallVBox(self):
        self.mainVBox.remove(self.mainVBox.get_children()[0])
        return self.mainVBox

    def getTimezoneInfo(self):
        return self.tz.getCurrent().tz, self.utcCheck.get_active(), self.asArc
