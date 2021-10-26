import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
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


#Vectorize
print("Vectorizing")
preprocessor = Preprocess()
vectorizer = CountVectorizer(tokenizer=lambda x: preprocessor.word_tokenize(x),
                             preprocessor=lambda x: preprocessor.preprocess(x),
                             ngram_range=(1,2))
vector_space=np.concatenate((x_train,x_test), axis=0)
vectors = vectorizer.fit_transform(vector_space)

#train/test split
x_train = vectors[0:x_train_size].toarray()
x_test = vectors[x_train_size:].toarray()

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
svm = LinearSVC(class_weight="balanced", max_iter=10)
svm.fit(x_train, y_train)
y_pred = svm.predict(x_test)


print("SVM accuracy:" ,accuracy_score(y_test, y_pred))
print("SVM balanced accuracy: ", balanced_accuracy_score(y_test, y_pred))
print("SVM recall score: ", recall_score(y_test, y_pred, average='weighted'))
print("SVM precision score: ", precision_score(y_test, y_pred, average=None))
print("SVM weighted f1score: ", f1_score(y_test, y_pred, average='weighted'))