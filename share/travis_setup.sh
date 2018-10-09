#!/bin/bash
set -evx

mkdir ~/.parkingcore

# safety check
if [ ! -f ~/.parkingcore/.parking.conf ]; then
  cp share/parking.conf.example ~/.parkingcore/parking.conf
fi
