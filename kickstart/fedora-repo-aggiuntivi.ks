#repo --name="Adobe Systems Incorporated" --baseurl=http://linuxdownload.adobe.com/linux/$basearch/
repo --name="RPM Fusion for Fedora $releasever - Free" --mirrorlist=http://mirrors.rpmfusion.org/mirrorlist?repo=free-fedora-$releasever&arch=$basearch
repo --name="RPM Fusion for Fedora $releasever - Free - Updates" --mirrorlist=http://mirrors.rpmfusion.org/mirrorlist?repo=free-fedora-updates-released-$releasever&arch=$basearch
repo --name="RPM Fusion for Fedora $releasever - Nonfree" --mirrorlist=http://mirrors.rpmfusion.org/mirrorlist?repo=nonfree-fedora-$releasever&arch=$basearch
repo --name="RPM Fusion for Fedora $releasever - Nonfree - Updates" --mirrorlist=http://mirrors.rpmfusion.org/mirrorlist?repo=nonfree-fedora-updates-released-$releasever&arch=$basearch
