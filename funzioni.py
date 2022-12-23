import csv
import requests
import zipfile


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
    filename = url.split('/')[-1].split('.')[0]
    with open(filename+'.zip', "wb") as zip:
        zip.write(r.content)

    # estrazione del file zip
    f = zipfile.ZipFile(filename+'.zip')
    f.extractall()
    # elaborazione delle singole ruote dal file generale
    with open(filename+'.txt', 'r') as infile, open(filename+'.csv', 'w') as outfile:
        stripped = (line.strip() for line in infile)
        lines = (line.split(",") for line in stripped if line)
        writer = csv.writer(outfile)
        writer.writerows(lines)
        
    estrai_ruote(filename+'.csv')

update_archivio()
