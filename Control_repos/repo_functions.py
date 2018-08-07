from github3 import login

"Contains useful functions to work with the Github repositories"


def repo_name(user, config):
    "Obtains the repo name for the user"
    output = "{0}-{1}-{2}-{3}-{4}".format(user, config["homework"], config[
        "organization"], config["year"], config["semester"])
    return output


def get_organization(username, password, organization):
    gh = login(username=username, password=password)
    return gh.organization("IIC2133-PUC")


def wait_list(process_list, process_name):
    "Waits every sub{} process untill all of them have finished".format(process_name)
    unfinished_processes = []
    total_processes = len(process_list)
    analyzed_proceses = 1
    for i in process_list:
        print("Analysing {2} processes (this might take a while): ({0}/{1})".format(
            analyzed_proceses, total_processes, process_name), flush=True, end='\r')
        i.wait()
        analyzed_proceses += 1
        if i.return_code:
            unfinished_processes.append(i)
    print("")
    print("{0} processes that didnt {1} propperly.".format(
        len(unfinished_processes), process_name))
    return unfinished_processes
