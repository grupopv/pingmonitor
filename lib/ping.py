#!/usr/bin/python3

from os import devnull
from csv import reader
from subprocess import call, STDOUT
from lib.mail import sendgrid_mail

# Define variables
count = "4"

# Define /dev/null
FNULL = open(devnull, 'w')

# Read the data in the hosts.csv file
hosts_reader = reader(open('hosts.csv'))
hosts = list(hosts_reader)

def ping_hosts():
    # Analyze every host in hosts.csv
    for host in range(len(hosts)):
        name = hosts[host][0]
        ip = hosts[host][1]
        res = call(['ping', '-c', count, ip], stdout=FNULL, stderr=STDOUT)
        if res == 0:
            print("Ping to", name, "OK")
        elif res == 2:
            # 100% failed
            print("No response from", name)
            sendgrid_mail(name, ip)
        else:
            print("ping to", name, "failed!")
