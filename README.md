# Project Argus


You can access to project webpage in:

<a href="https://projectargus.herokuapp.com/">Project Argus</a>


## Project Structure

Once you have pulled the repo from github you must have the next folder structure:

+-- Data<br>
+-- Scripts<br>
+-- projectargus.yml<br>
+-- Project Argus.ipynb<br>
+-- Spectrogram Generator.ipynb<br>
+-- README.md<br>
+-- resultados.csv<br>
+-- diagnosis.csv<br>


## Machine Learning

### Data Structure

For run machine learning part of the project first data mus be downloaded from the next link:

LINK TO DATA

Data must be downloaded to Data folder. The final Data structure must be like that:

+--Data<br>
&ensp; +-- Export<br>
&ensp;&ensp; +-- Zona 2 S-1 [1469]<br>
&ensp;&ensp;&ensp; +-- S1-M01 [1991]<br>
&ensp;&ensp;&ensp; +-- S1-M02 [1650]<br>
&ensp;&ensp;&ensp; +-- S1-M03 [1661]<br>
&ensp;&ensp;&ensp; +-- ...<br>
&ensp;&ensp; +-- Zona 2 S-2 [2002]<br>
&ensp;&ensp; +-- Zona 2 S-3 [235]<br>
&ensp;&ensp; +-- ...<br>

Every S** folder represent a machine folder. In this folder must be subfolder for every measure point and type of measure. Most important thing is to download Data in the correct folder.


### Notebook and Scripts

To get into ML project you must run the "Project Argus.ipynb" file. This file load some scripts created for data manipulation that are included in Scripts folder. There is nothing more to do than run the file and follow the instructions in the notebook.


### Frontend

The frontend is in the <a href="https://projectargus.herokuapp.com/">Project Webpage</a>. Just go to the Machine Learning Result section to visualize the Dashboard.

<img src="https://teromanager2.s3-us-west-2.amazonaws.com/projectargus/argus_front_ml.JPG">







