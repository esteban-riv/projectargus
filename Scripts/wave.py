#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 16:23:27 2021

@author: estebanrivera
"""
from scipy import signal
from scipy.fft import fftshift
import matplotlib.pyplot as plt
import pandas as pd
from Scripts.datosadash import datosADASH
import re
import os
import pandas as pd
import numpy as np
import pywt


diag = pd.read_csv('Data/diagnosis.csv')
spectro_diag = pd.DataFrame(columns=['file','time'])
                            
# We select the folder where waveforms are and get machine, points and files
path = 'Data/Export'

folder = datosADASH(path)
machines = folder.getmachines()
points = folder.getpoints()
files = folder.getfiles()

# First we create a folder to save Wavelets
try:
    os.mkdir('Data/Export/Wavelets')
except FileExistsError:
    pass


secador1 = {}

for key, value in points.items():
    if key.startswith('S6'):
        secador1[key]=value
        

counter = 0


# Wavelets and power spectrums are generated with pywt
for machine, points_iter in secador1.items():
    
    filteredmachines = list(filter(lambda x: machine in x, files))
    print("Maquina {} - {}".format(machine, counter))
    counter = counter + 1
    for iteration, point in enumerate(points_iter):
        acc_spec_text = "Aceleracion - Forma"
        filteredpoints = list(filter(lambda x: point in x, filteredmachines))
        filteredcsv = list(filter(lambda x:".csv" in x, filteredpoints))
                        
        # Get files by type of measurement
        accspec = list(filter(lambda x:acc_spec_text in x, filteredcsv))
                
                
        for filetime in accspec:
            forma = pd.read_csv(filetime, skiprows=1,
                                        delimiter=";", encoding = "ISO-8859-1")
            forma = forma.rename(columns={'time[ms]':'time',
                                                  ' amplitude[g]':'amplitude'})
            date = pd.read_csv(filetime, nrows=0,
                                        delimiter=";", encoding = "ISO-8859-1").columns[1][6:]
            
            
            time = forma['time']
            sst = forma['amplitude']
            dt = time[1] - time[0]

            wavelet = 'cmor1.5-1.0'
            scales = np.arange(1, 128)

            [cfs, frequencies] = pywt.cwt(sst, scales, wavelet, dt)
            power = (abs(cfs)) ** 2

            period = 1. / frequencies
            levels = [0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8]
            dpi = 96


            f, ax = plt.subplots(1, figsize=(400/dpi, 400/dpi))
            f.subplots_adjust(left=0,right=1,bottom=0,top=1)
            ax.contourf(time, np.log2(period), np.log2(power), np.log2(levels),
                        extend='both')
            ax.invert_yaxis()
            ax.axis('off')
            
            
            date_sub = re.sub('[^A-Za-z0-9]+','', date)    
             
            filename = str(date_sub) + "_" + str(machine) + "_" + str(point)
            filename = filename.replace('\\','/')
            folder = "Wavelets"
            filename = os.path.join(path, folder, filename)
            filename = filename.replace('\\','/')
            
            
            f.savefig(filename, transparent=True, pad_inches=0.0,
                                figsize=(96/96, 96/96), dpi=96)
            
            plt.close()
            
            
            spectro_diag = spectro_diag.append({"file":filename,
                                                "time":date,
                                                "machine":machine
                                                }, ignore_index=True)