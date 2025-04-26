from itertools import permutations
import numpy as np
import Models.Lottomatica as Lottomatica

# funzione per dire quando e' uscito un numero
def calculate_optputs_from_df(df, numero): 
    # prendiamo l'indice della riga che contiene un valore in una determinata colonna
    # la variabile numero e' una lista di numeri
    numbers = np.array(numero)
    outputs = np.array([])

    # se il numero di numeri e' 1
    if len(numbers) == 1:
        for i in df.columns[2:]:
            # aggiungi l'indice della riga che contiene il valore del numero nella colonna i
            outputs = np.append(outputs, df[df[i] == str(numbers[0])].index.values.astype(int))

    # se il numero di numeri e' maggiore di 1
    elif len(numbers) > 1:

        for i in range(len(df)):
            # prendiamo la riga i-esima con le colonne dalla 2 alla 8
            row = df.iloc[i, 2:]
            
            # preniamo tutte le possibili combianzioni di numeri e le mettiamo in una lista
            # e poi verifichiamo se sono uscite
            for j in permutations(row, len(numbers)):
                
                # convertiamo l´array numeri in una turpla di stringhe
                numbers = tuple(map(str, numbers))
                if j == numbers:
                    # se sono uscite, aggiungiamo l'indice della riga alla lista uscite
                    outputs = np.append(outputs, i)
                     
    
    # aggiungiamo ad ogni valore della lista il valore 1
    #uscite = np.sort(uscite + 1)
    outputs = np.sort(outputs)
    return outputs

# funzione per il calcolo dei ritardi
def calculate_delay_from_df(df, numero): 

    # calcoliamo le uscite
    outputs = calculate_optputs_from_df(df, numero)
    # calcuiamo la differenza tra ogni valore della lista e il successivo
    delays = np.diff(outputs)
    # inseriamo al primo posto il valore 0
    delays = np.insert(delays, 0, 0)

    return delays

# funzione per prevedere l'ucita in base ad una spia
def calcola_uscita_da_spia(spia, ruota, n_estr=20):
    temp = Lottomatica.Lotto()
    df_temp = temp.carica_estrazioni(ruota)
    temp.carica_numero([spia], df_temp, n_estr)
    #print(f"spia: {spia}, n_estr: {n_estr}")
    # calcoliamo le uscite
    x = int(temp.elenco_uscite[-1]) - 1
    #print(f"uscita: {temp.elenco_uscite[-1]} uscita -1 : {x}")
    #print(f"return: {len(df_temp) - x}")
    return len(df_temp) - x