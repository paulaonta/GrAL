import csv
import sys

year_pos = 0
id_pos = 1

def main(input_path: str):
    # open the data csv file
    mycsv = csv.reader(open(input_path))  # open
    first = True
    id_list, rows = [], []
    prev_year = None

    for line in mycsv:
        if first:
            first = False
            rows.append(line)
        else:
            year = line[year_pos]
            id = line[id_pos]
            if prev_year != None:
                if prev_year == year: #same year
                    if not id in id_list: #same id
                        rows.append(line)
                        id_list.append(id)
                else:
                    id_list = []
            prev_year = year

    myFile = open(input_path, 'w')
    writer = csv.writer(myFile)
    writer.writerows(rows)


if __name__ == '__main__':
    # Example usage of the main function
    if len(sys.argv) != 2:
        print("Usage: {} input_source".format(sys.argv[0]))
    else:
        arg1 = sys.argv[1]
        main(arg1)