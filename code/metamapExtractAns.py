# Load MetaMap
from pymetamap import MetaMap

# Import os to make system calls
import os

# For pausing
from time import sleep
import csv
import pandas as pd

def createFile(path):
    mydirname = './' + path
    if not os.path.exists(mydirname):
        os.makedirs(os.path.dirname(mydirname), exist_ok=True)

def get_keys_from_mm(concept, klist):
    conc_dict = concept._asdict()
    conc_list = [conc_dict.get(kk) for kk in klist]
    return (tuple(conc_list))

def get_diseases_and_signs(cons):
    gaixotasunak, gaixotasunakUMLS, sintomak, sintomakUMLS = [], [], [], []
    keys_of_interest = ['preferred_name', 'cui', 'semtypes']
    cols = [get_keys_from_mm(cc, keys_of_interest) for cc in cons]
    for c in cols:
        if c[2] != None:
            if 'dsyn' in c[2]:  # it's a disease
                gaixotasunak.append(c[0])
                gaixotasunakUMLS.append(c[1])
            elif 'sosy' in c[2]:  # it's a sign
                sintomak.append(c[0])
                sintomakUMLS.append(c[1])
    return gaixotasunak, gaixotasunakUMLS, sintomak, sintomakUMLS

data_csv_path = "./data/00-CasiMedicos_clinical_cases_translated_2_english.csv"
csv_path_folder = "./data/ANS_en/"
csv_path_file = "ANS_clinical_caseMIR_english.csv"

#define variables
first = True
SnoMot_pos = 5
SnoKod_pos = 4
Deepent_pos = 9
name_pos = 1

question_pos = 5
answer_pos = 12
num_answer = 5


# Setup UMLS Server
metamap_base_dir = './metamap/public_mm/'
metamap_base_dir_abs = '/home/paula/Escritorio/GrAL/metamap/public_mm/'
metamap_bin_dir = 'bin/metamap20'
metamap_pos_server_dir = 'bin/skrmedpostctl'
metamap_wsd_server_dir = 'bin/wsdserverctl'

# Start servers
os.system(metamap_base_dir + metamap_pos_server_dir + ' start') # Part of speech tagger
os.system(metamap_base_dir + metamap_wsd_server_dir + ' start') # Word sense disambiguation

# Sleep a bit to give time for these servers to start up
sleep(60)

# open the data csv file
mycsv = csv.reader(open(data_csv_path)) #open

metam = MetaMap.get_instance(metamap_base_dir_abs + metamap_bin_dir)

i = 0
for line in mycsv:#iterate through the csv
    if first:
        first = False
    else:
        # create a .csv to save the diseases and findings
        createFile(csv_path_folder + str(i)+"_"+ csv_path_file)
        myFile = open(csv_path_folder + str(i)+ "_"+ csv_path_file, 'w')
        writer = csv.writer(myFile)
        first_line = ["kasuZbkia", "gaixotasunak", "gaixotasunUMLS", "sintomak", "sintomenUMLS"]
        writer.writerow(first_line)

        # get all the posible answers
        for j in range(num_answer):
            answer = line[answer_pos + j]
            cons_ans, errs_ans = metam.extract_concepts([answer],  # input
                                                word_sense_disambiguation=True,
                                                restrict_to_sts=['sosy', 'dsyn'],# signs and symptoms, Disease or Syndrome
                                                composite_phrase=1,  # for memory issues
                                                prune=30)
            gaixotasunak, gaixotasunakUMLS, sintomak, sintomakUMLS = get_diseases_and_signs(cons_ans)
            # write in the csv
            row = [str(j), ",".join(gaixotasunak), ",".join(gaixotasunakUMLS), ",".join(sintomak),
                   ",".join(sintomakUMLS)]
            writer.writerow(row)
        i += 1
