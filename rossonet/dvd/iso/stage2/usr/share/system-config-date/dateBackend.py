## dateBackend.py - provides the backend for system date calls
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
import socket
import stat

class hostInfoCache:
    knownips = {}
    knownnames = {}
    def __init__ (self, nameoraddr = None):
        if not nameoraddr:
            # factory mode
            return
        self.name = None
        self.names = []
        self.ipaddrs = []

        self.nameinfo = None

        try:
            # Test whether this is an IP address
            dummy = socket.inet_aton (nameoraddr)
            self.__class__.knownips[nameoraddr] = self
            #try:
            #    self.nameinfo = socket.gethostbyaddr (nameoraddr)
            #except socket.herror:
            #    self.nameinfo = (None, [], [nameoraddr])
            self.nameinfo = (None, [], [nameoraddr])
        except socket.error:
            # No IP address, so it must be a hostname
            self.__class__.knownnames[nameoraddr] = self
            #try:
            #    ip = socket.gethostbyname (nameoraddr)
            #    self.nameinfo = socket.gethostbyaddr (ip)
            #except (socket.gaierror, socket.herror):
            #    self.nameinfo = (nameoraddr, [nameoraddr], [])
            self.nameinfo = (nameoraddr, [nameoraddr], [])
        if self.nameinfo != None:
            self.name = self.nameinfo[0]
            self.names = self.nameinfo[1]
            self.names.append (self.name)
            for name in self.names:
                self.__class__.knownnames[name] = self
            self.ipaddrs = self.nameinfo[2]
            for ip in self.ipaddrs:
                self.__class__.knownips[ip] = self

    def __repr__ (self):
        return "<hostInfoCache object name=%s nameinfo= names=%s ipaddrs=%s>" % (self.name, self.names, self.ipaddrs)

    def get (self, nameoraddr):
        try:
            # Check whether this is an IP
            dummy = socket.inet_aton (nameoraddr)
            if self.__class__.knownips.has_key (nameoraddr):
                return self.__class__.knownips[nameoraddr]
        except socket.error:
            if self.__class__.knownnames.has_key (nameoraddr):
                return self.__class__.knownnames[nameoraddr]
        return None

    def __ne__ (self, other):
        return not self.__eq__ (other)

    def __eq__ (self, other):
        if isinstance (other, type (self)):
            if self.name:
                return self.name == other.name
            else:
                for ip in self.ipaddrs:
                    if ip in other.ipaddrs:
                        return True
                return False
        elif isinstance (other, type ("")):
            if other in self.ipaddrs:
                return True
            if other in self.names:
                return True
            return False
        return NotImplemented

class dateBackend:
    def __init__(self):
        self.ntpFile = None
        self.ntpServers = None
        self.ntpServerChoices = None
        self.ntpBroadcastClient = False
        self.ntpLocalTimeSource = False
        self.readNtpConf()
        self.getNtpServers()
        pass

    def getDate (self):
        times = time.localtime(time.time())
        return times

    def writeDateConfig (self, sysDate, sysTime):
        year, month, day = sysDate
        hour, min, sec = sysTime

        #--cal.get_date starts counting months at 0 for Jan.  We need to start counting at 1
        month = month + 1
        path = '/bin/date -s %d/%d/%d\ %s:%s:%s' % (year, month, day, hour, min, sec)
        fd = os.popen(path, 'r')
        lines = fd.readlines()
        fd.close()

    def syncHardwareClock(self):
        # sync hardware clock.  Will use either localtime or utc
        # according to value in /etc/adjtime (recorded last time hwclock
        # was run).
        if os.access("/sbin/hwclock", os.F_OK) == 1:
            #The S390 has no hwclock binary, so don't try to run it if it isn't there
            os.system("/sbin/hwclock --systohc")

    def writeNtpConfig (self, ntpServers, ntpServerChoices, ntpBroadcastClient, ntpLocalTimeSource, ntpStepTime):
        broadcastclientFound = False
        ntpFileList = []

        servers = []
        for nameoraddr in ntpServers:
            hostInfoCache (nameoraddr)
            hi = hostInfoCache().get (nameoraddr)
            servers.append (hi)
        if ntpLocalTimeSource:
            hi = hostInfoCache ("127.127.1.0")
            servers.append (hostInfoCache ("127.127.1.0"))

        serversfound = []
        restrictfound = []

        #Write /etc/ntp.conf file
        if self.ntpFile:
            lines = self.ntpFile
        else:
            fd = open("/usr/share/system-config-date/ntp.template", "r")
            lines = fd.readlines()
            fd.close ()

        for line in lines:
            location = string.find(line, 'server')
            #If "server" is found in the line
            if location == 0:
                host = None
                tokens = string.split(line)

                #If the line doesn't begin with a '#', then we're good
                if tokens[0][0] != "#" and tokens[0] == "server":
                    if len(tokens) > 1:
                        nameoraddr = tokens[1]
                        host = hostInfoCache ().get (nameoraddr)
                        if not host:
                            host = hostInfoCache (nameoraddr)
                        if host in servers:
                            try:
                                ip = host.ipaddrs[0]
                                ntpFileList.append("server " + ip + "\n")
                            except IndexError:
                                # argh
                                ntpFileList.append("server " + host.name + "\n")
                            serversfound.append (host)
                    else:
                        # What do we do here? server without an address isn't described in the documentation.
                        # Barring any problems we'll leave the line as it is.
                        ntpFileList.append(line)
                else:
                    #Else the line must either be a comment or some other abberation
                    #Just add the line so we preserve comments
                    ntpFileList.append(line)
            else:
                host = None
                ip = None
                restrict = string.find(line, 'restrict')
                if restrict == 0:
                    #If 'restrict' is found in the line
                    tokens = string.split(line)

                    if tokens[0][0] != "#" and tokens[0] == "restrict":
                        nameoraddr = tokens[1]
                        if nameoraddr != "default":
                            host = hostInfoCache ().get (nameoraddr)
                            if not host:
                                host = hostInfoCache (nameoraddr)
                            name = host.name
                            try:
                                ip = host.ipaddrs[0]
                            except IndexError:
                                ip = host.name
                            restrictfound.append (host)
                            
                            if ip != "127.0.0.1":
                                if ip != "127.127.1.0" and host in servers:
                                    ntpFileList.append ("restrict %s mask 255.255.255.255 nomodify notrap noquery\n" % (name))
                                else:
                                    if self.restrict_hosts.has_key (name):
                                        # deleted host
                                        del self.restrict_hosts[name]
                                    else:
                                        ntpFileList.append (line)
                            else:
                                ntpFileList.append (line)
                        else:
                            ntpFileList.append(line)
                else:
                    broadcastclient = string.find(line, 'broadcastclient')
                    if broadcastclient == 0:
                        #If 'broadcastclient' is found in the line
                        tokens = string.split(line)

                        if (tokens[0][0] != "#" and tokens[0] == "broadcastclient") or (tokens[0][0] == "#" and tokens[1] == "broadcastclient") and not broadcastclientFound:
                            if not ntpBroadcastClient:
                                ntpFileList.append("#")
                            ntpFileList.append("broadcastclient\n")
                            broadcastclientFound = 1
                        else:
                            ntpFileList.append(line)

                    else:
                        #This is not the server line, so just add it to the list
                        ntpFileList.append(line)

        for server in servers:
            try:
                nameoraddr = server.ipaddrs[0]
            except IndexError:
                nameoraddr = server.name
            if not server in serversfound:
                ntpFileList.append ("server " + nameoraddr + "\n")
            if not server in restrictfound and server != "127.127.1.0":
                line = "restrict %s mask 255.255.255.255 nomodify notrap noquery\n" % (nameoraddr)
                self.restrict_hosts[nameoraddr] = line
                ntpFileList.append (line)

        if not broadcastclientFound and ntpBroadcastClient:
            ntpFileList.append("broadcastclient\n")

        #Now that we've got the list of data, open the file and write it out
        try:
            fd = open ("/etc/ntp.conf", "w")
        except IOError:
            fd = None
            #fd = open ("/tmp/ntp.conf", "w")
        if fd:
            for line in ntpFileList:
                fd.write(line)
            fd.close()
        self.ntpFile = ntpFileList

        if ntpStepTime and len (servers):
            # Write /etc/ntp/step-tickers file
            try:
                fd = open("/etc/ntp/step-tickers", "w")
            except IOError:
                fd = None
                #fd = open ("/tmp/step-tickers", "w")
            if fd:
                for server in servers:
                    try:
                        fd.write (server.ipaddrs[0] + "\n")
                    except IndexError:
                        fd.write (server.name + "\n")
                fd.close()
        else:
            try:
                fd = open ('/etc/ntp/step-tickers', 'w')
                fd.truncate ()
                fd.close ()
            except IOError:
                pass

        #Write /etc/ntp/ntpservers file
        if ntpServerChoices:
            try:
                fd = open("/etc/ntp/ntpservers", "w")
            except IOError:
                fd = None
                # fd = open ("/tmp/ntpservers", "w")
            if fd:
                for server in ntpServerChoices:
                    fd.write(server + "\n")
                fd.close()

        return 0
    
    def startNtpService (self, wait):
        if self.isNtpRunning() == 1:
            fullPath = '/sbin/service ntpd restart > /dev/null'
        else:
            fullPath = '/sbin/service ntpd start > /dev/null'
        path = "/sbin/service"
        args = [path, "ntpd", "restart"]

        retval = os.system(fullPath)
        return retval
        
    def chkconfigOn(self):
        path = ('/sbin/chkconfig --level 35 ntpd on')
        os.system (path)
        
    def chkconfigOff(self):
        path = ('/sbin/chkconfig --level 35 ntpd off')
        os.system (path)

    def stopNtpService (self):
        if self.isNtpRunning() == 1:
            path = ('/sbin/service ntpd stop > /dev/null')
            os.system (path)
            path = ('/sbin/chkconfig --level 35 ntpd off')
            os.system (path)
        
    def isNtpRunning (self):
        if not os.access("/etc/ntp.conf", os.R_OK):
            #The file doesn't exist, so return
            return 0

        command = ('/sbin/service ntpd status > /dev/null')

        result = os.system(command)

        try:
            if result == 0:
                #ntpd is running
                return 1
            else:
                #ntpd is stopped
                return 0
        except:
            #we cannot parse the output of the initscript
            #the initscript is busted, so disable ntp
            return None
            
    def getNtpServers (self):
        self.ntpServers = []
        self.ntpLocalTimeSource = False
        self.restrict_hosts = {}

        if self.ntpFile:
            for line in self.ntpFile:
                location = string.find(line, 'server')

                if location == 0:
                    tokens = string.split(line)
                    
                    if tokens[0][0] != "#" and tokens[0] == "server":
                        try:
                            server = tokens[1]
                            if server == "127.127.1.0":
                                self.ntpLocalTimeSource = True
                            else:
                                host = tokens[1]
                                try:
                                    socket.inet_aton (host)
                                    host = socket.gethostbyaddr (host)[0]
                                except:
                                    pass
                                self.ntpServers.append (host)
                        except:
                            #They have a server line in /etc/ntp.conf with no server specified
                            pass

                location = string.find(line, 'restrict')

                if location == 0:
                    tokens = string.split (line)
                    if tokens[0] == "restrict" and len (tokens) >= 2:
                        host = tokens[1]
                        if not self.restrict_hosts.has_key (host):
                            self.restrict_hosts[host] = line

            return (self.ntpServers, self.ntpLocalTimeSource)

    def getNtpBroadcastClient(self):
        broadcastclient = False

        if self.ntpFile:
            for line in self.ntpFile:
                location = string.find(line, 'broadcastclient')
                if location == 0:
                    tokens = string.split(line)

                    if tokens[0][0] != "#" and tokens[0] == "broadcastclient":
                        broadcastclient = True

        self.ntpBroadcastClient = broadcastclient

        return broadcastclient

    def getNtpStepTime (self):
        if os.access ('/etc/ntp/step-tickers', os.F_OK) and os.stat ('/etc/ntp/step-tickers')[stat.ST_SIZE] > 0:
            return True
        else:
            return False

    def readNtpConf(self):
        try:
            fd = open('/etc/ntp.conf', 'r')
            self.ntpFile = fd.readlines()
            fd.close()
        except:
            return

    def readServerChoicesFile(self):
        self.ntpServerChoices = []
        if os.access("/etc/ntp/ntpservers", os.R_OK) == 1:
            fd = open("/etc/ntp/ntpservers", "r")
            lines = fd.readlines()
            for line in lines:            
                line = string.strip(line)
                if line and line[0] != "#":
                    host = line
                    try:
                        socket.inet_aton (host)
                        host = socket.gethostbyaddr (host)[0]
                    except:
                        pass
                    self.ntpServerChoices.append (host)
            return self.ntpServerChoices
        else:
            return []

# vim: et ts=4
