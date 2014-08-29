#!/bin/bash
# Crea i cd

# i386
echo "Masterizza CentOS-5.9-i386-netinstall.iso"
mkisofs -o /var/www/html/rossonet/iso/CentOS-5.9-i386-netinstall.iso -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -R -J -v -T /var/www/html/rossonet/iso/i386
#
echo "md5sum CentOS-5.9-i386-netinstall.iso"
/usr/bin/implantisomd5 --supported-iso /var/www/html/rossonet/iso/CentOS-5.9-i386-netinstall.iso

# x86_64
echo "Masterizza CentOS-5.9-x86_64-netinstall.iso"
mkisofs -o /var/www/html/rossonet/iso/CentOS-5.9-x86_64-netinstall.iso -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -R -J -v -T /var/www/html/rossonet/iso/x86_64
#
echo "md5sum CentOS-5.9-x86_64-netinstall.iso"
/usr/bin/implantisomd5 --supported-iso /var/www/html/rossonet/iso/CentOS-5.9-x86_64-netinstall.iso

# i386
echo "Masterizza CentOS-5.9-i386-static.iso"
mkisofs -o /var/www/html/rossonet/iso/CentOS-5.9-i386-static.iso -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -R -J -v -T /var/www/html/rossonet/iso/i386-static
#
echo "md5sum CentOS-5.9-i386-static.iso"
/usr/bin/implantisomd5 --supported-iso /var/www/html/rossonet/iso/CentOS-5.9-i386-static.iso

# x86_64
echo "Masterizza CentOS-5.9-x86_64-static.iso"
mkisofs -o /var/www/html/rossonet/iso/CentOS-5.9-x86_64-static.iso -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -R -J -v -T /var/www/html/rossonet/iso/x86_64-static
#
echo "md5sum CentOS-5.9-x86_64-static.iso"
/usr/bin/implantisomd5 --supported-iso /var/www/html/rossonet/iso/CentOS-5.9-x86_64-static.iso

# i386
echo "Masterizza CentOS-5.9-i386-dhcp.iso"
mkisofs -o /var/www/html/rossonet/iso/CentOS-5.9-i386-dhcp.iso -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -R -J -v -T /var/www/html/rossonet/iso/i386-dhcp
#
echo "md5sum CentOS-5.9-i386-dhcp.iso"
/usr/bin/implantisomd5 --supported-iso /var/www/html/rossonet/iso/CentOS-5.9-i386-dhcp.iso

# x86_64
echo "Masterizza CentOS-5.9-x86_64-dhcp.iso"
mkisofs -o /var/www/html/rossonet/iso/CentOS-5.9-x86_64-dhcp.iso -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -R -J -v -T /var/www/html/rossonet/iso/x86_64-dhcp
#
echo "md5sum CentOS-5.9-x86_64-dhcp.iso"
/usr/bin/implantisomd5 --supported-iso /var/www/html/rossonet/iso/CentOS-5.9-x86_64-dhcp.iso

