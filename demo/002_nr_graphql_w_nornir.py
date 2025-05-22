#!/usr/bin/env python

import ipaddress
import json
import os

import requests
from config import nr
from dotenv import load_dotenv
from nornir.core.task import Result, Task
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file

load_dotenv(override=True)

NETBOX_FQDN = os.getenv("NETBOX_FQDN")
NETBOX_TOKEN = os.getenv("NETBOX_TOKEN")

# GraphQL query to collect device variables.
GRAPHQL_QUERY = """
query DeviceQuery($deviceName: String) {
  device_list(
    filters: { 
      name: { exact: $deviceName }, 
    }) {
    name
    id
    custom_fields
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

nr.filter(tenant="pod1")

result = nr.run(
    task=task_collect_graphql,
    name="Collect build inputs from NetBox GraphQL",
    netbox_fqdn=NETBOX_FQDN,
    netbox_token=NETBOX_TOKEN,
    query=GRAPHQL_QUERY,
)

# Condition to ensure code below will only be performed when this module is run (i.e not not imported).
if __name__ == "__main__":
    print_result(result)
