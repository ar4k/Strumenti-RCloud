##
## keyboard_gui.py - GUI front end code for keyboard configuration
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
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.


import string
import gtk
import gobject
import sys
import os

import rhpl.keyboard as keyboard

sys.path.append('/usr/share/firstboot')
from firstboot_module_window import FirstbootModuleWindow

sys.path.append('/usr/share/system-config-keyboard')
import keyboard_backend

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
translate.textdomain ("system-config-keyboard")
translate.textdomain ("rhpl")

##
## Icon for windows
##

iconPixbuf = None      
try:
    iconPixbuf = gtk.gdk.pixbuf_new_from_file("/usr/share/system-config-keyboard/pixmaps/system-config-keyboard.png")
except:
    pass

keyboardBackend = keyboard_backend.KeyboardBackend()

# hack around the fact that scroll-to in the installer acts wierd
def setupTreeViewFixupIdleHandler(view, store):
    id = {}
    id["id"] = gobject.idle_add(scrollToIdleHandler, (view, store, id))

def scrollToIdleHandler((view, store, iddict)):
    if not view or not store or not iddict:
	return

    try:
	id = iddict["id"]
    except:
	return
    
    selection = view.get_selection()
    if not selection:
	return
    
    model, iter = selection.get_selected()
    if not iter:
	return

    path = store.get_path(iter)
    col = view.get_column(0)
    view.scroll_to_cell(path, col, True, 0.5, 0.5)

    if id:
	gobject.source_remove(id)

class KeyboardWindow(FirstbootModuleWindow):
    runPriority = 20
    moduleName = N_("Keyboard")
    moduleClass = "reconfig"
    windowTitle = N_("Keyboard")
    commentTag = N_("Configure the system keyboard")
    htmlTag = "kybd"
    shortMessage = N_("Select the appropriate keyboard for the system.")
    instDataKeyboard = None

    def getNext(self):
        self.kbd.set(self.type)
        self.kbd.beenset = 1
        self.kbd.activate()

        if self.instDataKeyboard:
            self.instDataKeyboard.set(self.type)
            self.instDataKeyboard.beenset = 1
            self.instDataKeyboard.activate()

    def select_row(self, *args):
        rc = self.modelView.get_selection().get_selected()
        if rc:
            model, iter = rc
            if iter is not None:
                key = self.modelStore.get_value(iter, 0)
                if key:
                    self.type = key

    def setupScreen(self, defaultByLang, kbd):
        self.kbd = kbd

        if not self.kbd.beenset:
            default = defaultByLang
        else:
            default = self.kbd.get()
        self.type = default

        self.modelStore = gtk.ListStore(gobject.TYPE_STRING,
                                        gobject.TYPE_STRING)
        self.modelStore.set_sort_column_id(1, gtk.SORT_ASCENDING)

        # Sort the UI by the descriptive names, not the keymap abbreviations.
        self.kbdDict = kbd.modelDict
        lst = self.kbdDict.items()
        lst.sort(lambda a, b: cmp(a[1][0], b[1][0]))

        for item in lst:
            iter = self.modelStore.append()
            self.modelStore.set_value(iter, 0, item[0])
            self.modelStore.set_value(iter, 1, item[1][0])

        self.modelView = gtk.TreeView(self.modelStore)
        self.col = gtk.TreeViewColumn(None, gtk.CellRendererText(), text=1)
        self.modelView.append_column(self.col)
        self.modelView.set_property("headers-visible", False)
        self.modelView.get_selection().set_mode(gtk.SELECTION_BROWSE)

        # Type ahead should search on the names, not the keymap abbreviations.
        self.modelView.set_enable_search(True)
        self.modelView.set_search_column(1)

        selection = self.modelView.get_selection()
        selection.connect("changed", self.select_row)

        iter = self.modelStore.get_iter_root()
        while iter is not None:
            if self.modelStore.get_value(iter, 0) == default:
                path = self.modelStore.get_path(iter)
                self.modelView.set_cursor(path, self.col, False)
                self.modelView.scroll_to_cell(path, self.col, True,
                                              0.5, 0.5)
                break
            iter = self.modelStore.iter_next(iter)

        self.modelViewSW = gtk.ScrolledWindow()
        self.modelViewSW.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.modelViewSW.set_shadow_type(gtk.SHADOW_IN)
        self.modelViewSW.add(self.modelView)

        # XXX set up a test area and do some sort of instant apply ?

        # set up the icon
        p = None
        try:
            p = gtk.gdk.pixbuf_new_from_file("../pixmaps/system-config-keyboard.png")
        except:
            try:
                p = gtk.gdk.pixbuf_new_from_file("/usr/share/system-config-keyboard/pixmaps/system-config-keyboard.png")
            except:
                pass

        if p:
            self.icon = gtk.Image()
            self.icon.set_from_pixbuf(p)

        self.myVbox = gtk.VBox()
        self.myVbox.pack_start(self.modelViewSW, True)

	setupTreeViewFixupIdleHandler(self.modelView,
				      self.modelView.get_model())
        
        
    def apply(self, *args):
        self.getNext()
        if not self.doDebug:
            self.kbd.write()
        # XXX should we munge the xconfig from this tool?

        # If the /etc/X11/XF86Config file exists, then change it's keyboard settings
        fullname, layout, model, variant, options = self.kbdDict[self.kbd.get()]

        keyboardBackend.modifyXconfig(fullname, layout, model, variant, options)

        try:
            #If we're in reconfig mode, this will fail because there is no self.mainWindow
            self.mainWindow.destroy()
        except:
            pass
        return 0

    def launch(self, doDebug=None):
        self.doDebug = doDebug
        if doDebug:
            print "in keyboard launch"
        kbd = keyboard.Keyboard()
        kbd.read()
        # XXX read the language to determine default keyboard?
        self.setupScreen("en_US", kbd)

        label = gtk.Label(_(self.shortMessage))
        label.set_alignment(0.0, 0.5)
        label.set_size_request(500, -1)
        self.myVbox.pack_start(label, False)
        self.myVbox.reorder_child(label, 0)
        self.myVbox.set_spacing(10)
        self.myVbox.set_border_width(10)

        outerVBox = gtk.VBox()
        outerVBox.pack_start(self.myVbox)

        return outerVBox, self.icon, self.windowTitle

    def stand_alone(self):
        self.doDebug = None
        kbd = keyboard.Keyboard()
        kbd.read()
        # XXX read the language to determine default keyboard?
        self.setupScreen("en_US", kbd)
        return FirstbootModuleWindow.stand_alone(self, KeyboardWindow.windowTitle, iconPixbuf)

    def anacondaScreen(self, label, kbd, instDataKeyboard=None):
        print label, kbd.get()
        self.doDebug = None
        self.keyboardLabel = label
        self.instDataKeyboard = instDataKeyboard
        self.setupScreen(kbd.get(), kbd)
        return FirstbootModuleWindow.anacondaScreen(self, KeyboardWindow.windowTitle, iconPixbuf, 400, 350)

    def okAnacondaClicked(self, *args):
        print "okAnacondaClicked", args
        self.getNext()
        print self.kbd.get()
        self.keyboardLabel.set_text(self.kbd.modelDict[self.kbd.get()][0])
        self.mainWindow.destroy()

childWindow = KeyboardWindow

