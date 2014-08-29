## scdMainWindow.py - Program creates a user interface 
##             that allows the system time, system date,
##             time zone, and ntpd configuration to be easily set
## Copyright (C) 2001, 2002, 2003 Red Hat, Inc.
## Copyright (C) 2001, 2002, 2003 Brent Fox <bfox@redhat.com>
##                          Tammy Fox <tfox@redhat.com>

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
import gtk.glade
import gobject
import string
import re
import time
import os
import sys
import date_gui
import timezone_gui
import dateBackend
import timezoneBackend
import signal

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = "system-config-date"
translate.textdomain (domain)
gtk.glade.bindtextdomain (domain)

#Initialize date and timezone backend
dateBackend = dateBackend.dateBackend()
timezoneBackend = timezoneBackend.timezoneBackend()
        
nameTag = _("Date & Time")
commentTag = _("Change system date and time")

class scdMainWindow:
    def destroy(self, args=None):
        self.win.destroy()
        if gtk.__dict__.has_key ("main_quit"):
            gtk.main_quit ()
        else:
            gtk.mainquit ()

    def response_cb (self, dialog, response_id, pid):
        if response_id == gtk.RESPONSE_CANCEL:
            os.kill (pid, signal.SIGINT)
        dialog.hide ()

    def showNtpFailureDialog (self, ntpServers):
        yesno = self.showErrorDialog(_("Couldn't connect to one of these time servers:\n\n%s\n\n"
                                       "Either none of them are available or the firewall settings "
                                       "on your computer are blocking NTP connections.\n\n"
                                       "Do you want to change your configuration to work around this issue now?" %
                                       (string.join (ntpServers, "\n"))), gtk.BUTTONS_YES_NO)

        if yesno == gtk.RESPONSE_YES:
            return True
        else:
            return False

    def ok_clicked(self, *args):
        self.apply ()

    def apply (self):
        sysDate = self.datePage.getDate()
        sysTime = self.datePage.getTime()
        ntpEnabled = self.datePage.getNtpEnabled()

        if ntpEnabled == False:
            #We're not using ntp, so stop the service
            self.dateBackend.stopNtpService()
            #set the time on the system according to what the user set it to
            self.dateBackend.writeDateConfig(sysDate, sysTime)
            self.dateBackend.syncHardwareClock()
            self.closeParent = True
            self.dateBackend.chkconfigOff()

        elif ntpEnabled == True:
            #We want to use NTP
            ntpFailDialogShown = False
            ntpServers = self.datePage.getNtpServers ()
            ntpServerChoices = self.datePage.getNtpServerChoices ()
            ntpBroadcastClient = self.datePage.getNtpBroadcastClient ()
            ntpLocalTimeSource = self.datePage.getNtpLocalTimeSource ()
            ntpStepTime = self.datePage.getNtpStepTime ()

            if len (ntpServers) == 0 and not ntpBroadcastClient:
                self.showErrorDialog(_("Please specify an NTP server to use or enable NTP broadcast."))
                return

            if self.dateBackend.writeNtpConfig(ntpServers, ntpServerChoices, ntpBroadcastClient, ntpLocalTimeSource, ntpStepTime) == None:
                if self.showNtpFailureDialog (ntpServers):
                    return
                else:
                    ntpFailDialogShown = True
            
            self.failureServers = None
            self.childHandled = False

            def child_handler (signum, stack_frame):
                realpid, waitstat = os.waitpid(pid, os.WNOHANG)
                if realpid != pid:
                    return
                if gtk.__dict__.has_key ("main_quit"):
                    gtk.main_quit ()
                else:
                    gtk.mainquit()
                result = os.read (read,100)
                os.close (read)
                signal.signal (signal.SIGCHLD, signal.SIG_DFL)
                
                if not ntpFailDialogShown and (result == "" or  int(result) > 0):
                    self.failureServers = ntpServers
                else:
                    self.closeParent = True
                    if gtk.__dict__.has_key ("main_quit"):
                        gtk.main_quit ()
                    else:
                        gtk.mainquit ()
                    self.dateBackend.syncHardwareClock()

                self.childHandled = True
                return

            signal.signal (signal.SIGCHLD, child_handler)
            (read, write) = os.pipe ()
            pid = os.fork ()

            if pid == 0:
                signal.signal (signal.SIGCHLD, signal.SIG_DFL)
                # do something slow
                os.close (read)
                time.sleep (2)
                retval = self.dateBackend.startNtpService(None)
                retval = str(retval)
                os.write (write, retval)
                os._exit (0)

            os.close (write)

            dlg = gtk.Dialog('', self.win, 0, (gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL))
            dlg.set_border_width(10)
            label = gtk.Label(_("Contacting NTP server.  Please wait..."))
            dlg.vbox.set_spacing(5)
            dlg.vbox.add(label)
            dlg.set_position (gtk.WIN_POS_CENTER_ON_PARENT)
            dlg.set_modal(True)
            dlg.connect ('response', self.response_cb, pid)
            dlg.show_all()

            if gtk.__dict__.has_key ("main"):
                gtk.main ()
            else:
                gtk.mainloop()
            dlg.destroy()

            while not self.childHandled:
                if gtk.gdk.events_pending ():
                    gtk.main_iteration ()
                time.sleep (0.1)

            if self.failureServers and not ntpFailDialogShown:
                if not self.showNtpFailureDialog (self.failureServers):
                    self.closeParent = True
                ntpFailDialogShown = True

            self.dateBackend.chkconfigOn()

        #Get the timezone info from the timezone page
        if "timezone" in self.showPages:
            timezone, utc, arc = self.timezonePage.getTimezoneInfo()
        else:
            timezone, utc, arc = self.timezoneBackend.getTimezoneInfo()

        self.timezoneBackend.writeConfig(timezone, utc, arc)

        if self.closeParent == True and not self.firstboot:
            if gtk.__dict__.has_key ("main_quit"):
                gtk.main_quit ()
            else:
                gtk.mainquit()

        return 0

    def custom_handler (self, glade, function_name, widget_name, str1, str2, int1, int2):
        for module in self.custom_handler_modules:
            if module.__dict__.has_key ("custom_widgets") and module.custom_widgets.has_key (function_name):
                return module.custom_widgets[function_name] (glade)

    def firstboot_widget (self):
        if len (self.showPages) == 1:
            self.nb.set_show_tabs (False)
        else:
            self.nb.set_show_tabs (True)
        return self.nb

    def firstboot_apply (self):
        return self.apply ()

    def __init__(self, page=None, firstboot=False, showPages=None):
        self.page = page
        self.dateBackend = dateBackend
        self.timezoneBackend = timezoneBackend
        self.closeParent = False
        self.firstboot = firstboot
        self.allPages = ["datetime", "ntp", "timezone"]
        self.allPagesWidgets = {"datetime": "datetime_vbox", "ntp": "ntp_vbox", "timezone": "tz_vbox"}
        if showPages is None:
            self.showPages = self.allPages
        else:
            self.showPages = showPages

        self.custom_handler_modules = [date_gui, timezone_gui]
        gtk.glade.set_custom_handler (self.custom_handler)

        if os.access ("system-config-date.glade", os.F_OK):
            self.xml = gtk.glade.XML ("system-config-date.glade", domain="system-config-date")
        else:
            self.xml = gtk.glade.XML ("/usr/share/system-config-date/system-config-date.glade", domain="system-config-date")

        #-----------Main Window-----------#
        self.win = self.xml.get_widget ("window")
        self.win.set_property ("no_show_all", True)
        self.win.connect ('destroy', self.destroy)

        self.vbox = self.xml.get_widget ("main_vbox")

        #------------Notebook-------------#
        self.nb = self.xml.get_widget ("notebook")
        # remove pages that shall not be displayed (firstboot)
        for page in self.allPages:
            widget = self.xml.get_widget (self.allPagesWidgets[page])
            if widget:
                if page in self.showPages:
                    widget.show ()
                else:
                    widget.hide ()
        self.nb.set_property ("no_show_all", True)
        self.datePage = date_gui.datePage (self.dateBackend, self.xml)
        self.timezonePage = timezone_gui.timezonePage (self.xml)

        #-------------Buttons-------------#
        helpButton = self.xml.get_widget ("help_button")
        helpButton.connect ('clicked', self.help_clicked)        
        
        cancelButton = self.xml.get_widget ("cancel_button")
        cancelButton.connect('clicked', self.destroy)

        okButton = self.xml.get_widget ("ok_button")
        okButton.connect ('clicked', self.ok_clicked)

        if firstboot:
            self.vbox.remove(self.nb)

    def help_clicked(self, args):
        help_pages = ["file:///usr/share/doc/system-config-date-1.8.12/system-config-date.xml#s1-dateconfig-time-date",
                      "file:///usr/share/doc/system-config-date-1.8.12/system-config-date.xml#s1-dateconfig-ntp",
                      "file:///usr/share/doc/system-config-date-1.8.12/system-config-date.xml#s1-dateconfig-time-zone"
                      ]

        page = help_pages [self.nb.get_current_page ()]
        path = "/usr/bin/yelp"

        if path == None:
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,
                                    (_("Help is not available.")))
            dlg.set_position(gtk.WIN_POS_CENTER)
            dlg.run()
            dlg.destroy()
            return
        
        pid = os.fork()
        if not pid:
            os.execv(path, [path, page])
       
    def stand_alone(self):
        self.win.show ()
        if self.page and (self.page == 0 or self.page == 1):
            self.nb.set_current_page(self.page)
        if gtk.__dict__.has_key ("main"):
            gtk.main ()
        else:
            gtk.mainloop ()

    def showErrorDialog(self, text, buttons = gtk.BUTTONS_OK):
        dlg = gtk.MessageDialog(self.win, 0, gtk.MESSAGE_ERROR, buttons, text)

        dlg.set_title(_("Error"))
        dlg.set_default_size(100, 100)
        dlg.set_position (gtk.WIN_POS_CENTER_ON_PARENT)
        dlg.set_border_width(2)
        dlg.set_modal(True)
        rc = dlg.run()
        dlg.destroy()
        return rc

class childWindow:
    runPriority = 50
    moduleName = "Date/Time"
    moduleClass = "reconfig"

    def launch(self):
        mw = scdMainWindow().launch()        
        return mw

# vim: et ts=4
