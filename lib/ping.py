#!/usr/bin/python3

from os import devnull
from subprocess import call, STDOUT
from lib.mail import sendgrid_mail
from yaml import load
from datetime import datetime

# Define /dev/null
FNULL = open(devnull, 'w')

def read_config():
    with open('config.yml', 'r') as f:
        doc = load(f)
    return doc

def ping_hosts():
    # Analyze every host in config.yml
    config = read_config()
    for host in range(len(config["hosts"])):
        name = config["hosts"][host]["name"]
        ip = config["hosts"][host]["host"]
        schedule = config["hosts"][host]["schedule"]
        count = config["ping"]["count"]
        if schedule == 'always' or (schedule == 'working hours' and working_hours(config) == 'true'):
            res = call(['ping', '-c', str(count), ip], stdout=FNULL, stderr=STDOUT)
            if res == 0:
                print("Ping to", name, "OK")
            elif res == 2:
                # 100% failed
                print("No response from", name)
                sendgrid_mail('ping', name, ip)
            else:
                print("ping to", name, "failed!")

def working_hours(config):
    weekdays_working_hours_start = datetime.now().replace(hour=config["working_hours"]["weekdays"]["start"]["hour"], minute=config["working_hours"]["weekdays"]["start"]["minute"], second=config["working_hours"]["weekdays"]["start"]["second"])
    weekdays_working_hours_finish = datetime.now().replace(hour=config["working_hours"]["weekdays"]["finish"]["hour"], minute=config["working_hours"]["weekdays"]["finish"]["minute"], second=config["working_hours"]["weekdays"]["finish"]["second"])
    weekend_working_hours_start = datetime.now().replace(hour=config["working_hours"]["weekend"]["start"]["hour"], minute=config["working_hours"]["weekend"]["start"]["minute"], second=config["working_hours"]["weekend"]["start"]["second"])
    weekend_working_hours_finish = datetime.now().replace(hour=config["working_hours"]["weekend"]["finish"]["hour"], minute=config["working_hours"]["weekend"]["finish"]["minute"], second=config["working_hours"]["weekend"]["finish"]["second"])
    current_time = datetime.now()
    current_day = int(current_time.strftime('%w'))
    if 0 < current_day and current_day < 6:
        if weekdays_working_hours_start < current_time and current_time < weekdays_working_hours_finish:
            return "true"
        else:
            return "false"
    elif current_day == 6:
        if weekend_working_hours_start < current_time and current_time < weekend_working_hours_finish:
            return "true"
        else:
            return "false"
