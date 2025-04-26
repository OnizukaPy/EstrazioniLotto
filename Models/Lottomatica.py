import pandas as pd
import numpy as np
from itertools import permutations
import pandas_ta as ta
import Lib.Funtions as fn
import Lottomatica.Funtions as Lfn
import Lib.Path as Path

class Lotto:

    def __init__(self, path=Path.PATH_ESTR):
        """Di default il path e' la cartella estrazioni"""
        self.ruota = None
        self.df = None
        self.numero = None
        self.path = path

    def carica_estrazioni(self, ruota):
        """Carica le estrazioni di una ruota in un dataframe"""
        r = self.path+ruota+'.csv'
        estrazioni = fn.leggi_da_csv(r)
        df = pd.DataFrame(estrazioni[1:], columns=estrazioni[0])
        # eliminiamo le righe duplicate
        df.drop_duplicates(inplace=True)
        self.ruota = ruota
        return df

    def carica_numero(self, numero, df, n_estr=10):
        """
        Elabora le informazioni statistiche sul numero e sui numeri inseiriti
        Il numero va inserito come [] di numeri interi
        """
        self.df = df
        self.n_estr = n_estr
        self.numero = numero
        # il totale delle estrazioni e' dato dalla lunghezza del dataframe
        self.totale_estrazioni = len(self.df)
        # calcoliamo le posizioni di indice delle uscite del numero
        self.elenco_uscite = Lfn.calculate_optputs_from_df(self.df, self.numero)
        # il numero totali delle volte che e' uscito e' dato dalla lunghezza della lista
        self.n_uscite = len(self.elenco_uscite)
        if self.n_uscite > 0:
            # il vettore delle frequenze e' dato dal vettore del numero di uscite diviso il vettore dell'indice del vettore stesso + 1
            self.frequenze = self.elenco_uscite / (np.arange(len(self.elenco_uscite))+1)
            # la frequenza media (ultima frequenza o frequenza attuale) e' data dal totale delle estrazioni diviso il numero di uscite
            self.ultima_frequenza = round(float(self.totale_estrazioni/self.n_uscite), 2)
            # l'elenco dei ritardi e' dato dal vettore dei ritardi
            self.ritardi = Lfn.calculate_delay_from_df(self.df, self.numero)
            # il ritardo attuale e' dato dalla differenza tra il totale delle estrazioni e l'indice l'ultima uscita
            self.ritardo_attuale = self.totale_estrazioni - self.elenco_uscite[-1]
            # calcoliamo il ritardo massimo storico
            self.ritardo_massimo = self.ritardi.max()
            # salviamo l'ultimo ritardo
            self.ultimo_ritardo = self.ritardi[-1]
            # calcoliamo la scompensazione
            self.scompensazioni = self.ritardi - self.frequenze
            # calcoliamo la scompensazione attuale e l'ultima scompensazione
            self.ultima_scompensazione = self.scompensazioni.sum()
            self.scompensazione_attuale = self.ultima_scompensazione + (self.ritardo_attuale - self.ultima_frequenza)     
            # calcoliamo le spie
            self.spia_num, self.spia_rip = self.spia()
            # salviamo le statistiche in un dizionario
        else:
            self.frequenze = np.nan
            self.ultima_frequenza = np.nan
            self.ritardi = np.nan
            self.ritardo_attuale = np.nan
            self.ritardo_massimo = np.nan
            self.ultimo_ritardo = np.nan
            self.scompensazioni = np.nan
            self.ultima_scompensazione = np.nan
            self.scompensazione_attuale = np.nan
            self.spia_num, self.spia_rip, self.spia_estr = np.nan, np.nan, np.nan
            print(f'{self.numero}, non è mai uscito')

        self.statistiche = {
            'ruota': self.ruota,
            'numero': self.numero,
            'n_uscite': self.n_uscite,
            'totale_estrazioni': self.totale_estrazioni,
            'ultima_frequenza': self.ultima_frequenza,
            'ritardo_attuale': self.ritardo_attuale,
            'ritardo_massimo': self.ritardo_massimo,
            'ultimo_ritardo': self.ultimo_ritardo,
            'ultima_scompensazione': self.ultima_scompensazione,
            'scompensazione_attuale': self.scompensazione_attuale,
            'spia_num': self.spia_num,
            'spia_rip': self.spia_rip,
            'spia_estr': self.n_estr
        }
        
    def stampa_statistihe(self):
        
        for k, v in self.statistiche.items():
            print(f'{k}: {v}')

    def spia(self):
        t = np.array([])
        for i in self.elenco_uscite:
            i = int(i) - 2
            t = np.append(t, self.df.iloc[i-self.n_estr:i, 2:].values)
        pf = pd.DataFrame(columns=['n_spia', 'rip'])
        pf['n_spia'], pf['rip'] = np.unique(t.flatten(), return_counts=True)
        pf.sort_values(by=['rip'], inplace=True)
        u, c = pf.iloc[-1]
        return u, c
    
    def calcolo_zigzag(self, percentage):
        """
        Calcola il grafico a zigzag
        """

        # Calcola i punti ZigZag
        zigzag_result = fn.zigzag(self.df_trend, percentage)

        # salviamo i punti ZigZag nel dataframe
        self.df_trend['zigzag'] = np.nan
        for index, value, pivot_type in zigzag_result:
            self.df_trend.loc[index, 'zigzag'] = value

        
        # Stampa i risultati
        print("Punti ZigZag trovati:")
        for point in zigzag_result:
            index, value, pivot_type = point
            timestamp = self.df_trend["close"].iloc[index]
            print(f"Indice: {index}, Timestamp: {timestamp}, Valore: {value}, Tipo: {pivot_type}")
        

    def calcolo_trend(self):

        l10 = 10
        l30 = 30 

        try:
            # utilizzo le funzioni di pandas_ta per calcolare il trend della scompensazione
            self.df_trend = pd.DataFrame()
            self.df_trend['scompensi'] = self.scompensazioni
            # aggiungo la colonna close perche' la funzione ta.sma la richiede
            self.df_trend['close'] = self.df_trend['scompensi'].cumsum()
            sma10 = self.df_trend.ta.sma(length=l10)
            sma30 = self.df_trend.ta.sma(length=l30)
            self.df_trend = pd.concat([self.df_trend, sma10, sma30], axis=1)
            self.df_trend['scomp_sigLine'] = np.where(self.df_trend['SMA_10'] > self.df_trend['SMA_30'], 1, 0 )
            self.df_trend['scomp_position'] = self.df_trend['scomp_sigLine'].diff()
            self.df_trend["Status"] = np.where(self.df_trend['scomp_sigLine'] == 0, 'F', 'R')
            self.trend = self.df_trend['Status'].iloc[-1]
            self.statistiche['trend'] = self.trend

        except:
            print('Impossibile calcolare il trend')
            self.statistiche['trend'] = np.nan

    def print_trend(self):
        if self.statistiche['trend'] is not np.nan:
            fn.plot_graph(self.df_trend[['close', 'SMA_10', 'SMA_30']])
        #print(self.df_trend.columns)

    def previsioni(self, ruota):

        temp = self.carica_estrazioni(ruota)
        df = pd.DataFrame()

        # calcoliamo le previsioni
        for i in range(1, 91):

            self.carica_numero([i], temp)
            self.calcolo_trend()
            nuovo_df = pd.DataFrame([self.statistiche])
            df = pd.concat([df, nuovo_df], ignore_index=True)
            #df = df.append(self.statistiche, ignore_index=True)
        
        df = df[(df['ritardo_attuale'] < 15) & (df['scompensazione_attuale'] < 0) & (df['trend'] == 'F')].sort_values(by='ultima_frequenza', ascending=False)
        self.previsione = df['numero'].values
        # stampiamo le previsioni con un ciclo for
        lista = []
        for i in range(len(self.previsione)):
            lista.append(self.previsione[i])
        print(f"i numeri da giocare su {ruota} sono: {lista}")
        #return f"i numeri da giocare su {ruota} sono: {self.previsione}"