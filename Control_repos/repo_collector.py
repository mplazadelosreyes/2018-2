"""Recolecta los repositorios de los alumnos"""


import sys
import subprocess
import os
import time
import toml
from github3 import login
from repo_functions import repo_name


def clone_repo(cloning_user, configuration, org):
    "Clones a repo"
    try:
        completed_process = subprocess.run(("git clone https://github.com/{0}/{1}.git".format(
            org.login, repo_name(cloning_user, configuration))).split(" "), timeout=30)
        if completed_process.returncode != 0:
            print("error {0} al pullear el repo de {1}, reintentando".format(
                completed_process.returncode, cloning_user))
            subprocess.run(
                ("rm -rf {0}".format(repo_name(cloning_user, configuration))).split(" "))
            time.sleep(1)
            return clone_repo(cloning_user, configuration, org)
        return True
    except subprocess.TimeoutExpired:
        print("## cloning took too long (more than 8 seconds). Retrying ##")
        subprocess.run(
            ("rm -rf {0}".format(repo_name(cloning_user, configuration))).split(" "))
        time.sleep(1)
        return clone_repo(cloning_user, configuration, org)


_, CONFIG_FILE, GITHUB_USERNAME, GITHUB_PASSWORD = sys.argv

with open(CONFIG_FILE) as conf:
    CONFIG = toml.loads(conf.read())

print(CONFIG)
print("########### LOGGING INTO GITHUB ###########")
GH = login(username=GITHUB_USERNAME, password=GITHUB_PASSWORD)
print("########### DONE ###########")
print("########### ACCESSING {} REPO ###########".format(
    CONFIG["organization"]))
ORGANIZATION = GH.organization(CONFIG["organization"])
print("########### DONE ###########")


NEWPATH = './{}_rep'.format(CONFIG["homework"])
if not os.path.exists(NEWPATH):
    os.makedirs(NEWPATH)
else:
    raise Exception("La carpeta de las tareas ya existe!")


os.chdir("./{}".format(NEWPATH))
with open("../{}".format(CONFIG["github_users_file"]), 'r') as f:
    for line in f:
        user = line.strip()
        clone_repo(user, CONFIG, ORGANIZATION)
        # os.chdir("./{}".format(repo_name(user, CONFIG)))
        # completed_rev = subprocess.run(('git rev-list -n 1 --before="{}" master'.format(CONFIG["collection_time"])).split(" "))
        # print(completed_rev)
        # os.chdir("../")

os.chdir("../")
print("########### FINISHED ###########")
