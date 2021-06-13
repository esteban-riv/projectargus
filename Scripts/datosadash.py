# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 18:40:19 2021

@author: Esteban
"""

import pandas as pd
from scipy.fft import rfft, rfftfreq
from scipy.stats import kurtosis, skew
import numpy as np
from matplotlib import pyplot as plt
import os


class datosADASH:
    """Para obtener los datos de un directorio
    
    ---
    root_dir: Directorio donde estan los datos
    
    ---
    """
    def __init__(self, rootdir):
        self.rootdir = rootdir
        
    def getfiles(self):
        listado_archivos = []

        for dirpath, subdirs, files in os.walk(self.rootdir):
            for file in files:        
                    listado_archivos.append(os.path.join(dirpath,file))
        
        return listado_archivos      
        
    
    def getmachines(self):
        maquinas = []
        
        listado_archivos = self.getfiles()
        listadoFFT = list(filter(lambda x:"Velocidad - Espectro" in x, listado_archivos))
        
        for lista in listadoFFT:
            
            equipo = lista.split('/')[-4].split('[')[0][:-1]
            maquinas.append(equipo)
    
        maquinas = list(dict.fromkeys(maquinas))
        
        return maquinas
    
    def getpoints(self):
        maquinas = self.getmachines()
        
        listado_archivos = self.getfiles()
        listadoFFT = list(filter(lambda x:"Velocidad - Espectro" in x, listado_archivos))
        puntos_maquina = {i: [] for i in maquinas}
        
        for maquina in maquinas:
            for elemento in listadoFFT:
                if maquina in elemento:
                    puntos_maquina[maquina].append(elemento.split('/')[-3].split('[')[0][:-1])
        
        
        for item, value in puntos_maquina.items():            
            puntos_maquina[item] = list(dict.fromkeys(value))
            
        
        return puntos_maquina
        