import csv
import sys
import os
import random
import argparse

four_ans_only = [249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507]
first_opt_pos = 2
cop_pos = 6
def addRandomColumn(input_path, output_path, partial):
    first_row = ["id", "question", "opa", "opb", "opc", "opd", "ope", "cop", "choice_type", "exp", "subject_name",
                 "topic_name"]
    myFile = open(output_path, 'w')
    writer = csv.writer(myFile)
    writer.writerow(first_row)

    # open the data csv file
    mycsv = csv.reader(open(input_path))  # open
    first = True
    count = 0
    for line in mycsv:
        if first:
            first = False
        else:
            if (partial and count in four_ans_only) or not partial:
                row = []
                option = random.randint(first_opt_pos,first_opt_pos+4)#get a random number between first_opt_pos and first_opt_pos+4
                for i in range(len(line)):
                    if i == option:
                        row.append("")
                        if option != first_opt_pos+4:
                            row.append(line[i])
                    elif (i == cop_pos and not partial) or (i == cop_pos+1 and partial):
                        if int(line[i])>=(option - first_opt_pos):
                            row.append(int(line[i])+1)
                        else:
                            row.append(line[i])
                    elif i == cop_pos and partial:
                        pass
                    else:
                        row.append(line[i])
                writer.writerow(row)
            else:
                writer.writerow(line)
            count += 1


def main(input_path: str, output_path:str, partial:bool):
    if os.path.isfile(input_path) and os.path.isfile(output_path):
        addRandomColumn(input_path, output_path, partial)
    else:
        print("The paths must be of existing files")


if __name__ == '__main__':
    # Example usage of the main function
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: {} (--partial) input_source output_source".format(sys.argv[0]))
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("arg1", type=str, help="input source")
        parser.add_argument("arg2", type=str, help="output source")
        parser.add_argument("--partial", help="Add a random empty case partially", action="store_true")
        args = parser.parse_args()
        main(args.arg1, args.arg2, args.partial)