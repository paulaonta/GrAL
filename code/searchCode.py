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

csv_path_file= "_ANS_clinical_caseMIR.csv"
not_code_file_path = "./not_code_ANS.csv"

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

def search_code_in_Wikidata(code, wikidata_path):
    mycsv = csv.reader(open(wikidata_path))  # open input
    first = True

    for line in mycsv:
        if first:
            first = False
        else:
            code_umls = line[umls_pos].split(",")
            if code in code_umls:
                return line[sign_code_pos].split(",")
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
def write_csv(ans_number, names, names_codes, output_path):
    str_names = ""
    str_codes = ""
    for i in range(len(names)):
        str_names += ", ".join(names[i]) + " # "
        str_codes += ", ".join(names_codes[i]) + " # "

    row = [ans_number, str_codes[:-2], str_names[:-2]]
    myFile = open(output_path, 'a')
    writer = csv.writer(myFile)
    writer.writerow(row)

def search_codes(input_path, wikidata_path, output_path, max_files):
    # create a .csv to save the diseases and findings
    first_line = ["erantzunZbkia", "gaixotasunCodes", "sintomak"]
    create_and_write_csv(first_line, output_path)
    first_line = ["erantzunZbkia", "gaixotasunCodes", "gaixotasunIzenak"]
    create_and_write_csv(first_line, not_code_file_path)

    for i in range(max_files):
        mycsv = csv.reader(open(input_path + str(i) + csv_path_file))  # open input
        first = True
        signs, signs_codes, not_signs_codes, not_signs_names, codes = [], [], [], [], []

        for line in mycsv:
            if first:
                first = False
            else:
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
                        print("An error occurs {} has no name.".format(not_sign))
                not_signs_names.append(names)

        #test that it's doing well
        luz_sign, luz_no_sign = 0, 0
        for elem in not_signs_codes:
            luz_no_sign += len(elem)
        for elem in signs_codes:
            luz_sign += len(elem)
        assert ((luz_no_sign + luz_sign) >= (len(codes)))

        write_csv(str(i), signs, signs_codes, output_path)
        write_csv(str(i), not_signs_names, not_signs_codes, not_code_file_path)

def search_by_levenshtein(input_path, wikidata_path, output_path, max_files, levenshtein):
    pass
def count_files(dir_path):
    count = 0
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return count

def main(input_path: str, wikidata_path:str, output_path: str, levenshtein:int):
    if os.path.isfile(wikidata_path) and wikidata_path.find(".csv") != -1 and output_path.find(".csv") != -1:# they are .csv files
        if os.path.isdir(input_path):
            if input_path[-1] != "/":
                input_path += "/"
            max_files = count_files(input_path)
            if levenshtein is not None:
                search_by_levenshtein(input_path, wikidata_path, output_path, max_files, levenshtein)
            else:
                search_codes(input_path, wikidata_path, output_path, max_files)
        else:
            print("The first path must be a directory path.")
    else:
        print("The last two files must be csv files.")


if __name__ == '__main__':
    # Example usage of the main function
    if len(sys.argv) != 4 and len(sys.argv) != 6:
        print("Usage: {} (--l THRESHOLD) input_source wikidata_path output_source ".format(sys.argv[0]))
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("arg1", type=str, help="input source")
        parser.add_argument("arg2", type=str, help="wikidata source")
        parser.add_argument("arg3", type=str, help="output source")
        parser.add_argument("--l", type=int, help="Calculate de levenshtein distance between the"
                        "input and output with a threshold", )
        args = parser.parse_args()
        main(args.arg1, args.arg2, args.arg3, args.l)

