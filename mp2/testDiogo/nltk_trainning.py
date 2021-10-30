import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import recall_score
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from load_data import Load_Data 
from nltk_preprocessing import Preprocess

#Load Data
print("Loading Data")
x_train, y_train , x_test, y_test = Load_Data('./data/trainWithoutDev.txt','./data/dev.txt').load()
x_train_size = x_train.shape[0] 
x_test_size =  x_test.shape[0]

#get the vocabulary
print("Getting the vocabulary")
preprocessor = Preprocess()

def get_vocabulary(x_train,x_test, preprocessor):
    vocabulary = dict()
    tokens_train = list(map(preprocessor.preprocess_tokenize, x_train))
    tokens_test = list(map(preprocessor.preprocess_tokenize, x_test))
    token_count = 0 
    for sentence in tokens_train:
        for token in sentence:
            if token not in vocabulary:
                vocabulary[token] = token_count
                token_count+=1
    for sentence in tokens_test:
        for token in sentence:
            if token not in vocabulary:
                vocabulary[token] = token_count
                token_count+=1
    return vocabulary

dataset_vocabulary = get_vocabulary(x_train, x_test, preprocessor)

#Vectorize
print("Vectorizing")
vectorizer = TfidfVectorizer(tokenizer=lambda x: preprocessor.word_tokenize(x),
                             preprocessor=lambda x: preprocessor.preprocess(x),
                             ngram_range=(1,2),vocabulary=dataset_vocabulary)

#train/test split
x_train = vectorizer.fit_transform(x_train)
x_test = vectorizer.fit_transform(x_test)

"""
#train data
print("Trainning NB")
from sklearn.naive_bayes import GaussianNB

gnb = GaussianNB()
gnb.fit(x_train, y_train)
y_pred = gnb.predict(x_test)

print("NB accuracy:" ,accuracy_score(y_test, y_pred))
print("NB balanced accuracy: ", balanced_accuracy_score(y_test, y_pred))
print("NB recall score: ", recall_score(y_test, y_pred, average='weighted'))
print("NB precision score: ", precision_score(y_test, y_pred, average=None))
print("NB weighted f1score: ", f1_score(y_test, y_pred, average='weighted'))

print("Trainning RF")
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(max_depth=20, n_jobs=-1,class_weight="balanced")
rf.fit(x_train, y_train)
y_pred = rf.predict(x_test)

print("RF accuracy:" ,accuracy_score(y_test, y_pred))
print("RF balanced accuracy: ", balanced_accuracy_score(y_test, y_pred))
print("RF recall score: ", recall_score(y_test, y_pred, average='weighted'))
print("RF precision score: ", precision_score(y_test, y_pred, average=None))
print("RF weighted f1score: ", f1_score(y_test, y_pred, average='weighted'))
"""

print("Trainning SVC")
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier

"""
svm = SVC(gamma='auto')
"""
svm = LinearSVC(class_weight="balanced")
svm.fit(x_train, y_train)
y_pred = svm.predict(x_test)


print("SVM accuracy:" ,accuracy_score(y_test, y_pred))
print("SVM balanced accuracy: ", balanced_accuracy_score(y_test, y_pred))
print("SVM recall score: ", recall_score(y_test, y_pred, average='weighted'))
print("SVM precision score: ", precision_score(y_test, y_pred, average=None))
print("SVM weighted f1score: ", f1_score(y_test, y_pred, average='weighted'))