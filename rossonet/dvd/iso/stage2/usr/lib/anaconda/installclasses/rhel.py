from installclass import BaseInstallClass
import rhpl
from rhpl.translate import N_,_
from constants import *
from flags import flags
import os
import iutil
import string
import types
try:
    import instnum
except ImportError:
    instnum = None

import logging
log = logging.getLogger("anaconda")

# custom installs are easy :-)
class InstallClass(BaseInstallClass):
    # name has underscore used for mnemonics, strip if you dont need it
    id = "centos"
    name = N_("CentOS Linux")
    _description = N_("The default installation of %s includes a set of "
                     "software applicable for general internet usage. "
                     "What additional tasks would you like your system "
                     "to include support for?")
    _descriptionFields = (productName,)
    sortPriority = 10000
    allowExtraRepos = True
    if 0: # not productName.startswith("Red Hat Enterprise"):
        hidden = 1

    tasks = [(N_("Desktop - Gnome "), ["graphics", "office", "games", "sound-and-video","base-x","gnome-desktop","graphical-internet","printing"]),
             (N_("Desktop - KDE "), ["graphics", "office", "games", "sound-and-video","base-x","kde-desktop","graphical-internet","printing"]),
             (N_("Server "), ["server-cfg", "dns-server", "web-server", "ftp-server", "smb-server", "mail-server", "network-server", "legacy-network-server", "news-server"]),
             (N_("Server - GUI "), ["server-cfg", "dns-server", "web-server", "ftp-server", "smb-server", "mail-server", "network-server", "legacy-network-server", "news-server", "base-x", "gnome-desktop", "admin-tools"]),
             (N_("Virtualization"), ["virtualization"]),
             (N_("Clustering"), ["clustering"]),
             (N_("Storage Clustering"), ["cluster-storage"]) ]

    instkeyname = N_("Installation Number")
    instkeydesc = N_("Would you like to enter an Installation Number "
                     "(sometimes called Subscription Number) now? This feature "
                     "enables the installer to access any extra components "
                     "included with your subscription.  If you skip this step, "
                     "additional components can be installed manually later.\n\n"
                     "See http://www.redhat.com/InstNum/ for more information.")
    skipkeytext = N_("If you cannot locate the Installation Number, consult "
                     "http://www.redhat.com/InstNum/")

    def setInstallData(self, anaconda):
	BaseInstallClass.setInstallData(self, anaconda)
        BaseInstallClass.setDefaultPartitioning(self, anaconda.id.partitions,
                                                CLEARPART_TYPE_LINUX)

    def setGroupSelection(self, anaconda):
        grps = anaconda.backend.getDefaultGroups(anaconda)
        map(lambda x: anaconda.backend.selectGroup(x), grps)
        coregrps = ["core", "base", "dialup", "text-internet"]
        map(lambda x: anaconda.backend.selectGroup(x), coregrps)
        desktopgrps = ["editors", "graphics", "office", "games", "sound-and-video","base-x","gnome-desktop","graphical-internet","printing"]
        map(lambda x: anaconda.backend.selectGroup(x), desktopgrps)


    def setSteps(self, dispatch):
	BaseInstallClass.setSteps(self, dispatch);
	dispatch.skipStep("partition")
	dispatch.skipStep("regkey", skip = 1)        

    # for rhel, look up the given name and determine if it is allowed
    # by the package key
    def repoIsAllowed(self, repoName):
        if not self.inum or not instnum:
            return True

        name = repoName.lower()
        prod = self.inum.get_product()
        controlledRepos = map(string.lower, instnum.encodingMaps[instnum.IN_OPTIONS][prod].values())
        for (k, lst) in instnum.encodingMaps[instnum.IN_REPO][prod].items():
            for repo in lst:
                if not type(repo) == types.StringType:
                    continue

                controlledRepos.append(repo.lower())

        if name not in controlledRepos:
            return True

        allowedRepos = map(string.lower, self.inum.get_repos()) + \
                       map(string.lower, self.inum.get_repos_dict().keys())
        return name in allowedRepos

    def handleRegKey(self, key, intf, interactive = True):
        self.repopaths = { "base": "%s" %(productPath,) }
        self.tasks = self.taskMap[productPath.lower()]
        self.installkey = key

        try:
            self.inum = instnum.InstNum(key)
        except Exception, e:
            if True or not BETANAG: # disable hack keys for non-beta
                # make sure the log is consistent
                log.info("repopaths is %s" %(self.repopaths,))
                raise
            else:
                self.inum = None

        if self.inum is not None:
            # make sure the base products match
            if self.inum.get_product_string().lower() != productPath.lower():
                raise ValueError, "Installation number incompatible with media"

            for name, path in self.inum.get_repos_dict().items():
                # virt is only supported on i386/x86_64.  so, let's nuke it
                # from our repo list on other arches unless you boot with
                # 'linux debug'
                if name.lower() == "virt" and ( \
                        rhpl.getArch() not in ("x86_64","i386","ia64")
                        and not flags.debug):
                    continue
                self.repopaths[name.lower()] = path
                log.info("Adding %s repo" % (name,))

        else:
            key = key.upper()
            # simple and stupid for now... if C is in the key, add Clustering
            # if V is in the key, add Virtualization. etc
            if key.find("C") != -1:
                self.repopaths["cluster"] = "Cluster"
                log.info("Adding Cluster option")
            if key.find("S") != -1:
                self.repopaths["clusterstorage"] = "ClusterStorage"
                log.info("Adding ClusterStorage option")
            if key.find("W") != -1:
                self.repopaths["workstation"] = "Workstation"
                log.info("Adding Workstation option")
            if key.find("V") != -1:
                self.repopaths["virt"] = "VT"
                log.info("Adding Virtualization option")

        for repo in self.repopaths.values():
            if not self.taskMap.has_key(repo.lower()):
                continue

            for task in self.taskMap[repo.lower()]:
                if task not in self.tasks:
                    self.tasks.append(task)
        self.tasks.sort()

        log.info("repopaths is %s" %(self.repopaths,))

    def __init__(self, expert):
	BaseInstallClass.__init__(self, expert)

        self.inum = None
        self.repopaths = { "base": "%s" %(productPath,) }

        # minimally set up tasks in case no key is provided
        # self.tasks = self.taskMap[productPath.lower()]

