#!/usr/bin/python3
from lib.ping import *
from lib.hdd import check_hdd
from lib.memory import check_ram

ping_hosts()
check_hdd()
check_ram()
