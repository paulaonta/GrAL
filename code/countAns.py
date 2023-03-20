import csv
import os.path
import sys
import argparse

file_name = "_ANS_clinical_caseMIR.csv"
max_ans = 5

def read_and_count(path):
    try:
        mycsv = csv.reader(open(path))  # open
        first = True
        count = 0

        for line in mycsv:
            if first:
                first = False
            else:
                for j in range(1, len(line)):
                    if len(line[j]) > 0:
                        count += 1
                        break
    except:
        count = -1
        pass

    return count

def count_all(input_path, max_cases, input_path2 = None):
    cases0, cases1, cases2, cases3, cases4, cases5 = [], [], [], [], [], []

    for i in range(max_cases):#iterate cases
        count = read_and_count(input_path + str(i) + file_name)
        if input_path2 is not None:
            count += read_and_count(input_path2 + str(i) + file_name)

        match count:
            case 0:
                cases0.append(i)
            case 1:
                cases1.append(i)
            case 2:
                cases2.append(i)
            case 3:
                cases3.append(i)
            case 4:
                cases4.append(i)
            case 5:
                cases5.append(i)

    for i in range(max_ans+1):
        print(str(i) + " answers detected: " + str(len(eval('cases'+str(i)))))
        print(eval('cases'+str(i)))


def count_files(dir_path):
    count = 0
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return count

def main(input_path: str, input_path2= None):
    if os.path.isdir(input_path): # if it a directory
        if input_path[-1] != "/":
            input_path += "/"
        max_files = count_files(input_path)
        if input_path2:
            if os.path.isdir(input_path): # if it a directory
                if input_path2[-1] != "/":
                    input_path2 += "/"
                max_files2 = count_files(input_path2)
                if max_files2 != max_files:
                    print("The two directories must have the same number of files")
                else:
                    count_all(input_path, max_files, input_path2)
            else:
                print("The optional argument must be a directory path.")
        else:
            count_all(input_path, max_files)
    else:
        print("It must be a directory path.")

if __name__ == '__main__':
    # Example usage of the main function
    if len(sys.argv) != 2 and len(sys.argv) != 4:
        print("Usage: {} (--two input_source2) input_source".format(sys.argv[0]))
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("arg1", type=str, help="input source")
        parser.add_argument("--two", type=str, help="Taking into account a second path")
        args = parser.parse_args()
        main(args.arg1, args.two)