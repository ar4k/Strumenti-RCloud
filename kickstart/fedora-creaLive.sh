#!/bin/bash
# crea il dvd da ks

livecd-creator --debug --verbose --config=$1 --fslabel=Rossonet --cache=/var/cache/live
