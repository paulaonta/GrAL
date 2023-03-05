import os
import csv
import sys

# define paths
    #questions
csv_path_quest = "/QUEST_clinical_caseMIR.csv"
question_file_partial_name = "_QUEST_clinical_caseMIR.conll"

    #answers
ans_file_partial_name = "_ANS_clinical_caseMIR.conll"
csv_path_ans = "ANS_clinical_caseMIR.csv"
csv_path_folder_UMLS = "/ANS_es_UMLS/"
csv_path_folder_NO_UMLS = "/ANS_es_NO_UMLS/"

#define variables
question_pos = 5
answer_pos = 12
num_answer = 5

SnoMot_pos = 5
SnoKod_pos = 4
Deepent_pos = 9
name_pos = 1

def createFile(path):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

def get_name_and_code(elements, lista, listUMLS, listNO_UMLS, extractQuest):
    if extractQuest:
        listNO_UMLS = []
        lista.append(elements[name_pos])
        listUMLS.append(elements[SnoKod_pos])
    else:
        if elements[SnoKod_pos].find("-") == -1:#it has code
            lista.append(elements[name_pos])
            listUMLS.append(elements[SnoKod_pos])
        else: #it hasn't code
            listNO_UMLS.append(elements[name_pos])
    return lista, listNO_UMLS, listUMLS

def concatenate(elements, lista, list_codes):
    lista[-1] += " " + elements[name_pos]
    list_codes[-1] = list_codes[-1].split("_")[0] + " " + elements[SnoKod_pos].split("_")[0]
    return lista, list_codes

def get_diseases_and_signs(conll_lines, extractQuest = True):
    gaixotasunak, gaixotasunak_NOcode, gaixotasunakUMLS, sintomak, sintomak_NOcode, sintomakUMLS, gaixSin, gaixSin_NOcode,gaixSinUMLS =  [], [], [], [], [], [], [], [], []
    isPartS, isPartG, isPartGS = False, False, False

    for line in conll_lines:
        elements = line.split("\t")
        findSno = False
        if len(elements) > 1:  # not iterate  empty rows
            if elements[SnoMot_pos].find("hallazgo") != -1: #sintoma bada
                findSno = True
                if not isPartS:
                    if elements[name_pos] not in sintomak and elements[name_pos] != "le":
                        sintomak, sintomak_NOcode, sintomakUMLS = get_name_and_code(elements, sintomak,
                                                                            sintomakUMLS, sintomak_NOcode, extractQuest)
                if elements[SnoMot_pos][-2] == "_":
                    if isPartS:
                        sintomak, sintomakUMLS = concatenate(elements, sintomak, sintomakUMLS)
                    isPartS = True
                else:
                    isPartS = False
                isPartG = False

            if elements[SnoMot_pos].find("trastorno") != -1 or elements[SnoMot_pos].find("anomalía_morfológica") != -1:
                findSno = True
                if not isPartG:
                    if elements[name_pos] not in gaixotasunak and elements[name_pos] != "le":
                        gaixotasunak, gaixotasunak_NOcode, gaixotasunakUMLS = get_name_and_code(elements, gaixotasunak,
                                                                    gaixotasunakUMLS, gaixotasunak_NOcode, extractQuest)
                if elements[SnoMot_pos][-2] == "_":
                    if isPartG:
                        gaixotasunak, gaixotasunakUMLS = concatenate(elements, gaixotasunak, gaixotasunakUMLS)
                    isPartG = True
                else:
                    isPartG = False
                isPartS = False

            if not findSno and elements[Deepent_pos].find("Grp_Enfermedad") != -1 or elements[Deepent_pos].find("Alergia") != -1:
                # hemen sartzen baldin bada, bada SnoMot ez daukalako edo ez dagoelako def. artean, beraz ezin da jakin
                # sintoma edo gaixotasuna den
                if elements[Deepent_pos][0] == "B" or ( elements[Deepent_pos][0] == "I" and not isPartGS):
                    if elements[name_pos] not in gaixSin and elements[name_pos] != "le":
                        gaixSin, gaixSin_NOcode, gaixSinUMLS = get_name_and_code(elements, gaixSin, gaixSinUMLS, gaixSin_NOcode, extractQuest)
                        isPartGS = True

                elif elements[Deepent_pos][0] == "I" : #it's inside
                    gaixSin, gaixSinUMLS = concatenate(elements, gaixSin, gaixSinUMLS)
                    isPartGS = True
                else:
                    isPartGS = False


    return gaixotasunak, gaixotasunak_NOcode, gaixotasunakUMLS, sintomak, sintomak_NOcode, sintomakUMLS, gaixSin, gaixSin_NOcode, gaixSinUMLS

def create_and_write_csv(line, path):
    # create a .csv to save the diseases and findings
    createFile(path)
    myFile = open(path, 'w')
    writer = csv.writer(myFile)
    writer.writerow(line)
    return writer

def extract_questions(input_path, output_path, max_files):
    # create a .csv to save the diseases and findings
    first_line = ["kasuZbkia", "gaixotasunak", "gaixotasunUMLS", "sintomak", "sintomenUMLS", "gaixSin", "gaixSinUMLS"]
    writer =  create_and_write_csv(first_line, output_path +"/" + csv_path_quest)

    for i in range(max_files):  # iterate all the cases
        my_conll_file_location =  input_path + str(i) + question_file_partial_name
        conll_file = open(my_conll_file_location, "r")
        conll_lines = conll_file.readlines()

        gaixotasunak, gaixotasunak_NOcode, gaixotasunakUMLS, sintomak, sintomak_NOcode, sintomakUMLS, gaixSin, \
            gaixSin_NOcode, gaixSinUMLS = get_diseases_and_signs(conll_lines)

        # write in the csv
        row = [str(i), ",".join(gaixotasunak), ",".join(gaixotasunakUMLS), ",".join(sintomak), ",".join(sintomakUMLS),
               ",".join(gaixSin), ",".join(gaixSinUMLS)]
        writer.writerow(row)
        conll_file.close()

def extract_answers(input_path, output_path, max_files):
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

                gaixotasunak, gaixotasunak_NOcode, gaixotasunakUMLS, sintomak, sintomak_NOcode, sintomakUMLS, gaixSin, \
                    gaixSin_NOcode, gaixSinUMLS = get_diseases_and_signs(conll_lines, extractQuest=False)
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

def main(input_path: str, output_path: str, mode: str):
    createFile(output_path)
    max_files = count_files(input_path)

    if mode == "Q" or mode == "q":
        print("Extracting questions info...")
        extract_questions(input_path, output_path, max_files)
    elif mode == "A" or mode == "a":
        print("Extracting answers info...")
        extract_answers(input_path, output_path, max_files)
    else:
        print("The option is not correct. Please select (Q)uestion or (A)nswer. \n")

if __name__ == '__main__':
    # Example usage of the main function
    if len(sys.argv) != 4:
        print("Usage: {} input_source output_source mode".format(sys.argv[0]))
    else:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]
        main(arg1, arg2, arg3)



