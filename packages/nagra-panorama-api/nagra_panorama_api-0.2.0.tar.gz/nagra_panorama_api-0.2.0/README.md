# README

This repository contains a wrapper around Panorama/PaloAlto API.
It also provides a cli tool `panorama_api`


## CLI
This package also provide a CLI tool for some operations:
* Generating an API Key
* Upgrading a group of devices
* Generating a boilerplate configuration file for the upgrades


```bash
pip install nagra_panorama_api
panorama_api --help
```


## Why the need for this library ?

For simple resource retrieval, the existing API is enough, but:

* The libraries available are not practical for it, the manual management of urls is easier
* For more complex operation, this does not suits well

The [official python SDK of PaloAltoNetworks](https://github.com/PaloAltoNetworks/pan-os-python) itself relies on a [third party wrapper](https://github.com/kevinsteves/pan-python) for their API.


This library takes a more popular approach when wrapping the API, making it easier to use. It also provides types' wrappers to simplify their usage or utility functions to re-structure the data we receive.
It provides a client for the REST API and for the XML API

* A simple client for the API
* Tool to manage the xml configuration


## Library Usage Example

```python
client = XMLApi(HOST, API_KEY)
tree = client.get_tree()

# Find your object using its name (may not be unique)
my_object = config.find_by_name("my_object_name")[0]
print(my_object)  # /address/entry[@name='my_object_name']

# Find the references to it (0 or multiple results are possible)
ref = my_object.get_references()[0]
print(ref)  # /post-rulebase/security/rules/entry[@uuid='...']/destination/member


# We must not delete the <member> tag, but we can delete its parent
client.delete(ref.parent.xpath)

# Now we must commit the changes
client.commit_changes()
# We can also revert it
# client.revert_changes()
```

The library currently doesn't provide helper tools to know how to edit the configuration. Theses changes must be done manually


## TODO

* Provide wrapper classes for the resources.

  ```python
  nat = NatPolicy(...)
  tree.insert(nat)  # or nat.insertInto(tree)
  client.create(nat.insert_xpath, nat.xml)
  ```
* # Mix Rest API and XML API ?
  https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-panorama-api/get-started-with-the-pan-os-rest-api/create-security-policy-rule-rest-api


## Links
* [Official upgrade procedure on HA with API](https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-panorama-api/pan-os-xml-api-use-cases/upgrade-pan-os-on-multiple-ha-firewalls-through-panorama-api)
