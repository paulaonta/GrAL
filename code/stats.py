import csv

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

path = "./results_Wikidata/results_Wikidata_es_lev_NO_UMLS_relations/"
max_cases = 508
gaixBAI = 0
gaixEZ = 0
gaixEZ_izen = 0
sin = 0
sin_ez = 0
sin_bai = 0
sin_hutsik = 0

for i in range(max_cases):
    try:
        mycsv = csv.reader(open(path + str(i)+ "_ANS_clinical_caseMIR.csv"))  # open
        first = True
        for line in mycsv:
            if first:
                first = False
            else:
                aux = line[1].split(",")
                if aux != ['']:
                    gaixEZ += len(aux)

                aux = line[3].split(",")
                if aux != ['']:
                    for a in aux:
                        if a.find("#") != -1:
                            for elem in a.split("#"):
                                if len(elem) > 2:
                                    gaixBAI += 1
                        else:
                            gaixBAI += 1

                aux = line[2].split(",")
                if aux != ['']:
                    for a in aux:
                        if a!= '-' and a!= ' -':
                            gaixEZ_izen+=len(line[1].split(","))
                            aux = line[3].split(",")
                            if aux != ['']:
                                for a in aux:
                                    sartu = False
                                    sin += len(a.split("#"))

                                    for j in a.split("#"):
                                        if j != '-' and j != ' -':
                                            sartu = True
                                        else:
                                            sin_hutsik += 1
                                if sartu:
                                    sin_bai += len(line[1].split(","))
                                else:
                                    sin_ez += len(line[1].split(","))
                                break
                '''
                #aux = line[4].split(",")
                if  line[4] != '':
                    diseases = get_list_with_brackets(line,4)
                    for d in diseases:
                        if len(d) > 1:
                            gaixEZ_izen += 1
                #lev ez denean deskomentatu
                '''




    except:
        pass

print(gaixEZ)
print(gaixBAI)
print(gaixEZ_izen)

print(sin)
print(sin_ez)
print(sin_bai)
print(sin_hutsik)