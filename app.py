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

# upload arhivio
fn.update_archivio()


lotto = Lottomatica.Lotto()
lotto.previsioni('MI')
df = lotto.carica_estrazioni('MI')
lotto.carica_numero([17, 10], df, 10)
lotto.calcolo_trend()
#ambo.calcolo_zigzag(40)
lotto.stampa_statistihe()
lotto.print_trend()