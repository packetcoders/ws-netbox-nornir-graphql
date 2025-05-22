import os

import requests
from dotenv import load_dotenv
from rich import print as rprint

load_dotenv(override=True)

NETBOX_FQDN = os.getenv("NETBOX_FQDN")
NETBOX_TOKEN = os.getenv("NETBOX_TOKEN")

# Create the GraphQL query
GRAPHQL_QUERY = """
query DeviceQuery($deviceName: String) {
  device_list(
    filters: { 
      name: { exact: $deviceName }, 
    }) {
    name
    id
  }
}
"""

# Create the HTTP headers
headers = {
    "Authorization": f"Token {NETBOX_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# Create the GraphQL variables
graphql_variables = {
  "deviceName": "leaf1",
}

# Build the GraphQL query
response = requests.post(
    url=f"{NETBOX_FQDN}/graphql/",
    json={
        "query": GRAPHQL_QUERY,
        "variables": graphql_variables,
    },
    headers=headers,
)

# Print the response
rprint(response.json())

    
