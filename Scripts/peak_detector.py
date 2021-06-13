# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 19:26:16 2021

@author: Esteban
"""
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


# Lectura del csv obtenido de SECADERO 1 - M32
df_bad = pd.read_csv('../data/acc_spec.csv', skiprows=1, delimiter=";", encoding = "ISO-8859-1")
df_good = pd.read_csv('../data/acc_spec_good.csv', skiprows=1, delimiter=";", encoding = "ISO-8859-1")
df_bad_2 = pd.read_csv('../data/acc_spec_bad_2.csv', skiprows=1, delimiter=";", encoding = "ISO-8859-1")

def rename_columns(df):
    df = df.rename(columns={'frequency[Hz]':'freq',' amplitude[g RMS]':'amp'})
    return df

def peak_detection(df):
    # Detección de picos, genera un vector de picos y un diccionario de parámetros
    peaks, parameters = find_peaks(df['amp'], height=0.08, distance=25)  


    # Para pintarlos multiplico por 2 dada la resolución espectral
    plt.plot(df['freq'], df['amp'])
    plt.plot(peaks*2, df['amp'][peaks], "x")
    plt.show()
    print(len(peaks))



df_bad = rename_columns(df_bad)
df_good = rename_columns(df_good)
df_bad_2 = rename_columns(df_bad_2)

peak_detection(df_bad)
peak_detection(df_bad_2)
peak_detection(df_good)