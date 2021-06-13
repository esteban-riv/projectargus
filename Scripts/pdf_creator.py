# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 19:05:20 2021

@author: Esteban
"""

from fpdf import FPDF
import pandas as pd
from scipy.fft import rfft, rfftfreq
from scipy.stats import kurtosis, skew
import numpy as np
from matplotlib import pyplot as plt
import os
from datosadash import datosADASH
import itertools
import datetime

    



pdf = FPDF()



''' FIRST PAGE '''
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.image('teromanager.jpg')



pdf.add_page()

pdf.image('S1-M1.png', 5, 30, w=200)
pdf.image('S1-M1.png', 5, 160, w=200)


pdf.output('tuto1.pdf', 'F')