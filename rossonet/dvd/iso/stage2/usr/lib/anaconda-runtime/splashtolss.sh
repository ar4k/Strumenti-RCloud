#!/bin/sh

usage() {
  echo "Usage: $0 <source> <output>"
  exit 1
}

if [ -z "$1" -o -z "$2" ]; then
  usage
fi

pngtopnm $1 | ppmtolss16 > $2
