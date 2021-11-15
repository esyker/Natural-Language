import pickle
from string import punctuation

import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer, SnowballStemmer
from nltk.tokenize import word_tokenize
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import RidgeClassifier
from sklearn.naive_bayes import ComplementNB
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier

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

def preprocess(tokenized_line, proc = 'Snowball', keep_stop_words = True, punctuation_remove = True,
               proc_number = True, lower = True):
    if(not bool(proc)):
        return tokenized_line
    processor = None
    if(proc == 'Snowball'):
        processor = SnowballStemmer('english')
    elif(proc == 'Porter'):
        processor = PorterStemmer()
    elif(proc == 'Lemmatizer'):
        processor = WordNetLemmatizer()
    stop_words = stopwords.words("english")
    tokens=[]
    for word in tokenized_line:
        if(keep_stop_words or (word not in stop_words)):#default is no stop-word removal
            if(punctuation_remove):#default is punctuation removal
                word = remove_punctuation(word)
            word = remove_letter_only(word)
            if(proc_number):
                word = process_number(word)
            if(lower):
                word = word.lower()
            if word:
                if(proc == 'Lemmatizer'):
                    word = processor.lemmatize(word)
                else:
                    word = processor.stem(word)
                tokens.append(word)
    return tokens
    
def process_data(file, proc = 'Snowball', keep_stop_words = True, punctuation_remove = True,
               proc_number = True, lower = True):
    with open(file, "r", encoding='utf-8') as fp:
        x_data = []
        y_data = []
        for line in fp.readlines():
            tokenized_line = word_tokenize(line)
            tokens = preprocess(tokenized_line[1:], proc, keep_stop_words, punctuation_remove,
                                proc_number, lower)
            label = tokenized_line[0]
            x_data.append(tokens)
            y_data.append(label)
        return x_data, y_data


def vectorize(x_train, x_test, is_count=False):
    if is_count:
        vectorizer = CountVectorizer(tokenizer = lambda x: x, stop_words =None , 
                                     lowercase = False)
        x_train = vectorizer.fit_transform(x_train)
        x_test = vectorizer.transform(x_test)
    else:
        vectorizer = TfidfVectorizer(sublinear_tf=True, tokenizer = lambda x: x
                            , stop_words =None , lowercase = False)
        x_train = vectorizer.fit_transform(x_train)
        x_test = vectorizer.transform(x_test)
    return x_train, x_test

def vectorize_single(X, is_count = False):
    if is_count:
        vectorizer = CountVectorizer(tokenizer = lambda x: x, stop_words =None , 
                                     lowercase = False)
        X = vectorizer.fit_transform(X)
    else:
        vectorizer = TfidfVectorizer(sublinear_tf=True, tokenizer = lambda x: x
                            , stop_words =None , lowercase = False)
        X = vectorizer.fit_transform(X)
    return X


#classifiers
NB_classifier = ComplementNB()

et_classifier = ExtraTreesClassifier(n_jobs=-1)

SVC_classifier = SVC(kernel='linear')

ridge_classifier = RidgeClassifier()

#voting_classifier = VotingClassifier(estimators=[('nb', NB_classifier), ('et', et_classifier), 
#                                     ('svc', SVC_classifier), ('ridge',ridge_classifier)]
#                         , voting='hard', weights=[1,1,1,1],flatten_transform=True, n_jobs=1)

voting_classifier = VotingClassifier(estimators=[('nb', NB_classifier), 
                                     ('svc', SVC_classifier), ('ridge',ridge_classifier)]
                         , voting='hard', weights=[1,1,1],flatten_transform=True, n_jobs=1)

"""
#####################
#CROSS_VALIDATION####
#####################

x_train, y_train = process_data("trainWithoutDev.txt")
x_test, y_test = process_data("dev.txt")
X_prep = x_train + x_test
X_prep = vectorize_single(X_prep)
Y_prep = y_train +  y_test
X = X_prep
Y = Y_prep

from sklearn.model_selection import KFold
from sklearn.model_selection import cross_validate

print("Trainning with Cross-Validation")

kfold = KFold(n_splits=5, shuffle=False)
scoring = ['accuracy', 'balanced_accuracy','f1_macro']

def print_scores(scores, name):
    print("-------",name," --------\n" )
    print("Avg. Acc ", round(scores['test_accuracy'].mean(),3), " sd: ", round(scores['test_accuracy'].std(),3))
    print("Avg. Bal. Acc ",round(scores['test_balanced_accuracy'].mean(),3), " sd: ", round(scores['test_balanced_accuracy'].std(),3))
    print("Avg. f1-score ",round(scores['test_f1_macro'].mean(),3), " sd: ", round(scores['test_f1_macro'].std(),3))
        

scores_ridge = cross_validate(ridge_classifier, X , Y, cv=kfold, scoring = scoring)
print_scores(scores_ridge, "scores_RIDGE")

scores_SVC = cross_validate(SVC_classifier, X , Y, cv=kfold, scoring = scoring)

print_scores(scores_SVC, "scores_SVC")

scores_NB = cross_validate(NB_classifier, X, Y, cv=kfold, scoring = scoring)
print_scores(scores_NB, "scores_NB")

scores_ET = cross_validate(et_classifier, X, Y, cv=kfold, scoring = scoring)
print_scores(scores_ET, "scores_ET")

scores_voting = cross_validate(voting_classifier, X, Y, cv=kfold, scoring = scoring)
print_scores(scores_voting, "scores_VOTING")
"""
#################################################
#FINAL RESULTS: NO CROSS_VALIDATION !!!!!!!!!####
#################################################

x_train, y_train = process_data("trainWithoutDev.txt")
x_test, y_test = process_data("dev.txt")

x_train, x_test = vectorize(x_train, x_test)

print("Trainning without Cross-Validation")

ridge_classifier.fit(x_train, y_train)
y_pred_ridge = ridge_classifier.predict(x_test)
print("Accuracy Ridge:", metrics.accuracy_score(y_test, y_pred_ridge),
      "Balanced Accuracy Ridge:", metrics.balanced_accuracy_score(y_test, y_pred_ridge),
      "F1-Score Ridge:", metrics.f1_score(y_test, y_pred_ridge, average='macro'))

# Support Vector
SVC_classifier.fit(x_train, y_train)
y_pred_SVC = SVC_classifier.predict(x_test)
print("Accuracy SVC:", metrics.accuracy_score(y_test, y_pred_SVC),
      "Balanced Accuracy SVC:", metrics.balanced_accuracy_score(y_test, y_pred_SVC),
      "F1-Score SVC:", metrics.f1_score(y_test, y_pred_SVC, average='macro'))

NB_classifier.fit(x_train, y_train)
y_pred_NB = NB_classifier.predict(x_test)
print("Accuracy ComplementNB:", metrics.accuracy_score(y_test, y_pred_NB),
      "Balanced Accuracy NB:", metrics.balanced_accuracy_score(y_test, y_pred_NB),
      "F1-Score NB:", metrics.f1_score(y_test, y_pred_NB, average='macro'))

et_classifier.fit(x_train, y_train)
y_pred_et = et_classifier.predict(x_test)
print("Accuracy ET:", metrics.accuracy_score(y_test, y_pred_et),
      "Balanced Accuracy ET:", metrics.balanced_accuracy_score(y_test, y_pred_et),
      "F1-Score ET:", metrics.f1_score(y_test, y_pred_et, average='macro'))



voting_classifier.fit(x_train,y_train)
y_pred_voting_classifier = voting_classifier.predict(x_test)
print("Accuracy Voting:", metrics.accuracy_score(y_test, y_pred_voting_classifier),
      "Balanced Accuracy Voting:", metrics.balanced_accuracy_score(y_test, y_pred_voting_classifier),
      "F1-Score Voting:", metrics.f1_score(y_test, y_pred_voting_classifier, average='macro'))