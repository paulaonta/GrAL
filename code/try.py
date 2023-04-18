import csv
path = "./medmcqa/4ans_gureTest(1.b)_bert-base-uncased@@@@@@use_contextFalse@@@daata._content_medmcqa_data_train_MEDMCQA_orig.csv@@@seqlen192/dev_results.csv"

mycsv = csv.reader(open(path))  # open
first = True
count = 0
correct = 0

for line in mycsv:
    if first:
        first = False
    else:
        if line[6] == line[11]:
            correct += 1
        count += 1
print(str(correct/count))