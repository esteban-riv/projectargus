# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 15:12:43 2021

@author: Esteban

"""

from Scripts.waveform import Waveform, Raw_Waveform_Date
from Scripts.spectrum import Spectrum
from multiprocessing import Pool
import pandas as pd
import time

waveform_parameters = []

df_mms_params = pd.DataFrame(columns=['machine','point','time','max_mms','rms_mms'])
df_acc_params = pd.DataFrame(columns=['machine','point','time','max_acc',
                                      'med_acc','rms_acc', 'kur_acc', 'cf_acc'])
df_dem_params = pd.DataFrame(columns=['machine','point','time','max_dem','rms_dem'])
df_spec_acc_params = pd.DataFrame(columns=['machine','point','time','num_peaks',
                                          'a_range','b_range', 'c_range','d_range',
                                          'e_range','f_range','g_range','h_range',
                                          'i_range','j_range'])


# To identify the type of measurement we must copy
# the point definition in ADASH Software
vel_time_text = "Velocidad - Forma de onda"
acc_time_text = "Aceleracion - Forma de onda"
demod_time_text = "Demodulacion - Forma de onda"
acc_spec_text = "Aceleracion - Espectro"



def get_values(index, machines, points, files, df_mms_params, df_acc_params, df_dem_params, df_spec_acc_params):
    points_filtered = {k: v for k, v in points.items() if k in list(machines) }
    for machine, points_iter in points_filtered.items():        
        filteredmachines = list(filter(lambda x: machine in x, files))  
        for iteration, point in enumerate(points_iter):
           
            
            # Get the files for every point        
            filteredpoints = list(filter(lambda x: point in x, filteredmachines))
            filteredcsv = list(filter(lambda x:".csv" in x, filteredpoints))

            # Get files by type of measurement
            veltime = list(filter(lambda x:vel_time_text in x, filteredcsv))
            acctime = list(filter(lambda x:acc_time_text in x, filteredcsv))
            demodtime = list(filter(lambda x:demod_time_text in x, filteredcsv))
            accspec = list(filter(lambda x:acc_spec_text in x, filteredcsv))

            
            # Get mms parameters for analysis
            for filetime in veltime:

                # We use Raw_Waveform_Date model to get
                # column with waveform data and date
                # measurement
                raw_data = Raw_Waveform_Date(filetime)
                column_vel = raw_data.get_raw_data()
                date_df_time = raw_data.get_datetime()         

                # Now we use get_mm_params method to get useful 
                # features of raw signal
                calculated_params = Waveform(column_vel).get_mms_params()
                # Creation of a row to be append in the dataframe
                time_mms_row = {'machine':machine, 'point':point, 'max_mms':calculated_params[0],
                           'rms_mms':calculated_params[1], 'time':date_df_time}
                
                df_mms_params = df_mms_params.append(time_mms_row, ignore_index=True)
              
            try:
                df_mms_params.to_csv('Data/mms_params.csv', mode='a', header=False, index=False)
            except:
                time.sleep(0.01)
                print("Error al escribir")
                df_mms_params.to_csv('Data/mms_params.csv', mode='a', header=False, index=False)
            
            df_mms_params = df_mms_params.iloc[0:0]


                
            # Get acceleration params. Same procedure as mms, but
            # we use get_acc_params method wich return parameters
            # associated with acceleration
            for filetime in acctime:

                raw_data = Raw_Waveform_Date(filetime)
                column_vel = raw_data.get_raw_data()
                date_df_time = raw_data.get_datetime()

                calculated_params = Waveform(column_vel).get_acc_params()

                time_acc_rows = {'machine':machine, 'point':point, 'max_acc':calculated_params[0],
                           'med_acc':calculated_params[1], 'rms_acc':calculated_params[2],
                            'kur_acc':calculated_params[3], 'cf_acc':calculated_params[4],
                            'time':date_df_time}
                
                df_acc_params = df_acc_params.append(time_acc_rows, ignore_index=True)
                
            try:
                df_acc_params.to_csv('Data/acc_params.csv', mode='a', header=False, index=False)
            except:
                time.sleep(0.01)
                print("Error al escribir")
                df_acc_params.to_csv('Data/acc_params.csv', mode='a', header=False, index=False)
                    
            df_acc_params = df_acc_params.iloc[0:0]
                    

            # Get demod params. Mostly the same than mm/s
            # params                
            for filetime in demodtime:

                raw_data = Raw_Waveform_Date(filetime)
                column_vel = raw_data.get_raw_data()
                date_df_time = raw_data.get_datetime()

                calculated_params = Waveform(column_vel).get_demod_params()

                time_demod_rows = {'machine':machine, 'point':point, 'max_dem':calculated_params[0],
                                   'rms_dem':calculated_params[1],  'time':date_df_time}  
                
                df_dem_params = df_dem_params.append(time_demod_rows, ignore_index=True)
                
            try:
                df_dem_params.to_csv('Data/dem_params.csv', mode='a', header=False, index=False)
            except:
                time.sleep(0.01)                    
                print("Error al escribir")
                df_dem_params.to_csv('Data/dem_params.csv', mode='a', header=False, index=False)
                
            df_dem_params = df_dem_params.iloc[0:0]
            
            # Get spectrum params. In spectrum is important
            # peaks that are excitated. The number of peaks is
            # associated with damage severity.
            for filespec in accspec:
                spectrum_data = Spectrum(filespec) 
                date_df_spec = spectrum_data.get_datetime()
                peaks, calculated_params, a_range, b_range, c_range, d_range, e_range, f_range, \
                g_range, h_range, i_range, j_range = spectrum_data.get_spec_params()
                spec_acc_row = {'machine':machine, 'point':point,
                                'num_peaks': float(len(peaks)), 
                                'time':date_df_spec, 'a_range':a_range, 'b_range':b_range, 
                                'c_range':c_range, 'd_range':d_range, 'e_range':e_range,
                                'f_range':f_range, 'g_range':g_range, 'h_range':h_range,
                                'i_range':i_range, 'j_range':j_range}     
                
                
                df_spec_acc_params = df_spec_acc_params.append(spec_acc_row, ignore_index=True)
            
            try:
                df_spec_acc_params.to_csv('Data/spec_acc_params.csv', mode='a', header=False, index=False)
            except:
                time.sleep(0.01)                    
                print("Error al escribir")
                df_spec_acc_params.to_csv('Data/spec_acc_params.csv', mode='a', header=False, index=False)
            
            df_spec_acc_params = df_spec_acc_params.iloc[0:0]
            
        print("Ended with machine {} in process {}".format(machine, index))
    print("Ended with proccess {}".format(index))