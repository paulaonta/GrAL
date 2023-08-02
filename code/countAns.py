import csv
import os.path
import sys
import argparse

file_name = "_ANS_clinical_caseMIR.csv"
max_ans = 5
four_ans_only = [249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507]

def read_and_count(path, lista = None):
    try:
        mycsv = csv.reader(open(path))  # open
        first = True
        count = 0
        cases = []
        cont = 0
        for line in mycsv:
            if first:
                first = False
            else:
                for j in range(1, len(line)):
                    if (len(line[j]) > 0 and lista is not None and cont not in lista) or (len(line[j]) > 0 and lista is None):
                        count += 1
                        cases.append(cont)
                        break
                cont+=1
    except:
        count = -1
        pass

    return count, cases

def count_all(input_path, max_cases, input_path2 = None):
    cases0, cases1, cases2, cases3, cases4, cases5 = [], [], [], [], [], []
    cont_three, cont_four = 0,0
    cont_three_list, cont_four_list = [],[]
    count2 = 0
    for i in range(max_cases):#iterate cases
        count,cases = read_and_count(input_path + str(i) + file_name)
        if input_path2 is not None:
            count2,cases = read_and_count(input_path2 + str(i) + file_name, cases)
        count += count2
        match count:
            case 0:
                cases0.append(i)
            case 1:
                cases1.append(i)
            case 2:
                cases2.append(i)
            case 3:
                cases3.append(i)
                if input_path2 is not None and i in four_ans_only:
                    cont_three += 1
                    cont_three_list.append(i)
            case 4:
                cases4.append(i)
                if input_path2 is not None and i in four_ans_only:
                    cont_four += 1
                    cont_four_list.append(i)
            case 5:
                cases5.append(i)

    for i in range(max_ans+1):
        print(str(i) + " answers detected: " + str(len(eval('cases'+str(i)))))
        print(eval('cases'+str(i)))
    if input_path2 is not None:
        print("4/4:" + str(cont_four))
        print(cont_four_list)
        print("3/4:" + str(cont_three))
        print(cont_three_list)


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
        parser.add_argument("arg1", type=str, help="input source directory")
        parser.add_argument("--two", type=str, help="Taking into account a second path")
        args = parser.parse_args()
        main(args.arg1, args.two)