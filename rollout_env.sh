#!/bin/sh
# niet hieraan zitten!
export INTERFACE_USR=$HOSTNAME
export INTERFACE_PASS=$(echo $HOSTNAME | md5sum | cut -c1-4)