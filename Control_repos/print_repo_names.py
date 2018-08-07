"""Podría ser útil, who knows. Si quieres imprimir
 los nombres de todos los repos que crearás"""

from github3 import login
import sys
import toml
from repo_functions import repo_name

program_name, config_file = sys.argv


with open(config_file) as conf:
    config = toml.loads(conf.read())

with open("{}".format(config["github_users_file"]), 'r') as f:
    for line in f:
        user = line.strip()
        print(repo_name(user, config))
