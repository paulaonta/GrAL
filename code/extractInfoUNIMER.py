import os
import csv
import sys
import argparse
import linecache
import numpy as np

# define paths
    #questions
csv_path_quest = "/QUEST_clinical_caseMIR_relations.csv"
question_file_partial_name = "_QUEST_clinical_caseMIR.conll"

    #answers
ans_file_partial_name = "_ANS_clinical_caseMIR.conll"
csv_path_ans = "ANS_clinical_caseMIR.csv"
csv_path_folder_UMLS = "/ANS_es_UMLS/" #"/ANS_es_UMLS_relations/"
csv_path_folder_NO_UMLS = "/ANS_es_NO_UMLS/" #"/ANS_es_NO_UMLS_relations/"

#define variables
question_pos = 5
answer_pos = 12
num_answer = 5

SnoMot_pos = 5
SnoKod_pos = 4
Deepent_pos = 9
name_pos = 1
case_number_pos = 0
relation_pos = 13
relation_to_pos = 11

def createFile(path):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

def unique(list1, list2):
    remove_list = []
    for i in range(len(list1)-1):
        for j in range(i+1,len(list1)):
            if list1[i] == list1[j]:
                if list2[i] == list2[j] and j not in remove_list:
                    remove_list.append(j) #remove j

    for elem in sorted(remove_list, reverse = True): #remove all elements in the 2 lists
        list1.pop(elem)
        list2.pop(elem)
    return list1, list2

def remove_and_get_no_codes(lista, listaUMLS, extractQuest = True):
    lista_NOcodes = []
    remove_list = []
    if not extractQuest:
        for i in range(len(listaUMLS)):
            if listaUMLS[i].find("C") == -1:
                remove_list.append(i)
                lista_NOcodes.append(lista[i]) #append the name

    for elem in sorted(remove_list, reverse = True): #remove all elements in the 2 lists
        lista.pop(elem)
        listaUMLS.pop(elem)

    return lista_NOcodes, lista, listaUMLS

def get_name_and_code(elements, lista, listUMLS):
    lista.append(elements[name_pos])
    listUMLS.append(elements[SnoKod_pos].split("_")[0])
    return lista, listUMLS

def concatenate(elements, lista, list_codes):
    lista[-1] += " " + elements[name_pos]
    if not elements[SnoKod_pos].split("_")[0] in list_codes:
        list_codes[-1] = list_codes[-1].split("_")[0] + " " + elements[SnoKod_pos].split("_")[0]
    return lista, list_codes

def get_elements_of_the_middle(path, line_pos, from_pos, to_pos):
    line_pos1 = line_pos - (int(to_pos) - int(from_pos))
    pos = 1
    suffix = ""
    while line_pos != line_pos1:
        line = linecache.getline(path, line_pos1)
        elements = line.split("\t")
        suffix += " " + elements[name_pos]
        line_pos1 += 1
    return suffix

def get_all_relations(conll_lines):
    all_relations = {}
    cont = -1
    line_cont = -1
    for line in conll_lines:
        line_cont += 1
        elements = line.split("\t")
        if len(elements) > 1: #if the line is not empty
            if elements[case_number_pos] == "1":
                cont += 1
            relation = elements[relation_pos]
            relation_to = elements[relation_to_pos]
            if relation.find("-") == -1: #erlazioa baldin badaukate
                '''
                if int(relation_to) < int(elements[case_number_pos]) -1 : #ez dago jarraian
                    suffix = get_elements_of_the_middle(path, line_cont, relation_to, elements[case_number_pos])
                else:
                    suffix = ""
                '''
                if relation.find("Causada_por") != -1:
                    if relation_to + "," + str(cont) in all_relations.keys(): #it's in the dict
                        all_relations.get(relation_to + "," + str(cont)).append((str(elements[name_pos] + "+"), elements[case_number_pos])) #to identify "Causada_por" erlazioak
                    else:
                        all_relations[relation_to + "," + str(cont)] = [(str(elements[name_pos] + "+"), elements[case_number_pos])]
                else:
                    if relation_to + "," + str(cont) in all_relations.keys(): #it's in the dict
                        all_relations.get(relation_to + "," + str(cont)).append((str(elements[name_pos]), elements[case_number_pos]))  # to identify "Causada_por" erlazioak
                    else:
                        all_relations[relation_to + "," + str(cont)] = [(str(elements[name_pos]), elements[case_number_pos])]
    return all_relations #returns ALL relations, not only medical relations

def complete(path, pos, type, lista, listaUMLS, cont, all_relations = None, relations = None):
    cases = []
    pos_final = pos
    line = linecache.getline(path, pos)
    elements = line.split("\t")
    lista, listaUMLS = get_name_and_code(elements, lista, listaUMLS)
    if relations and elements[case_number_pos] + "," + str(cont) in all_relations.keys():
        elem = all_relations.get(elements[case_number_pos] + "," + str(cont))
        positions = []
        for i in range(len(elem)):
            positions.append(elem[i][1])
        if not pos+1 in positions:
            name = get_name_recursive(elements[case_number_pos], cont, all_relations, cases)
            if name != "":
                lista[-1] += " (" +  name +")"
    enum = int(elements[SnoMot_pos][-1])
    while True:
        pos += 1
        line = linecache.getline(path, pos)
        elements = line.split("\t")
        if elements[SnoMot_pos].find(type) != -1: #if it's the same type
            if elements[SnoMot_pos][-2] == "_" and int(elements[SnoMot_pos][-1]) == (enum+1): #it's part
                enum = int(elements[SnoMot_pos][-1]) #update
                if lista[-1].find(elements[name_pos]) == -1:
                    lista, listaUMLS = concatenate(elements, lista, listaUMLS)
                elif not elements[SnoKod_pos].split("_")[0] in listaUMLS:
                    listaUMLS[-1] = listaUMLS[-1].split("_")[0] + " " + elements[SnoKod_pos].split("_")[0]
                pos_final += 1

                if relations and elements[case_number_pos] + "," + str(cont) in all_relations.keys() :
                    name = get_name_recursive(elements[case_number_pos], cont, all_relations, cases)
                    if name != "":
                        lista[-1] += " (" +  name +")"
            else:
                break
        else:
            break
    return  lista, listaUMLS, pos_final

def complete_BIO(path, pos, type, lista, listaUMLS, cont, all_relations = None, relations = None):
    cases = []
    line = linecache.getline(path, pos)
    elements = line.split("\t")
    if elements[Deepent_pos][0] == "I": #inside
        while True:
            pos -= 1
            line = linecache.getline(path, pos)
            elements = line.split("\t")
            if elements[Deepent_pos][0] == "B" and elements[Deepent_pos].find(type) != -1: #go to the begining
                break
    pos_final = pos

    if elements[Deepent_pos][0] == "B": #begining
        line = linecache.getline(path, pos)
        elements = line.split("\t")
        lista, listaUMLS = get_name_and_code(elements, lista, listaUMLS)
        if relations and elements[case_number_pos] + "," + str(cont) in all_relations.keys():
            name = get_name_recursive(elements[case_number_pos], cont, all_relations, cases)
            if name != "":
                lista[-1] += " (" +  name +")"
        while True:
            pos += 1
            line = linecache.getline(path, pos)
            elements = line.split("\t")
            if elements[Deepent_pos].find(type) != -1:  # if it's the same type
                if elements[Deepent_pos][0] == "I":  # it's part
                    if lista[-1].find(elements[name_pos]) == -1:
                        lista, listaUMLS = concatenate(elements, lista, listaUMLS)
                    elif not elements[SnoKod_pos].split("_")[0] in listaUMLS:
                        listaUMLS[-1] = listaUMLS[-1].split("_")[0] + " " + elements[SnoKod_pos].split("_")[0]

                    pos_final += 1
                    if relations and elements[case_number_pos] + "," + str(cont) in all_relations.keys():
                        name = get_name_recursive(elements[case_number_pos], cont, all_relations, cases)
                        if name != "":
                            lista[-1] += " (" +  name +")"
                else:
                    break
            else:
                break
    return  lista, listaUMLS, pos_final

def update_list(path, pos, type, lista, listaUMLS, elements, cont, all_relations = None, relations = None):
    cases = []
    if elements[name_pos] != "le" and elements[name_pos] != "Le":
        if type != "Grp_Enfermedad" and type != "Alergia":
            if elements[SnoMot_pos][-2] != "_":
                lista, listaUMLS = get_name_and_code(elements, lista, listaUMLS)
                if relations and elements[case_number_pos] + "," + str(cont) in all_relations.keys():
                    name = get_name_recursive(elements[case_number_pos], cont, all_relations, cases)
                    if name != "":
                        lista[-1] += " (" +  name +")"
            else:
                lista, listaUMLS, pos = complete(path, pos, type, lista, listaUMLS, cont, all_relations, relations)
        else:
            lista, listaUMLS, pos = complete_BIO(path, pos, type, lista, listaUMLS, cont, all_relations, relations)
    return lista, listaUMLS, pos

def get_name_recursive(pos, cont, all_relations, cases):
    if not pos + "," + str(cont) in all_relations.keys() or  pos + "," + str(cont) in cases: #oinarrizko kasua
        return ""
    else:
        elem = all_relations.get(pos + "," + str(cont))
        cases.append(pos + "," + str(cont))
        names, positions = [], []
        for i in range(len(elem)):
            names.append(elem[i][0] + " ")
            positions.append(elem[i][1])
        name = ""
        for i in range(len(positions)):
            returned_name = get_name_recursive(positions[i], cont, all_relations, cases)
            if len(returned_name) > 1:
                if names[i].find("+") != -1: #Causado_por
                    name += "(Causado por: " + names[i][:-2] + "(" + returned_name + "))"
                else:
                    name += names[i] + "(" + returned_name + ")"
            else:
                if names[i].find("+") != -1:  # Causado_por
                    name += "(Causado por: " + names[i][:-2]  + returned_name +")"
                else:
                    name += names[i]  + returned_name
    return  name

def get_diseases_and_signs(conll_lines, path, extractQuest = True, all_relations = None, relations = None):
    gaixotasunak, gaixotasunakUMLS, sintomak, sintomakUMLS, gaixSin,gaixSinUMLS =  [], [], [], [], [], []
    pos, cont, pos_final = 0, -1, float("-Inf")
    pos_final1, pos_final2, pos_final3 = float("-Inf"), float("-Inf"), float("-Inf")

    if relations:
        all_relations = get_all_relations(conll_lines)

    for line in conll_lines:
        pos += 1
        elements = line.split("\t")
        findSno, findDeep = False, False
        if len(elements) > 1 and pos > pos_final:  # not iterate  empty rows
            if elements[case_number_pos] == "1":
                cont += 1
            if elements[SnoMot_pos].find("hallazgo") != -1: #sintoma bada
                findSno = True
                sintomak, sintomakUMLS, pos_final1 = update_list(path, pos, "hallazgo", sintomak, sintomakUMLS, elements,
                                                                 cont, all_relations,  relations)

            if elements[SnoMot_pos].find("trastorno") != -1:
                findSno = True
                gaixotasunak, gaixotasunakUMLS, pos_final2 = update_list(path, pos, "trastorno", gaixotasunak,
                                                            gaixotasunakUMLS, elements, cont, all_relations, relations)

            if elements[SnoMot_pos].find("anomalía_morfológica") != -1:
                findSno = True
                gaixotasunak, gaixotasunakUMLS, pos_final3 = update_list(path, pos,"anomalía_morfológica", gaixotasunak,
                                                            gaixotasunakUMLS, elements, cont, all_relations,  relations)

            pos_final = max([pos_final1, pos_final2, pos_final3])

            if not findSno and elements[Deepent_pos].find("Grp_Enfermedad") != -1:
                #hemen sartzen baldin bada, bada SnoMot ez daukalako edo ez dagoelako def. artean, beraz ezin da jakin
                # sintoma edo gaixotasuna den
                findDeep = True
                gaixSin, gaixSinUMLS, pos_final = update_list(path, pos, "Grp_Enfermedad", gaixSin, gaixSinUMLS, elements,
                                                              cont, all_relations, relations)
            elif not findSno and elements[Deepent_pos].find("Alergia") != -1:
                #hemen sartzen baldin bada, bada SnoMot ez daukalako edo ez dagoelako def. artean, beraz ezin da jakin
                # sintoma edo gaixotasuna den
                findDeep = True
                gaixSin, gaixSinUMLS, pos_final = update_list(path, pos, "Alergia", gaixSin, gaixSinUMLS, elements,
                                                              cont, all_relations,  relations)

    gaixotasunak, gaixotasunakUMLS = unique(gaixotasunak, gaixotasunakUMLS)
    gaixotasunak_NOcode, gaixotasunak, gaixotasunakUMLS = remove_and_get_no_codes(gaixotasunak, gaixotasunakUMLS, extractQuest)
    sintomak, sintomakUMLS = unique(sintomak, sintomakUMLS)
    sintomak_NOcode, sintomak, sintomakUMLS = remove_and_get_no_codes(sintomak, sintomakUMLS, extractQuest)
    gaixSin, gaixSinUMLS = unique(gaixSin, gaixSinUMLS)
    gaixSin_NOcode, gaixSin, gaixSinUMLS = remove_and_get_no_codes(gaixSin, gaixSinUMLS, extractQuest)

    return gaixotasunak, gaixotasunakUMLS,  gaixotasunak_NOcode, sintomak, sintomakUMLS, sintomak_NOcode, gaixSin, gaixSinUMLS, gaixSin_NOcode

def create_and_write_csv(line, path):
    # create a .csv to save the diseases and findings
    createFile(path)
    myFile = open(path, 'w')
    writer = csv.writer(myFile)
    writer.writerow(line)
    return writer

def extract_questions(input_path, output_path, max_files, relations = None):
    # create a .csv to save the diseases and findings
    first_line = ["kasuZbkia", "gaixotasunak", "gaixotasunUMLS", "sintomak", "sintomenUMLS", "gaixSin", "gaixSinUMLS"]
    writer =  create_and_write_csv(first_line, output_path +"/" + csv_path_quest)

    for i in range(max_files):  # iterate all the cases
        my_conll_file_location =  input_path + str(i) + question_file_partial_name
        conll_file = open(my_conll_file_location, "r")
        conll_lines = conll_file.readlines()

        gaixotasunak, gaixotasunakUMLS, gaixotasunak_NOcode, sintomak, sintomakUMLS, sintomak_NOcode, gaixSin, \
            gaixSinUMLS, gaixSin_NOcode = get_diseases_and_signs(conll_lines, my_conll_file_location, relations=relations)

        # write in the csv
        row = [str(i), ",".join(gaixotasunak), ",".join(gaixotasunakUMLS), ",".join(sintomak), ",".join(sintomakUMLS),
               ",".join(gaixSin), ",".join(gaixSinUMLS)]
        writer.writerow(row)
        conll_file.close()

def extract_answers(input_path, output_path, max_files, relations = None):
    createFile(output_path + csv_path_folder_UMLS)
    createFile(output_path + csv_path_folder_NO_UMLS)
    for i in range(max_files):  # iterate all the cases
        # create a .csv to save the diseases and findings WITH umls codes
        first_line = ["erantzunZbkia", "gaixotasunak", "gaixotasunUMLS", "sintomak", "sintomenUMLS", "gaixSin", "gaixSinUMLS"]
        writer_umls = create_and_write_csv(first_line, output_path + csv_path_folder_UMLS + str(i) + "_" + csv_path_ans)

        # create a .csv to save the diseases and findings WITH NO umls codes
        first_line = ["erantzunZbkia", "gaixotasunak", "sintomak", "gaixSin"]
        writer_no_umls = create_and_write_csv(first_line, output_path + csv_path_folder_NO_UMLS + str(i) + "_" + csv_path_ans)

        for j in range(num_answer):
            gaixotasunak, gaixotasunak_NOcode, gaixotasunakUMLS, sintomak, sintomak_NOcode, sintomakUMLS, gaixSin, \
                gaixSin_NOcode, gaixSinUMLS = [], [], [], [], [], [], [], [], []
            try:
                my_conll_file_location = input_path + str(i) + "(" + str(j) + ")" + ans_file_partial_name
                conll_file = open(my_conll_file_location, "r")
                conll_lines = conll_file.readlines()

                gaixotasunak, gaixotasunakUMLS, gaixotasunak_NOcode, sintomak, sintomakUMLS, sintomak_NOcode, gaixSin, \
                    gaixSinUMLS, gaixSin_NOcode = get_diseases_and_signs(conll_lines, my_conll_file_location,
                                                                         extractQuest=False,  relations=relations)
            except:
                pass

            # write in the csv the diseases and signs WITH UMLS code
            row = [str(j), ",".join(gaixotasunak), ",".join(gaixotasunakUMLS), ",".join(sintomak),
                   ",".join(sintomakUMLS), ",".join(gaixSin), ",".join(gaixSinUMLS)]
            writer_umls.writerow(row)

            # write in the csv the diseases and signs WITHOUT UMLS code
            row = [str(j), ",".join(gaixotasunak_NOcode), ",".join(sintomak_NOcode), ",".join(gaixSin_NOcode)]
            writer_no_umls.writerow(row)
            conll_file.close()

def count_files(dir_path):
    count = 0
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)) and path.find(question_file_partial_name) != -1:
            count += 1
    return count

def main(input_path: str, output_path: str, mode: str, relations=None):
    createFile(output_path)
    max_files = count_files(input_path)

    if mode == "Q" or mode == "q":
        print("Extracting questions info...")
        extract_questions(input_path, output_path, max_files, relations)
    elif mode == "A" or mode == "a":
        print("Extracting answers info...")
        extract_answers(input_path, output_path, max_files, relations)
    else:
        print("The option is not correct. Please select (Q)uestion or (A)nswer. \n")

if __name__ == '__main__':
    # Example usage of the main function
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print("Usage: {} input_source output_source mode (--relations)".format(sys.argv[0]))
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("arg1", type=str, help="input source 1")
        parser.add_argument("arg2", type=str, help="input source 2")
        parser.add_argument("arg3", type=str, help="input source 3 ")
        parser.add_argument("--relations", help="Get diseases with their relations", action="store_true")
        args = parser.parse_args()
        main(args.arg1, args.arg2, args.arg3, args.relations)



