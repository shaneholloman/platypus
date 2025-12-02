#!/bin/sh
#
# UninstallPlatypus.sh
# Platypus

if [ -e "%%PROGRAM_APP_SUPPORT_PATH%%" ]; then
    echo "Deleting application support folder..."
    mv "%%PROGRAM_APP_SUPPORT_PATH%%" ~/.Trash/%%PROGRAM_NAME%%ApplicationSupport-TRASHED-$RANDOM
fi

if [ -e ~/Library/Preferences/%%PROGRAM_BUNDLE_IDENTIFIER%%.plist ]; then
    echo "Deleting %%PROGRAM_NAME%% preferences..."
    mv ~/Library/Preferences/%%PROGRAM_BUNDLE_IDENTIFIER%%.plist ~/.Trash/%%PROGRAM_BUNDLE_IDENTIFIER%%-TRASHED-$RANDOM.plist
fi

if [ -e "%%APP_BUNDLE_PATH%%" ]; then
    echo "Moving %%PROGRAM_NAME%%.app to Trash"
    mv "%%APP_BUNDLE_PATH%%" ~/.Trash/%%PROGRAM_NAME%%-TRASHED-$RANDOM.app
fi
