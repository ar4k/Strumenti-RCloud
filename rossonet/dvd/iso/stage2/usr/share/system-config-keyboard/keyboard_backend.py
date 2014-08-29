#
# keyboard_backend.py - backend code for mouse configuration
#
# Copyright (C) 2002, 2003 Red Hat, Inc.
# Brent Fox <bfox@redhat.com>
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

#!/usr/bin/python2.2

import sys
import os

class KeyboardBackend:

    def modifyXconfig(self, fullname, layout, model, variant, options):
        #import xf86config and make the necessary changes
        if os.access("/etc/X11/XF86Config", os.W_OK) or os.access("/etc/X11/xorg.conf", os.W_OK):        
            import xf86config
            (xconfig, xconfigpath) = xf86config.readConfigFile()
            keyboard = xf86config.getCoreKeyboard(xconfig)
            
            found = 0
            for o in keyboard.options:
                if o.name == "XkbLayout":
                    found = 1

            if not found:
                #If there's not an XkbLayout option for some reason, create one
                option = xf86config.XF86Option("XkbLayout")
                keyboard.options.insert(option)

            found_variant = None
            found_options = None
            count = 0
            for o in keyboard.options:
                if o.name == "XkbModel":
                    o.val = model
                if o.name == "XkbLayout":
                    o.val = layout
                if o.name == "XkbVariant":
                    found_variant = 1
                    if variant == "":
                        #remove variant here
                        keyboard.options.remove(count)
                    o.val = variant

                if o.name == "XkbOptions":
                    found_options = 1
                    if options == "":
                        #remove option here
                        keyboard.options.remove(count)

                count = count + 1

            if variant != "" and found_variant == None:
                #Need to create a XkbVariant entry
                opt = xf86config.XF86Option("XkbVariant", variant)
                keyboard.options.insert(opt)

            if options != "" and found_options == None:
                #Need to create an XkbOptions entry
                opt = xf86config.XF86Option("XkbOptions", options)
                keyboard.options.insert(opt)

            xconfig.write(xconfigpath)
    
