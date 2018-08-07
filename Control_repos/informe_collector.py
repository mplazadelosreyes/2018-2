"""Lo escribí en inglés... no se por qué:

in this program we follow the repo naming convention used in repo_creator
it doesnt use the user list of config because the users in there might
differ from the ones assigned to the homework
we assume the informes are in pdf format

Se le entrega como argumentos el directorio donde estan todos los 
repositorios recolectados y el directorio donde se guardarán todos los
informes

Si hay repositorios en los que no se encuentra un informe, al finalizar el
programa, se imprime una lista de éstos. Para que se realize una inspección manual.

"""


import shutil
import sys
import os
import re

program_name, repos_folder, informes_destination = sys.argv
repos = os.listdir("./{}".format(repos_folder))


repos_con_problemas = []
for i in repos:

    username = i.split("-")[0]
    repo_files = os.listdir("./{}/{}".format(repos_folder, i))
    informe_folder_name = set(repo_files).intersection(
        set(["informe", "Informe"]))
    if len(informe_folder_name) > 0:
        informe_folder_name = informe_folder_name.pop()
        informe_files = os.listdir(
            "./{}/{}/{}".format(repos_folder, i, informe_folder_name))
        accepted_names = set(["informe.pdf", "Informe.pdf"])
        file_name = accepted_names.intersection(set(informe_files))
        if len(file_name) != 1:
            print("ALERTA: {} TIENE UN PROBLEMA EN LA ENTREGA DE INFORME, NO SE COPIA A LA CARPETA FINAL. HACER MANUALMENTE APLICANDO DESCUENTO.".format(username))
            repos_con_problemas.append(i)
            continue
        file_name = file_name.pop()

        shutil.copy("./{0}/{1}/{2}/{3}".format(repos_folder, i, informe_folder_name, file_name),
                    "./{0}/{1}.pdf".format(informes_destination, username))

print("\nLos siguientes {} repositorios tuvieron problemas:".format(len(repos_con_problemas)))
print(repos_con_problemas)