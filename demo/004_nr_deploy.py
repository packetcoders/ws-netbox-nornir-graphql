#!/usr/bin/env python
import os
from pathlib import Path
from config import nr
from dotenv import load_dotenv
from nornir.core.task import Result, Task
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F

# Load the environment variables from the .env file.
load_dotenv(override=True)  

# Variables for the Nornir tasks.
DEVICE_CONFIG_PATH = f"{Path(__file__).parent}/output"

# Pull the device username/password from the environment variables and assign to the inventory defaults.
nr.inventory.defaults.username = os.getenv("DEVICE_USERNAME")
nr.inventory.defaults.password = os.getenv("DEVICE_PASSWORD")

# Filter for hosts with a specific NetBox tenant name
nr = nr.filter(F(role__name="spine"))

def deploy_config(task: Task) -> Result:
    napalm_result = task.run(
        task=napalm_configure,
        filename=f"{DEVICE_CONFIG_PATH}/{task.host}.txt",
        replace=True,
    )

    return Result(
        host=task.host,
        result=f"{napalm_result.result}",
    )

if __name__ == "__main__":
    deploy_result = nr.run(
        name="Deploy Config", 
        task=deploy_config,
    )

    print_result(deploy_result)