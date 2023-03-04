import csv
import os.path
import sys
import argparse
import numpy as np

#define variables
ans_kop = 5
gaix_pos = 1
sin_pos = 3
gaiSin_pos = 5
gaix_pos_noUMLS = 1
sin_pos_noUMLS = 2
gaiSin_pos_noUMLS = 3

def createFile(path):
    mydirname = './' + path
    if not os.path.exists(mydirname):
        os.makedirs(os.path.dirname(mydirname), exist_ok=True)

def unique(list1):
    x = np.array(list1)
    return np.unique(x)
def remove_(str):
    elem = str.split("_")
    return elem[0]
def convert_2_correct_format(lista):
    return_lista = []
    for l in lista.split(","):
        if l.find("#") != -1:  # has #
            for elem in l.split("#"):
                return_lista.append(remove_(elem))
        elif l.find(" ") != -1:  # has space
            for elem in unique(list(l.split(" "))):
                return_lista.append(remove_(elem))
        else:
            return_lista.append(remove_(l))
    return  return_lista
def compareUMLSlist(lista1, lista2, listaBAI, listaEZ):
    for elem in lista1:
        if elem in lista2:
            listaBAI.append(elem)
        else:
            listaEZ.append(elem)
    return listaBAI, listaEZ

def writeQuest(cont, gaixotasuna, sintoma, gaixSin, writer, mycsv):
    cont1 = 0
    gaixotasunakBAI, gaixotasunakEZ, sintomaBAI, sintomaEZ, gaixSinBAI, gaixSinEZ = [], [], [], [], [], []
    for line in mycsv:
        if cont1 == cont:
            gaixotasuna1 = line[gaix_pos+1] #get the code
            gaixotasunakBAI, gaixotasunakEZ = compareUMLSlist(gaixotasuna, gaixotasuna1.split(","), gaixotasunakBAI, gaixotasunakEZ)
            sintoma1 = line[sin_pos+1] #get the code
            sintomaBAI, sintomaEZ = compareUMLSlist(sintoma, sintoma1.split(","), sintomaBAI, sintomaEZ)
            gaixSin1 = line[gaiSin_pos+1] #get the code
            gaixSinBAI, gaixSinEZ = compareUMLSlist(gaixSin, gaixSin1.split(","), gaixSinBAI, gaixSinEZ)
            row = [str(cont), ",".join(gaixotasunakBAI), ",".join(gaixotasunakEZ), ",".join(sintomaBAI), ",".join(sintomaEZ),
               ",".join(gaixSinBAI), ",".join(gaixSinEZ)]
            writer.writerow(row)
    return writer
def compareAndWriteQuest(path1, parth2, output_path):
    mycsv1 = csv.reader(open(path1))  # open
    mycsv2 = csv.reader(open(parth2))  # open
    myFile = open(output_path, 'w')
    writer = csv.writer(myFile)
    first_line = ["KasuZbkia", "GaixotasunakBAI", "GaixotasunakEZ", "SintomaBAI", "SintomaEZ", "GaixSinBAI", "GaixSinEZ"]
    writer.writerow(first_line)

    first = True
    cont = 0
    for line in mycsv1:
        if first:
            first = False
        else:
            gaixotasuna_aux = line[gaix_pos+1] #get the code
            gaixotasuna = convert_2_correct_format(gaixotasuna_aux)

            sintoma_aux = line[sin_pos+1] #get the code
            sintoma = convert_2_correct_format(sintoma_aux)

            gaixSin_aux = line[gaiSin_pos+1] #get the code
            gaixSin = convert_2_correct_format(gaixSin_aux)

            writer = writeQuest(cont, gaixotasuna, sintoma, gaixSin, writer, mycsv2)
        cont += 1

def compareQuest(csv_path_es, csv_path_en, equals_arg = None):
    #COMPARE QUESTIONS IN ENGLISH AND SPANISH
    gaixotasun_kop_es, gaixotasun_kop_es_NO_umls, gaixotasun_kop_en = 0, 0, 0
    sintoma_kop_es, sintoma_kop_es_NO_umls, sintoma_kop_en = 0, 0, 0
    gaixSin_kop_es, gaixSin_kop_es_NO_umls = 0, 0

    # open the data csv file
    mycsv_es = csv.reader(open(csv_path_es)) #open
    mycsv_en = csv.reader(open(csv_path_en)) #open

    if equals_arg:
        output_path = "./compare_quest.csv"
        createFile(output_path)
        compareAndWriteQuest(csv_path_es, csv_path_en, output_path)

    first = True
    for line_es in mycsv_es:
        if first:
            first = False
        else:
            gaixotasun_kop_es += len(line_es[gaix_pos])
            sintoma_kop_es += len(line_es[sin_pos])
            gaixSin_kop_es += len(line_es[gaiSin_pos])

    first = True
    for line_en in mycsv_en:
        if first:
            first = False
        else:
            gaixotasun_kop_en += len(line_en[gaix_pos])
            sintoma_kop_en += len(line_en[sin_pos])

    print("Number of diseases in spanish: " + str(gaixotasun_kop_es))
    print("Number of diseases in english: " + str(gaixotasun_kop_en))
    print("Number of signs in spanish: " + str(sintoma_kop_es))
    print("Number of signs in english: " + str(sintoma_kop_en))
    print("Number of signs or diseases in spanish: " + str(gaixSin_kop_es) +"\n")
def compareAns(csv_path_en_folder, csv_path_es_folder_umls, csv_path_es_folder_no_umls, max_cases):
    #COMPARE ANSWERS IN ENGLISH AND SPANISH
    file_name_es = "_ANS_clinical_caseMIR.csv"
    file_name_en = "_ANS_clinical_caseMIR_english.csv"

    gaixotasun_kop_es, gaixotasun_kop_es_NO_umls, gaixotasun_kop_en = 0, 0, 0
    sintoma_kop_es, sintoma_kop_es_NO_umls, sintoma_kop_en = 0, 0, 0
    gaixSin_kop_es, gaixSin_kop_es_NO_umls = 0 , 0
    empty_en, empty_es = [], []

    for i in range(max_cases):#iterate cases
        aldatu = False
        first = True
        # open the data csv file
        mycsv_es_umls = csv.reader(open(csv_path_es_folder_umls + str(i) + file_name_es)) #open
        mycsv_es_no_umls = csv.reader(open(csv_path_es_folder_no_umls + str(i) + file_name_es))  # open
        try:
            mycsv_en = csv.reader(open(csv_path_en_folder + str(i) + file_name_en)) #open

            for line_en in mycsv_en:
                if first:
                    first = False
                else:
                    gaixotasun_kop_en += len(line_en[gaix_pos])
                    sintoma_kop_en += len(line_en[sin_pos])

                    if len(line_en[gaix_pos]) != 0 or len(line_en[sin_pos]) != 0:
                        aldatu = True

            if not aldatu:
                empty_en.append(str(i))
            aldatu = False

        except:
            pass

        first = True
        for line_es_umls in mycsv_es_umls:
            if first:
                first = False
            else:
                gaixotasun_kop_es += len(line_es_umls[gaix_pos])
                sintoma_kop_es += len(line_es_umls[sin_pos])
                gaixSin_kop_es += len(line_es_umls[gaiSin_pos])

                if len(line_es_umls[gaix_pos]) != 0 or len(line_es_umls[sin_pos]) != 0 or len(line_es_umls[gaiSin_pos]) != 0:
                    aldatu = True

        first = True
        for line_es_no_umls in mycsv_es_no_umls:
            if first:
                first = False
            else:
                gaixotasun_kop_es_NO_umls += len(line_es_no_umls[gaix_pos_noUMLS])
                sintoma_kop_es_NO_umls += len(line_es_no_umls[sin_pos_noUMLS])
                gaixSin_kop_es_NO_umls += len(line_es_no_umls[gaiSin_pos_noUMLS])

                if len(line_es_no_umls[gaix_pos_noUMLS]) != 0 or len(line_es_no_umls[sin_pos_noUMLS]) != 0 or len(line_es_no_umls[gaiSin_pos_noUMLS]) != 0:
                    aldatu = True

        if not aldatu:
            empty_es.append(str(i))


    print("Number of diseases in spanish with UMLS: " + str(gaixotasun_kop_es))
    print("Number of diseases in spanish with NO UMLS: " + str(gaixotasun_kop_es_NO_umls))
    print("Number of diseases in english: " + str(gaixotasun_kop_en))
    print("Number of signs in spanish with UMLS: " + str(sintoma_kop_es))
    print("Number of signs in spanish with  NO UMLS: " + str(sintoma_kop_es_NO_umls))
    print("Number of signs in english: " + str(sintoma_kop_en))
    print("Number of signs or diseases in spanish with UMLS: " + str(gaixSin_kop_es))
    print("Number of signs or diseases in spanish with NO UMLS: " + str(gaixSin_kop_es_NO_umls))
    print("Empty cases in spanish: " + str(len(empty_es)) + ": " + ",".join(empty_es))
    print("\nEmpty cases in english: " + str(len(empty_en)) + ": "  + ",".join(empty_en))
def count_files(dir_path):
    count = 0
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return count
def main(input_path1: str, input_path2: str, input_path3:str, mode:str, equals_arg=None):
    if mode == "Q" or mode == "q":
        if os.path.isfile(input_path1) and os.path.isfile(input_path2) and input_path1.find(".csv") != -1 and input_path2.find(".csv") != -1: #if it is question mode and they are .csv files
            compareQuest(input_path1, input_path2, equals_arg)
        else:
            print("If it is question mode, you have to enter the path of two csv files.")
    elif mode == "A" or mode == "a":
        max_files1 = count_files(input_path1)
        max_files2 = count_files(input_path2)
        max_files3 = count_files(input_path3)

        if max_files1 > max_files2:
            max_files = max_files1
        else:
            if max_files1 > max_files3:
                max_files = max_files1
            elif max_files2 > max_files3:
                max_files = max_files2
            else:
                max_files = max_files3

        if os.path.isdir(input_path1) and os.path.isdir(input_path2) and os.path.isdir(input_path3): # if it is answer mode and they are directories
            if input_path1[-1] != "/":
                input_path1 += "/"
            if input_path2[-1] != "/":
                input_path2 += "/"
            if input_path3[-1] != "/":
                input_path3 += "/"
            compareAns(input_path1, input_path2, input_path3, max_files)#,equals_arg)
        else:
            print("If it is answer mode, you have to enter the path of three directories.")
    else:
        print("The option is not correct. Please select (Q)uestion or (A)nswer. \n")

if __name__ == '__main__':
    # Example usage of the main function
    if len(sys.argv) != 5 and len(sys.argv) != 6:
        print("Usage: {} input_source1 input_source2 input_source3 (-1 when it is question mode) mode (--equals_arg)".format(sys.argv[0]))
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("arg1", type=str, help="input source 1")
        parser.add_argument("arg2", type=str, help="input source 2")
        parser.add_argument("arg3", type=str, help="input source 3 ")
        parser.add_argument("arg4", type=str, help="mode")
        parser.add_argument("--equals_arg", help="Get all the coincidences for each case", action="store_true")
        args = parser.parse_args()
        main(args.arg1, args.arg2, args.arg3, args.arg4, args.equals_arg)
