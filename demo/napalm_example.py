#!/usr/bin/env python

import os
from dotenv import load_dotenv
from napalm import get_network_driver
from rich import print

load_dotenv(override=True)

username = os.getenv("DEVICE_USERNAME")
password = os.getenv("DEVICE_PASSWORD")

# Creating a NAPALM driver object for Junos devices.
eos_driver = get_network_driver("eos")

with eos_driver(hostname="172.29.152.201", username=username, password=password) as device:
    # Get network data from NAPALM getters
    print(device.get_facts())
    print(device.get_interfaces_counters())