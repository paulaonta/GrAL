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

gaixBAI_pos = 1
gaixEZ_pos = 2
sinBAI_pos = 3
sinEZ_pos = 4
gaixSinBAI_pos = 5
gaixSinEZ_pos = 6

file_name = "_ANS_clinical_caseMIR.csv"

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
            for elem in unique(l.split("#")):
                return_lista.append(remove_(elem))
        elif l.find(" ") != -1:  # has space
            for elem in unique(list(l.split(" "))):
                return_lista.append(remove_(elem))
        else:
            return_lista.append(remove_(l))
    return  unique(return_lista)

def compareUMLSlist(lista1, lista2, listaBAI, listaEZ): #lista1:en, lista2:es
    
    for elem in lista1:
        if elem in lista2 and len(elem) > 1 and elem not in listaBAI: #UMLS kodeak 1ko luzera baino gehiago izango dute
            listaBAI.append(elem)
        elif len(elem) > 1 and elem not in listaEZ:
            listaEZ.append(elem)
    '''
    for elem in lista2:
        if elem in lista1 and elem not in listaBAI and len(elem) > 1:
            listaBAI.append(elem)
        elif not elem in lista1  and elem not in listaEZ and len(elem) > 1:
            listaEZ.append(elem)
    '''
    return listaBAI, listaEZ

def write(cont, gaixotasuna, sintoma, gaixSin, writer, path):
    mycsv = csv.reader(open(path))  # open
    cont1 = -1
    gaixotasunakBAI, gaixotasunakEZ, sintomaBAI, sintomaEZ, gaixSinBAI, gaixSinEZ = [], [], [], [], [], []
    for line in mycsv:
        if cont1 == cont:
            gaixotasuna1 = line[gaix_pos+1] #get the code
            gaixotasunakBAI, gaixotasunakEZ = compareUMLSlist(gaixotasuna, gaixotasuna1.split(","), gaixotasunakBAI, gaixotasunakEZ)

            sintoma1 = line[sin_pos+1] #get the code
            sintomaBAI, sintomaEZ = compareUMLSlist(sintoma, sintoma1.split(","), sintomaBAI, sintomaEZ)

            if sintoma1 != None and gaixotasuna1 != None:
                gaixSinBAI, gaixSinEZ = compareUMLSlist(gaixSin, list(gaixotasuna1.split(",")) + list(sintoma1.split(",")), gaixSinBAI, gaixSinEZ)
            elif gaixotasuna1 != None:
                gaixSinBAI, gaixSinEZ = compareUMLSlist(gaixSin, gaixotasuna1.split(","), gaixSinBAI, gaixSinEZ)
            elif sintoma1 != None:
                gaixSinBAI, gaixSinEZ = compareUMLSlist(gaixSin, sintoma1.split(","), gaixSinBAI, gaixSinEZ)

            row = [str(cont), ",".join(gaixotasunakBAI), ",".join(gaixotasunakEZ), ",".join(sintomaBAI), ",".join(sintomaEZ),
               ",".join(gaixSinBAI), ",".join(gaixSinEZ)]
            writer.writerow(row)
            break
        cont1 += 1

def compareAndWriteQuest(path1, path2, output_path): #path1:es, path2:en
    mycsv1 = csv.reader(open(path1))  # open
    myFile = open(output_path, 'w')
    writer = csv.writer(myFile)
    first_line = ["KasuZbkia", "GaixotasunakBAI", "GaixotasunakEZ", "SintomaBAI", "SintomaEZ", "GaixSinBAI", "GaixSinEZ"]
    writer.writerow(first_line)

    first = True
    cont = -1
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
            write(cont, gaixotasuna, sintoma, gaixSin, writer, path2)
        cont += 1

def count_compare_file(path, gaixotasunakBAI, gaixotasunakEZ, sintomaBAI, sintomaEZ, gaixSinBAI, gaixSinEZ):
    mycsv_compare = csv.reader(open(path)) # open
    first = True
    for line in mycsv_compare:
        if first:
            first = False
        else:
            if len(line[gaixBAI_pos]) > 0:
                gaixotasunakBAI += len(line[gaixBAI_pos].split(","))
            if len(line[gaixEZ_pos]) > 0:
                gaixotasunakEZ += len(line[gaixEZ_pos].split(","))
            if len(line[sinBAI_pos]) > 0:
                sintomaBAI += len(line[sinBAI_pos].split(","))
            if len(line[sinEZ_pos]) > 0:
                sintomaEZ += len(line[sinEZ_pos].split(","))
            if len(line[gaixSinBAI_pos]) > 0:
                gaixSinBAI += len(line[gaixSinBAI_pos].split(","))
            if len(line[gaixSinEZ_pos]) > 0:
                gaixSinEZ += len(line[gaixSinEZ_pos].split(","))
    return gaixotasunakBAI, gaixotasunakEZ, sintomaBAI, sintomaEZ, gaixSinBAI, gaixSinEZ

def compareQuest(csv_path_en, csv_path_es, equals_arg = None):
    #COMPARE QUESTIONS IN ENGLISH AND SPANISH
    gaixotasun_kop_es, gaixotasun_kop_en, UMLSgaix_es, UMLSgaix_en = 0, 0, 0, 0
    sintoma_kop_es, sintoma_kop_en, UMLSsin_es, UMLSsin_en = 0, 0, 0, 0
    gaixSin_kop_es, UMLSgaixSin_es = 0, 0

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
            if len(line_es[gaix_pos]) > 0:
                gaixotasun_kop_es += len(line_es[gaix_pos].split(","))
                UMLSgaix_es += len(convert_2_correct_format(line_es[gaix_pos+1]))
            if len(line_es[sin_pos]) > 0:
                sintoma_kop_es += len(line_es[sin_pos].split(","))
                UMLSsin_es += len(convert_2_correct_format(line_es[sin_pos + 1]))
            if len(line_es[gaiSin_pos]) > 0:
                gaixSin_kop_es += len(line_es[gaiSin_pos].split(","))
                UMLSgaixSin_es += len(convert_2_correct_format(line_es[gaiSin_pos + 1]))

    first = True
    for line_en in mycsv_en:
        if first:
            first = False
        else:
            if len(line_en[gaix_pos]) > 0:
                gaixotasun_kop_en += len(line_en[gaix_pos].split(","))
                UMLSgaix_en += len(convert_2_correct_format(line_en[gaix_pos + 1]))
            if len(line_en[sin_pos]) > 0:
                sintoma_kop_en += len(line_en[sin_pos].split(","))
                UMLSsin_en += len(convert_2_correct_format(line_en[sin_pos + 1]))

    print("Number of diseases in spanish: " + str(gaixotasun_kop_es))
    print("Number of UMLS code of diseases in spanish: " + str(UMLSgaix_es))
    print("Number of diseases in english: " + str(gaixotasun_kop_en))
    print("Number of UMLS code of diseases in english: " + str(UMLSgaix_en))
    print("Number of signs in spanish: " + str(sintoma_kop_es))
    print("Number of UMLS code of signs in spanish: " + str(UMLSsin_es))
    print("Number of signs in english: " + str(sintoma_kop_en))
    print("Number of UMLS code of signs in english: " + str(UMLSsin_en))
    print("Number of signs or diseases in spanish: " + str(gaixSin_kop_es))
    print("Number of UMLS codes of signs or diseases in spanish: " + str(UMLSgaixSin_es) +"\n")

    ####################################################
    if equals_arg:
        gaixotasunakBAI, gaixotasunakEZ, sintomaBAI, sintomaEZ, gaixSinBAI, gaixSinEZ = 0, 0, 0, 0, 0, 0
        gaixotasunakBAI, gaixotasunakEZ, sintomaBAI, sintomaEZ, gaixSinBAI, gaixSinEZ = count_compare_file(
            output_path, gaixotasunakBAI, gaixotasunakEZ, sintomaBAI, sintomaEZ, gaixSinBAI, gaixSinEZ)

        print("Number of common diseases: " +str(gaixotasunakBAI))
        print("Number of NOT common diseases: " + str(gaixotasunakEZ))
        print("Number of common signs: " +str(sintomaBAI))
        print("Number of NOT common signs: " + str(sintomaEZ))
        print("NUmber of common diseases or signs: " +str(gaixSinBAI))
        print("Number of NOT common diseases or signs: " + str(gaixSinEZ))

def compareAndWriteAns(path1, path2, output_path, output_file_name, max_cases):
    for i in range(max_cases):  # iterate cases
        # open the data csv file
        mycsv_es_umls = csv.reader(open(path2 + str(i) + file_name))  # open

        myFile = open(output_path + str(i) + output_file_name, 'w')
        writer = csv.writer(myFile)
        first_line = ["ErantzunZbkia", "GaixotasunakBAI", "GaixotasunakEZ", "SintomaBAI", "SintomaEZ", "GaixSinBAI","GaixSinEZ"]
        writer.writerow(first_line)

        first = True
        cont = -1
        for line in mycsv_es_umls:
            if first:
                first = False
            else:
                gaixotasuna_aux = line[gaix_pos + 1]  # get the code
                gaixotasuna = convert_2_correct_format(gaixotasuna_aux)

                sintoma_aux = line[sin_pos + 1]  # get the code
                sintoma = convert_2_correct_format(sintoma_aux)

                gaixSin_aux = line[gaiSin_pos + 1]  # get the code
                gaixSin = convert_2_correct_format(gaixSin_aux)
                write(cont, gaixotasuna, sintoma, gaixSin, writer, path1 + str(i) + file_name)
            cont += 1

def compareAns( csv_path_en_folder, csv_path_es_folder_umls, csv_path_es_folder_no_umls, max_cases, equals_arg = None):
    #COMPARE ANSWERS IN ENGLISH AND SPANISH
    gaixotasun_kop_es, gaixotasun_kop_es_NO_umls, gaixotasun_kop_en, UMLSgaix_es, UMLSgaix_en = 0, 0, 0, 0, 0
    sintoma_kop_es, sintoma_kop_es_NO_umls, sintoma_kop_en, UMLSsin_es, UMLSsin_en = 0, 0, 0, 0, 0
    gaixSin_kop_es, gaixSin_kop_es_NO_umls, UMLSgaixSin_es = 0, 0, 0
    empty_en, empty_es = [], []

    if equals_arg:
        output_path = "./COMPARE_ANS/"
        output_file_name = "_ANS_compare.csv"
        createFile(output_path)
        compareAndWriteAns(csv_path_en_folder, csv_path_es_folder_umls, output_path, output_file_name, max_cases)

    for i in range(max_cases):#iterate cases
        aldatu = False
        first = True
        # open the data csv file
        mycsv_es_umls = csv.reader(open(csv_path_es_folder_umls + str(i) + file_name)) #open
        mycsv_es_no_umls = csv.reader(open(csv_path_es_folder_no_umls + str(i) + file_name))  # open
        try:
            mycsv_en = csv.reader(open(csv_path_en_folder + str(i) + file_name)) #open

            for line_en in mycsv_en:
                if first:
                    first = False
                else:
                    if len(line_en[gaix_pos]) > 0:
                        gaixotasun_kop_en += len(line_en[gaix_pos].split(","))
                        UMLSgaix_en += len(convert_2_correct_format(line_en[gaix_pos + 1]))
                    if len(line_en[sin_pos]) > 0:
                        sintoma_kop_en += len(line_en[sin_pos].split(","))
                        UMLSsin_en += len(convert_2_correct_format(line_en[sin_pos + 1]))

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
                if len(line_es_umls[gaix_pos]) > 0:
                    gaixotasun_kop_es += len(line_es_umls[gaix_pos].split(","))
                    UMLSgaix_es += len(convert_2_correct_format(line_es_umls[gaix_pos + 1]))
                if len(line_es_umls[sin_pos]) > 0:
                    sintoma_kop_es += len(line_es_umls[sin_pos].split(","))
                    UMLSsin_es += len(convert_2_correct_format(line_es_umls[sin_pos + 1]))
                if len(line_es_umls[gaiSin_pos]) > 0:
                    gaixSin_kop_es += len(line_es_umls[gaiSin_pos].split(","))
                    UMLSgaixSin_es += len(convert_2_correct_format(line_es_umls[gaiSin_pos + 1]))

                if len(line_es_umls[gaix_pos]) != 0 or len(line_es_umls[sin_pos]) != 0 or len(line_es_umls[gaiSin_pos]) != 0:
                    aldatu = True

        first = True
        for line_es_no_umls in mycsv_es_no_umls:
            if first:
                first = False
            else:
                if len(line_es_no_umls[gaix_pos_noUMLS]) > 0:
                    gaixotasun_kop_es_NO_umls += len(line_es_no_umls[gaix_pos_noUMLS].split(","))
                if len(line_es_no_umls[sin_pos_noUMLS]) > 0:
                    sintoma_kop_es_NO_umls += len(line_es_no_umls[sin_pos_noUMLS].split(","))
                if len(line_es_no_umls[gaiSin_pos_noUMLS]) > 0:
                    gaixSin_kop_es_NO_umls += len(line_es_no_umls[gaiSin_pos_noUMLS].split(","))

                if len(line_es_no_umls[gaix_pos_noUMLS]) != 0 or len(line_es_no_umls[sin_pos_noUMLS]) != 0 or len(line_es_no_umls[gaiSin_pos_noUMLS]) != 0:
                    aldatu = True

        if not aldatu:
            empty_es.append(str(i))


    print("Number of diseases in spanish with UMLS: " + str(gaixotasun_kop_es))
    print("Number of UMLS code of diseases in spanish: " + str(UMLSgaix_es))
    print("Number of diseases in spanish with NO UMLS: " + str(gaixotasun_kop_es_NO_umls))
    print("Number of diseases in english: " + str(gaixotasun_kop_en))
    print("Number of UMLS code of diseases in english: " + str(UMLSgaix_en))
    print("Number of signs in spanish with UMLS: " + str(sintoma_kop_es))
    print("Number of UMLS code of signs in spanish: " + str(UMLSsin_es))
    print("Number of signs in spanish with  NO UMLS: " + str(sintoma_kop_es_NO_umls))
    print("Number of signs in english: " + str(sintoma_kop_en))
    print("Number of UMLS code of signs in english: " + str(UMLSsin_en))
    print("Number of signs or diseases in spanish with UMLS: " + str(gaixSin_kop_es))
    print("Number of UMLS codes of signs or diseases in spanish: " + str(UMLSgaixSin_es))
    print("Number of signs or diseases in spanish with NO UMLS: " + str(gaixSin_kop_es_NO_umls))
    print("\nEmpty cases in spanish: " + str(len(empty_es)) + ": " + ",".join(empty_es))
    print("\nEmpty cases in english: " + str(len(empty_en)) + ": "  + ",".join(empty_en))

    ####################################################
    if equals_arg:
        gaixotasunakBAI, gaixotasunakEZ, sintomaBAI, sintomaEZ, gaixSinBAI, gaixSinEZ = 0, 0, 0, 0, 0, 0
        for i in range(max_cases):  # iterate cases
            gaixotasunakBAI, gaixotasunakEZ, sintomaBAI, sintomaEZ, gaixSinBAI, gaixSinEZ = count_compare_file(
            output_path + str(i) + output_file_name ,gaixotasunakBAI, gaixotasunakEZ, sintomaBAI, sintomaEZ, gaixSinBAI, gaixSinEZ)
        print("\nNumber of common diseases: " + str(gaixotasunakBAI))
        print("Number of NOT common diseases: " + str(gaixotasunakEZ))
        print("Number of common signs: " + str(sintomaBAI))
        print("Number of NOT common signs: " + str(sintomaEZ))
        print("NUmber of common diseases or signs: " + str(gaixSinBAI))
        print("Number of NOT common diseases or signs: " + str(gaixSinEZ))

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
            compareAns(input_path1, input_path2, input_path3, max_files, equals_arg)
        else:
            print("If it is answer mode, you have to enter the path of three directories.")
    else:
        print("The option is not correct. Please select (Q)uestion or (A)nswer. \n")

if __name__ == '__main__':
    # Example usage of the main function
    if len(sys.argv) != 5 and len(sys.argv) != 6:
        print("Usage: {} input_sourceEN input_sourceES input_sourceES (-1 when it is question mode) mode (--equals_arg)".format(sys.argv[0]))
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("arg1", type=str, help="input source 1")
        parser.add_argument("arg2", type=str, help="input source 2")
        parser.add_argument("arg3", type=str, help="input source 3 ")
        parser.add_argument("arg4", type=str, help="mode")
        parser.add_argument("--equals_arg", help="Get all the coincidences for each case", action="store_true")
        args = parser.parse_args()
        main(args.arg1, args.arg2, args.arg3, args.arg4, args.equals_arg)
