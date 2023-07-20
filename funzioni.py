import csv
import requests
import zipfile

import os
import sys

PATH = sys.path[0] + '/'
PATH_ESTR = PATH + 'estrazioni/'
def estrai_ruote(filecsv):
    
    #index = [["Data", "Ruota", "1","2","3","4","5"]]
    ruote = ["BA", "FI", "MI", "NA", "PA", "RM", "TO", "VE"]

    for r in ruote:
        #print(r)
        temp = [["Data", "Ruota", "1","2","3","4","5"]]
        with open(filecsv, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                row = row[0].split()
                if r in row:
                    #print(r)
                    temp.append(row)
        with open(PATH_ESTR+r+'.csv', 'w', newline='') as csvfile:
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

# Funzione per scaricare il database dei numeri
def update_archivio():
    
    # download archivio
    url = "https://www.igt.it/STORICO_ESTRAZIONI_LOTTO/storico.zip"
    r = requests.get(url)
    filename = url.split('/')[-1].split('.')[0]
    with open(PATH_ESTR+filename+'.zip', "wb") as zip:
        zip.write(r.content)

    # estrazione del file zip nella cartella estrazioni
    f = zipfile.ZipFile(PATH_ESTR+filename+'.zip', )
    f.extractall(path=PATH_ESTR)
    # elaborazione delle singole ruote dal file generale
    
    with open(PATH_ESTR+filename+'.txt', 'r') as infile, open(PATH_ESTR+filename+'.csv', 'w') as outfile:
        stripped = (line.strip() for line in infile)
        lines = (line.split(",") for line in stripped if line)
        writer = csv.writer(outfile)
        writer.writerows(lines)
        
    estrai_ruote(PATH_ESTR+filename+'.csv')

update_archivio()
