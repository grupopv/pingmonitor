from os import system
from yaml import load

def read_config():
    with open('config.yml', 'r') as f:
        doc = load(f)
    return doc

config = read_config()

def check_hdd():
    for hdd in range(len(config["hdd"]["partitions"])):
        partition = config["hdd"]["partitions"][hdd]
        available_space_col = config["hdd"]["available_space"]["column"]
        system("df -h | grep %s | awk '{ print $%s }'" % (partition, available_space_col))
