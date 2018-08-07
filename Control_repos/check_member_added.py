from github3 import login
import sys
import re
import subprocess
import shutil
import os
import toml

program_name, config_file, github_username, github_password = sys.argv

gh = login(username=github_username, password=github_password)

organization = gh.organization("IIC2133-PUC")

with open(config_file) as conf:
    config = toml.loads(conf.read())


members = [x.login for x in organization.members()]
not_added = list()
print(sorted(members))

with open("{}".format(config["github_users_file"]), 'r') as f:
    for line in f:
        user = line.strip()
        if not user in members:
            not_added.append(user)

print("lista de usuarios no agregados a la organizacion: {}".format(str(not_added)))
