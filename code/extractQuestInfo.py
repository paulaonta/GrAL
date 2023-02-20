import os
import csv


def createFile(path):
    mydirname = './' + path
    if not os.path.exists(mydirname):
        os.makedirs(os.path.dirname(mydirname), exist_ok=True)


# define paths
path = "./output_unimer/"
question_file_partial_name = "_QUEST_clinical_caseMIR.conll"
csv_path = "./data/QUEST_clinical_caseMIR.csv"

#define variables
max_files = 790
SnoMot_pos = 5
SnoKod_pos = 4
Deepent_pos = 9
name_pos = 1

# create a .csv to save the diseases and findings
createFile(csv_path)
myFile = open(csv_path, 'w')
writer = csv.writer(myFile)
first_line = ["kasuZbkia", "gaixotasunak", "gaixotasunUMLS", "sintomak", "sintomenUMLS", "gaixSin", "gaixSinUMLS"]
writer.writerow(first_line)

for i in range(max_files): #iterate all the cases
    my_conll_file_location = path + str(i) + question_file_partial_name
    conll_file = open(my_conll_file_location, "r")
    conll_lines = conll_file.readlines()

    gaixotasunak, gaixotasunakUMLS, sintomak, sintomakUMLS, gaixSin, gaixSinUMLS = [], [], [], [], [], []
    isPartS, isPartG = False, False
    for line in conll_lines:
        elements = line.split("\t")
        findSno = False
        if len(elements) > 1: #not iterate  empty rows
            if elements[SnoMot_pos].find("hallazgo") != -1:
                if not isPartS:
                    sintomak.append(elements[name_pos])
                    sintomakUMLS.append(elements[SnoKod_pos])

                if elements[SnoMot_pos][-2] == "_":
                    if isPartS:
                        sintomak[-1] += " " + elements[name_pos]
                        sintomakUMLS[-1] = sintomakUMLS[-1].split("_")[0] + " " + elements[SnoKod_pos].split("_")[0]
                    isPartS = True
                else:
                    isPartS = False
                isPartG = False
            if elements[SnoMot_pos].find("trastorno") != -1 or elements[SnoMot_pos].find("anomalía_morfológica") != -1:
                if not isPartG:
                    gaixotasunak.append(elements[name_pos])
                    gaixotasunakUMLS.append(elements[SnoKod_pos])

                if elements[SnoMot_pos][-2] == "_":
                    if isPartG:
                        gaixotasunak[-1] += " " + elements[name_pos]
                        gaixotasunakUMLS[-1] = gaixotasunakUMLS[-1].split("_")[0] + " " + elements[SnoKod_pos].split("_")[0]
                    isPartG = True
                else:
                    isPartG = False
                isPartS = False
            if not findSno and elements[Deepent_pos].find("Grp_Enfermedad") != -1 or elements[Deepent_pos].find("Alergia") != -1:
                # hemen sartzen baldin bada, bada SnoMot ez daukalako edo ez dagoelako def. artean, beraz ezin da jakin
                # sintoma edo gaixotasuna den
                gaixSin.append(elements[name_pos])
                gaixSinUMLS.append(elements[SnoKod_pos])
    #write in the csv
    row = [str(i), ",".join(gaixotasunak), ",".join(gaixotasunakUMLS), ",".join(sintomak), ",".join(sintomakUMLS),
           ",".join(gaixSin), ",".join(gaixSinUMLS)]
    writer.writerow(row)
    conll_file.close()




