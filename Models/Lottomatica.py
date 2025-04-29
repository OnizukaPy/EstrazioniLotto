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
        self._ruota = None
        self._df = None
        self._numero = None
        self._path = path

        # inizializziamo le variabili statistiche
        self._totale_estrazioni = np.nan
        self._elenco_uscite = np.nan
        self._n_uscite = np.nan
        self._frequenze = np.nan
        self._ultima_frequenza = np.nan
        self._ritardi = np.nan
        self._ritardo_attuale = np.nan
        self._ritardo_massimo = np.nan
        self._ultimo_ritardo = np.nan
        self._scompensazioni = np.nan
        self._ultima_scompensazione = np.nan
        self._scompensazione_attuale = np.nan

        # variabili per le spie
        self._n_estr = None
        self._spia_num, self._spia_rip, self._spia_estr = np.nan, np.nan, np.nan

        # inizializziamo le variabili di statistica globali
        self._statistiche = None
        self._df_trend = None
        self._previsione = None

    def set_ruota(self, ruota):
        """Setta la ruota"""
        self._ruota = ruota

    def load_estrazioni(self):
        """Carica le estrazioni di una ruota in un dataframe"""
        r = self._path+self._ruota+'.csv'
        estrazioni = fn.leggi_da_csv(r)
        df = pd.DataFrame(estrazioni[1:], columns=estrazioni[0])
        # eliminiamo le righe duplicate
        df.drop_duplicates(inplace=True)
        self._df = df
        #return df
    
    def get_estrazioni(self):
        """Restituisce il dataframe delle estrazioni"""
        return self._df
    
    def get_uscite(self):
        """Restituisce il numero di uscite"""
        return self._n_uscite

    def get_spia(self):
        """Restituisce la spia"""
        return self._spia_num, self._spia_rip

    def load_number_statistics(self, numero, n_estr=10):
        """
        Elabora le informazioni statistiche sul numero e sui numeri inseiriti
        Il numero va inserito come [] di numeri interi
        """
        #self.df = df
        self._n_estr = n_estr
        self._numero = numero
        # il totale delle estrazioni e' dato dalla lunghezza del dataframe
        self._totale_estrazioni = len(self._df)
        # calcoliamo le posizioni di indice delle uscite del numero
        self._elenco_uscite = Lfn.calculate_optputs_from_df(self._df, self._numero)
        # il numero totali delle volte che e' uscito e' dato dalla lunghezza della lista
        self._n_uscite = len(self._elenco_uscite)
        if self._n_uscite > 0:
            # il vettore delle frequenze e' dato dal vettore del numero di uscite diviso il vettore dell'indice del vettore stesso + 1
            self._frequenze = self._elenco_uscite / (np.arange(len(self._elenco_uscite))+1)
            # la frequenza media (ultima frequenza o frequenza attuale) e' data dal totale delle estrazioni diviso il numero di uscite
            self._ultima_frequenza = round(float(self._totale_estrazioni/self._n_uscite), 2)
            # l'elenco dei ritardi e' dato dal vettore dei ritardi
            self._ritardi = Lfn.calculate_delay_from_df(self._df, self._numero)
            # il ritardo attuale e' dato dalla differenza tra il totale delle estrazioni e l'indice l'ultima uscita
            self._ritardo_attuale = self._totale_estrazioni - self._elenco_uscite[-1]
            # calcoliamo il ritardo massimo storico
            self._ritardo_massimo = self._ritardi.max()
            # salviamo l'ultimo ritardo
            self._ultimo_ritardo = self._ritardi[-1]
            # calcoliamo la scompensazione
            self._scompensazioni = self._ritardi - self._frequenze
            # calcoliamo la scompensazione attuale e l'ultima scompensazione
            self._ultima_scompensazione = self._scompensazioni.sum()
            self._scompensazione_attuale = self._ultima_scompensazione + (self._ritardo_attuale - self._ultima_frequenza)     
            # calcoliamo le spie
            self._spia_num, self._spia_rip = self.set_spia_numbers()
            # salviamo le statistiche in un dizionario
        else:

            print(f'{self._numero}, non è mai uscito')

        self._statistiche = {
            'ruota': self._ruota,
            'numero': self._numero,
            'n_uscite': self._n_uscite,
            'totale_estrazioni': self._totale_estrazioni,
            'ultima_frequenza': self._ultima_frequenza,
            'ritardo_attuale': self._ritardo_attuale,
            'ritardo_massimo': self._ritardo_massimo,
            'ultimo_ritardo': self._ultimo_ritardo,
            'ultima_scompensazione': self._ultima_scompensazione,
            'scompensazione_attuale': self._scompensazione_attuale,
            'spia_num': self._spia_num,
            'spia_rip': self._spia_rip,
            'spia_estr': self._n_estr
        }
        
    def print_statistics(self):
        
        for k, v in self._statistiche.items():
            print(f'{k}: {v}')

    def set_spia_numbers(self):
        t = np.array([])
        for i in self._elenco_uscite:
            i = int(i) - 2
            t = np.append(t, self._df.iloc[i-self._n_estr:i, 2:].values)
        pf = pd.DataFrame(columns=['n_spia', 'rip'])
        pf['n_spia'], pf['rip'] = np.unique(t.flatten(), return_counts=True)
        pf.sort_values(by=['rip'], inplace=True)
        u, c = pf.iloc[-1]
        return u, c
    
    def calculate_zigzag_indicator(self, percentage):
        """
        Calcola il grafico a zigzag
        """

        # Calcola i punti ZigZag
        zigzag_result = fn.zigzag(self._df_trend, percentage)

        # salviamo i punti ZigZag nel dataframe
        self._df_trend['zigzag'] = np.nan
        for index, value, pivot_type in zigzag_result:
            self._df_trend.loc[index, 'zigzag'] = value

        
        # Stampa i risultati
        print("Punti ZigZag trovati:")
        for point in zigzag_result:
            index, value, pivot_type = point
            timestamp = self._df_trend["close"].iloc[index]
            print(f"Indice: {index}, Timestamp: {timestamp}, Valore: {value}, Tipo: {pivot_type}")
        

    def calculate_trend(self):

        l10 = 10
        l30 = 30 

        try:
            # utilizzo le funzioni di pandas_ta per calcolare il trend della scompensazione
            self._df_trend = pd.DataFrame()
            self._df_trend['scompensi'] = self._scompensazioni
            # aggiungo la colonna close perche' la funzione ta.sma la richiede
            self._df_trend['close'] = self._df_trend['scompensi'].cumsum()
            sma10 = self._df_trend.ta.sma(length=l10)
            sma30 = self._df_trend.ta.sma(length=l30)
            self._df_trend = pd.concat([self._df_trend, sma10, sma30], axis=1)
            self._df_trend['scomp_sigLine'] = np.where(self._df_trend['SMA_10'] > self._df_trend['SMA_30'], 1, 0 )
            self._df_trend['scomp_position'] = self._df_trend['scomp_sigLine'].diff()
            self._df_trend["Status"] = np.where(self._df_trend['scomp_sigLine'] == 0, 'F', 'R')
            self._trend = self._df_trend['Status'].iloc[-1]
            self._statistiche['trend'] = self._trend

        except:
            print('Impossibile calcolare il trend')
            self._statistiche['trend'] = np.nan

    def print_trend(self):
        if self._statistiche['trend'] is not np.nan:
            fn.plot_graph(self._df_trend[['close', 'SMA_10', 'SMA_30']])
        #print(self.df_trend.columns)

    def get_forecast(self):

        #temp = self.carica_estrazioni(ruota)
        df = pd.DataFrame()

        # calcoliamo le previsioni
        for i in range(1, 91):

            self.load_number_statistics([i])
            self.calculate_trend()
            nuovo_df = pd.DataFrame([self._statistiche])
            df = pd.concat([df, nuovo_df], ignore_index=True)
            #df = df.append(self.statistiche, ignore_index=True)
        
        df = df[(df['ritardo_attuale'] < 15) & (df['scompensazione_attuale'] < 0) & (df['trend'] == 'F')].sort_values(by='ultima_frequenza', ascending=False)
        self._previsione = df['numero'].values
        # stampiamo le previsioni con un ciclo for
        lista = []
        for i in range(len(self._previsione)):
            lista.append(self._previsione[i])
        print(f"i numeri da giocare su {self._ruota} sono: {lista}")
        #return f"i numeri da giocare su {ruota} sono: {self.previsione}"