#
# bootyutil.py: functions commonly used by various booty and anaconda modules
#
# Copyright 2011 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# library public license.
#
# You should have received a copy of the GNU Library Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#

import os
import string

import rhpl.executil

# return (disk, partition number) eg ('hda', 1)
def getDiskPart(dev):
    cut = len(dev)
    if dev[-1] in string.digits:
        if (dev.startswith('rd/') or dev.startswith('ida/') or
            dev.startswith('cciss/') or dev.startswith('sx8/') or
            dev.startswith('mapper/')):
            if dev[-2] == 'p':
                cut = -1
            elif dev[-3] == 'p' and dev[-2] in string.digits:
                cut = -2
        else:
            if dev[-2] in string.digits:
                cut = -2
            else:
                cut = -1

    name = dev[:cut]
    if cut < 0 and name[-1] == 'p':
        # hack off the trailing 'p' if we found the partition part
        name = name[:-1]

    if cut < 0:
        partNum = int(dev[cut:]) - 1
    else:
        partNum = None

    return (name, partNum)

def name_from_dm_node(dm_node):
    """ Translate dm node to the device name.

        For instance "dm-0" to "mpath0".
    """

    full_path = "/sys/block/%s/dev" % dm_node
    if not os.path.exists(full_path):
        raise RuntimeError("name_from_dm_node: device does not exist: %s" %
                           full_path)
    dev_file = open(full_path)
    (major, minor) = dev_file.readline().strip().split(":")
    name = rhpl.executil.execWithCapture(\
        "/sbin/dmsetup",["/sbin/dmsetup", "info", "--columns", "--noheadings",
                         "-o", "name", "-j", str(major), "-m", str(minor)])
    return name.strip()
