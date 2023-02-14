import os
import csv

def createFile(path):
    mydirname = './' + path
    if not os.path.exists(mydirname):
        os.makedirs(os.path.dirname(mydirname), exist_ok=True)

#define paths
path = "./input_unimer/"
question_file_partial_name = "_QUEST_clinical_caseMIR.txt"
answer_file_partial_name = "_ANS_clinical_caseMIR.txt"
csv_path = "./data/all_together_clinical_casesMIR.csv"

#define variables
first = True
question_pos = 5
answer_pos = 12
num_answer = 5

cont = 0
# open the csv file
mycsv = csv.reader(open(csv_path)) #open

for line in mycsv:#iterate through the csv
    if first:
        first = False
    else:
        answer_list = []
        question = line[question_pos] #get question
        #get all the posible answers
        for i in range(num_answer):
            answer_list.append(line[answer_pos+i])

        #create a file to save the question and a file to save the answer
        question_path = path + str(cont) + question_file_partial_name
        createFile(question_path)
        answer_path = path + str(cont) + answer_file_partial_name
        createFile(answer_path)

        #save the text in the files already created
        with open(question_path, 'w',  encoding='utf8') as file:
            file.write(question)
            file.write('\n')

        with open(answer_path, 'w', encoding='utf8') as file:
            for ans in answer_list:
                file.write(ans)
                file.write('\n')
        cont += 1


