## timezoneBackend - provides the backend for system timezone calls
## Copyright (C) 2001, 2002, 2003 Red Hat, Inc.
## Copyright (C) 2001, 2002, 2003 Brent Fox <bfox@redhat.com>
##                                Tammy Fox <tfox@redhat.com>

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

import os
import time
import string
import shutil

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
translate.textdomain ("system-config-date")

def bool(val):
    if val: return "true"
    return "false"

class timezoneBackend:
    def writeConfig (self, timezone, utc=0, arc=0):
        fromFile = "/usr/share/zoneinfo/" + timezone

        if utc == 0 or utc == 'false':
            utc = "false"
        else:
            utc = "true"

        if arc != "false":
            if arc != 0:
                arc = "true"
            else:
                arc = "false"

        try:
            shutil.copyfile(fromFile, "/etc/localtime")
        except OSError, (errno, msg):
            print (_("Error copying timezone (from %s): %s") % (fromFile, msg))

        try:
            os.chmod("/etc/localtime", 0644)
        except OSError, (errno, msg):
            print (_("Changing permission of timezone: %s") % (msg))

        #Check to see if /var/spool/postfix/etc/localtime exists
        if os.access("/var/spool/postfix/etc/localtime", os.F_OK) == 1:
            #If it does, copy the new timezone file into the chroot jail
            try:
                os.remove("/var/spool/postfix/etc/localtime")
            except OSError, (errno, msg):
                print (_("Error removing /var/spool/postfix/etc/localtime")), msg

            try:
                shutil.copyfile(fromFile, "/var/spool/postfix/etc/localtime")
            except OSError, (errno, msg):
                print (_("Error copying timezone (from %s): %s") % (fromFile, msg))

            try:
                os.chmod("/var/spool/postfix/etc/localtime", 0644)
            except OSError, (errno, msg):
                print (_("Changing permission of timezone: %s") % (msg))

        #Write info to the /etc/sysconfig/clock file
        f = open("/etc/sysconfig/clock", "w")
        f.write('# The ZONE parameter is only evaluated by system-config-date.\n')
        f.write('# The timezone of the system is defined by the contents of /etc/localtime.\n')
        f.write('ZONE="%s"\n' % timezone)
        f.write("UTC=%s\n" % utc)
        f.write("ARC=%s\n" % arc)
        f.close()

        f = open("/etc/sysconfig/clock", "r")
        tmp = f.read()

    def copyFile(self, source, to):
        f = os.open(source, os.O_RDONLY)
        t = os.open(to, os.O_RDWR | os.O_TRUNC | os.O_CREAT)

        try:
            count = os.read(f, 262144)
            total = 0
            while (count):
                os.write(t, count)

                total = total + len(count)
                count = os.read(f, 16384)
        finally:
            os.close(f)
            os.close(t)

    def getTimezoneInfo (self):
        return (self.tz, self.utc, self.arc)

    def setTimezoneInfo (self, timezone, asUtc = 0, asArc = 0):
        self.tz = timezone
        self.utc = asUtc
        self.arc = asArc

    def __init__(self):
        self.tz = "America/New_York"
        self.utc = "false"
        self.arc = "false"
        path = '/etc/sysconfig/clock'
        lines = []

        if os.access(path, os.R_OK):
            fd = open(path, 'r')
            lines = fd.readlines()
            fd.close()
        else:
            #There's no /etc/sysconfig/clock file, so make one
            fd = open(path, 'w')
            fd.close
            pass
        
        try:
            for line in lines:
                line = string.strip(line)
                if len (line) and line[0] == '#':
                    continue
                try:
                    tokens = string.split(line, "=")
                    if tokens[0] == "ZONE":
                        self.tz = string.replace(tokens[1], '"', '')
                    if tokens[0] == "UTC":
                        self.utc = tokens[1]
                    if tokens[0] == "ARC":
                        if string.lower(tokens[1]) == "true":
                            self.arc = tokens[1]
                        else:
                            self.arc = "false"
                except:
                    pass
        except:
            pass
