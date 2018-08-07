"""elimina todos los repos de la organizacion que cumplan con cierta expresion regular
una vez eliminados los repos, estos todavia aparecen en la cache de github.
se demora un poco en desaparecer
se recomienda no hacer esto en la internet de la u ya que por problemas de
conexion pasa que algunos repos no se borran (o repetir hartas veces el comando)
"""

import sys
import re
from repo_functions import get_organization

program_name, USERNAME, PASSWORD, REGEXP = sys.argv
REGEXP = re.compile(REGEXP)

ORGANIZATION = get_organization("IIC2133-PUC", USERNAME, PASSWORD)

COUNTER = 0
for i in ORGANIZATION.repositories():
    if REGEXP.search(str(i)):
        COUNTER += 1
        print("deleting {}".format(str(i)))
        i.delete()
print("Eliminados {} repos.".format(COUNTER))
