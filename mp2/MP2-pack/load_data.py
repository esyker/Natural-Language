# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 12:10:36 2021

@author: Utilizador
"""

import pandas as pd
from preprocessing import Preprocess
import numpy as np

file = './data/trainWithoutDev.txt'

#load data
train = pd.read_csv('./data/trainWithoutDev.txt',index_col=False, sep='\t+', header = None)
dev= pd.read_csv('./data/dev.txt',index_col=False, sep='\t+', header = None)

#preprocess data

preprocesser = Preprocess()

train[1] = train[1].apply(lambda x: preprocesser.preprocess(x))
dev[1] = dev[1].apply(lambda x: preprocesser.preprocess(x))

x_train = train[1].to_numpy();
y_train = train [0].to_numpy();
x_test = dev[1].to_numpy();
y_test = dev[0].to_numpy();


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import recall_score
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score

vectorizer = CountVectorizer()
vector_space=np.concatenate((x_train,x_test), axis=0)
vectors = vectorizer.fit_transform(' '.join(inner_list) for inner_list in vector_space)

x_train_size = x_train.shape[0] 
x_test_size =  x_test.shape[0]
x_train = vectors[0:x_train_size]
x_test = vectors[x_train_size:]

#vectorizer = CountVectorizer(tokenizer=lambda x: preprocesser.sklearn_tokenize(x),preprocessor=lambda x: preprocesser.sklearn_preprocess(x))

#train data
from sklearn.naive_bayes import GaussianNB

gnb = GaussianNB()
gnb.fit(x_train.toarray(), y_train)
y_pred = gnb.predict(x_test.toarray())

print("NB accuracy:" ,accuracy_score(y_test, y_pred))
print("NB balanced accuracy: ", balanced_accuracy_score(y_test, y_pred))
print("NB recall score: ", recall_score(y_test, y_pred, average='weighted'))
print("NB precision score: ", precision_score(y_test, y_pred, average=None))
print("NB weighted f1score: ", f1_score(y_test, y_pred, average='weighted'))

