import csv
from matplotlib import pyplot as plt
import requests
import zipfile

import os

# salviamo il path della cartella corrente
# in modo da non doverlo scrivere ogni volta
from Lib.Path import PATH, PATH_ESTR

def estrai_ruote(filecsv):
    
    #index = [["Data", "Ruota", "1","2","3","4","5"]]
    ruote = ["BA", "CA", "FI", "GE", "MI", "NA", "PA", "RM", "TO", "VE", "RN"]

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

# creiamo una funzione per calcolare e massimi e minimi relativi per fare un grafico a zigzag
def zigzag(df, percentage):
    """
    Calcola l'indicatore ZigZag su una colonna di un DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame contenente i dati
        column_name (str): Nome della colonna da analizzare
        percentage (float): Soglia percentuale per identificare i pivot (es. 5 per 5%)
    
    Returns:
        list: Lista di tuple (indice, valore, tipo) dove tipo è 'High' o 'Low'
    """
    # Estrai la colonna come lista di valori
    data = df["close"].tolist()
    
    if not data or len(data) < 2:
        return []

    zigzag_points = []
    last_pivot = data[0]
    last_pivot_index = 0
    direction = None  # None: iniziale, 1: crescente, -1: decrescente

    for i in range(1, len(data)):
        value = data[i]
        
        # Calcola la variazione percentuale rispetto all'ultimo pivot
        # Evita divisione per zero usando un valore piccolo se last_pivot è 0
        if last_pivot == 0:
            change = float('inf') if value != 0 else 0
        else:
            change = abs((value - last_pivot) / last_pivot * 100)
        
        if change >= percentage:
            if direction is None:
                # Primo pivot dopo l'inizio
                if value > last_pivot:
                    zigzag_points.append((last_pivot_index, last_pivot, "Low"))
                    direction = 1
                elif value < last_pivot:
                    zigzag_points.append((last_pivot_index, last_pivot, "High"))
                    direction = -1
                last_pivot = value
                last_pivot_index = i
                
            elif direction == 1 and value < last_pivot:
                # Cambio da crescente a decrescente
                zigzag_points.append((last_pivot_index, last_pivot, "High"))
                direction = -1
                last_pivot = value
                last_pivot_index = i
                
            elif direction == -1 and value > last_pivot:
                # Cambio da decrescente a crescente
                zigzag_points.append((last_pivot_index, last_pivot, "Low"))
                direction = 1
                last_pivot = value
                last_pivot_index = i
                
            elif (direction == 1 and value > last_pivot) or (direction == -1 and value < last_pivot):
                # Aggiorna il pivot se continua nella stessa direzione
                last_pivot = value
                last_pivot_index = i

    # Aggiungi l'ultimo punto se significativo
    if last_pivot_index != len(data) - 1:
        last_value = data[-1]
        if last_pivot == 0:
            change = float('inf') if last_value != 0 else 0
        else:
            change = abs((last_value - last_pivot) / last_pivot * 100)
        if change >= percentage:
            zigzag_points.append((last_pivot_index, last_pivot, "High" if direction == 1 else "Low"))

    return zigzag_points

# Funzione per plottare i grafici
def plot_graph(pf):

    pf = pf.astype(float)
    plt.rcParams["figure.figsize"] = (36, 30)
    # plt.rcParams["savefig.format"] = 'png'  

    # plotting di tutte le curve 
    plt.plot(pf['close'][:], color='blue', label='Scompensazione')
    # plotting zigzag che è un grafico linee di punti
    #plt.plot(pf.index, pf["zigzag"], label="zigzag", color='black', linewidth=1)

    # plotting medie mobili
    plt.plot(pf["SMA_10"][:], color='red', label='SMA_10')
    plt.plot(pf["SMA_30"][:], color='green', label='SMA_30')

    # configuraione degli assi
    plt.xlabel('Numero uscita', fontsize=18)
    plt.ylabel('Scompensazione', fontsize=18)

    # configurazioni del titolo, leggende, griglia
    plt.title('GRAFICO', fontsize=20)
    plt.legend()
    plt.grid()
    plt.show()

# Funzione per scaricare il database dei numeri
def update_archivio():
    
    # download archivio
    url = "https://www.igt.it/STORICO_ESTRAZIONI_LOTTO/storico.zip"
    r = requests.get(url)
    filename = url.split('/')[-1].split('.')[0]
    # creazione della cartella estrazioni se non esiste
    if not os.path.exists(PATH_ESTR):
        os.makedirs(PATH_ESTR)
    # creazione del file zip
    # se esiste lo cancella
    if os.path.exists(PATH_ESTR+filename+'.zip'):
        os.remove(PATH_ESTR+filename+'.zip')
    # scrittura del file zip
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

def progress(num=0, den=100, width=30):
    num = int(num)
    den = int(den)
    width = int(width)
    percent = num / den * 100
    left = width * num // den
    right = width - left
    print('\r[', '#' * left, ' ' * right, ']',
          f' {percent: .0f}%', sep='', end='', flush=True)