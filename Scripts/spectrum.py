# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 12:00:28 2021

@author: Esteban
"""

import pandas as pd
import datetime
import pandas as pd
from scipy.signal import find_peaks


class Spectrum:
    """
    Get the raw spectrum data and datetime
    of mesurement
    
    ---
    file: csv file with data
    ---
    """
    def __init__(self, file):
        self.file = file
        
        
    def get_datetime(self):
        fecha_df_spec = pd.read_csv(self.file, nrows=1, header=None,
                                    delimiter=";", decimal=".",
                                    encoding = "ISO-8859-1").iloc[0,1][6:]
        
        fecha_df_spec = datetime.datetime.strptime(fecha_df_spec, '%Y-%m-%d %H:%M:%S.%f')
        
        return fecha_df_spec
    
    
    def get_spec_params(self):
        df_spectrum = pd.read_csv(self.file, skiprows=[0], delimiter=";",
                              decimal=".", encoding = "ISO-8859-1")
        
        df_spectrum = df_spectrum.rename(columns={'frequency[Hz]':'freq',
                                                  ' amplitude[g RMS]':'amp'})
        
        peaks, parameters = find_peaks(df_spectrum['amp'], height=0.08, distance=25)
        
        # Peaks need to by multiplied by two due
        # spectrum resolution
        peaks = peaks*2
        
        # In this part of the function peaks are grouped by 500Hz
        # and ampliuted values are added
        a_range = 0
        b_range = 0
        c_range = 0
        d_range = 0
        e_range = 0
        f_range = 0
        g_range = 0
        h_range = 0
        i_range = 0
        j_range = 0
        
        dictionary = zip(peaks,parameters['peak_heights'])
        
        for key, value in dictionary:
            if key < 500:                
                a_range += value
            if key >= 500 and key < 1000 :
                b_range += value
            if key >= 1000 and key < 1500 :
                c_range += value
            if key >= 1500 and key < 2000 :
                d_range += value
            if key >= 2000 and key < 2500 :
                e_range += value
            if key >= 2500 and key < 3000 :
                f_range += value
            if key >= 3000 and key < 3500 :
                g_range += value
            if key >= 3500 and key < 4000 :
                h_range += value  
            if key >= 4000 and key < 4500 :
                i_range += value
            if key >= 4500 and key < 5000 :
                j_range += value  
        
            
            
        
        return peaks, parameters, a_range, b_range, c_range, d_range, e_range, f_range, \
              g_range, h_range, i_range, j_range
    

        