from os import listdir, makedirs
from os.path import isdir, join, exists
from shutil import copyfile
import sys
import csv

mal_formato = []
no_entrega = []
entregan = []

semestre = "-2017-2"

def read_csv(filename):
	with open(filename) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		dictionary = dict(map(lambda x: (x[4].lower(), x[0]),reader))
		return dictionary

def list_to_file(lista, path, filename):
	with open(join(path,filename), "w") as file:
		for elem in lista:
			file.write(elem)
			file.write("\n")

def find_pdf(path, repo):
	pdfs = list(filter(lambda x: x[-3:] == "pdf", listdir(path)))
	repo = repo.split("-")[0]
	if (len(pdfs) == 0):
		no_entrega.append(repo)
		return None
	entregan.append(repo)
	if ("Informe.pdf" in pdfs):
		return "Informe.pdf"
	mal_formato.append(repo)
	return pdfs[0]
	
def print_all(lista):
	for elem in lista:
		print("Repo: {0}".format(elem))
	
def recoltar_informes(numero_tarea):
	path_final = "Informes-{0}{1}".format(numero_tarea, semestre)
	if not exists(path_final):
		makedirs(path_final)

	path = "Recoleccion-{0}{1}".format(numero_tarea, semestre)
	tareas_entregadas = list(filter(lambda x: isdir(join(path,x)),listdir(path)))

	for tarea in tareas_entregadas:
		carpeta_informe = join(path,"{0}/Informe".format(tarea))
		repo = tarea[:-3]	
		pdf = find_pdf(carpeta_informe, repo)
		if pdf:
			informe = join(path,"{0}/Informe/{1}".format(tarea, pdf))
			github_user = repo.split("-")[0]
			copyfile(informe, join(path_final, "{0}.pdf".format(github_user)))

	list_to_file(mal_formato, path_final, "mal_formato.txt")
	list_to_file(no_entrega, path_final, "no_entrega.txt")

	print("-------- MAL FORMATO --------")
	print_all(mal_formato)
	print("\n-------- NO ENTREGAN --------")
	print_all(no_entrega)
	print("\n-------- ENTREGAN {0} ALUMNOS --------".format(len(entregan)))

recoltar_informes(sys.argv[1])

