import csv

#COMPARE QUESTIONS IN ENGLISH AND SPANISH
csv_path_es = "./data/QUEST_clinical_caseMIR.csv"
csv_path_en = "./data/QUEST_clinical_caseMIR_english.csv"

#define variables
max_cases = 791
gaixotasun_kop_es, gaixotasun_kop_en = 0, 0
sintoma_kop_es, sintoma_kop_en = 0, 0
gaixSin_kop_es = 0
gaix_pos = 1
sin_pos = 3
gaiSin_pos = 5

# open the data csv file
mycsv_es = csv.reader(open(csv_path_es)) #open
mycsv_en = csv.reader(open(csv_path_en)) #open

for line_es in mycsv_es:
    gaixotasun_kop_es += len(line_es[gaix_pos])
    sintoma_kop_es += len(line_es[sin_pos])
    gaixSin_kop_es += len(line_es[gaiSin_pos])

for line_en in mycsv_en:
    gaixotasun_kop_en += len(line_en[gaix_pos])
    sintoma_kop_en += len(line_en[sin_pos])

print("Number of diseases in spanish: " + str(gaixotasun_kop_es))
print("Number of diseases in english: " + str(gaixotasun_kop_en))
print("Number of signs in spanish: " + str(sintoma_kop_es))
print("Number of signs in english: " + str(sintoma_kop_en))
print("Number of signs oR diseases in spanish: " + str(gaixSin_kop_es))

