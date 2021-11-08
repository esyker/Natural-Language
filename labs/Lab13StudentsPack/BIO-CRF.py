# -*- coding:utf-8 -*-
# Code strongly based on https://towardsdatascience.com/named-entity-recognition-and-classification-with-scikit-learn-f05372f07ba2
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.feature_extraction import DictVectorizer


import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics
from collections import Counter

import warnings
warnings.filterwarnings('always') # previously complains if y_test has labels not in y_train
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

df = pd.read_csv('./train.csv')
df = df[:100000] # play with this

df = df.fillna(method='ffill') # faz o fill dos valores em branco ("propagate last valid observation forward to next valid")

#df.groupby('Tag').size().reset_index(name='counts') # dá output para fins de debug

X = df.drop('Tag', axis=1)
v = DictVectorizer(sparse=False)
X = v.fit_transform(X.to_dict('records'))
y = df.Tag.values
classes = np.unique(y)
classes = classes.tolist()

# The following code is to retrieve sentences with their tags
class SentenceGetter(object):
    
    def __init__(self, data):
        self.n_sent = 1
        self.data = data
        self.empty = False
        agg_func = lambda s: [(w, t) for w, t in zip(s['Word'].values.tolist(), 
                                                           s['Tag'].values.tolist())]
        self.grouped = self.data.groupby('Sentence #').apply(agg_func)
        self.sentences = [s for s in self.grouped]
        
    def get_next(self):
        try: 
            s = self.grouped['Sentence: {}'.format(self.n_sent)]
            self.n_sent += 1
            print(s)
            return s 
        except:
            return None
getter = SentenceGetter(df)
sentences = getter.sentences

# Extracts more features and convert them to sklearn-crfsuite format — each sentence should be converted to a list of dicts. 
# The following code were taken from sklearn-crfsuites official site.
def word2features(sent, i):
    word = sent[i][0]
    features = {
        'word.lower()': word.lower(), 
        'word[-3:]': word[-3:], #sufixo 3 = last 3 characters
        'word[-2:]': word[-2:], #sufixo 2 = last 2 characters
        'word.isupper()': word.isupper(), # all characters caps
        'word.istitle()': word.istitle(), # just the first
        'word.isdigit()': word.isdigit(),
    }
    if i > 0: # after first word
        word1 = sent[i-1][0] # previous word
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
        })
    else:
        features['BOS'] = True # beggining of sentence
    if i < len(sent)-1:
        word1 = sent[i+1][0] # next word
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
        })
    else:
        features['EOS'] = True # end of sentence
    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]
def sent2labels(sent):
    return [label for token, label in sent]
def sent2tokens(sent):
    return [token for token, label in sent]

# Split train and test sets
X = [sent2features(s) for s in sentences]
y = [sent2labels(s) for s in sentences]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

# Train a CRF model
crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)
crf.fit(X_train, y_train)

# Evaluation
new_classes = classes.copy()
new_classes.pop() # see the difference. Eliminates O as a tag (test)
y_pred = crf.predict(X_test)
print(metrics.flat_classification_report(y_test, y_pred, labels = new_classes))

# What our model learned?
def print_transitions(trans_features):
    for (label_from, label_to), weight in trans_features:
        print("%-6s -> %-7s %0.6f" % (label_from, label_to, weight))
print("Top likely transitions:")
print_transitions(Counter(crf.transition_features_).most_common(20))
print("\nTop unlikely transitions:")
print_transitions(Counter(crf.transition_features_).most_common()[-20:])

# Check the state features
def print_state_features(state_features):
    for (attr, label), weight in state_features:
        print("%0.6f %-8s %s" % (weight, label, attr))
print("Top positive:")
print_state_features(Counter(crf.state_features_).most_common(30))
print("\nTop negative:")
print_state_features(Counter(crf.state_features_).most_common()[-30:])

