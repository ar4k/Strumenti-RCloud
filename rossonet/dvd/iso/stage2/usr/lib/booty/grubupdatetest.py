#!/usr/bin/python
#
# simple test updating of lilo.conf type files
#
# Jeremy Katz <katzj@redhat.com>
#
# Copyright 2002 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# library public license.
#
# You should have received a copy of the GNU Library Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

import bootloader


# iterate over all of the config files in a directory with a
# known set of arguments and compare against "good" copies to
# make this automatable?
bootloader.__installNewKernelImagesX86Grub([('2.4.7-10', None),
                                            ('2.4.17-0.1smp', "smp")],
                                           "rpmsave", 1, "grub.conf")

