from github3 import login
import sys
import subprocess
import os
import toml
import time

def clone_base_repo(config, organization):
    try:
        completed_process=subprocess.run(("git clone --bare git@github.com:{0}/{1}.git".format(organization.login, config["base_repo"])).split(" "), timeout=30)
        if completed_process.returncode != 0:
            print("error {} al pullear el repo base, reintentando".format(completed_process.returncode))
            time.sleep(1)
            clone_base_repo(config, organization)
        return True
    except subprocess.TimeoutExpired as err:
        print("## cloning took too long (more than 30 seconds). Retrying ##")
        subprocess.run(("rm -rf {0}.git".format(config["base_repo"])).split(" "))
        time.sleep(1)
        clone_base_repo(config, organization)

def repo_name(user, config):
    return "{0}-{1}-{2}-{3}-{4}".format(user, config["homework"], config["organization"], config["year"], config["semester"])

def push_mirror(organization, repo_name):
    try:
        completed_process = subprocess.run(("git push --mirror git@github.com:{0}/{1}.git".format(organization.login, repo_name)).split(" "), timeout=30)
        if completed_process.returncode != 0:
            print("error {} al pushear, reintentando".format(completed_process.returncode))
            rime.sleep(0.5)
            push_mirror(organization, repo_name)
        return True
    except subprocess.TimeoutExpired as err:
        print("## push mirror took too long (more than 30 seconds). Retrying ##")
        push_mirror(organization, repo_name)

program_name, config_file, github_username, github_password = sys.argv

error_output = ""

with open(config_file) as conf:
    config = toml.loads(conf.read())
gh = login(username=github_username, password=github_password)
organization = gh.organization(config["organization"])
clone_base_repo(config, organization)
os.chdir("./{0}.git".format(config["base_repo"]))

with open("../{}".format(config["github_users_file"]), 'r') as f:
    for line in f:
        user = line.strip()
        if repo_name(user, config) not in [x.name for x in organization.repositories()]:
            error_output+="no se ha CREADO EL REPO para {0}\n".format(user)
        else:
            # push_mirror(organization, repo_name(user, config))
            for i in organization.repositories():
                if i.name == repo_name(user, config):
                    repo=i

            if user not in [x.login.lower() for x in repo.collaborators()]:
                error_output+="el repo de {0} NO ESTA CORRECTAMENTE ASIGNADO\n".format(user)
            else:
                print("repo de {0} creado correctamente".format(user))

os.chdir("../")
subprocess.run(("rm -rf {0}.git".format(config["base_repo"])).split(" "))

print(error_output)
print("########### FINISHED ###########")
