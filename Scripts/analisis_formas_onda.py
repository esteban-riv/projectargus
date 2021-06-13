# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 15:00:44 2021

@author: Esteban
"""

import pandas as pd
from scipy.fft import rfft, rfftfreq
from scipy.stats import kurtosis, skew
import numpy as np
from matplotlib import pyplot as plt
import os
from datosadash import datosADASH
import itertools
import datetime
from fpdf import FPDF
import pandas as pd



nombres_columnas = ['tiempo', 'amplitud']


forma = pd.read_csv('../data/m30acc.csv', skiprows=1, delimiter=";")
forma = forma.rename(columns={'time[ms]':'time', ' amplitude[g]':'amplitude'})

SAMPLE_RATE = 16384  
DURATION = 0.5
N = int(SAMPLE_RATE * DURATION)




# Obtención de espectro
yf = rfft(forma['amplitude'])
xf = rfftfreq(N, 1 / SAMPLE_RATE)


# Obtención de indicadores

## Fórmula para obtención de factor de cresta
def crest_factor(column):
    return abs(np.max(np.abs(column))/np.sqrt(np.mean(np.square(column))))


def maximo(column):
    return max(abs(column))

def media(column):
    return np.mean(abs(column))

def rms(column):
    return np.sqrt(np.mean(abs(column)))

def kurtosis_col(column):
    return abs(kurtosis(column))

def skewness(column):
    return skew(column)

def obtener_valores(column):
    maximo_value = maximo(column)
    media_value = media(column)
    rms_value = rms(column)
    crest_factor_value = crest_factor(column)
    kurtosis_value = abs(kurtosis(column))
    skewnewss_value = skewness(column)
    
    return [maximo_value, media_value, rms_value, kurtosis_value, crest_factor_value]
    


# Lectura de todos los archivos
rootdir = r'C:\Users\Esteban\Desktop\Proyecto KSCHOOL\Data\Zona 2 S-1 [1649]'

datos = datosADASH(rootdir)        
archivos = datos.getfiles()
maquinas = datos.getmachines()
puntos = datos.getpoints()  


# Para pruebas 

puntos = dict(itertools.islice(puntos.items(), 2))



pdf = FPDF()



''' FIRST PAGE '''
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.image('teromanager.jpg')






#Bucle para la creación de gráficos y subida
for maquina,puntos in puntos.items():
    pdf.add_page()

    for indice, punto in enumerate(puntos):
        if indice > 0 and indice % 2 == 0 :
            pdf.add_page()
            
        
        # Obtención de los archivos
        FiltradoMaquinas = list(filter(lambda x: maquina in x, archivos))
        FiltradoPuntos = list(filter(lambda x:punto in x, FiltradoMaquinas))
        FiltradoCSV = list(filter(lambda x:".csv" in x, FiltradoPuntos))
        VELTIME = list(filter(lambda x:"Velocidad - Forma de onda" in x, FiltradoCSV))
        VELFFT = list(filter(lambda x:"Velocidad - Espectro" in x, FiltradoCSV))
        ACCTIME = list(filter(lambda x:"Aceleracion - Forma de onda" in x, FiltradoCSV))
        ACCFFT = list(filter(lambda x:"Aceleracion - Espectro" in x, FiltradoCSV))
        
        
        df_time = pd.read_csv(VELTIME[0], skiprows=[0], delimiter=";",
                              decimal=".", encoding = "ISO-8859-1")
        
        columna_vel = df_time.iloc[:,1]        
    
        
        valores_vel = obtener_valores(columna_vel) 
        indicadores = ['MAX', 'MEAN', 'RMS', 'KU', 'CF']       
      
        
        
        
        fecha_df_time = pd.read_csv(VELTIME[0], nrows=1, header=None,
                                    delimiter=";", decimal=".",
                                    encoding = "ISO-8859-1").iloc[0,1][6:]
        fecha_df_time = datetime.datetime.strptime(fecha_df_time, '%Y-%m-%d %H:%M:%S.%f')
        
        df_FFT = pd.read_csv(VELFFT[0], skiprows=[0], delimiter=";",
                             decimal=".", encoding = "ISO-8859-1")
        
       
        
        df_time_A = pd.read_csv(ACCTIME[0], skiprows=[0], delimiter=";",
                                decimal=".", encoding = "ISO-8859-1")
        
        
        columna_acc = df_time_A.iloc[:,1]
        valores_acc = obtener_valores(columna_acc) 
    
    
        
        df_FFT_A = pd.read_csv(ACCFFT[0], skiprows=[0], delimiter=";",
                               decimal=".", encoding = "ISO-8859-1")
        

        
        fig, axes = plt.subplots(3,3, figsize=(12,7))
        fig.suptitle("Maquina: {} - Punto: {} - Fecha {}".format(maquina,
                                                                 punto, fecha_df_time), fontsize=14)
        
        axes[0,0].set_title("Forma de onda Velocidad")
        axes[0,0].plot(df_time['time[ms]'], df_time[' amplitude[mm/s]'])
        
        axes[0,1].set_title("Espectro Velocidad")
        axes[0,1].plot(df_FFT['frequency[Hz]'], df_FFT[' amplitude[mm/s RMS]'])
        

        axes[0,2].set_title("Valores")        
        axes[0,2].bar(indicadores,valores_vel)

        
        axes[1,0].set_title("Forma de onda Aceleración")
        axes[1,0].plot(df_time_A['time[ms]'], df_time_A[' amplitude[g]'])
        
  
        axes[1,1].set_title("Espectro Aceleración")
        axes[1,1].plot(df_FFT_A['frequency[Hz]'], df_FFT_A[' amplitude[g RMS]'])
        
        axes[1,2].set_title("Valores") 
        axes[1,2].bar(indicadores,valores_acc)
        
        # Habria que cambiar por DEMOD
        axes[2,0].set_title("Forma de onda Aceleración")
        axes[2,0].plot(df_time_A['time[ms]'], df_time_A[' amplitude[g]'])
        
        axes[2,1].set_title("Espectro Aceleración")
        axes[2,1].plot(df_FFT_A['frequency[Hz]'], df_FFT_A[' amplitude[g RMS]'])
        
        axes[2,2].set_title("Valores") 
        axes[2,2].bar(indicadores,valores_acc)
        
 
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        filename = str(maquina) + str(punto) +'.png'
        plt.savefig(filename)
        plt.show()
        
        plt.close()

        if indice % 2 == 0:  
            pdf.cell(40, 10, maquina)
            pdf.image(str(filename), 5, 30, w=200)
        else:            
            pdf.image(str(filename), 5, 160, w=200)
            
        os.remove(filename) 


pdf.output('tuto2.pdf', 'F')
        
    
        