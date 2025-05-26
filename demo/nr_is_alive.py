from config import nr
from rich import print
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from nornir.core.task import Result, Task
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file.
load_dotenv(override=True)  

# Pull the device username/password from the environment variables and assign to the inventory defaults.
nr.inventory.defaults.username = os.getenv("DEVICE_USERNAME")
nr.inventory.defaults.password = os.getenv("DEVICE_PASSWORD")

# Filter for hosts with a specific NetBox tenant name
nr = nr.filter(F(tenant__name="pod1"))

def check_is_alive(task: Task) -> Result:
    try:
        # Try to establish a NAPALM connection (no facts retrieved)
        task.run(task=napalm_get, getters=[], name="Connect")

        # Retrieve connection and check is_alive status
        connection = task.host.get_connection("napalm", task.nornir.config)
        alive = connection.is_alive().get("is_alive", False)

        return Result(
            host=task.host,
            result=f"Host is {'alive' if alive else 'not reachable'}",
            failed=not alive
        )

    except Exception as e:
        return Result(
            host=task.host,
            result=f"Host is not reachable (error: {str(e)})",
            failed=True
        )

result = nr.run(task=check_is_alive)
print_result(result)
