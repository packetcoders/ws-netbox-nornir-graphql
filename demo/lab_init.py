from config import nr
from rich import print
from nornir_netmiko.tasks import netmiko_send_command
from nornir_inspect import nornir_inspect
from dotenv import load_dotenv
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.files import write_file
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
import os

load_dotenv(override=True)

nr.inventory.defaults.username = os.getenv("DEVICE_USERNAME")
nr.inventory.defaults.password = os.getenv("DEVICE_PASSWORD")

STUDENT_ID = os.getenv("STUDENT_ID")
NETBOX_FQDN = os.getenv("NETBOX_FQDN")
NETBOX_TOKEN = os.getenv("NETBOX_TOKEN")


