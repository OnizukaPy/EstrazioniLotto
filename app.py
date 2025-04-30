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
import Models.Ruote as Rt
from Lib.Path import PATH_ESTR

# upload arhivio
# chiediamo all'utente se vuole aggiornare l'archivio
update = input("Vuoi aggiornare l'archivio? (s/n): ").lower()
if update == 's':
    # scarichiamo l'archivio
    fn.update_archivio()

ruota = "MI"
""" ruote = Rt.RUOTE

for rt in ruote:
    # estraiamo le ruote
    temp = Lottomatica.Lotto()
    temp.set_ruota(rt)
    temp.load_estrazioni()
    temp.load_forecast() """

lotto = Lottomatica.Lotto()
lotto.set_ruota(ruota)
lotto.set_estrazioni()
lotto.load_forecast()

# elenco delle previsioni
previsioni = lotto.get_forecast()

# settiamo il numero di estrazioni
n_estr = 10
col = f'tra{n_estr}'

# creiamo un dataframe vuoto per le previsioni
df_previsioni = pd.DataFrame(columns=['ruota', 'numero', 'n_uscite', 'totale_estrazioni', 'frequenza_attuale', 'ritardo_attuale', 'ritardo_massimo', 'ultimo_ritardo', 'ultima_scompensazione', 'scompensazione_attuale', 'spia_num', 'spia_rip', col, 'spia_estr'])


for numero in previsioni:
    lotto2 = Lottomatica.Lotto()
    lotto2.set_ruota(ruota)
    lotto2.set_estrazioni()
    lotto2.set_number_statistics(numero, n_estr)
    lotto2.calculate_trend()
    # otteniamo le statistiche
    stats = lotto2.get_statistics()
    stats[col] = n_estr - Lfn.calcola_uscita_da_spia(stats['spia_num'], ruota, n_estr)
    # creiamo una nuova riga con le statistiche
    df_temp = pd.DataFrame(stats)
    df_temp = df_temp.dropna(axis=1, how='all') # Rimuove le colonne con tutti NaN
    if not df_temp.empty:
        df_previsioni = pd.concat([df_previsioni, df_temp], ignore_index=True)
    else:
        print("Attenzione: Dopo la rimozione delle colonne vuote, il DataFrame è vuoto.")
    #df_previsioni = pd.concat([df_previsioni, pd.DataFrame(stats)], ignore_index=True)

print(df_previsioni)
print()

# salviamo solo le righe che hanno la colonna tra20 > 0 
df_previsioni = df_previsioni[df_previsioni[col] > 0]

print(df_previsioni)
print()

# salviamo solo le righe che hanno un ritardo attuale maggiore della differenza  20 - tra20
df_previsioni = df_previsioni[df_previsioni['ritardo_attuale'] > (n_estr - df_previsioni[col])]

# ordiniamo il dataframe in base alla colonna tra20
df_previsioni = df_previsioni.sort_values(by=col, ascending=False)

print(df_previsioni)


""" lotto.load_number_statistics([17], 10)
lotto.calculate_trend()
#ambo.calcolo_zigzag(40)
lotto.print_statistics()
lotto.print_trend() """