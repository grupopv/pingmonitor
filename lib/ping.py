#!/usr/bin/python3

import os
import csv
import subprocess
from lib.mail import *

# Define variables
count = "4"

# Define /dev/null
FNULL = open(os.devnull, 'w')

# Read the data in the hosts.csv file
hosts = open('hosts.csv')
hosts_reader = csv.reader(hosts)
hosts = list(hosts_reader)

def ping_hosts():
    # Analyze every host in hosts.csv
    for host in range(len(hosts)):
        name = hosts[host][0]
        ip = hosts[host][1]
        res = subprocess.call(['ping', '-c', count, ip], stdout=FNULL, stderr=subprocess.STDOUT)
        if res == 0:
            print("ping to", name, "OK")
        elif res == 2:
            # 100% failed
            print("no response from", name)
            sendgrid_mail(name, ip)
        else:
            print("ping to", name, "failed!")
