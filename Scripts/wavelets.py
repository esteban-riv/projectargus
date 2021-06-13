#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 10:52:00 2021

@author: estebanrivera
"""

from scipy import signal
from scipy.fft import fftshift
import matplotlib.pyplot as plt
import pandas as pd
from datosadash import datosADASH
import re
import os
import numpy as np
import pandas as pd
import pywt



# We select the folder where waveforms are and get machine, points and files
folder = datosADASH('../Data/Export')
machines = folder.getmachines()
points = folder.getpoints()
files = folder.getfiles()


# We have to read diagnosis of equipments to be associated with Power Spectrums
diag = pd.read_csv('../Data/diagnosis.csv')
spectro_diag = pd.DataFrame(columns=['file','time'])



# Waveletes are created with pywt library.
for machine, points_iter in points.items():
    filteredmachines = list(filter(lambda x: machine in x, files))
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
            plt.ioff()
            ax.contourf(time, np.log2(period), np.log2(power), np.log2(levels),
                        extend='both')
            ax.invert_yaxis()
            ax.axis('off')
                    
            date_sub = re.sub('[^A-Za-z0-9]+','', date)    
            filename = str(date_sub) + "_" + str(machine) + "_" + str(point)
            folder = "../Data/Wavelets"
            filename = os.path.join(folder, filename)
            f.savefig(filename, transparent=True, pad_inches=0.0,
                                figsize=(96/96, 96/96), dpi=96)
            
            
            
            plt.close()
            
            spectro_diag = spectro_diag.append({"file":filename,
                                                "time":date,
                                                "machine":machine
                                                }, ignore_index=True)
            
            
            
def sorted_index_by_time(df):
    """Function for sorting values
    by time and set it to index"""
    df = df.sort_values(['time'])
    df['time'] = pd.to_datetime(df['time'])
    return df

diag = sorted_index_by_time(diag)
spectro_diag = sorted_index_by_time(spectro_diag)

merged_diagnostic = pd.merge_asof(spectro_diag, diag, on="time", by=['machine'],
                  tolerance=pd.Timedelta('10 days'), direction='nearest')

merged_diagnostic[['file', 'time', 'machine','Nombre', 'diagnostico',
       'Id_Estado_Activo_fixed']]

# Move files to separate labeled folders


merged_diagnostic.file = merged_diagnostic.file + '.png'
merged_diagnostic['filecut'] = merged_diagnostic['file'].str[18:]


for index, row in merged_diagnostic.iterrows():
    filecut = row.filecut
    file = row.file
    if row.Id_Estado_Activo_fixed == 1.0:
        filename = "../Data/Wavelets/class_a/"
        final_filename = filename + filecut
        os.rename(file, final_filename)
    if row.Id_Estado_Activo_fixed > 1:
        filename = "../Data/Wavelets/class_b/"
        final_filename = filename + filecut
        os.rename(file, final_filename)