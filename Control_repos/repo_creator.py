"""Crea los repositorios para los alumnos"""


from github3 import login
import sys
import subprocess
import os
import toml
import time

# TODO chequear que no se demore mucho tiempo no solo el push, si no que el verificar colaborador y demases


def push_mirror(organization, repo_name):
    try:
        print("########### PUSHING THE MIRROR ###########".format(user))

        completed_process = subprocess.run(("git push --mirror https://github.com/{0}/{1}.git".format(organization.login, repo_name)).split(" "), timeout=50)
        if completed_process.returncode != 0:
            print("error {} al pushear, reintentando".format(completed_process.returncode))
            time.sleep(0.5)
            push_mirror(organization, repo_name)
        return True
    except subprocess.TimeoutExpired as err:
        print("## push mirror took too long (more than 8 seconds). Retrying ##")
        push_mirror(organization, repo_name)


def clone_base_repo(config, organization):
    try:
        print("git clone --bare git@github.com:{0}/{1}.git".format(organization.login, config["base_repo"]))
        completed_process = subprocess.run(("git clone --bare https://github.com/{0}/{1}.git".format(organization.login, config["base_repo"])).split(" "), timeout=15)
        if completed_process.returncode != 0:
            print("error {} al pullear el repo base, reintentando".format(completed_process.returncode))
            subprocess.run(("rm -rf {0}.git".format(config["base_repo"])).split(" "))
            time.sleep(1)
            clone_base_repo(config, organization)
        return True
    except subprocess.TimeoutExpired as err:
        print("## cloning took too long (more than 15 seconds). Retrying ##")
        subprocess.run(("rm -rf {0}.git".format(config["base_repo"])).split(" "))
        time.sleep(1)
        clone_base_repo(config, organization)


def repo_name(user, config):
    return "{0}-{1}-{2}-{3}-{4}".format(user, config["homework"], config["organization"], config["year"], config["semester"])


def create_repo(user, config, organization):
    if not repo_exists(user, config, organization):
        print("########### CREATING {0}'S REPO ###########".format(user))

        new_repo = organization.create_repository(repo_name(user, config), description="repo de {0} para la tarea {1}".format(user, config["homework"]), private=True, has_wiki=False)
        time.sleep(0.5)
    else:
        for i in organization.repositories():
            if i.name == repo_name(user, config):
                new_repo = i

    push_mirror(organization, repo_name(user, config))

    if not is_collaborator(user, config, organization):
        print("########### ADDING {0} AS COLLABORATOR ###########".format(user))
        new_repo.add_collaborator(user)
        time.sleep(0.1)
    print("########### DONE ###########")


def repo_exists(user, config, organization):
    print("########### CHECKING {0}'S REPO EXISTANCE ###########".format(user))
    repos = [x.name for x in organization.repositories()]
    if repo_name(user, config) in repos:
        print("########### {0}'S REPO EXISTS ###########".format(user))
        return True
    print("########### {0}'S REPO DOES NOT EXIST ###########".format(user))
    return False


def is_collaborator(user, config, organization):
    print("########### CHECKING IF {0} IS ASSIGNED TO THE REPO ###########".format(user))
    repos = organization.repositories()
    for i in repos:
        if i.name == repo_name(user, config):
            if user in [x.login for x in i.collaborators()]:
                print("########### {0} IS ASSIGNED TO THE REPO ###########".format(user))
                return True
            else:
                print("########### {0} IS NOT ASSIGNED TO THE REPO ###########".format(user))
                return False
    raise Exception("el repo no esta creado!!, no se deberia estar llegando aca!")


program_name, config_file, github_username, github_password = sys.argv

with open(config_file) as conf:
    config = toml.loads(conf.read())

print(config)
print("########### LOGGING INTO GITHUB ###########")
gh = login(username=github_username, password=github_password)
print("########### DONE ###########")
print("########### ACCESSING {} REPO ###########".format(config["organization"]))
organization = gh.organization(config["organization"])
print("########### DONE ###########")
print("########### CLONING BASE REPO ###########")
clone_base_repo(config, organization)
print("########### DONE ###########")
os.chdir("./{0}.git".format(config["base_repo"]))

with open("../{}".format(config["github_users_file"]), 'r') as f:
    for line in f:
        user = line.strip()
        create_repo(user, config, organization)
        time.sleep(0.1)

print("########### DELETING BASE REPO FROM THE MACHINE ###########")
os.chdir("../")
subprocess.run(("rm -rf {0}.git".format(config["base_repo"])).split(" "))
print("########### FINISHED ###########")
