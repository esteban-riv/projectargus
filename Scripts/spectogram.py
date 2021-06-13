# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 16:28:19 2021

@author: Esteban
"""

from scipy import signal
from scipy.fft import fftshift
import matplotlib.pyplot as plt
import pandas as pd
from Scripts.datosadash import datosADASH
import re
import os


class Spectrograms:
    """ Crea los espectrogramas a partir
    de las formas de onda
   
    ---
    root_dir: Directorio donde estan los datos
    
    ---
    """
    def __init__(self, rootdir):
        rootdir = rootdir
        self.machines = rootdir.getmachines()
        self.points = rootdir.getpoints()
        self.files = rootdir.getfiles()
    
    def get_spectrograms(self):
        for machine, points_iter in self.points.items():
            filteredmachines = list(filter(lambda x: machine in x, self.files))
            for iteration, point in enumerate(points_iter):
                acc_spec_text = "Aceleracion - Forma"
                filteredpoints = list(filter(lambda x: point in x, filteredmachines))
                filteredcsv = list(filter(lambda x:".csv" in x, filteredpoints))
                        
                # Get files by type of measurement
                accspec = list(filter(lambda x:acc_spec_text in x, filteredcsv))
                
                
                for filetime in accspec:
                    print(machine, filetime)
                    forma = pd.read_csv(filetime, skiprows=1,
                                        delimiter=";", encoding = "ISO-8859-1")
                    forma = forma.rename(columns={'time[ms]':'time',
                                                  ' amplitude[g]':'amplitude'})
                    fecha = pd.read_csv(filetime, nrows=0,
                                        delimiter=";", encoding = "ISO-8859-1").columns[1][6:]
                    fs = 12000
                    fig,ax = plt.subplots(1)
                    fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
                    ax.axis('off')
                    f, t, Sxx = signal.spectrogram(forma['amplitude'], fs)
                    plt.pcolormesh(t, f, Sxx)
                    ax.axis('tight')
                    ax.axis('off')
                    fecha = re.sub('[^A-Za-z0-9]+','', fecha)
                    
                    filename = str(fecha) + "_" + str(machine) + "_" + str(point)
                    #filename = re.sub('[^A-Za-z0-9]+','', filename) + '.png'
                    folder = "Spectrograms"
                    filename = os.path.join(folder, filename)
                    fig.savefig(filename, transparent=True, pad_inches=0.0,
                                figsize=(96/96, 96/96), dpi=96)
                    plt.close()
        
        
        
    
    
"""
folder = datosADASH('../Data/Export')


machines = folder.getmachines()
points = folder.getpoints()
files = folder.getfiles()




for machine, points_iter in points.items():
    filteredmachines = list(filter(lambda x: machine in x, files))
    for iteration, point in enumerate(points_iter):
        acc_spec_text = "Aceleracion - Forma"
        filteredpoints = list(filter(lambda x: point in x, filteredmachines))
        filteredcsv = list(filter(lambda x:".csv" in x, filteredpoints))
                
        # Get files by type of measurement
        accspec = list(filter(lambda x:acc_spec_text in x, filteredcsv))
        
        
        for filetime in accspec:
            print(machine, filetime)
            forma = pd.read_csv(filetime, skiprows=1,
                                delimiter=";", encoding = "ISO-8859-1")
            forma = forma.rename(columns={'time[ms]':'time',
                                          ' amplitude[g]':'amplitude'})
            fecha = pd.read_csv(filetime, nrows=0,
                                delimiter=";", encoding = "ISO-8859-1").columns[1][6:]
            fs = 12000
            fig,ax = plt.subplots(1)
            fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
            ax.axis('off')
            f, t, Sxx = signal.spectrogram(forma['amplitude'], fs)
            plt.pcolormesh(t, f, Sxx)
            ax.axis('tight')
            ax.axis('off')
            fecha = re.sub('[^A-Za-z0-9]+','', fecha)
            
            filename = str(fecha) + "_" + str(machine) + "_" + str(point)
            #filename = re.sub('[^A-Za-z0-9]+','', filename) + '.png'
            folder = "Spectrograms"
            filename = os.path.join(folder, filename)
            fig.savefig(filename, transparent=True, pad_inches=0.0,
                        figsize=(96/96, 96/96), dpi=96)
            plt.close()




forma = pd.read_csv('acc2.csv', skiprows=1, delimiter=";", encoding = "ISO-8859-1")
forma = forma.rename(columns={'time[ms]':'time', ' amplitude[g]':'amplitude'})
fs = 12000



  
fig,ax = plt.subplots(1)
fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
ax.axis('off')
f, t, Sxx = signal.spectrogram(forma['amplitude'], fs)
plt.pcolormesh(t, f, Sxx)
ax.axis('tight')
ax.axis('off')
fig.savefig('sp_xyz2.png', transparent=True, pad_inches=0.0,
            figsize=(96/96, 96/96), dpi=96)
"""