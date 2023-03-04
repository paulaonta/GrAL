import numpy as np
import csv
import time

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    return (matrix[size_x - 1, size_y - 1])

path_wikidata = "./results_Wikidata/diseases_info_es.csv"
disease_pos = 0
also_known_pos = 21
sympton_pos = 2
umls_pos = 16
threshold = 2.0

mycsv = csv.reader(open(path_wikidata))  # open
first = True
symptons = []
sartu = False
gaixotasun = "gastrinomas" #"Miopericarditís"
levenshteinKalk = True
code = "C0277359" #azkenengo UMLS hartuta

t1 = time.time()
# iterate the csv file
for line in mycsv:
    diseases = []
    if first:
        first = False
    else:
        if levenshteinKalk:
            diseases.append(line[disease_pos])  # lortu gaixotasunaren izena(k)
            diseases.append(line[also_known_pos])  # lortu gaixotasunaren sinonimoak
            for disease in diseases:
                dist = levenshtein(gaixotasun.lower(), disease.lower())  # distantzia neurtu
                if dist <= threshold:
                    if len(line[sympton_pos]) > 1:  # hutsunea ez bada
                        symptons.append(line[sympton_pos])  # linka sortu
                    if not sartu:
                        print("First apperance time: " + str(time.time() - t1))
                        print("Levenshtein gaixotasunarekin: " + disease)
                        sartu = True
        else:
            if code == line[umls_pos]:
                symptons.append(line[sympton_pos])  # linka sortu
                print("Time: " + str(time.time() - t1))
                print("Code: " + line[umls_pos])
                print("Sintomak: " + ", ".join(symptons))
                break

if levenshtein:
    print("All cases time: " + str(time.time() - t1))
    print(symptons)