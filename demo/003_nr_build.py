#!/usr/bin/env python

import os
from pathlib import Path
import requests
from config import nr
from dotenv import load_dotenv
from nornir.core.task import Result, Task
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file
from nornir.core.filter import F

load_dotenv(override=True)

STUDENT_ID = os.getenv("STUDENT_ID")
NETBOX_FQDN = os.getenv("NETBOX_FQDN")
NETBOX_TOKEN = os.getenv("NETBOX_TOKEN")
DEVICE_PASSWORD = os.getenv("DEVICE_PASSWORD")

J2_FILE = "device.j2"
J2_PATH_TEMPLATE = Path(__file__).parent / "templates"
J2_PATH_OUTPUT = Path(__file__).parent / "output"

# Filter for hosts with a specific NetBox tenant name
#nr = nr.filter(F(tenant__name="pod1"))
#nr = nr.filter(F(name=f"leaf{STUDENT_ID}"))
nr = nr.filter(F(role__name="spine"))

# GraphQL query to collect device variables.
GRAPHQL_QUERY = """
query DeviceQuery($deviceName: String) {
  device_list(
    filters: { 
      name: { exact: $deviceName }, 
    }) {
    name
    custom_fields
    role {
      name
    }
    device_type {
        model
        slug
    }
    platform {
        name
    }
    interfaces {
        name
        mgmt_only
        ip_addresses {
            address
        }
    }
    primary_ip4 {
      address
    }
  }
}
"""


# Get data from NetBox using GraphQL on a per host basis.
def task_collect_graphql(task: Task, netbox_fqdn: str, netbox_token: str, query: str) -> Result:
    """
    This task will query NetBox using GraphQL and return the data from the GraphQL query
    """

    headers = {
        "Authorization": f"Token {netbox_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    graphql_variables = {"deviceName": task.host.name}

    result = requests.post(
        url=f"{netbox_fqdn}/graphql/",
        json={"query": query, "variables": graphql_variables},
        headers=headers,
    ).json()

    return Result(host=task.host, result=result["data"]["device_list"][0])

def task_build_config(task: Task, output_path: str) -> Result:
    """
    This task will build the configuration for the device using Jinja2.
    """

    # Collect host variables from NetBox using GraphQL.
    netbox_device_data = task.run(
        task=task_collect_graphql,
        netbox_fqdn=NETBOX_FQDN,
        netbox_token=NETBOX_TOKEN,
        query=GRAPHQL_QUERY,
    )

    # Render the configuration using Jinja and the variables collected from NetBox.
    rendered_config = task.run(
        task=template_file,
        path=J2_PATH_TEMPLATE,
        template=J2_FILE,
        **netbox_device_data.result,
        device_password=DEVICE_PASSWORD,
    )

    # Write the rendered configuration to a file.
    task.run(
        task=write_file,
        content=rendered_config.result,
        filename=f"{output_path}/{task.host}.txt",
    )

    Result(host=task.host, result=True)

# Run the main build task.
result = nr.run(
    name="Build Config",
    output_path=J2_PATH_OUTPUT,
    task=task_build_config,
)


# Condition to ensure code below will only be performed when this module is run (i.e not not imported).
if __name__ == "__main__":
    print_result(result)