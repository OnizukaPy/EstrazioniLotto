import csv
import requests
import zipfile

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

class numero:

    def __init__(self, n):

        self.ritardo = 0
        self.numero = int(n)

    def calcolo_ritardo(self, df):
        ritardo = 0
        posto = ["1", "2", "3", "4", "5"]
        for j in range(len(df)):
            for i in posto:
                if self.numero in df[i][j]:
                    ritardo = 1
                else:

