#!/usr/bin/perl

my ($rpm_path, $arch) = @ARGV;

if (!-e $rpm_path)
{
    print_usage ("RPM path '$rpm_path' does not exist");
}
if (!$arch)
{
    print_usage ("Architecture not specified");
}

@queue = ();
%copied_packages = {};
foreach (<*rpm>)
{
    push (@queue, $_);
    my ($package_name) = (m#(.+?)-\d#);
    $copied_packages{$package_name} = 1;
}

while (@queue)
{
    $rpm_name = pop (@queue);

    $cmd = "rpm -qRp $rpm_name | sort | uniq";
    @output = `$cmd`;

    foreach (@output)
    {
        s/^\s+//;
        s/\s+$//;
        s/\s+[<>=].+$//;  # strip off stuff like " >= 2003a"

        $cmd = "rpm -q --whatprovides '$_'";
        $output = `$cmd`;
        if ($output =~ m#no package provides#)
        {
            next;
        }
        my ($package_name) = ($output =~ m#(.+?)(-\d|\s)#);

        if ($copied_packages{$package_name})
        {
            next;
        }

        print "$rpm_name requires $package_name...\n";

        foreach (<$rpm_path/$package_name-[0-9]*$arch.rpm>)
        {
            push (@queue, $_);
            $cmd = "cp $_ .";
            print "  $cmd\n";
            `$cmd 2>&1`;
            $copied_packages{$package_name} = 1;
        }
        foreach (<$rpm_path/$package_name-[0-9]*noarch.rpm>)
        {
            push (@queue, $_);
            $cmd = "cp $_ .";
            print "  $cmd\n";
            `$cmd 2>&1`;
            $copied_packages{$package_name} = 1;
        }
    }
}

sub print_usage
{
    my ($msg) = @_;

    ($msg) && print "$msg\n\n";

    print <<__TEXT__;
follow_deps.pl rpm_path arch
    rpm_path     the full path to the directory of all RPMs from the distro
    arch         the target system architecture (e.g. x86_64)


__TEXT__

    exit;
}


