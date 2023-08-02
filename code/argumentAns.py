import csv
import argparse
import sys
import os
import pandas as pd
import random
import numpy as np
import re

num_ans = 5
cop_pos = 17
max_cases = 508


part_ans_cases_es = [0, 8, 10, 31, 35, 37, 44, 52, 58, 69, 97, 165, 174, 183, 188, 189, 190, 197, 205, 243, 246, 255, 256, 263, 265, 266, 267, 268, 269, 270, 271, 272, 273, 276, 278, 279, 280, 281, 284, 288, 289, 294, 297, 306, 307, 311, 313, 317, 319, 321, 322, 324, 330, 331, 332, 336, 338, 346, 348, 351, 357, 360, 366, 374, 375, 377, 378, 379, 380, 383, 387, 390, 391, 392, 394, 395, 396, 399, 400, 401, 407, 412, 415, 418, 421, 422, 423, 425, 426, 435, 437, 441, 442, 444, 445, 446, 453, 460, 466, 471, 472, 473, 474, 475, 477, 478, 479, 480, 487, 492, 493, 494, 495, 499, 500, 501, 505, 507, 3, 11, 13, 14, 15, 16, 17, 19, 22, 23, 24, 25, 27, 29, 30, 32, 47, 48, 49, 50, 54, 61, 63, 66, 67, 68, 71, 77, 78, 84, 85, 88, 90, 92, 94, 96, 99, 100, 101, 102, 105, 107, 108, 112, 114, 115, 118, 119, 120, 121, 122, 123, 124, 126, 127, 128, 130, 131, 132, 133, 140, 142, 146, 147, 149, 152, 159, 160, 167, 168, 170, 175, 177, 178, 179, 181, 184, 193, 194, 196, 200, 201, 202, 206, 207, 210, 215, 216, 218, 219, 222, 223, 226, 228, 230, 231, 233, 235, 239, 240, 247, 251, 253, 258, 275, 283, 287, 308, 315, 318, 328, 337, 339, 340, 342, 349, 364, 369, 386, 393, 397, 406, 409, 411, 430, 432, 440, 450, 451, 468, 483, 484, 489, 498]
all_ans_cases_es = [3, 11, 13, 14, 15, 16, 17, 19, 22, 23, 24, 25, 27, 29, 30, 32, 47, 48, 49, 50, 54, 61, 63, 66, 67, 68, 71, 77, 78, 84, 85, 88, 90, 92, 94, 96, 99, 100, 101, 102, 105, 107, 108, 112, 114, 115, 118, 119, 120, 121, 122, 123, 124, 126, 127, 128, 130, 131, 132, 133, 140, 142, 146, 147, 149, 152, 159, 160, 167, 168, 170, 175, 177, 178, 179, 181, 184, 193, 194, 196, 200, 201, 202, 206, 207, 210, 215, 216, 218, 219, 222, 223, 226, 228, 230, 231, 233, 235, 239, 240, 247, 255, 256, 263, 265, 266, 267, 268, 269, 270, 271, 272, 273, 276, 278, 279, 280, 281, 284, 288, 289, 294, 297, 306, 307, 311, 313, 317, 319, 321, 322, 324, 330, 331, 332, 336, 338, 346, 348, 351, 357, 360, 366, 374, 375, 377, 378, 379, 380, 383, 387, 390, 391, 392, 394, 395, 396, 399, 400, 401, 407, 412, 415, 418, 421, 422, 423, 425, 426, 435, 437, 441, 442, 444, 445, 446, 453, 460, 466, 471, 472, 473, 474, 475, 477, 478, 479, 480, 487, 492, 493, 494, 495, 499, 500, 501, 505, 507]
one_cases_es = [7, 38, 41, 43, 53, 55, 59, 60, 64, 65, 70, 89, 98, 116, 129, 136, 153, 154, 162, 169, 173, 176, 191, 203, 208, 209, 212, 213, 214, 229, 236, 237, 238, 245, 252, 254, 262, 264, 277, 282, 292, 295, 298, 299, 309, 310, 320, 326, 333, 341, 344, 352, 372, 385, 388, 448, 458, 465, 470, 482, 488, 504]
zero_cases_es = [1, 9, 18, 21, 28, 33, 34, 36, 39, 42, 51, 56, 57, 62, 72, 73, 74, 75, 76, 79, 80, 81, 82, 83, 87, 91, 103, 104, 106, 109, 110, 111, 134, 135, 137, 141, 144, 148, 150, 151, 155, 156, 163, 164, 166, 171, 172, 185, 186, 198, 211, 217, 220, 224, 225, 227, 232, 234, 241, 242, 244, 248, 257, 259, 260, 261, 274, 285, 286, 290, 291, 296, 300, 301, 303, 304, 305, 312, 314, 316, 323, 325, 327, 329, 334, 343, 345, 347, 353, 354, 356, 361, 362, 365, 370, 371, 373, 381, 382, 384, 389, 398, 402, 403, 404, 405, 408, 410, 413, 414, 416, 417, 420, 424, 427, 428, 429, 431, 433, 434, 436, 438, 443, 447, 452, 454, 455, 457, 461, 462, 463, 464, 467, 469, 481, 485, 496, 497, 506]
two_cases_es = [20, 26, 45, 46, 86, 93, 157, 180, 182, 187, 192, 199, 221, 249, 250, 293, 302, 335, 350, 355, 358, 359, 363, 367, 368, 376, 419, 439, 449, 456, 459, 476, 486, 490, 491, 502, 503]
three_cases_es = [2, 4, 5, 6, 12, 40, 95, 113, 117, 125, 138, 139, 143, 145, 158, 161, 195, 204, 251, 253, 258, 275, 283, 287, 308, 315, 318, 328, 337, 339, 340, 342, 349, 364, 369, 386, 393, 397, 406, 409, 411, 430, 432, 440, 450, 451, 468, 483, 484, 489, 498]
four_cases_es = [0, 8, 10, 31, 35, 37, 44, 52, 58, 69, 97, 165, 174, 183, 188, 189, 190, 197, 205, 243, 246, 255, 256, 263, 265, 266, 267, 268, 269, 270, 271, 272, 273, 276, 278, 279, 280, 281, 284, 288, 289, 294, 297, 306, 307, 311, 313, 317, 319, 321, 322, 324, 330, 331, 332, 336, 338, 346, 348, 351, 357, 360, 366, 374, 375, 377, 378, 379, 380, 383, 387, 390, 391, 392, 394, 395, 396, 399, 400, 401, 407, 412, 415, 418, 421, 422, 423, 425, 426, 435, 437, 441, 442, 444, 445, 446, 453, 460, 466, 471, 472, 473, 474, 475, 477, 478, 479, 480, 487, 492, 493, 494, 495, 499, 500, 501, 505, 507]
five_cases_es = [3, 11, 13, 14, 15, 16, 17, 19, 22, 23, 24, 25, 27, 29, 30, 32, 47, 48, 49, 50, 54, 61, 63, 66, 67, 68, 71, 77, 78, 84, 85, 88, 90, 92, 94, 96, 99, 100, 101, 102, 105, 107, 108, 112, 114, 115, 118, 119, 120, 121, 122, 123, 124, 126, 127, 128, 130, 131, 132, 133, 140, 142, 146, 147, 149, 152, 159, 160, 167, 168, 170, 175, 177, 178, 179, 181, 184, 193, 194, 196, 200, 201, 202, 206, 207, 210, 215, 216, 218, 219, 222, 223, 226, 228, 230, 231, 233, 235, 239, 240, 247]

part_ans_cases_en = [3, 13, 14, 16, 25, 50, 63, 66, 67, 84, 90, 92, 105, 114, 115, 123, 126, 127, 140, 147, 159, 160, 178, 179, 184, 193, 201, 207, 219, 223, 226, 230, 233,10, 15, 29, 30, 32, 49, 68, 78, 85, 94, 99, 118, 128, 130, 146, 167, 170, 215, 228, 231, 235, 240, 247, 250, 256, 266, 267, 268, 270, 272, 276, 279, 281, 288, 297, 308, 321, 322, 324, 330, 348, 360, 375, 390, 399, 407, 412, 423, 426, 435, 437, 442, 460, 466, 468, 473, 474, 475, 493, 494, 499, 500, 501,265, 269, 271, 273, 283, 284, 289, 294, 307, 313, 317, 319, 332, 366, 380, 383, 387, 409, 440, 441, 444, 453, 471, 472, 478, 480]
all_ans_cases_en = [3, 13, 14, 16, 25, 50, 63, 66, 67, 84, 90, 92, 105, 114, 115, 123, 126, 127, 140, 147, 159, 160, 178, 179, 184, 193, 201, 207, 219, 223, 226, 230, 233, 250, 256, 266, 267, 268, 270, 272, 276, 279, 281, 288, 297, 308, 321, 322, 324, 330, 348, 360, 375, 390, 399, 407, 412, 423, 426, 435, 437, 442, 460, 466, 468, 473, 474, 475, 493, 494, 499, 500, 501]
one_cases_en = [2, 4, 5, 12, 23, 24, 41, 42, 45, 61, 70, 87, 93, 96, 117, 124, 133, 144, 153, 154, 158, 174, 176, 180, 192, 197, 198, 200, 203, 205, 209, 221, 237, 262, 264, 277, 280, 287, 315, 320, 326, 329, 331, 334, 337, 338, 340, 341, 342, 351, 355, 358, 359, 363, 364, 368, 374, 376, 381, 386, 393, 394, 420, 445, 448, 449, 451, 454, 465, 470, 482, 483, 489, 492, 503, 505]
zero_cases_en = [0, 1, 6, 7, 8, 9, 11, 17, 18, 19, 20, 21, 22, 26, 28, 33, 34, 36, 38, 39, 43, 46, 47, 48, 51, 53, 55, 56, 57, 59, 60, 62, 64, 65, 72, 73, 74, 75, 76, 79, 80, 81, 82, 83, 86, 89, 91, 95, 98, 100, 103, 104, 106, 107, 108, 109, 110, 111, 116, 121, 122, 131, 132, 134, 135, 136, 137, 138, 139, 141, 148, 150, 151, 155, 156, 157, 162, 163, 164, 166, 169, 171, 172, 173, 181, 182, 185, 186, 187, 188, 191, 199, 208, 211, 212, 213, 214, 217, 220, 224, 225, 227, 229, 232, 234, 236, 238, 239, 241, 242, 244, 245, 248, 251, 252, 254, 255, 257, 258, 259, 260, 261, 274, 278, 282, 285, 286, 290, 291, 292, 293, 295, 296, 298, 299, 300, 301, 302, 303, 304, 305, 309, 310, 311, 312, 314, 316, 318, 323, 325, 327, 328, 333, 335, 336, 339, 343, 344, 345, 347, 352, 353, 354, 356, 357, 361, 362, 365, 367, 370, 371, 372, 373, 377, 382, 384, 385, 388, 389, 392, 395, 396, 398, 402, 403, 404, 405, 406, 408, 410, 413, 414, 415, 416, 417, 418, 419, 422, 424, 427, 428, 429, 430, 431, 432, 433, 434, 436, 438, 439, 443, 446, 447, 450, 452, 455, 457, 458, 459, 461, 462, 463, 464, 467, 469, 477, 479, 481, 484, 485, 487, 488, 490, 491, 495, 496, 497, 498, 502, 504, 506]
two_cases_en = [35, 37, 40, 54, 69, 71, 97, 102, 120, 125, 129, 168, 177, 183, 189, 190, 196, 204, 206, 216, 218, 243, 249, 253, 263, 275, 306, 346, 349, 350, 369, 378, 379, 391, 397, 400, 401, 411, 421, 425, 456, 476, 486, 507]
three_cases_en = [27, 31, 44, 52, 58, 77, 88, 101, 112, 113, 119, 142, 143, 145, 149, 152, 161, 165, 175, 194, 195, 202, 210, 222, 246, 265, 269, 271, 273, 283, 284, 289, 294, 307, 313, 317, 319, 332, 366, 380, 383, 387, 409, 440, 441, 444, 453, 471, 472, 478, 480]
four_cases_en = [10, 15, 29, 30, 32, 49, 68, 78, 85, 94, 99, 118, 128, 130, 146, 167, 170, 215, 228, 231, 235, 240, 247, 250, 256, 266, 267, 268, 270, 272, 276, 279, 281, 288, 297, 308, 321, 322, 324, 330, 348, 360, 375, 390, 399, 407, 412, 423, 426, 435, 437, 442, 460, 466, 468, 473, 474, 475, 493, 494, 499, 500, 501]
five_cases_en = [3, 13, 14, 16, 25, 50, 63, 66, 67, 84, 90, 92, 105, 114, 115, 123, 126, 127, 140, 147, 159, 160, 178, 179, 184, 193, 201, 207, 219, 223, 226, 230, 233]

not_cases_es = [1, 9, 17, 18, 19, 21, 22, 23, 28, 33, 34, 36, 39, 42, 51, 55, 56, 57, 62, 64, 72, 73, 74, 75, 76, 79, 80, 81, 82, 83, 87, 91, 103, 104, 106, 107, 108, 109, 110, 111, 129, 134, 135, 137, 141, 144, 148, 150, 151, 155, 156, 162, 163, 164, 166, 171, 172, 185, 186, 198, 211, 214, 217, 220, 224, 225, 227, 232, 234, 241, 242, 244, 248, 257, 259, 260, 261, 274, 285, 286, 290, 291, 296, 298, 299, 300, 301, 303, 304, 305, 310, 312, 314, 316, 323, 325, 327, 329, 334, 343, 345, 347, 353, 354, 356, 358, 361, 362, 365, 370, 371, 372, 373, 381, 382, 384, 388, 389, 398, 402, 403, 404, 405, 408, 410, 413, 414, 416, 417, 420, 424, 427, 428, 429, 431, 433, 434, 436, 438, 443, 447, 452, 454, 455, 457, 461, 462, 463, 464, 467, 469, 481, 485, 496, 497, 506]
not_cases_en = [0,1,6,7,8,9,11,17,18,19,20,21,22,26,28,33,34,36,38,39,43,46,47,48,51,53,55,56,57,59,60,62,64,65,72,73,74,75,76,79,80,81,82,83,86,89,91,95,98,100,103,104,106,107,108,109,110,111,116,121,122,131,132,134,135,136,137,138,139,141,148,150,151,155,156,157,162,163,164,166,169,171,172,173,181,182,185,186,187,188,191,199,208,211,212,213,214,217,220,224,225,227,229,232,234,236,238,239,241,242,244,245,248,251,252,254,255,257,258,259,260,261,274,278,282,285,286,290,291,292,293,295,296,298,299,300,301,302,303,304,305,309,310,311,312,314,316,318,323,325,327,328,333,335,336,339,343,344,345,347,352,353,354,356,357,361,362,365,367,370,371,372,373,377,382,384,385,388,389,392,395,396,398,402,403,404,405,406,408,410,413,414,415,416,417,418,419,422,424,427,428,429,430,431,432,433,434,436,438,439,443,446,447,450,452,455,457,458,459,461,462,463,464,467,469,477,479,481,484,485,487,488,490,491,495,496,497,498,502,504,506]

file_en = "results_en"
file_es = "results_es"
test_en = "test_results_en"
test_es = "test_results_es"
csv_path_file = "_ANS_clinical_caseMIR.csv"
csv_path_file_merged = "_ANS_clinical_caseMIR"
correct = []
GLOBAL_TIE = 0
GLOBAL_TIE1 = 0
GLOBAL_TIE2 = 0
GLOBAL_TIE3 = 0
GLOBAL_TIE4 = 0
GLOBAL_TIE5 = 0
GLOBAL_MAX = 0
GLOBAL_MAX_CASES = []

def createFile(path):
    mydirname = './' + path
    if not os.path.exists(mydirname):
        os.makedirs(os.path.dirname(mydirname), exist_ok=True)

def createFile_and_write(path, first_line):
    mydirname = './' + path
    if not os.path.exists(mydirname):
        os.makedirs(os.path.dirname(mydirname), exist_ok=True)
        myFile = open(path, 'w')
        writer = csv.writer(myFile)
        writer.writerow(first_line)

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    return (matrix[size_x - 1, size_y - 1])

def find_nested_brackets(string):
    stack = []
    result = []

    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
        elif c == ')':
            if len(stack) > 0:
                start = stack.pop()
                result.append(string[start:i+1])

    return result

def get_list_with_brackets(line, position):
    returned_list = []
    for s in line[position].split(","):
        returned_list.append(s.split("(")[0].strip())
        results = find_nested_brackets(s)
        results = sorted(list(results), key=len, reverse=True)
        for i in range(len(results)):
            r = results[i][1:]
            if r.split("(")[0].find("Causado por") != -1:
                break
            r = r[:-1]
            aurk = False
            part_s = "".join(r.split("(")[0])
            for p in "".join(r.split("(")[1:]).split(" "):
                if aurk and p.find("(") == -1 and p.find(" ") == -1:
                    part_s += p
                if len(p.split(")")) > 0 and p.find(")") != -1:
                    part_s += str(p.split(")")[1]) + " "
                elif len(p.split(")")) == 0:
                    aurk = True

            prev = returned_list[-1]
            elem = str(s.split("(" + part_s)[0].split(" ")[-2].split(")")[-1].replace("(", "").replace(")", ""))
            if len(elem) > 0 and i > 0:
                part_s = prev.split(" " + elem)[0].strip() + " " + elem + " " + part_s.strip() + "".join(
                    prev.split(" " + elem)[1:])
            elif i == 0:
                part_s = prev + " " + part_s
            returned_list.append(part_s.strip())
    return returned_list

def get_at_position(path, num_case, position, relations = False):
    cont =  0
    mycsv = csv.reader(open(path))  # open
    first = True
    for line in mycsv:
        if first:
            first = False
        else:
            if cont == num_case:
                if relations:
                    return get_list_with_brackets(line, position)
                return [s.lower().strip() for s in line[position].split(",")]
            cont += 1
    return None


def in_common(signs, lista):
    count = 0
    args = []
    for s in signs.split(","):
        s = s.strip()
        if len(s)>0 and s != '-' and s.lower() in lista:
            count += 1
            args.append(s.lower())
        elif len(s) > 0 and s != '-':
            for l in lista:
                if s.lower() in l:
                    count += 1
                    args.append(s.lower().strip())
    return count, args


def in_common_with_levenshtein(signs, lista, lev):
    count = 0
    args = []
    for s in signs.split(","):
        for cs in lista:
            if len(s) > 0 and len(cs) > 0:
                dist = levenshtein(s.lower().strip(), cs)
                if dist <= lev:
                    count += 1
                    args.append(s.lower().strip())
    return count, args

def unique(lista):
    x = np.array(lista)
    return list(np.unique(x))

def argument_correct_ans(file, number, quest_sign_path, lev, relations, lang):
    check_signs = get_at_position(quest_sign_path, number, 3, relations = relations)
    check_diseases = get_at_position(quest_sign_path, number, 1, relations = relations)
    if check_signs is None:
        print("There is an error with the names of the files path. They must start with a number")
    mycsv = csv.reader(open(file))  # open
    first = True
    pos_sign = 1
    check_num = {}
    for line in mycsv:
        if first:
            first = False
        else:
            signs = line[pos_sign]

            if lev is None:
                common_num, common_args = in_common(signs, check_signs) # + in_common(signs, check_diseases)
            else:
                common_num, common = in_common(signs, check_signs)
                common_num_l, common_l = in_common_with_levenshtein(signs, check_signs, lev)# +in_common(signs, check_diseases) #+ in_common_with_levenshtein(signs, check_diseases, lev)
                if common and common_l:
                    if set(common) == set(common_l):
                        common_args = unique(common)
                    else:
                        common.extend(unique(common_l))
                        common_args = unique(common)
                elif common:
                    common_args = unique(common)
                elif common_l:
                    common_args = unique(common_l)
                else:
                    common_args = []
                common_num += common_num_l
            check_num[line[0]] = (common_num, common_args)

    #see what answer has the maximum signs in common
    maxi = 1
    correct_ans = -1
    correct_args = []
    possible_ans = []
    found = False
    for key, value in check_num.items():
        if value[0] >= maxi:
            found = True
            maxi = value[0]
            correct_ans = key
            correct_args = value[1]
    for key, value in check_num.items():
        if value[0] == maxi:
            possible_ans.append(key)

    if maxi >= 1 and found and number not in eval("not_cases_" + lang):
        global  GLOBAL_TIE
        GLOBAL_TIE += 1
        print("\nIn " + str(number) +" case the maximum is of: " +str(maxi) +" and there are "+ str(len(possible_ans)) +" cases in the tie")
    if maxi >= 1 and found and not len(possible_ans) > 1 and number not in eval("not_cases_" + lang):
        correct.append(number)
        global GLOBAL_MAX
        GLOBAL_MAX += 1
        global  GLOBAL_MAX_CASES
        GLOBAL_MAX_CASES.append(number)
        print("In " + str(number) +" case there is a maximum choice")
    if maxi >= 1 and found and number not in eval("not_cases_" + lang):
        if  number in eval("one_cases_" + lang):
            print("CASE1")
            if len(possible_ans) == 1:
                global GLOBAL_TIE1
                GLOBAL_TIE1 += 1
                print("In " + str(number) +" case there is a tie. Case1 ")
        if  number in eval("two_cases_" + lang):
            print("CASE2")
            if len(possible_ans) == 2:
                global GLOBAL_TIE2
                GLOBAL_TIE2 += 1
                print("In " + str(number) +" case there is a tie. Case2 ")
        if number in eval("three_cases_" + lang):
            print("CASE3")
            if len(possible_ans) == 3:
                global GLOBAL_TIE3
                GLOBAL_TIE3 += 1
                print("In " + str(number) +" case there is a tie. Case3 ")
        if number in eval("four_cases_" + lang):
            print("CASE4")
            if len(possible_ans) == 4:
                global GLOBAL_TIE4
                GLOBAL_TIE4 += 1
                print("In " + str(number) +" case there is a tie. Case4 ")
        if number in eval("five_cases_" + lang):
            print("CASE5")
            if len(possible_ans) == 5:
                global GLOBAL_TIE5
                GLOBAL_TIE5 += 1
                print("In " + str(number) +" case there is a tie. Case5 ")
    #KOMENTATU NAHI BADA BERDINKETA KONTUTAN HARTU
    if len(possible_ans) > 1:
        correct_ans = random.choice(possible_ans)
        correct_args = check_num[correct_ans][1]
    if number in eval("not_cases_"+lang):
        correct_ans = -1
        correct_args = []
    return correct_ans, correct_args #possible_ans

def write_correct_ans(write_ans_path, correct_ans, correct_args, quest_num):
    myFile = open(write_ans_path, 'a')
    writer = csv.writer(myFile)
    line = [quest_num, correct_ans, ",".join(correct_args)]
   # line = [quest_num, ",".join(correct_ans)]
    writer.writerow(line)

def get_diseases_signs_and_argument(file, quest_sign_path, write_ans_path, lev, id_list, relations, lang):
    for i in range(max_cases):
        if len(id_list) == 0 or (len(id_list) > 0 and i in id_list):
            if (i not in not_cases_es and file.find("es") != -1) or (i not in not_cases_en and file.find("en") != -1) :
                mycsv = csv.reader(open(file + str(i) + csv_path_file_merged + '_merged.csv'))  # open
                first = True
                pos_sign, pos_disease =  [], []
                rows = []
                cont = 0
                for line in mycsv:  # iterate through the csv
                    signs, diseases = [], []
                    if first:
                        createFile(file + str(i) + '_merged.csv')
                        rows.append(["ansZbkia", "sintomak", "gaixotasunak"])
                        first = False
                        for j in range(len(line)):
                            if line[j] == "sintomak":
                                pos_sign.append(j)
                            if line[j] == "gaixotasunIzenOrig" or line[j] == "gaixotasunIzenLev":
                                pos_disease.append(j)
                    else:
                        for p in pos_sign:
                            list = line[p].split(",")
                            for l in list:
                                if len(l) > 1 and l != "-" and l != " -":
                                    for j in l.split("#"):
                                        if len(j) > 1 and j != "-" and j != " -":
                                            signs.append(j)
                        for p in pos_disease:
                            list = line[p].split(",")
                            for l in list:
                                if len(l) > 1 and l != "-" and l != " -":
                                    for j in l.split("#"):
                                        if len(j) > 1 and j != "-" and j != " -":
                                            diseases.append(j)
                        rows.append([cont, ",".join(signs), ",".join(diseases)])
                        cont += 1
            myFile = open(file + str(i) + '_merged.csv', 'w')
            writer = csv.writer(myFile)
            writer.writerows(rows)
            myFile.close()

            correct_ans, correct_args = argument_correct_ans("./" + file + str(i) + '_merged.csv', i, quest_sign_path, lev, relations, lang)
            write_correct_ans(write_ans_path, correct_ans, correct_args, i)

def merge(input_path, paths, file_merge, id_list):
    for i in range(max_cases):
        if len(id_list) == 0 or (len(id_list) > 0 and i in id_list):
            df = pd.DataFrame()
            all_paths = []
            for path in paths:
                complete_path = input_path + path + "/" + str(i) + csv_path_file
                if os.path.exists(complete_path):
                    all_paths.append(complete_path)
            for p in all_paths:
                data = pd.read_csv(p)
                df = pd.concat([df, data], axis=1)

            df.to_csv(file_merge + str(i) + csv_path_file_merged + '_merged.csv', index=False)

def get_correct_option(check_path, num_case):
    count = 0
    mycsv = csv.reader(open(check_path))
    first = True
    for line in mycsv:
        if first:
            first = False
        else:
            if count == num_case:
                return str(int(line[cop_pos]) -1)
            count += 1
    return None

def check(test_path, check_path, language, id_list):
    createFile_and_write("results.csv",["test_path", "all test", "5/5,4/4", "4-5/5,3-4/4", "1-5/5,1-4/4", "CORRECT CASES OF MAX","GLOBAL_TIE",
           "GLOBAL_TIE1", "GLOBAL_TIE2", "GLOBAL_TIE3", "GLOBAL_TIE4", "GLOBAL_TIE5", "GLOBAL_MAX"])
    myFile = open("results.csv", 'a')
    writer = csv.writer(myFile)
    pos_test_opc = 1
    pos_test_case_number = 0
    pos_test_args = 2
    correct_ans, correct_ans_max = 0, 0
    correct_ans_all1, correct_ans_all2 = 0, 0
    count = 0
    mycsv = csv.reader(open(test_path))
    first = True
    type1 = "all_ans_cases_"
    if len(id_list) > 0:
        count1 = len([elem for elem in eval(type1+language) if elem in id_list])
    else:
        count1 = len(eval(type1+language))
    type2 = "part_ans_cases_"
    if len(id_list) > 0:
        count2 = len([elem for elem in eval(type2 + language) if elem in id_list])
    else:
        count2 = len(eval(type2 + language))

    for line in mycsv:
        if first:
            first = False
        else:
            cop = get_correct_option(check_path, int(line[pos_test_case_number]))
            if cop is None:
                print("ERROR: it's not exit " + str(count) +" case")
            elif cop == line[pos_test_opc] and int(line[pos_test_case_number]) not in eval("not_cases_"+language):# and int(line[pos_test_case_number]) in correct:
            #elif cop in line[pos_test_opc]:
                if count in GLOBAL_MAX_CASES:
                    correct_ans_max += 1
                print("\n"+line[pos_test_case_number] + " kasua asmatu du, erantzun egokia "+line[pos_test_opc] +" izanik.\n"
                                                        " ARRAZOIA: sintoma hauek ditu: "+line[pos_test_args])
                correct_ans += 1
                if int(line[pos_test_case_number]) in eval(type1+language):
                    correct_ans_all1 += 1
                if int(line[pos_test_case_number]) in eval(type2+language):
                    correct_ans_all2 += 1
            count += 1
    print(" ACCURACY WITH ALL CASES: ")
    print("\tErantzun kopuru zuzenak: "+str(correct_ans) + ", erantzun kopuru totala: " + str(count))
    print("\tThe accuracy: "+ str(correct_ans/(count)))
    print(" ACCURACY WITH ALL CASES WITH ALL ANSWER FULL: ")
    print("\tErantzun kopuru zuzenak: " + str(correct_ans_all1) + ", erantzun kopuru totala: " + str(count1))
    print("\tThe accuracy: " + str(correct_ans_all1 / count1))
    print(" ACCURACY WITH ALL CASES WITH ALL ANSWER FULL OR ALL CASES WITH 4/5,3/4 ANSWER FULL: ")
    print("\tErantzun kopuru zuzenak: " + str(correct_ans_all2) + ", erantzun kopuru totala: " + str(count2))
    print("\tThe accuracy: " + str(correct_ans_all2 / count2))
    print(" ACCURACY WITH ALL CASES WITH AT LEAST ONE ANSWER FULL: ")
    print("\tErantzun kopuru zuzenak: " + str(correct_ans) + ", erantzun kopuru totala: " + str(count-len(eval("zero_cases_"+language))))
    print("\tThe accuracy: " + str(correct_ans /(count-len(eval("zero_cases_"+language)))))
    print("CORRECT CASES OF MAX: " + str(correct_ans_max))
    print("GLOBAL TIE " +str(GLOBAL_TIE))
    print("GLOBAL TIE1 " + str(GLOBAL_TIE1))
    print("GLOBAL TIE2 " + str(GLOBAL_TIE2))
    print("GLOBAL TIE3 " + str(GLOBAL_TIE3))
    print("GLOBAL TIE4 " + str(GLOBAL_TIE4))
    print("GLOBAL TIE5 " + str(GLOBAL_TIE5))
    print("GLOBAL MAX " + str(GLOBAL_MAX))
    row = [test_path, str(correct_ans)+ " " + str(count) +" "+str(correct_ans/(count)), str(correct_ans_all1)+ " " + str(count1) +" "+str(correct_ans_all1 / count1),
           str(correct_ans_all2)+ " " + str(count2) +" "+str(correct_ans_all2 / count2), str(correct_ans)+ " " + str(count-len(eval("zero_cases_"+language))) +" "+str(correct_ans / (count-len(eval("zero_cases_"+language)))),
           str(correct_ans_max), str(GLOBAL_TIE), str(GLOBAL_TIE1),str(GLOBAL_TIE2), str(GLOBAL_TIE3), str(GLOBAL_TIE4), str(GLOBAL_TIE5), str(GLOBAL_MAX)]
    writer.writerow(row)


def merge_and_getSigns(language, input_path, quest_sign_path, check_path, seed, lev, id_list,id_path, relations, nci):
    if id_path is not None:
        name = "_relationsIs"+str(relations)+"_levIs"+str(lev)+"_id_"+id_path.replace("/","_")+"_seed"+str(seed)
    else:
        name = "_relationsIs" + str(relations) + "_levIs" + str(lev) + "_id_" + "_seed" + str(seed)
    createFile(eval("file_"+language)+name+"/1")
    first_line = ['QuestZbki', 'cop', "Args"]
    createFile_and_write(eval("test_"+language)+name+".csv", first_line)

    paths = []
    for path in os.listdir(input_path):
        if nci:
            if path.find("_"+language) != -1 and path.find("NCID") != -1:
                paths.append(path)
        elif not relations:
            if path.find("_"+language) != -1 and path.find("NCID") == -1 and path.find("relations") == -1:
                paths.append(path)
        else:
            if path.find("_"+language) != -1 and path.find("relations") != -1:
                paths.append(path)
    print(paths)
    merge(input_path, paths, eval("file_"+language)+name+"/", id_list)
    get_diseases_signs_and_argument(eval("file_"+language)+name+"/", quest_sign_path, eval("test_"+language)+name+".csv", lev, id_list, relations, language)
    check(eval("test_"+language)+name+".csv", check_path, language, id_list)

def main(input_path: str, quest_sign_path:str, check_path:str, language:str, seed:int, lev:int, id_path:str, relations:bool, nci:bool):
    if os.path.isdir(input_path) and os.path.isfile(quest_sign_path) and os.path.isfile(check_path):
        if input_path[-1] != "/":
            input_path += "/"
        if language != "es" and language != "en":
            print("The language must be en or es")
        elif id_path is None or (id_path is not None and os.path.isfile(id_path)):
            if id_path is None:
                id_list = []
            else:
                id_list = []
                mycsv = csv.reader(open(id_path))  # open
                first = True
                cont = 0
                for line in mycsv:  # iterate through the csv
                    if first:
                        first = False
                    else:
                        id_list.append(int(line[0]))
                        if int(line[0]) in eval("not_cases_"+language):
                            cont+=1
                print(str(cont)+" number of cases are empty.")
            random.seed(seed)
            merge_and_getSigns(language, input_path, quest_sign_path, check_path,seed, lev, id_list, id_path, relations, nci)
        else:
            print("The ID path must be a file.")
    else:
        print("The first path must be of a exiting directory and the last two must be exiting files")

if __name__ == '__main__':
    # Example usage of the main function
    if len(sys.argv) != 6  and len(sys.argv) != 7 and len(sys.argv) != 8 and len(sys.argv) != 9 and len(sys.argv) != 10  and len(sys.argv) != 11  and len(sys.argv) != 12:
        print("Usage: {} (--l THRESHOLD) (--id id_path) (--relations) (--nci) input_source quest_sign_source check_source language seed".format(sys.argv[0]))
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("arg1", type=str, help="Input source")
        parser.add_argument("arg2", type=str, help="The source with questions signs")
        parser.add_argument("arg3", type=str, help="The source with correct answers")
        parser.add_argument("lan", type=str, help="Language (en/es)")
        parser.add_argument("seed", type=int, help="Define seed")
        parser.add_argument("--l", type=int, help="Calculate levenshtein distance to check" )
        parser.add_argument("--id", type=str, help="Source of the optional IDs")
        parser.add_argument("--relations", help="The source with questions signs has relations", action="store_true")
        parser.add_argument("--nci", help="The source with questions signs has nci signs", action="store_true")
        args = parser.parse_args()
        main(args.arg1, args.arg2, args.arg3, args.lan, args.seed, args.l, args.id, args.relations, args.nci)
