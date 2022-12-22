import csv
import requests
import zipfile
import csv


def estrai_ruote(filecsv):

    #index = [["Data", "Ruota", "1","2","3","4","5"]]
    ruote = ["BA", "FI", "MI", "NA", "PA", "RO", "TO", "VE", "NZ"]

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

# Funzione per scaricare il database dei numeri
def update_archivio():
    # download archivio
    url = "https://www.igt.it/STORICO_ESTRAZIONI_LOTTO/storico.zip"
    r = requests.get(url)
    with open("storico.zip", "wb") as zip:
        zip.write(r.content)

    # estrazione del file zip
    f = zipfile.ZipFile("storico.zip")
    f.extractall()
    # elaborazione delle singole ruote dal file generale
    with open('storico.txt', 'r') as infile, open('storico.csv', 'w') as outfile:
        stripped = (line.strip() for line in infile)
        lines = (line.split(",") for line in stripped if line)
        writer = csv.writer(outfile)
        writer.writerows(lines)
        
    estrai_ruote('storico.csv')

update_archivio()
