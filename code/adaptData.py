import csv
import sys
import os

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
def adapt(input_path, output_path):
    first_row = ["id","question","opa","opb","opc","opd","ope","cop","choice_type","exp","subject_name","topic_name"]
    myFile = open(output_path, 'w')
    writer = csv.writer(myFile)
    writer.writerow(first_row)

    # open the data csv file
    mycsv = csv.reader(open(input_path))  # open
    first = True

    for line in mycsv:
        if first:
            first = False
        else:
            row = [str(line[0])+"-"+str(line[1]), line[question_pos], line[ans_pos], line[ans_pos+1], line[ans_pos+2],
                   line[ans_pos+3], line[ans_pos+4], line[correct_ans_pos], "single", line[exp_pos],
                   convert_subject[line[subject_pos]], ""]
            writer.writerow(row)

def main(input_path: str, output_path:str):
    if os.path.isfile(input_path) and os.path.isfile(output_path):
        adapt(input_path, output_path)
    else:
        print("The paths must be of existed files")


if __name__ == '__main__':
    # Example usage of the main function
    if len(sys.argv) != 3:
        print("Usage: {} input_source output_source".format(sys.argv[0]))
    else:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        main(arg1, arg2)