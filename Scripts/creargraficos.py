import os
import glob
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError
import re
import requests
from bokeh.io import output_file, show
from bokeh.layouts import row, gridplot
from bokeh.plotting import figure
from bokeh.models import HoverTool,WheelZoomTool, PanTool, ResetTool
from datetime import date


#Datos de conexión al servidor Amazon
AWS_ACCESS_KEY_ID = 'AKIAZC6PX7PF44MXIUBG'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'teromanager2'
PARAM = {'nombreplanta':"",'nombreactivo':"",'nombrepunto':"", 'fechamedida':"" ,'punto':"", "archivo":"", }
URL = "https://teromanager.herokuapp.com/crud/postmedidas"


#Leo el archivo nombres para ponerle nombre en plataforma
nombres = pd.read_csv('nombres.csv', skiprows=[5],delimiter=";", decimal=",", encoding = "ISO-8859-1" )


def upload_to_aws(local_file,bucket,s3_file):
    s3 = boto3.client('s3',aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
   
    
    try:
        s3.upload_file(local_file, bucket,'medidas/{}'.format(s3_file),  ExtraArgs={
        "ContentType": 'text/html'
    })
        print("Uploaded")
    except FileNotFoundError:
        print("File not found")
        return False
    except NoCredentialsError:
        print("Sin credenciales")
        return False
    
    
#Poner nombre de planta que tenga en Adash
NOMBRE_PLANTA = "EDAR COPERO"

#Nombre de planta en Terohome y filtro el archivo nombres para que solo tenga los de la planta
Planta = "EDAR Copero"
nombre_planta = nombres[nombres['Planta_home'] == Planta]


#Directorio donde estan las medidas y fecha
rootdir = r'G:\Mi unidad\Personal\BBDD ADASH\Puebas Python - copia\Nueva carpeta'
maquinas = []
puntos = []
fecha = "2020-12-24"


''' La idea que voy implementar:
    Hacer un listado con todos los archivos de la planta
    Buscar los archivos de cada punto por maquina
    Buscar los archicos que solo sean CSV
    Buscar los archivos por cada tipo de medida
'''   


#Hago un listado de todos los archivos del directorio y subdirectorios
lst = os.listdir(rootdir)
todos = []

for dirpath, subdirs, files in os.walk(rootdir):
    for file in files:
        todos.append(os.path.join(dirpath,file))
        
        
#Para obtener el listado de maquinas: tomo donde haya csv con nombre FFT
listadoCSV = list(filter(lambda x:".csv" in x, todos))
listadoFFT = list(filter(lambda x:"Vel_FFT" in x, listadoCSV))


for lista in listadoFFT:
    equipo = lista.split('\\')[-4]
    equipo = equipo.split('[')[0][:-1]
    maquinas.append(equipo)
  
maquinas = list(dict.fromkeys(maquinas))


#Intenar obtener un diccionario con los puntos por maquina
diccionarioEquiposPuntos = {i : [] for i in maquinas}
for maquina in maquinas:
    for elemento in listadoFFT:
        if maquina in elemento:
            diccionarioEquiposPuntos[maquina].append(elemento.split('\\')[-3].split('[')[0][:-1])



        

#Bucle para la creación de gráficos y subida
for maquina,puntos in diccionarioEquiposPuntos.items():
    for punto in puntos:
        FiltradoMaquinas = list(filter(lambda x: maquina in x, todos))
        FiltradoPuntos = list(filter(lambda x:punto in x, FiltradoMaquinas))
        FiltradoCSV = list(filter(lambda x:".csv" in x, FiltradoPuntos))
        VELTIME = list(filter(lambda x:"Vel_Time" in x, FiltradoCSV))
        VELFFT = list(filter(lambda x:"Vel_FFT" in x, FiltradoCSV))
        ACCTIME = list(filter(lambda x:"Acc_Time" in x, FiltradoCSV))
        ACCFFT = list(filter(lambda x:"Acc_FFT" in x, FiltradoCSV))
        
        df_time = pd.read_csv(VELTIME[0], skiprows=[0], delimiter=";", decimal=".", encoding = "ISO-8859-1")
        df_FFT = pd.read_csv(VELFFT[0], skiprows=[0], delimiter=";", decimal=".", encoding = "ISO-8859-1")
        df_time_A = pd.read_csv(ACCTIME[0], skiprows=[0], delimiter=";", decimal=".", encoding = "ISO-8859-1")
        df_FFT_A = pd.read_csv(ACCFFT[0], skiprows=[0], delimiter=";", decimal=".", encoding = "ISO-8859-1")
        
        filename = (maquina+ '-' + punto + fecha)
        filename = re.sub('[^A-Za-z0-9]+','', filename) +  ".html"
        output_file(filename, title= maquina + '-' + punto + fecha)
        tools = [PanTool(), WheelZoomTool(), ResetTool(), HoverTool]

        #Forma onda mm/s
        p=figure(title="Forma de onda mm/s",plot_width=600, plot_height=400)
        p.add_tools(HoverTool(tooltips = [
                                ("(Tiempo,Amplitud)", "($x, $y)"),
                                ]))
        p.line(df_time['time[ms]'],df_time[' amplitude[mm/s]'])

        p.xaxis.axis_label = 'Tiempo(ms)'
        p.yaxis.axis_label = 'Amplitud (mm/s)'


        #Espetro mm/s
        p2=figure(title="Espectro mm/s", plot_width=600, plot_height=400)
        p2.add_tools(HoverTool(tooltips = [
                                ("(Frecuenca,Amplitud)", "($x, $y)"),
                                ]))
        p2.line(df_FFT['frequency[Hz]'],df_FFT[' amplitude[mm/s RMS]'])

        p2.xaxis.axis_label = 'Frecuencia (Hz)'
        p2.yaxis.axis_label = 'Amplitud (mm/s)'


        #Forma onda g's
        p3=figure(title="Forma de onda g's",plot_width=600, plot_height=400)
        p3.add_tools(HoverTool(tooltips = [
                                ("(Tiempo,Amplitud)", "($x, $y)"),
                                ]))
        p3.line(df_time_A['time[ms]'],df_time_A[' amplitude[g]'])

        p3.xaxis.axis_label = 'Tiempo (ms)'
        p3.yaxis.axis_label = 'Amplitud (g)'



        #Espectro g's
        p4=figure(title="Espectro g's", plot_width=600, plot_height=400)
        p4.add_tools(HoverTool(tooltips = [
                                ("(Frecuencia,Amplitud)", "($x, $y)"),
                                ]))
        p4.line(df_FFT_A['frequency[Hz]'],df_FFT_A[' amplitude[g RMS]'])

        p4.xaxis.axis_label = 'Frecuencia (Hz)'
        p4.yaxis.axis_label = 'Amplitud (g)'




        #Creo el grid y lo muestro              
        grid = gridplot([[p,p2],[p3,p4]], plot_width=500, plot_height=250)
        show(grid)
        
        uploaded = upload_to_aws(filename,'teromanager2',filename)
        
        
        
        PARAM = {'nombreplanta':"",'nombreactivo':"",'nombrepunto':"", 'fechamedida':"" , "archivo":"", }
        
        maquina = nombre_planta[nombre_planta['Equipo_adash'] == maquina].iloc[0].Equipo_home
        
        PARAM['nombreplanta'] = Planta
        PARAM["nombreactivo"] = maquina        
        PARAM["nombrepunto"] = punto
        PARAM["fechamedida"] = fecha
        PARAM["archivo"] = "https://teromanager2.s3-us-west-2.amazonaws.com/medidas/"+filename
        r = requests.post(url = URL, data = PARAM)
        pastebin_url=r.text
            
        print("The pastebin URL is:%s" %pastebin_url + maquina + Planta) 
        









