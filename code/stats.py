import csv

path = "./compareData/clinical_cases_spanish.csv"

mycsv = csv.reader(open(path))  # open
first = True
cases =[]
cases_comp = []
pos = 16
count = 0
comp = [8, 10, 35, 37, 44, 69, 97, 117, 165, 188, 189, 190, 195, 197, 205, 243, 246, 255, 256, 258, 263, 267, 268, 269, 270, 272, 276, 278, 279, 280, 289, 294, 306, 307, 311, 313, 317, 319, 321, 324, 330, 332, 336, 338, 346, 348, 349, 351, 357, 360, 375, 377, 378, 379, 380, 383, 386, 387, 390, 391, 392, 393, 394, 396, 399, 401, 407, 412, 418, 421, 422, 423, 425, 426, 435, 441, 442, 444, 445, 446, 453, 460, 466, 471, 472, 473, 474, 475, 477, 478, 479, 480, 483, 484, 487, 489, 492, 494, 495, 500, 501, 507
]

for line in mycsv:
    if first:
        first = False
    else:
        text = line[pos]
        if len(text) < 1:
            cases.append(count)
            if count in comp:
                cases_comp.append(count)
        count += 1
print(cases)
print(len(cases_comp))
print(cases_comp)