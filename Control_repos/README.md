Los diferentes scripts a usar  su modo de uso:

1) repo_deleter.py:
Elimina todos los repositorios de la organización "IIC2133-PUC" que cumplan con la expresión regular entregada.

Modo de uso:
$python3 repo_deleter.py miusuariogithub mipasswordgithub expresionregular

2) repo_creator.py:
Le crea los repositorios para las tareas a los alumnos. Usa un repositorio como base.

Notar que usa un archivo de configuración que por defecto se llama config.toml el cual
hay que modificar antes de correr este comando colocando los datos necesarios.

Modo de uso:
$python3 repo_creator.py config.toml miusuariogithub mipasswordgithub

3) repo_collector.py:
Recolecta las tareas de la organización. Notar que nuevamente usa el archivo config.toml

Modo de uso:
$python3 repo_collector.py config.toml miusuariogithub mipasswordgithub

4) print_repo_names.py:
Sirve solo para asegurarse que los nombres de los repos a crear son los esperados. No es un programa necesario.

Modo de uso:
$python3 print_repo_names.py config.toml

5) informe_collector.py:
Sirve para recolectar todos los repositorios desde un directorio que ya los posee (usar antes el repo collector). Recibe como parámetros el directorio donde se encuentran los repositorios y un directorio de destino.

Modo de uso:
$python3 informe_collector.py directorioconrepos directoriodestino

6) feedback_pusher.py:
Pushea todos los feedbacks a sus respectivos repositorios. Nuevamente utiliza el archivo de configuración. 

OJO: se asume que los feedbacks estaran en el directorios /Feedbacks/TX
donde TX es la tarea. ej: T3 es la tarea 3

Modo de uso:
$python3 feedback_pusher.py config.toml miusuariogithub mipasswordgithub
