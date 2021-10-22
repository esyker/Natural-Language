# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 12:10:36 2021

@author: Utilizador
"""

import pandas as pd

file = './data/trainWithoutDev.txt'

data = pd.read_csv('./data/trainWithoutDev.txt',index_col=False, sep='\t+', header = None)

