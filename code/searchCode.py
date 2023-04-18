import numpy as np
import csv
import sys
import argparse
import os

#positions in wikidata
disease_pos = 0
also_known_pos = 21
sympton_pos = 2
umls_pos = 16

#positions in input
gaix_code_pos = 2
gaix_name_pos = 1
sign_code_pos = 4
sign_name_pos = 3
gaiSin_code_pos = 6
gaiSin_name_pos = 5
#####
gaix_name_pos_dif = 1
sign_name_pos_dif = 2
gaiSin_name_pos_dif = 3
gaix_name_pos_no_dif = 4

csv_path_file= "_ANS_clinical_caseMIR.csv"

not_cases_es = [1,9,18,21,28,33,34,36,39,42,51,56,57,62,72,73,74,75,76,79,80,81,82,83,87,91,103,104,106,109,110,111,134,135,137,141,144,148,150,151,155,156,163,164,166,171,172,185,186,198,211,217,220,224,225,227,232,234,241,242,244,248,257,259,260,261,274,285,286,290,291,296,300,301,303,304,305,312,314,316,323,325,327,329,334,343,345,347,353,354,356,361,362,365,370,371,373,381,382,384,389,398,402,403,404,405,408,410,413,414,416,417,420,424,427,428,429,431,433,434,436,438,443,447,452,454,455,457,461,462,463,464,467,469,481,485,496,497,506]
not_cases_en = [0,1,6,7,8,9,11,17,18,19,20,21,22,26,28,33,34,36,38,39,43,46,47,48,51,53,55,56,57,59,60,62,64,65,72,73,74,75,76,79,80,81,82,83,86,89,91,95,98,100,103,104,106,107,108,109,110,111,116,121,122,131,132,134,135,136,137,138,139,141,148,150,151,155,156,157,162,163,164,166,169,171,172,173,181,182,185,186,187,188,191,199,208,211,212,213,214,217,220,224,225,227,229,232,234,236,238,239,241,242,244,245,248,251,252,254,255,257,258,259,260,261,274,278,282,285,286,290,291,292,293,295,296,298,299,300,301,302,303,304,305,309,310,311,312,314,316,318,323,325,327,328,333,335,336,339,343,344,345,347,352,353,354,356,357,361,362,365,367,370,371,372,373,377,382,384,385,388,389,392,395,396,398,402,403,404,405,406,408,410,413,414,415,416,417,418,419,422,424,427,428,429,430,431,432,433,434,436,438,439,443,446,447,450,452,455,457,458,459,461,462,463,464,467,469,477,479,481,484,485,487,488,490,491,495,496,497,498,502,504,506]


def createFile(path):
    mydirname = './' + path
    if not os.path.exists(mydirname):
        os.makedirs(os.path.dirname(mydirname), exist_ok=True)

def create_and_write_csv(line, path):
    # create a .csv to save the diseases and findings
    createFile(path)
    myFile = open(path, 'w')
    writer = csv.writer(myFile)
    writer.writerow(line)

def unique(list1):
    x = np.array(list1)
    return np.unique(x)

def remove_(str):
    elem = str.split("_")
    return elem[0]

def remove_empty_elements(lista):
    return_list = []
    for elem in lista:
        if len(elem) > 1:
            return_list.append(elem)
    return return_list

def convert_2_correct_format(lista):
    return_lista = []
    for l in lista.split(","):
        if l.find("#") != -1:  # has #
            for elem in unique(l.split("#")):
                return_lista.append(remove_(elem))
        elif l.find(" ") != -1:  # has space
            for elem in unique(list(l.split(" "))):
                return_lista.append(remove_(elem))
        else:
            return_lista.append(remove_(l))
    return_lista = remove_empty_elements(return_lista)
    return  unique(return_lista)

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

def search_code_in_Wikidata(code, wikidata_path):
    mycsv = csv.reader(open(wikidata_path))  # open input
    first = True

    for line in mycsv:
        if first:
            first = False
        else:
            code_umls = line[umls_pos].split(",")
            if code in code_umls:
                return line[sympton_pos].split(",")
    return None

def get_all_signs(code, wikidata_path):
    signs, signs_codes, not_signs_codes = [], [], []
    sign = search_code_in_Wikidata(code, wikidata_path)
    has_sign = False
    if sign is None:
        not_signs_codes.append(code)
    else:
        for s in sign:
            if s is None:
                not_signs_codes.append(code)
            elif len(s) <= 1:
                signs.append("-")
                has_sign = True
            else:
                signs.append(s)
                has_sign = True
        if has_sign:
            signs_codes.append(code)

    return signs, signs_codes, not_signs_codes

def get_name(code, path):
    mycsv = csv.reader(open(path))  # open input
    first = True
    for line in mycsv:
        if first:
            first = False
        else:
            codes = line[gaix_code_pos].split(",")
            for i in range(len(codes)):
                if code in codes[i]:
                    return line[gaix_name_pos].split(",")[i]

            codes = line[sign_code_pos].split(",")
            for i in range(len(codes)):
                if code in codes[i]:
                    return line[sign_name_pos].split(",")[i]

            try:  # because in english there aren't gaiSin
                codes = line[gaiSin_code_pos].split(",")
                for i in range(len(codes)):
                    if code in codes[i]:
                        return line[gaiSin_name_pos].split(",")[i]
            except:
                pass
    return None

def write_csv(ans_number, names, names_codes, no_names, no_names_codes, output_path):
    str_names = ""
    str_codes = ""
    str_no_codes = ""
    str_no_names = "# ".join(no_names)

    for i in range(len(names)):
        str_names += ", ".join(names[i]) + "# "

    for i in range(len(names_codes)):
        str_codes += ", ".join(names_codes[i]) + "# "

    for i in range(len(no_names_codes)):
        str_no_codes += ", ".join(no_names_codes[i]) + "# "

    row = [ans_number, str_codes[:-2], str_names[:-2], str_no_codes[:-2], str_no_names]
    myFile = open(output_path, 'a')
    writer = csv.writer(myFile)
    writer.writerow(row)

def write_csv_lev(ans_number, names, names_lev, signs, output_path):
    str_signs = ""
    str_lev_names = ""
    str_names = "#".join(names)

    for i in range(len(names_lev)):
        str_lev_names += ", ".join(names_lev[i]) + "# "
        str_signs += ", ".join(signs[i]) + "# "
    print(str_names)
    row = [ans_number, str_names, str_lev_names[:-2], str_signs[:-2]]
    myFile = open(output_path, 'a')
    writer = csv.writer(myFile)
    writer.writerow(row)


def search_codes(input_path, wikidata_path, output_path, max_files):
    for i in range(max_files):
        if i not in not_cases_es:
            # create a .csv to save the diseases and findings
            first_line = ["erantzunZbkia", "gaixotasunCodes", "sintomak", "gaixotasunNOCodes", "gaixotasunNOIzenak"]
            create_and_write_csv(first_line, output_path + str(i) + csv_path_file)
            mycsv = csv.reader(open(input_path + str(i) + csv_path_file))  # open input
            first = True

            for line in mycsv:
                if first:
                    first = False
                else:
                    signs, signs_codes, not_signs_codes, not_signs_names, codes = [], [], [], [], []
                    codes.extend(convert_2_correct_format(line[gaix_code_pos]))
                    codes.extend(convert_2_correct_format(line[sign_code_pos]))
                    try: #because in english there aren't gaiSin
                        codes.extend(convert_2_correct_format(line[gaiSin_code_pos]))
                    except:
                        pass

                    for code in codes:
                        sign, sign_codes, not_sign = get_all_signs(code, wikidata_path)
                        if sign:
                            signs.append(sign)
                        if sign_codes:
                            signs_codes.append(sign_codes)
                        if not_sign:
                            not_signs_codes.append(not_sign)
                            names = []
                            for ns in not_sign:
                                name = get_name(ns, input_path + str(i) + csv_path_file)
                                if name is not None:
                                    names.append(name)
                                else:
                                    print("An error occurs, {} has no name.".format(not_sign))
                            not_signs_names.append(names)

                    #test that it's doing well
                    luz_sign, luz_no_sign = 0, 0
                    for elem in not_signs_codes:
                        luz_no_sign += len(elem)
                    for elem in signs_codes:
                        luz_sign += len(elem)
                    assert ((luz_no_sign + luz_sign) >= (len(codes)))

                    write_csv(str(i), signs, signs_codes, unique(not_signs_names), not_signs_codes, output_path + str(i) + csv_path_file)
def search_codes(input_path, wikidata_path, output_path, max_files):
    for i in range(max_files):
        if i not in not_cases_es:
            # create a .csv to save the diseases and findings
            first_line = ["erantzunZbkia", "gaixotasunCodes", "sintomak", "gaixotasunNOCodes", "gaixotasunNOIzenak"]
            create_and_write_csv(first_line, output_path + str(i) + csv_path_file)
            mycsv = csv.reader(open(input_path + str(i) + csv_path_file))  # open input
            first = True

            for line in mycsv:
                if first:
                    first = False
                else:
                    signs, signs_codes, not_signs_codes, not_signs_names, codes = [], [], [], [], []
                    codes.extend(convert_2_correct_format(line[gaix_code_pos]))
                    codes.extend(convert_2_correct_format(line[sign_code_pos]))
                    try: #because in english there aren't gaiSin
                        codes.extend(convert_2_correct_format(line[gaiSin_code_pos]))
                    except:
                        pass

                    for code in codes:
                        sign, sign_codes, not_sign = get_all_signs(code, wikidata_path)
                        if sign:
                            signs.append(sign)
                        if sign_codes:
                            signs_codes.append(sign_codes)
                        if not_sign:
                            not_signs_codes.append(not_sign)
                            names = []
                            for ns in not_sign:
                                name = get_name(ns, input_path + str(i) + csv_path_file)
                                if name is not None:
                                    names.append(name)
                                else:
                                    print("An error occurs, {} has no name.".format(not_sign))
                            not_signs_names.append(names)

                    #test that it's doing well
                    luz_sign, luz_no_sign = 0, 0
                    for elem in not_signs_codes:
                        luz_no_sign += len(elem)
                    for elem in signs_codes:
                        luz_sign += len(elem)
                    assert ((luz_no_sign + luz_sign) >= (len(codes)))

                    write_csv(str(i), signs, signs_codes, unique(not_signs_names), not_signs_codes, output_path + str(i) + csv_path_file)

def get_diseases(line, different):
    disease = []
    if different: #there are three columns to store the names
        if line[gaix_name_pos_dif] != '':
            disease.extend(line[gaix_name_pos_dif].split(","))
        if line[sign_name_pos_dif] != '':
            disease.extend(line[sign_name_pos_dif].split(","))
        if line[gaiSin_name_pos_dif] != '':
            disease.extend(line[gaiSin_name_pos_dif].split(","))
    else:
        if line[gaix_name_pos_no_dif] != '':
            if line[gaix_name_pos_no_dif][0] == " ":
                disease.extend(line[gaix_name_pos_no_dif][1:].split("#"))
            else:
                disease.extend(line[gaix_name_pos_no_dif].split("#"))
    return  disease

def get_signs_by_levenshtein(wikidata_path, threshold, gaixotasun):
    mycsv = csv.reader(open(wikidata_path))  # open input
    first = True
    symptons, dis_names = [], []
    for line in mycsv:
        diseases = []
        if first:
            first = False
        else:
            if line[disease_pos] != " ":
                diseases.extend(line[disease_pos].split(","))  # lortu gaixotasunaren izena(k)
            if line[also_known_pos] != " ":
                diseases.extend(line[also_known_pos].split(","))  # lortu gaixotasunaren sinonimoak
            for disease in diseases:
                dist = levenshtein(gaixotasun.lower(), disease.lower())  # distantzia neurtu
                if dist <= float(threshold):
                    if len(line[sympton_pos]) > 1:  # hutsunea ez bada
                        symptons.append(line[sympton_pos])  #lortu sintoma
                        dis_names.append(line[disease_pos])
                    else:
                        symptons.append("-")  # lortu sintoma
                        dis_names.append(line[disease_pos])
    return symptons, dis_names

def search_by_levenshtein(input_path, wikidata_path, output_path, max_files, threshold, different = None):
    cont = 0
    for i in range(max_files):
        if i not in not_cases_es:
            # create a .csv to save the diseases and findings
            first_line = ["erantzunZbkia", "gaixotasunIzenOrig", "gaixotasunIzenLev", "sintomak"]
            create_and_write_csv(first_line, output_path + str(i) + csv_path_file)

            mycsv = csv.reader(open(input_path + str(i) + csv_path_file))  # open input
            first = True

            for line in mycsv:
                if first:
                    first = False
                else:
                    diseases = get_diseases(line, different)
                    if len(diseases) >0:
                        print(diseases)
                    all_symptons, all_dis_names = [], []

                    for d in diseases:
                        symptons, dis_names = get_signs_by_levenshtein(wikidata_path, threshold, d)
                        if len(symptons) > 1:
                            all_symptons.append(symptons)
                        else:
                            all_symptons.append(["-"])

                        if len(dis_names) > 1:
                            all_dis_names.append(dis_names)
                        else:
                            all_dis_names.append(["-"])
                    write_csv_lev(str(i), diseases, all_dis_names, all_symptons, output_path + str(i) + csv_path_file )
def count_files(dir_path, lev = False):
    if lev:
        count = float("-Inf")
        for path in os.listdir(dir_path):
            number = int(path.split("_ANS_clinical_caseMIR.csv")[0])
            if number > count:
                count = number
    else:
        count = 0
        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1
    return count

def main(input_path: str, wikidata_path:str, output_path: str, levenshtein_dist:int, d):
    if os.path.isfile(wikidata_path) and wikidata_path.find(".csv") != -1:# they are .csv files
        if os.path.isdir(input_path) and os.path.isdir(output_path):
            if input_path[-1] != "/":
                input_path += "/"
            if output_path[-1] != "/":
                output_path += "/"
            if levenshtein_dist is not None:
                max_files = count_files(input_path, lev = True) +1
                search_by_levenshtein(input_path, wikidata_path, output_path, max_files, levenshtein_dist, d)
            else:
                max_files = count_files(input_path)
                search_codes(input_path, wikidata_path, output_path, max_files)
        else:
            print("The first and last paths must be from existing directories.")
    else:
        print("The file of the middle must be a csv file.")


if __name__ == '__main__':
    # Example usage of the main function
    if len(sys.argv) != 4 and len(sys.argv) != 6 and len(sys.argv) != 7:
        print("Usage: {} (--l THRESHOLD) input_source wikidata_path output_source --d ".format(sys.argv[0]))
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("arg1", type=str, help="input source")
        parser.add_argument("arg2", type=str, help="wikidata source")
        parser.add_argument("arg3", type=str, help="output source")
        parser.add_argument("--l", type=int, help="Calculate de levenshtein distance between the input and output with a threshold" )
        parser.add_argument("--d",  help="The input source is  different, there is a .csv only with the names",
                            action="store_true")
        args = parser.parse_args()
        main(args.arg1, args.arg2, args.arg3, args.l, args.d)

