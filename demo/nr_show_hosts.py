from config import nr
from rich import print
from nornir.core.filter import F

# Filter for hosts with a specific NetBox tenant name
nr = nr.filter(F(tenant__name="pod1"))

print(nr.inventory.hosts)

# Print matched hosts
print(nr.inventory.hosts['leaf1'].dict())