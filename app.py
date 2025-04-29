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
lotto.load_estrazioni()
lotto.load_forecast()
lotto.load_number_statistics([17], 10)
lotto.calculate_trend()
#ambo.calcolo_zigzag(40)
lotto.print_statistics()
lotto.print_trend()