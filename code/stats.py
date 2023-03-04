import csv

#define variables
max_cases = 791
ans_kop = 5
gaixotasun_kop_es, gaixotasun_kop_es_NO_umls, gaixotasun_kop_en = 0, 0, 0
sintoma_kop_es, sintoma_kop_es_NO_umls, sintoma_kop_en = 0, 0, 0
gaixSin_kop_es, gaixSin_kop_es_NO_umls = 0, 0
empty_en, empty_es = [], []

gaix_pos = 1
sin_pos = 3
gaiSin_pos = 5
gaix_pos_noUMLS = 1
sin_pos_noUMLS = 2
gaiSin_pos_noUMLS = 3

#COMPARE QUESTIONS IN ENGLISH AND SPANISH
csv_path_es = "./data/questions/QUEST_clinical_caseMIR.csv"
csv_path_en = "./data/questions/QUEST_clinical_caseMIR_english.csv"

# open the data csv file
mycsv_es = csv.reader(open(csv_path_es)) #open
mycsv_en = csv.reader(open(csv_path_en)) #open

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

#####################################################################################

#COMPARE ANSWERS IN ENGLISH AND SPANISH
csv_path_es_folder_umls = "./data/answers/ANS_es_UMLS/"
csv_path_es_folder_no_umls = "./data/answers/ANS_es_NO_UMLS/"
csv_path_en_folder = "./data/answers/ANS_en/"
file_name_es = "_ANS_clinical_caseMIR.csv"
file_name_en = "_ANS_clinical_caseMIR_english.csv"

gaixotasun_kop_es, gaixotasun_kop_es_NO_umls, gaixotasun_kop_en = 0, 0, 0
sintoma_kop_es, sintoma_kop_es_NO_umls, sintoma_kop_en = 0, 0, 0
gaixSin_kop_es, gaixSin_kop_es_NO_umls = 0, 0


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

