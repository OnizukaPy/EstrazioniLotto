# importazione delle librerie
import pandas as pd
import pandas_ta as ta
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from itertools import combinations, permutations

import Lib.Funtions as fn
import Lottomatica.Funtions as Lfn
import Models.Lottomatica as Lottomatica
from Lib.Path import PATH_ESTR

# creiamo una lista in numpy con tutti gli ambi in 90 numeri
numeri = np.arange(1,91)
ambi = np.array(list(combinations(numeri,2)))
print(len(ambi))

# creiamo in dataframe contenenti tutti gli ambi e il loro numero spia a 5, 10 e 20 estrazioni
dataframe = pd.DataFrame(columns=['Ambi', 'uscite', 'Spia10', 'rip10', 'tra10','Spia20', 'rip20', 'tra20'])
n = Lottomatica.Lotto()
count = 1
n.set_ruota('MI')
n.load_estrazioni()
for i in ambi:
    i = list(map(int, i))
    #print(f"Coppia di numeri: {i}")
    n.load_number_statistics(i, 10)
    n_uscite = n.get_uscite()
    spia10, rip10 = n.get_spia()
    # calcoliamo il ritardo dell'uscita della spia (se è negativa significa che è in ritardo)
    tra10 = 10 - Lfn.calcola_uscita_da_spia(spia10, 'MI', 10)
    n.load_number_statistics(i, 20)
    spia20, rip20 = n.get_spia()
    # calcoliamo il ritardo dell'uscita della spia (se è negativa significa che è in ritardo)
    tra20 = 20 - Lfn.calcola_uscita_da_spia(spia20, 'MI', 20)

    nuova_riga = pd.DataFrame({
        'Ambi': [i],
        'uscite': [n_uscite],
        'Spia10': [spia10],
        'rip10': [rip10],
        'tra10': [tra10],
        'Spia20': [spia20],
        'rip20': [rip20],
        'tra20': [tra20]
    })

    dataframe = pd.concat([dataframe, nuova_riga], ignore_index=True)

    # salviamo in un file csv in modalità append
    dataframe.to_csv(PATH_ESTR+'ambi.csv', mode='w', index=False, header=True)

    fn.progress(num=count, den=len(ambi), width=30)
    count+=1

dataframe.head(100)