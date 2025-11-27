#!/bin/sh
#
# UninstallCommandLineTool.sh
# Platypus

echo "Uninstalling command line tool"

if [ -e "/usr/local/share/platypus" ]; then
    echo "Deleting '/usr/local/share/platypus' directory"
    rm -R "/usr/local/share/platypus" &> /dev/null
fi

if [ -e "/usr/local/bin/platypus" ]; then
    echo "Deleting platypus command line tool in /usr/local/bin/platypus"
    rm "/usr/local/bin/platypus" &> /dev/null
fi

if [ -e "/usr/local/share/man/man1/platypus.1.gz" ]; then
    echo "Deleting platypus man page"
    rm "/usr/local/share/man/man1/platypus.1" &> /dev/null
    rm "/usr/local/share/man/man1/platypus.1.gz" &> /dev/null
fi

