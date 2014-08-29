# Copyright 2000-2003 Red Hat, Inc
#
# This software may be freely redistributed under the terms of the GNU
# public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import _kudzu
import sys

consts=('BUS_', 'CLASS_', 'PROBE_')

for n in _kudzu.__dict__.keys():
    for c in consts:
        if len(n) > len(consts) and n[:len(c)] == c:
            sys.modules[__name__].__dict__[n] = _kudzu.__dict__[n]

# The base device class

class device:
    def __init__(self,table):
        self.deviceclass=table["class"]
        self.bus=table["bus"]
        self.index=table["index"]
        self.detached=table["detached"]
        self.desc=table["desc"]
        self.driver=table["driver"]
        self.device=table["device"]
	if self.deviceclass == CLASS_NETWORK:
	    if table.has_key("hwaddr"):
		self.hwaddr = table["hwaddr"]
	    else:
	    	self.hwaddr = None
	if self.deviceclass == CLASS_VIDEO:
	    if table.has_key("xdriver"):
		self.xdriver = table["xdriver"]
	    else:
		self.xdriver = None

    # maintain backwards compatibility
    def __getitem__(self, which):
        if which == 0:
            return self.device
        if which == 1:
            return self.driver
        if which == 2:
            return self.desc
        raise IndexError
    
    def setIndex(self,index):
        self.index=index

    def setDetached(self,detached):
        self.detached=detached

    def setDesc(self,desc):
        self.desc=desc

    def setDriver(self,driver):
        self.driver=driver

    def __repr__(self):
        res=""
        res=res+"Desc:           %s\n" % (self.desc)
        res=res+"Driver:         %s\n" % (self.driver)
        res=res+"Device:         %s\n" % (self.device)
        return res

# One class for each structure in the kudzu include files

class scsiDevice(device):
    def __init__(self,table):
        device.__init__(self,table)
        self.host=table["host"]
        self.channel=table["channel"]
        self.id=table["id"]
        self.lun=table["lun"]

    def setHost(self,host):
        self.host=host

    def setChannel(self,channel):
        self.channel=channel

    def setId(self,id):
        self.id=id

    def setLun(self,lun):
        self.lun=lun

class serialDevice(device):
    def __init__(self,table):
        device.__init__(self,table)
        self.pnpdesc=table["pnpdesc"]
        self.pnpmodel=table["pnpmodel"]
        self.pnpcompat=table["pnpcompat"]
        self.pnpmfr=table["pnpmfr"]

    def setPnPMfr(self,mfr):
        self.pnpmfr=mfr

    def setPnpModel(self,model):
        self.pnpmodel=model

    def setPnPCompat(self,compat):
        self.pnpcompat=compat

    def setPnpDesc(self,desc):
        self.pnpdesc=desc
    

class ideDevice(device):
    def __init__(self,table):
        device.__init__(self,table)
        self.physical=table["physical"]
        self.logical=table["logical"]

    def setPhysical(self,cyls):
        self.physical=cyls

    def setLogical(self,cyls):
        self.logical=cyls


class keyboardDevice(device):
    def __init__(self,table):
        device.__init__(self,table)

class psauxDevice(device):
    def __init__(self,table):
        device.__init__(self,table)


class sbusDevice(device):
    def __init__(self,table):
        device.__init__(self,table)
        self.width=table["width"]
        self.height=table["height"]
        self.freq=table["freq"]
        self.monitor=table["monitor"]

    def setRes(self,height,width):
        self.width=width
        self.height=height

    def setFreq(self,freq):
        self.freq=freq

    def setMonitor(self,monitor):
        self.monitor=monitor

class parallellDevice(device):
    def __init__(self,table):
        device.__init__(self,table)
        self.pnpdesc=table["pnpdesc"]
        self.pnpmodel=table["pnpmodel"]
        self.pnpmodes=table["pnpmodes"]
        self.pnpmfr=table["pnpmfr"]
        if(table.has_key("xres")):
            self.printeres=(table["xres"],table["yres"])
            self.printercolor=table["color"]
            self.printerascii=table["ascii"]
            self.printeruniprint=table["uniprint"]
        else:
            self.printeres=""
            self.printercolor=""
            self.printerascii=""
            self.printeruniprint=""
            
    def setPnPModel(self,model):
        self.pnpmodel=model

    def setPnPMfr(self,mfr):
        self.pnpmfr=mfr

    def setPnPModes(self,modes):
        self.pnpmodes=modes

    def setPnPDesc(self,desc):
        self.pnpdesc=desc

    def setPrinterRes(self,x,y):
        self.printerres=(x,y)

    def setPrinterColor(self,color):
        self.printercolor=color

    def setPrinterASCII(self,ascii):
        self.printerascii=ascii

    def setPrinterUniPrint(self,uniprint):
        self.printeruniprint=uniprint

class pciDevice(device):
    def __init__(self,table):
        device.__init__(self,table)
        self.vendorId=table["vendorId"]
        self.deviceId=table["deviceId"]
        self.subVendorId=table["subVendorId"]
        self.subDeviceId=table["subDeviceId"]
        self.pciType=table["pciType"]
	self.pcibus=table["pcibus"]
	self.pcidev=table["pcidev"]
	self.pcifn=table["pcifn"]

    def setVendorId(self,id):
        self.vendorId=id

    def setDeviceId(self,id):
        self.deviceId=id

    def setPciType(self,type):
        self.pciType=type

    def setSubVendorId(self,id):
        self.subVendorId=id

    def setSubDeviceId(self,id):
        self.subDeviceId=id
            
class pcmciaDevice(device):
    def __init__(self,table):
        device.__init__(self,table)
        self.vendorId=table["vendorId"]
        self.deviceId=table["deviceId"]

    def setVendorId(self,id):
        self.vendorId=id

    def setDeviceId(self,id):
        self.deviceId=id

    def setFunction(self,id):
        self.function=id

    def setSlot(self,id):
        self.slot=id
            
class ddcDevice(device):
    def __init__(self,table):
        device.__init__(self,table)
        if table.has_key("id"):
	    self.id=table["id"]
	else:
	    self.id = None
        self.horizSyncMin=table["horizSyncMin"]
        self.horizSyncMax=table["horizSyncMax"]
        self.vertRefreshMin=table["vertRefreshMin"]
        self.vertRefreshMax=table["vertRefreshMax"]
        self.physicalWidth=table["physicalWidth"]
        self.physicalHeight=table["physicalHeight"]
        self.mem=table["mem"]

    def __repr__(self):
        res=""
        res=res+"Desc:           %s\n" % (self.desc)
        res=res+"Id:             %s\n" % (self.id)
        res=res+"Mem on card:    %d\n" % (self.mem)
        res=res+"HSync:          %d-%d\n" % (self.horizSyncMin,
                                             self.horizSyncMax)
        res=res+"VSync:          %d-%d\n" % (self.vertRefreshMin,
                                             self.vertRefreshMax)
        res=res+"Physical width: %d mm\n" % (self.physicalWidth)
        res=res+"Physical height: %d mm\n" % (self.physicalHeight)
        return res

    def setID(self,id):
        self.id=id

    def setHorizSyncRange(self,min,max):
        self.horizSyncMin=min
        self.horizSyncMax=max

    def setVertRefreshRange(self,min,max):
        self.vertRefreshMin=min
        self.vertRefreshMax=max

    def setMem(self,mem):
        self.mem=mem

    def setPhysicalWidth(self, width):
        self.physicalWidth = width
    
    def setPhysicalHeight(self, height):
        self.physicalHeight = height
    
    def setModes(self,intdata):
        self.modes=[]

        # This is of the format xyxyxy....
        for i in range(0,len(intdata),2):
            modes.append((intdata[i],intdata[i+1]))

class usbDevice(device):

    def __init__(self,deviceclass,bus):
        device.__init__(self,deviceclass,bus)
        self.usbclass=""
        self.usbsubclass=""
        self.usbprotocol=""

    def __init__(self,table):
        device.__init__(self,table)
        self.usbclass=table["usbclass"]
        self.usbsubclass=table["usbsubclass"]
        self.usbprotocol=table["usbprotocol"]
        self.usbbus=table["usbbus"]
        self.usblevel=table["usblevel"]
        self.usbport=table["usbport"]
        self.vendorId=table["vendorid"]
        self.deviceId=table["deviceid"]
        self.usbmfr=table["usbmfr"]        
        self.usbprod=table["usbprod"]        
        

    def setUsbClass(self,usbclass):
        self.usbclass=usbclass

    def setUsbSubClass(self,usbclass):
        self.usbsubclass=usbclass

    def setUsbProtocol(self,protocol):
        self.usbprotocol=protocol


# Call the probefunction and return an array of
# objects with device information

def probe(devclass,bus,mode):
    res=_kudzu.probe(devclass,bus,mode)
    res2=[]
    for i in range(0,len(res)):
        dev=res[i]
        bus=dev["bus"]
        if(bus==BUS_PCI):
            res2.append(pciDevice(dev))
        elif(bus==BUS_SBUS):
            res2.append(sbusDevice(dev))
        elif(bus==BUS_PSAUX):
            res2.append(psauxDevice(dev))
        elif(bus==BUS_SERIAL):
            res2.append(serialDevice(dev))
        elif(bus==BUS_PARALLEL):
            res2.append(parallellDevice(dev))
        elif(bus==BUS_SCSI):
            res2.append(scsiDevice(dev))
        elif(bus==BUS_IDE):
            res2.append(ideDevice(dev))
        elif(bus==BUS_KEYBOARD):
            res2.append(keyboardDevice(dev))
        elif(bus==BUS_DDC):
            res2.append(ddcDevice(dev))
        elif(bus==BUS_USB):
            res2.append(usbDevice(dev))
	elif(bus==BUS_PCMCIA):
	    res2.append(pcmciaDevice(dev))
        else:
            res2.append(device(dev))

    return res2
