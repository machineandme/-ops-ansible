import os
import sys
from fnmatch import fnmatch

import requests
import yaml

headers = {"Authorization": "Bearer %s" % os.getenv("DO_API_KEY")}

r = requests.get("https://api.digitalocean.com/v2/droplets", headers=headers)
r.raise_for_status()

inventory = dict()
test_inventory = dict()

for droplet in r.json()["droplets"]:
    ips = [n["ip_address"] for n in droplet["networks"]["v4"] if n["type"] == "public"]
    is_test = "test" in droplet["tags"]
    for tag in droplet["tags"]:
        if tag in ["test"]:
            continue
        if is_test:
            test_inventory.setdefault(tag, dict(hosts=dict()))
            test_inventory[tag]["hosts"][droplet["name"]] = {"ansible_host": ips[0]}
        else:
            inventory.setdefault(tag, dict(hosts=dict()))
            inventory[tag]["hosts"][droplet["name"]] = {"ansible_host": ips[0]}

with open("inventory.yaml", "w") as file:
    conf = {"all": {"children": inventory}}
    if test_inventory:
        conf["all"]["children"]["test"] = {"children": test_inventory}
    file.write(yaml.safe_dump(conf))
