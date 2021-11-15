"""
import spacy

nlp = spacy.load("en_core_web_lm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)
"""

import spacy
    
import pickle
from string import punctuation

import re
from nltk.corpus import stopwords

from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import RidgeClassifier
from sklearn.naive_bayes import ComplementNB
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import VotingClassifier
from spacy_preprocessing import SpacyPreprocessor

spacy_model = SpacyPreprocessor.load_model()
preprocessor = SpacyPreprocessor(spacy_model=spacy_model, lemmatize=True, remove_numbers=True,
                                 remove_stopwords=True)
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
          "december"]


def remove_punctuation(word):
    return ''.join(c for c in word if c not in punctuation)

def remove_letter_only(word):
    if len(word) == 1 and word.isalpha():
        return ""
    return word

def process_number(word):
    if bool(re.match("(^(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})$)", word)):
        return "roman_numeral"
    if bool(re.match("[0-9]+(th|nd|st|rd)", word)):
        return "cardinal_number"
    if word.isnumeric() and len(word) == 4:
        return "year"
    if word.isnumeric():
        return "number"
    if word.lower() in MONTHS:
        return "month"
    return word


def process_data(file,preprocessor):
    with open(file, "r", encoding='utf-8') as fp:
        x_data = []
        pos_tags = []
        y_data = []
        for line in fp.readlines():
            processed_tokenized_line = preprocessor.preprocess_text(line)
            x_data.append(processed_tokenized_line)
            y_data.append(label)
        return x_data, y_data


def vectorize(x_train, x_test, is_count=False):
    if is_count:
        vectorizer = CountVectorizer()
        x_train = vectorizer.fit_transform(x_train).toarray()
        x_test = vectorizer.transform(x_test).toarray()
    else:
        vectorizer = TfidfVectorizer(sublinear_tf=True)
        x_train = vectorizer.fit_transform(x_train)
        x_test = vectorizer.transform(x_test)
    return x_train, x_test


x_train, y_train = process_data("trainWithoutDev.txt", preprocessor)
x_test, y_test = process_data("dev.txt", preprocessor)

file = open('processed_trained_data.txt', 'w', encoding='utf-8')
file.writelines(x_train)
file.close()

x_train, x_test = vectorize(x_train, x_test)

with open("variables.pickle", "wb") as f:
    pickle.dump([x_train, y_train, x_test, y_test], f)

# with open('variables.pickle', 'rb') as f:
#     x_train, y_train, x_test, y_test = pickle.load(f)

NB_classifier = ComplementNB()
NB_classifier.fit(x_train, y_train)
y_pred_NB = NB_classifier.predict(x_test)
print("Accuracy ComplementNB:", metrics.accuracy_score(y_test, y_pred_NB))

et_classifier = ExtraTreesClassifier(n_jobs=-1)
et_classifier.fit(x_train, y_train)
y_pred_et = et_classifier.predict(x_test)
print("Accuracy ExtraTreesClassifier:", metrics.accuracy_score(y_test, y_pred_et))

# Support Vector
SVC_classifier = SVC(kernel='linear', probability=True)
SVC_classifier.fit(x_train, y_train)
y_pred_SVC = SVC_classifier.predict(x_test)
print("Accuracy SVC:", metrics.accuracy_score(y_test, y_pred_SVC))

ridge_classifier = RidgeClassifier()
ridge_classifier.fit(x_train, y_train)
y_pred_ridge = ridge_classifier.predict(x_test)
print("Accuracy RidgeClassifier:", metrics.accuracy_score(y_test, y_pred_ridge))

adaboost_classifier = AdaBoostClassifier(n_estimators=100)
adaboost_classifier.fit(x_train,y_train)
y_pred_adaboost = ridge_classifier.predict(x_test)
print("Accuracy AdaboostClassifier:", metrics.accuracy_score(y_test, y_pred_adaboost))

voting_classifier = VotingClassifier(estimators=[('nb', NB_classifier), ('et', et_classifier), 
                                     ('svc', SVC_classifier), ('ada',adaboost_classifier), 
                                     ('ridge',ridge_classifier)]
                         , voting='hard', weights=[1,1,1,1,1],flatten_transform=True, n_jobs=-1)
voting_classifier.fit(x_train,y_train)
y_pred_voting_classifier = voting_classifier.predict(x_test)
print("Accuracy VotingClassifier:", metrics.accuracy_score(y_test, y_pred_voting_classifier))

from sklearn.model_selection import cross_val_score

#####################
#CROSS_VALIDATION####
#####################

#import numpy as np

from scipy import sparse

print("Trainning with Cross-Validation")
X = sparse.vstack([x_train, x_test])
Y = y_train +  y_test
"""
#X = np.concatenate((x_train, x_test), axis=0)
#Y = np.concatenate((y_train, y_test), axis=0)
scores_NB = cross_val_score(NB_classifier, X, Y, cv=20)
print("NB %0.2f accuracy with a standard deviation of %0.2f" % (scores_NB.mean(), scores_NB.std()))
scores_ET = cross_val_score(et_classifier, X, Y, cv=20)
print("ET %0.2f accuracy with a standard deviation of %0.2f" % (scores_ET.mean(), scores_ET.std()))
scores_SVC = cross_val_score(SVC_classifier, X, Y, cv=20)
print("SVC %0.2f accuracy with a standard deviation of %0.2f" % (scores_SVC.mean(), scores_SVC.std()))
scores_ridge = cross_val_score(ridge_classifier, X, Y, cv=20)
print("ridge %0.2f accuracy with a standard deviation of %0.2f" % (scores_ridge.mean(), scores_ridge.std()))
scores_adaboost = cross_val_score(adaboost_classifier, X, Y, cv=20)
print("adaboost %0.2f accuracy with a standard deviation of %0.2f" % (scores_adaboost.mean(), scores_adaboost.std()))
#without adaboost_classifier
"""
#voting_classifier = VotingClassifier(estimators=[('nb', NB_classifier), ('et', et_classifier), 
#                                     ('svc', SVC_classifier),('ridge',ridge_classifier)]
#                         , voting='hard', weights=[1,1,1,1],flatten_transform=True, n_jobs=-1)
scores_voting = cross_val_score(voting_classifier, X, Y, cv=5)
print("voting %0.2f accuracy with a standard deviation of %0.2f" % (scores_voting.mean(), scores_voting.std()))


