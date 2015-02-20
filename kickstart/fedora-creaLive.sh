#!/bin/bash
# crea il dvd da ks

livecd-creator --verbose --config=$1 --fslabel=Rossonet --cache =/var/cache/live
