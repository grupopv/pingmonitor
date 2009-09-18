#!/bin/bash
# Simple SHELL script for Linux and UNIX system monitoring with
# ping command
# -------------------------------------------------------------------------
# Copyright (c) 2006 nixCraft project <http://www.cyberciti.biz/fb/>
# This script is licensed under GNU GPL version 2.0 or above
# -------------------------------------------------------------------------
# This script is part of nixCraft shell script collection (NSSC)
# Visit http://bash.cyberciti.biz/ for more information.
# -------------------------------------------------------------------------
 
# add ip / hostname separated by white space or enter
HOSTS="
"

# no ping request
COUNT=4
 
# email report when
for myHost in $HOSTS
do
  count=$(ping -c $COUNT $myHost | grep 'received' | awk -F',' '{ print $2 }' | awk '{ print $1 }')
  if [ $count -eq 0 ]; then
    # 100% failed
    python /root/PingMonitor/mail.py $myHost
  fi
done
