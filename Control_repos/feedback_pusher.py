"""
Pushea los feedbacks de los alumnos a sus respectivos repositorios
"""

from github3 import login
import sys
import subprocess
import os
import toml
import shutil
import time
import re
from tqdm import tqdm
from repo_functions import repo_name

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


newpath = './{}_rep'.format(config["homework"])
if not os.path.exists(newpath):
    os.makedirs(newpath)
feedbacks = os.listdir("./Feedbacks/{}".format(config["homework"]))
print(feedbacks)

os.chdir("./{}".format(newpath))
with open("../{}".format(config["github_users_file"]), 'r') as f:
    for line in f:
        user = line.strip()
        print("Working on {0}".format(user))
        repo = repo_name(user, config)

        os.chdir("./{}".format(repo))

        subprocess.run(("git pull").split(" "))

        if not os.path.exists("Feedback_{}".format(config["homework"])):
            os.makedirs("Feedback_{}".format(config["homework"]))
        else:
            os.chdir("../")
            print("### ALREADY HAS FEEDBACK ###")
            continue
            shutil.rmtree('Feedback_{}'.format(config["homework"]))
            os.makedirs("Feedback_{}".format(config["homework"]))

        regexp = re.compile("(?i){0}.md".format(user))
        matching = list(filter(regexp.match, feedbacks))
        if len(matching) == 0:
            print("NO TIENE FEEDBACK")
        else:
            user_feedback = list(filter(regexp.match, feedbacks))[0]

            shutil.copy("../../Feedbacks/{0}/{1}".format(config["homework"], user_feedback), "./Feedback_{}/".format(config["homework"]))

            subprocess.run(("git add --all").split(" "))
            subprocess.run(("git commit -m Feedback-{0}".format(config["homework"])).split(" "))
            subprocess.run(("git push").split(" "))

        os.chdir("../")


os.chdir("../")


print("########### FINISHED ###########")
