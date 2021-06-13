# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 15:03:16 2021

@author: Esteban
"""

import pandas as pd
import json
import os
from fpdf import FPDF

# Lectura de dataframes
df = pd.read_csv("../data/valores.csv",sep=";", decimal=",",parse_dates=[['Date', 'Time']])

df.rename(columns = {"Tree Level 1":"Zona", "Tree Level 2":"Maquina","Tree Level 3":"Punto","Reading": "Valor", "Date":"Fecha" }, inplace = True)
df = df.set_index('Date_Time')
#df = df.sort_index(inplace=True)

# Pruebas iniciales
equipos = df.Maquina.unique()
df_m2 = df[df['Maquina']=='S1-M32']
df_m2 = df_m2[df_m2['Unit']=='mm/s']
df_m2 = df_m2[df_m2['Punto']=='V-LA-H']
df_m2 = df_m2.sort_index()

vector = pd.Series([])

#Para la obtención de los parámetros 
for equipo in equipos:
    for punto in df[df['Maquina']==equipo].Punto.unique():
        df_calculo_talaf = df[(df['Maquina']==equipo)
                              & (df['Punto']==punto)
                              & (df['Measurement'].str.contains('Ac'))]
        
        df_calculo_talaf = df_calculo_talaf.sort_index()       
        valor_incial = df_calculo_talaf.Valor.iloc[0]
        #Cálculo dummy para prueba
        calculo = df_calculo_talaf['Valor'] / valor_incial
        vector = vector.append(calculo)

#Ya con los valores los inserto en el dataframe
df_vector = pd.DataFrame(vector, columns=['Parametro'])
df_acc = df[df['Measurement'].str.contains('Ac')]
df_result = pd.concat([df_acc, df_vector], axis=1)
df_result = df_result.sort_values(['Maquina','Punto'])




pdf = FPDF()



''' FIRST PAGE '''
pdf.add_page()
pdf.set_font('Arial', 'B', 8)


pdf.cell(50, 10, 'Punto', 1, 0, 'C')
pdf.cell(40, 10, 'Medida', 1, 0, 'C')
pdf.cell(40, 10, 'Valor', 1, 2, 'C')
pdf.cell(-90)

for i in range(0, len(df_result)):
    pdf.cell(50, 10, '%s' % (df_result['Punto'].iloc[i]), 1, 0, 'C')
    pdf.cell(40, 10, '%s' % (str(df_result.Measurement.iloc[i])), 1, 0, 'C')
    pdf.cell(40, 10, '%s' % (str(df_result.Valor.iloc[i].round(2))), 1, 2, 'C')
    pdf.cell(-90)
pdf.cell(90, 10, " ", 0, 2, 'C')
pdf.cell(-30)
pdf.output('test.pdf', 'F')
