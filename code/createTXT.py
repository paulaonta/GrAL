import os
import csv

def createFile(path):
    mydirname = './' + path
    if not os.path.exists(mydirname):
        os.makedirs(os.path.dirname(mydirname), exist_ok=True)


#define paths
question_file_partial_name = "_QUEST_clinical_caseMIR.txt"
answer_file_partial_name = "_ANS_clinical_caseMIR.txt"

#define variables
first = True
question_pos = 5
answer_pos = 12
num_answer = 5

def main(input_path: str, output_path: str):
    createFile(output_path)
    cont = 0
    # open the csv file
    mycsv = csv.reader(open(input_path))  # open

    for line in mycsv:  # iterate through the csv
        if first:
            first = False
        else:
            question = line[question_pos]  # get question
            new_question = question + "."  # append .
            final_question = new_question.replace("..", ".").replace(". .", ".")

            # get all the posible answers
            for i in range(num_answer):
                answer = line[answer_pos + i]  # get answer
                if len(answer) > 1:  # erantzun posible bat badago
                    new_answer = answer + "."  # append .
                    final_answer = new_answer.replace("..", " .").replace(". .", " .")
                    # create a file to save each answer
                    answer_path = output_path + "/" + str(cont) + "(" + str(i) + ")" + answer_file_partial_name
                    createFile(answer_path)

                with open(answer_path, 'w', encoding='utf8') as file:
                    file.write(final_answer)
                    file.write('\n')

            # create a file to save the question
            question_path = output_path + "/" + str(cont) + question_file_partial_name
            createFile(question_path)

            # save the text in the files already created
            with open(question_path, 'w', encoding='utf8') as file:
                file.write(final_question)
                file.write('\n')

            cont += 1

if __name__ == '__main__':
    # Example usage of the main function
    if len(sys.argv) != 3:
        print("Usage: {} input_source output_source".format(sys.argv[0]))
    else:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        main(arg1, arg2)