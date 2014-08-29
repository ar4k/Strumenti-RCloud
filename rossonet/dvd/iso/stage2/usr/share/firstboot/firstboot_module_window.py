#
# firstboot_module_window.py - GUI parent class for firstboot/anaconda modules
#
# Copyright 2002 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

import gtk
from rhpl.translate import _, N_

class FirstbootModuleWindow:
    moduleName = None
    windowTitle = None
    shortMessage = None
    icon = None
    toplevel = None

    # also need to define runPriority and moduleClass

    def __init__(self, ics=None, *args):
        self.ics = ics
        if self.ics:
            self.setupICS()

    def setupICS(self):
        """Sets up anaconda install interface."""

        if self.windowTitle:
            self.ics.setTitle(_(self.windowTitle))

    def getICS(self):
        return self.ics

    def getPrev(self, *args):
        pass

    # actually to set up the interface for the module
    def setupScreen(self, *args):
        pass

    def getScreen(self, *args):
        toplevel = gtk.VBox()
        iconBox = gtk.HBox(False, 5)

        if not self.shortMessage:
            self.shortMessage = ""
        msgLabel = gtk.Label(_(self.shortMessage))
        msgLabel.set_line_wrap(True)
        msgLabel.set_alignment(0.0, 0.5)

        apply(self.setupScreen, args)
        toplevel.set_spacing(5)
        if self.icon:
            iconBox.pack_start(self.icon, False)
        iconBox.pack_start(msgLabel)
        toplevel.pack_start(iconBox, False)
        toplevel.pack_start(self.myVbox, True)

        return toplevel

    def okClicked(self, *args):
        if self.apply():
            gtk.main_quit()
        else:
            #apply failed for some reason, so don't exit the gtk main loop
            pass

    def apply(self, *args):
        pass

    def okAnacondaClicked(self, *args):
        pass

    def launch(self):
        internalVBox = gtk.VBox(False, 10)
        internalVBox.set_border_width(10)

        if self.shortMessage:
            self.shortMessage = ""
            msgLabel = gtk.Label(_(self.shortMessage))
            msgLabel.set_line_wrap(True)
            msgLabel.set_alignment(0.0, 0.5)
            internalVBox.pack_start(msgLabel, False)

        # Some modules don't have a myVbox defined, so don't raise a
        # traceback window here.
        try:
            internalVBox.pack_start(self.myVbox, True)
        except:
            return None

        toplevel = gtk.VBox()
        toplevel.pack_start(internalVBox, True)
        return toplevel, self.icon, self.windowTitle

    def stand_alone(self, title=None, iconPixbuf=None):
        self.mainWindow = gtk.Dialog()
        self.mainWindow.connect("destroy", self.destroy)
        self.mainWindow.set_border_width(10)
        self.mainWindow.set_size_request(400, 350)
        self.mainWindow.set_position(gtk.WIN_POS_CENTER)

        if iconPixbuf:
            self.mainWindow.set_icon(iconPixbuf)

        if title:
            self.mainWindow.set_title(_(title))

        okButton = self.mainWindow.add_button('gtk-ok', 0)
        okButton.connect("clicked", self.okClicked)

        toplevel = gtk.VBox()
        toplevel.set_spacing(5)
        iconBox = gtk.HBox(False, 5)
        if self.icon:
            iconBox.pack_start(self.icon, False)

        if not self.shortMessage:
            self.shortMessage = ""
        msgLabel = gtk.Label(_(self.shortMessage))
        msgLabel.set_line_wrap(True)
        msgLabel.set_alignment(0.0, 0.5)            
        iconBox.pack_start(msgLabel)

        toplevel.pack_start(iconBox, False)
        toplevel.pack_start(self.myVbox, True)

        #Remove the hsep from the dialog.  It's ugly
        hsep = self.mainWindow.get_children()[0].get_children()[0]
        self.mainWindow.get_children()[0].remove(hsep)
        self.mainWindow.vbox.pack_start(toplevel)
        self.mainWindow.show_all()
        gtk.main()

    def anacondaScreen(self, title=None, iconPixbuf=None, x=None, y=None):
        self.mainWindow = gtk.Dialog()
        self.mainWindow.connect("destroy", self.destroy)
        self.mainWindow.set_border_width(10)

        if x != None and y != None:
            self.mainWindow.set_size_request(x, y)
        self.mainWindow.set_position(gtk.WIN_POS_CENTER)

        if iconPixbuf:
            self.mainWindow.set_icon(iconPixbuf)

        if title:
            self.mainWindow.set_title(_(title))

        okButton = self.mainWindow.add_button('gtk-ok', 0)
        okButton.connect("clicked", self.okAnacondaClicked)

        toplevel = gtk.VBox()
        toplevel.set_spacing(5)
        iconBox = gtk.HBox(False, 5)
        if self.icon:
            iconBox.pack_start(self.icon, False)

        if not self.shortMessage:
            self.shortMessage = ""
        msgLabel = gtk.Label(_(self.shortMessage))
        msgLabel.set_line_wrap(True)
        msgLabel.set_alignment(0.0, 0.5)            
        iconBox.pack_start(msgLabel)

        toplevel.pack_start(iconBox, False)
        toplevel.pack_start(self.myVbox, True)

        #Remove the hsep from the dialog.  It's ugly
        hsep = self.mainWindow.get_children()[0].get_children()[0]
        self.mainWindow.get_children()[0].remove(hsep)
        self.mainWindow.vbox.pack_start(toplevel)
        self.mainWindow.show_all()
        gtk.main()

    def destroy(self, *args):
        gtk.main_quit()

    def renderCallback(self):
	return None
