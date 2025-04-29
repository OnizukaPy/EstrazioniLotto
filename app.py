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
lotto.set_ruota('MI')
lotto.load_estrazioni()
lotto.get_forecast()
lotto.load_number_statistics([17], 10)
lotto.calculate_trend()
#ambo.calcolo_zigzag(40)
lotto.print_statistics()
lotto.print_trend()