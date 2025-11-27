#!/bin/sh

cd "$(dirname "$0")"

/usr/bin/man ./platypus.1 | ./cat2html > platypus.man.html
