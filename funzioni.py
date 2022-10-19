import csv



def estrai_ruote(filecsv):

    #index = [["Data", "Ruota", "1","2","3","4","5"]]
    ruote = ["BA", "FI", "MI", "NA", "PA", "RO", "TO", "VE", "NZ"]

    for r in ruote:
        #print(r)
        temp = [["Data", "Ruota", "1","2","3","4","5"]]
        with open(filecsv, 'r') as file:
            reader = csv.reader(file, delimiter=";")
            for row in reader:
                if r in row:
                    #print(r)
                    temp.append(row)
        with open(r+'.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            for i in temp:
                spamwriter.writerow(i)

def scrivi_su_csv(nomefile, list):

    with open(nomefile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        for i in list:
            spamwriter.writerow(i)

def leggi_da_csv(nomefile):
    temp = []
    with open(nomefile, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        for row in spamreader:
            temp.append(row)

    return temp

