#!/usr/bin/python3

from os import devnull
from subprocess import call, STDOUT
from lib.mail import sendgrid_mail
import yaml

# Define variables
count = "4"

# Define /dev/null
FNULL = open(devnull, 'w')

def read_config():
    with open('config.yml', 'r') as f:
        doc = yaml.load(f)
    return doc

def ping_hosts():
    config = read_config()
    # Analyze every host in hosts.csv
    for host in range(len(config["hosts"])):
        name = config["hosts"][host].split(" => ")[0]
        ip = config["hosts"][host].split(" => ")[1]
        res = call(['ping', '-c', count, ip], stdout=FNULL, stderr=STDOUT)
        if res == 0:
            print("Ping to", name, "OK")
        elif res == 2:
            # 100% failed
            print("No response from", name)
            sendgrid_mail(name, ip)
        else:
            print("ping to", name, "failed!")
