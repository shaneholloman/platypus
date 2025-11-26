#!/bin/sh

REMOTE_USER="$1"

scp PlatypusAppcast.xml "$REMOTE_USER@sveinbjorn.org:/www/sveinbjorn/html/files/appcasts/PlatypusAppcast.xml"
