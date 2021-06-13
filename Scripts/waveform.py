# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 11:47:05 2021

@author: Esteban
"""

import pandas as pd
from scipy.stats import kurtosis
import numpy as np
import os
import itertools
import datetime
import pandas as pd
from scipy.signal import find_peaks


class Raw_Waveform_Date:
    """
    Get the raw waveform data and datetime
    of mesurement
    
    ---
    file: csv file with data
    ---
    """
    
    def __init__(self, file):
        self.file = file
    
    def get_raw_data(self):
        df_time = pd.read_csv(self.file, skiprows=[0], delimiter=";",
                              decimal=".", encoding = "ISO-8859-1")
        
        columna_vel = df_time.iloc[:,1]
        
        return columna_vel
    
    def get_datetime(self):
        fecha_df_time = pd.read_csv(self.file, nrows=1, header=None,
                                    delimiter=";", decimal=".",
                                    encoding = "ISO-8859-1").iloc[0,1][6:]
        
        fecha_df_time = datetime.datetime.strptime(fecha_df_time, '%Y-%m-%d %H:%M:%S.%f')
        
        return fecha_df_time
    


class Waveform:
    """
    Get useful parameters of waveforms
    
    ---
    column: Waveform´s points
    ---
    """
    def __init__(self, column):
        self.column = column  
    

    def get_acc_params(self):
        maximo_value = max(abs(self.column))
        media_value = np.sqrt(np.mean(abs(self.column)))
        rms_value = np.sqrt(np.mean(abs(self.column ** 2)))
        crest_factor_value = abs(np.max(np.abs(self.column))/np.sqrt(np.mean(np.square(self.column))))
        kurtosis_value = abs(kurtosis(self.column))

        
        return [maximo_value, media_value, rms_value, kurtosis_value, crest_factor_value]
    
    
    def get_mms_params(self):
        maximo_value = max(abs(self.column))
        rms_value = np.sqrt(np.mean(abs(self.column ** 2)))

        
        return [maximo_value, rms_value]
    
    
    def get_demod_params(self):
        maximo_value = max(abs(self.column))
        rms_value = np.sqrt(np.mean(abs(self.column ** 2)))

        
        return [maximo_value, rms_value]







    
    
        