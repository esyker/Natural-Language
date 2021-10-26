# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 12:10:36 2021

@author: Utilizador
"""

import pandas as pd
import numpy as np
from nltk_preprocessing import Preprocess
#preprocess data

class Load_Data:
    def __init__(self,trainFile,testFile):       
        self.trainFile=trainFile #'./data/trainWithoutDev.txt'
        self.testFile=testFile #'./data/dev.txt'
        #load data
        self.train = pd.read_csv(trainFile,index_col=False, sep='\t+', header = None, engine='python')
        self.dev= pd.read_csv(testFile,index_col=False, sep='\t+', header = None, engine='python')
    
    def get_data(self):
        return self.train, self.dev
    
    def load(self):
        x_train = self.train[1].to_numpy();
        y_train = self.train [0].to_numpy();
        x_test = self.dev[1].to_numpy();
        y_test = self.dev[0].to_numpy();
        return x_train, y_train, x_test, y_test
    
#train, test = Load_Data('./data/trainWithoutDev.txt','./data/dev.txt' ).get_data()
