from subprocess import check_output
from yaml import load
from lib.mail import sendgrid_mail
from os import fsdecode

def read_config():
	with open('config.yml','r') as f:
		doc = load(f)
	return doc

def check_ram():
        config = read_config()
        total_memory_row = config["ram"]["total"]["row"]
        total_memory_col = config["ram"]["total"]["column"]
        available_memory_row = config["ram"]["available"]["row"]
        available_memory_col = config["ram"]["available"]["column"]
        porcentage = config["ram"]["porcentage_space"]
        total_memory = int(check_output("free | sed -n \'%sp' | awk \'{print $%s}\'" % (total_memory_row, total_memory_col), shell=True))
        available_memory = int(check_output("free | sed -n \'%sp' | awk \'{print $%s}\'" % (available_memory_row, available_memory_col), shell=True))
        ram_usage = int(100-(available_memory/total_memory)*100)
        host = fsdecode(check_output("hostname -f | tr -d \'\n\'", shell=True))
        if ram_usage >= porcentage:
                print("The host", host, "RAM usage is", ram_usage, "%")
                sendgrid_mail('ram', host, ram_usage)
        else:
                print("The RAM memory is at", ram_usage, "% [OK]")
