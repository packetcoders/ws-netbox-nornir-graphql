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

