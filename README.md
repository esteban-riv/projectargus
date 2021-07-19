# Project Argus

Repository of Project Argus, a Machine Learning and Deep Learning predictor of industrial machine health.


## Frontend and Project Report

The frontend and project report are in the <a href="https://projectargus.herokuapp.com/">Project Webpage</a>. This frontend contains the project report and the access to results and colab's notebooks. You must use the following credentials to access the content:

Username: kshool <br>
Pass: TVqcnvqfFesmmk4


This is a snapshot of the project dashboard:

<img src="https://teromanager2.s3-us-west-2.amazonaws.com/projectargus/argus_front_ml.JPG">

<br>

## Project Structure

Once you have pulled the repo from github you must have the next folder structure:

+-- Data<br>
+-- Model<br>
+-- Results<br>
+-- Scripts<br>
+-- environment.yml<br>
+-- Model Application.ipynb<br>
+-- Project Argus.ipynb<br>
+-- Spectrogram Generator.ipynb<br>
+-- README.md<br>

You must create a conda environment with the file environment.yml.



### Data Structure

For run machine learning part of the project first data must be downloaded from the next link:

<a href="https://teromanager2.s3.us-west-2.amazonaws.com/projectargus/Datos+ML.zip">Machine Learning Data</a>

Data must be downloaded to Data folder. The final Data structure must be like that:

+--Data<br>
&ensp; +-- Export<br>
&ensp;&ensp; +-- Zona 2 S-1 [1469]<br>
&ensp;&ensp; +-- Zona 2 S-1 [1469]<br>
&ensp;&ensp; +-- Zona 2 S-1 [1469]<br>
&ensp;&ensp;&ensp; +-- S1-M01 [1991]<br>
&ensp;&ensp;&ensp; +-- S1-M02 [1650]<br>
&ensp;&ensp;&ensp; +-- S1-M03 [1661]<br>
&ensp;&ensp;&ensp; +-- ...<br>
&ensp;&ensp; +-- Zona 2 S-2 [2002]<br>
&ensp;&ensp; +-- Zona 2 S-3 [235]<br>
&ensp;&ensp; +-- ...<br>

Every S** folder represent a machine folder. In this folder must be subfolder for every measure point and type of measure. Most important thing is to download Data in the correct folder.

For Deep Learning the next folders are used in Google Drive.


<a href="https://drive.google.com/drive/folders/1UUXI81gcGE8jYJLylK4ib0qMHWKt-ak-?usp=sharing">Spectrograms test and validation</a>

<a href="https://drive.google.com/drive/folders/1oKHiWTIrMz_c7KEMzNgR9VE57Hd96EGB?usp=sharing">Spectrograms prediction</a>

<a href="https://drive.google.com/drive/folders/11WAV4-qIz2fw3CeAq4kVfkFvq4FUtRaO?usp=sharing">Power Spectrums test and validation</a>

<a href="https://drive.google.com/drive/folders/1FxvEB5Qg3mtZ0VrI8UzAOGxRvcoT_mY1?usp=sharing">Power Spectrums prediction</a>


You must add it to your Drive and open them in Colab selecting the right path. Test and validation folders have two subfolders, 'class_a' and 'class_b'.


## Notebook and Scripts

To get into ML project you must run the "Project Argus.ipynb" file. This file load some scripts created for data manipulation that are included in Scripts folder. There is nothing more to do than run the file and follow the instructions in the notebook. This notebook will export three files to later be used in "Model Application.ipynb". The files are:

- "Data/diagnosis_2021.csv": This file contains data with no diagnosis to be predicted.
- "Model/ct.pkl": Column Transformer file to apply to this data.
- "Model/gcbmodel.sav": Gradient Boost Classifier model to apply.

The notebook "Model Application.ipynb" will load and apply this objects for predicting the new labels. The results of this notekooks are two .csv files that are used in the frontend.

For Deep Learning two Colab files are used:


<a href="https://colab.research.google.com/drive/1hP9gDx5AkAymNtzz9ZdeJgjlLtmZ0C-p?usp=sharing">Spectograms</a>

<a href="https://colab.research.google.com/drive/1aTTFh2tkkua5KA70EFGudJkS_GjBCY99?usp=sharing">Power Spectrums</a>

You must have the previously mentioned Google Drive folders added to your drive.












