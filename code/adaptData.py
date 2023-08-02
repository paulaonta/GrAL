import csv
import sys
import os
import pandas as pd
from sklearn.model_selection import train_test_split
import random

def createFile(path):
    mydirname = './' + path
    if not os.path.exists(mydirname):
        os.makedirs(os.path.dirname(mydirname), exist_ok=True)

question_pos = 5
ans_pos = 12
correct_ans_pos = 17
exp_pos = 6
subject_pos = 8
convert_subject = {
    "PEDIATRICS": "Pediatrics",
    "ENDOCRINOLOGY": "Medicine",
    "GYNECOLOGY AND OBSTETRICS": "Obstetrics and Gynecology (O&G)",
    "OBSTETRICS AND GYNECOLOGY": "Obstetrics and Gynecology (O&G)",
    "NEUROLOGY": "Medicine",
    "NEPHROLOGY": "Medicine",
    "TRAUMATOLOGY": "Medicine",
    "RHEUMATOLOGY": "Medicine",
    "HAEMATOLOGY": "Medicine",
    "DIGESTIVE SYSTEM": "Medicine",
    "OPHTHALMOLOGY": "Ophthalmology",
    "CARDIOLOGY AND VASCULAR SURGERY": "Surgery",
    "INFECTIOUS DISEASES": "Medicine",
    "DIGESTIVES": "Medicine",
    "PSYCHIATRY": "Psychiatry",
    "CARDIOLOGY": "Medicine",
    "GENERAL SURGERY": "Surgery",
    "PNEUMOLOGY": "Medicine",
    "HEMATOLOGY": "Medicine",
    "ANESTHESIOLOGY, CRITICAL CARE AND EMERGENCY MEDICINE": "Anesthesia",
    "ANESTHESIOLOGY, CRITICAL CARE AND EMERGENCIES": "Anesthesia",
    "ANESTHESIOLOGY AND CRITICAL CARE": "Anesthesia",
    "NEUROLOGY AND NEUROSURGERY": "Surgery",
    "DERMATOLOGY, VENEREOLOGY AND PLASTIC SURGERY": "Surgery",
    "CRITICAL CARE": "Preventive & Social Medicine (PSM)",
    "TRAUMATOLOGY AND ORTHOPAEDICS": "Orthopedics",
    "INFECTIOUS DISEASES AND MICROBIOLOGY": "Microbiology",
    "CRITICAL CARE AND EMERGENCY MEDICINE": "Preventive & Social Medicine (PSM)",
    "ORTHOPEDIC SURGERY AND TRAUMATOLOGY": "Surgery",
    "CARDIOLOGY AND CARDIOVASCULAR SURGERY": "Surgery",
    "PNEUMOLOGY AND THORACIC SURGERY": "Surgery",
    "ONCOLOGY": "Medicine",
    "DIGESTIVE": "Medicine",
    "DIGESTIVE TRACT": "Medicine",
    "DERMATOLOGY": "Skin",
    "INFECTIOUS": "Medicine",
    "OTORHINOLARYNGOLOGY AND MAXILLOFACIAL SURGERY": "Surgery",
    "OTOLARYNGOLOGY AND MAXILLOFACIAL SURGERY": "Surgery",
    "PATHOLOGICAL ANATOMY": "Anatomy",
    "SURGERY": "Surgery",
    "GENETICS AND IMMUNOLOGY": "Biochemistry",
    "OPHTHALMOLOGY (ECTOPIC)": "Ophthalmology",
    "ANAESTHESIOLOGY AND CRITICAL CARE": "Anesthesia",
    "OBSTETRICS AND GYNAECOLOGY": "Obstetrics and Gynecology (O&G)",
    "MEDICAL ONCOLOGY": "Medicine",
    "PHARMACOLOGY": "Pharmacology",
    "NEUROLOGY AND THORACIC SURGERY": "Surgery",
    "PULMONOLOGY AND THORACIC SURGERY": "Surgery",
    "UROLOGY": "Medicine",
    "NEUROSURGERY": "Surgery",
    "BIOSTATISTICS" : "Biochemistry",
    "PREVENTIVE MEDICINE": "Preventive & Social Medicine (PSM)",
    "ALLERGOLOGY": "Medicine",
    "GENETICS": "Biochemistry",
    "MICROBIOLOGY": "Biochemistry",
    "PRIMARY CARE" : "Preventive & Social Medicine (PSM)",
    "CRITICAL, PALLIATIVE AND EMERGENCY CARE": "Preventive & Social Medicine (PSM)",
    "INFECTOLOGY": "Biochemistry",
    "ONCOLOGY (ECTOPIC)": "Medicine",
    "PULMONOLOGY":"Medicine",
    "EPIDEMIOLOGY AND PREVENTIVE MEDICINE": "Preventive & Social Medicine (PSM)",
    "ANATOMY": "Anatomy",
    "TRAUMATOLOGY AND ORTHOPEDICS": "Orthopedics",
    "PALLIATIVE CARE": "Medicine",
    "PRIMARY CARE AND SOCIAL NETWORKS": "Preventive & Social Medicine (PSM)",
    "DERMATOLOGY AND PLASTIC SURGERY": "Surgery",
    "EPIDEMIOLOGY": "Biochemistry",
    "STATISTICS": "Biochemistry",
    "ANATOMIC PATHOLOGY": "Pathology",
    "PREVENTIVE MEDICINE AND EPIDEMIOLOGY": "Preventive & Social Medicine (PSM)",
    "CRITICAL CARE AND EMERGENCIES":"Preventive & Social Medicine (PSM)",
    "CRITICAL AND EMERGENCY CARE":"Preventive & Social Medicine (PSM)",
    "":""
}
cases_4_ans = [249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507]

random.seed(42)
def adapt(input_path, output_path):
    first_row = ["id","question","opa","opb","opc","opd","ope","cop","choice_type","exp","subject_name","topic_name"]
    myFile = open(output_path, 'w')
    writer = csv.writer(myFile)
    writer.writerow(first_row)

    # open the data csv file
    mycsv = csv.reader(open(input_path))  # open
    first = True
    cont = 0

    for line in mycsv:
        if first:
            first = False
        else:
            #if cont in cases_4_ans:
            row = [str(line[0])+"-"+str(line[1]), line[question_pos], line[ans_pos], line[ans_pos+1], line[ans_pos+2],
                       line[ans_pos+3], line[ans_pos+4], str(int(line[correct_ans_pos])-1), "single", line[exp_pos],
                       convert_subject[line[subject_pos]], ""]
            writer.writerow(row)
            cont += 1

    myFile.close()

    #split
    data = pd.read_csv(output_path, sep = ",")
    train_data, test_data = train_test_split(data, test_size=int(cont*0.2), train_size=cont-int(cont*0.2), random_state=42)
    train_data, dev_data = train_test_split(train_data, test_size=int(cont*0.2), train_size=cont -2*int(cont*0.2), random_state=42) #0.25 of train is the %20 of the all data
    train_data.to_csv('train_rm.csv', index=False)
    dev_data.to_csv('dev_rm.csv', index=False)
    test_data.to_csv('test_rm.csv', index=False)
    #train_data.to_csv('train_rm_ID.csv', index=False, columns = ["number_case"])
    #dev_data.to_csv('dev_rm_ID.csv', index=False, columns = ["number_case"])
    #test_data.to_csv('test_rm_ID.csv', index=False, columns = ["number_case"])

    #get ONLY the 4 answers cases
    files = ['train_rm.csv', 'dev_rm.csv', 'test_rm.csv']
    for file in files:
        file_path = "4_ans_only_" + file
        createFile(file_path)
        first_row = ["id", "question", "opa", "opb", "opc", "opd", "cop", "choice_type", "exp", "subject_name",
                     "topic_name"]
        myFile = open(file_path, 'w')
        writer = csv.writer(myFile)
        writer.writerow(first_row)

        mycsv = csv.reader(open(file))  # open
        first = True

        for line in mycsv:
            if first:
                first = False
            else:
                if len(line[6])==0: #it hasn't got a fifth answer
                    line.pop(6)
                    writer.writerow(line)

    # get the 4 answers cases + REMOVE fifth option when it's not the correct answer
    files = ['train_rm.csv', 'dev_rm.csv']
    for file in files:
        file_path = "4_5_ans_" + file
        createFile(file_path)
        first_row = ["id", "question", "opa", "opb", "opc", "opd", "cop", "choice_type", "exp", "subject_name",
                     "topic_name"]
        myFile = open(file_path, 'w')
        writer = csv.writer(myFile)
        writer.writerow(first_row)

        mycsv = csv.reader(open(file))  # open
        first = True

        for line in mycsv:
            if first:
                first = False
            else:
                # it hasn't got a fifth answer or it has a fifth answer and the fifth isn't the correct answer
                if len(line[6])==0 or (len(line[6])!=0 and int(line[7]) != 4):
                    line.pop(6)
                    writer.writerow(line)

    # get the 4 answers cases + REMOVE fifth option at random
    files = ['test_rm.csv']
    for file in files:
        file_path = "4_5_ans_" + file
        createFile(file_path)
        first_row = ["id", "question", "opa", "opb", "opc", "opd", "cop", "choice_type", "exp", "subject_name",
                     "topic_name"]
        myFile = open(file_path, 'w')
        writer = csv.writer(myFile)
        writer.writerow(first_row)

        not_file_path = "incorrect_ans.csv"
        createFile(not_file_path)
        rows = [first_row]

        mycsv = csv.reader(open(file))  # open
        first = True
        cont_incorrect_ans = 0
        for line in mycsv:
            if first:
                first = False
            else:
                option = random.randint(2, 6)
                if len(line[6])==0: # it hasn't  a fifth answer
                    line.pop(6)
                    writer.writerow(line)
                else:
                    line.pop(option)
                    if option - 2 == int(line[6]):  # if the option is the answer
                        rows.append(line)
                        cont_incorrect_ans += 1
                    else:
                        if int(line[6]) > (option - 2):
                            line[6] = int(line[6]) - 1
                        writer.writerow(line)
        rows[0] = [str(cont_incorrect_ans)]
        myFile = open(not_file_path, 'w')
        writer2 = csv.writer(myFile)
        writer2.writerows(rows)


def main(input_path: str, output_path:str):
    if os.path.isfile(input_path) and os.path.isfile(output_path):
        adapt(input_path, output_path)
    else:
        print("The paths must be of existing files")


if __name__ == '__main__':
    # Example usage of the main function
    if len(sys.argv) != 3:
        print("Usage: {} input_source output_source".format(sys.argv[0]))
    else:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        main(arg1, arg2)