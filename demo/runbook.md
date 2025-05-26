## GraphQL

**basic**

```
query {
  device_list {
    name
    id
  }
}
```

```
query {
  device_list {
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
```

**Arguments and filters**

```
{
  device_list(filters: { name: { exact: "rtr-spine1" }, tenant: ["acme1"] }) {
    name
    id
    tenant {
      name
    }
  }
}
```

**Variables**

```
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
```
```
{
  "deviceName": "leaf1",
}
```
