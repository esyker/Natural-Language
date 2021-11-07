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

stemmer = SnowballStemmer('english')
#stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
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

def preprocess(tokenized_line):
    stop_words = stopwords.words("english")
    tokens=[]
    for word in tokenized_line:
        if word not in stop_words:
            word = remove_punctuation(word)
            word = remove_letter_only(word)
            word = process_number(word)
            word = word.lower()
            if word:
                word = stemmer.stem(word)
                tokens.append(word)
    return tokens

def read_data(file):
    with open(file, "r", encoding='utf-8') as fp:
        x_data = []
        y_data = []
        for line in fp.readlines():
            tokens = line.split()
            x_data.append(' '.join(token for token in tokens[1:]))
            y_data.append(tokens[0])
        return x_data, y_data
    
def process_data(file):
    with open(file, "r", encoding='utf-8') as fp:
        x_data = []
        y_data = []
        for line in fp.readlines():
            tokenized_line = word_tokenize(line)
            tokens = preprocess(tokenized_line[1:])
            label = tokenized_line[0]
            x_data.append(tokens)
            y_data.append(label)
        return x_data, y_data


def vectorize(x_train, x_test, is_count=False):
    if is_count:
        vectorizer = CountVectorizer()
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
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(X)
    else:
        vectorizer = TfidfVectorizer(sublinear_tf=True, tokenizer = lambda x: x
                            , stop_words =None , lowercase = False)
        X = vectorizer.fit_transform(X)
    return X

#read the data
#no preprocessing
x_train, y_train = read_data("trainWithoutDev.txt")
x_test, y_test = process_data("dev.txt")
X_noprep = x_train + x_test
X_noprep = vectorize_single(X_noprep)
Y_noprep = y_train +  y_test
#preprocessing
x_train, y_train = process_data("trainWithoutDev.txt")
x_test, y_test = process_data("dev.txt")
X_prep = x_train + x_test
X_prep = vectorize_single(X_prep)
Y_prep = y_train +  y_test

#classifiers
NB_classifier = ComplementNB()

et_classifier = ExtraTreesClassifier(n_jobs=-1)

SVC_classifier = SVC(kernel='linear', probability=True)

ridge_classifier = RidgeClassifier()

voting_classifier = VotingClassifier(estimators=[('nb', NB_classifier), ('et', et_classifier), 
                                     ('svc', SVC_classifier), ('ridge',ridge_classifier)]
                         , voting='hard', weights=[1,1,1,1],flatten_transform=True, n_jobs=-1)

#####################
#CROSS_VALIDATION####
#####################
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_validate

print("Trainning with Cross-Validation")

kfold = KFold(n_splits=5, shuffle=True, random_state=1)
scoring = {'acc': 'accuracy', 'bal. acc': 'balanced_accuracy', 'prec.': 'precision_macro'
                   , 'recall' : 'recall_macro'}

experimental_setups = [{'prep': False,'classifiers':['all']},
                       {'prep':'Snowball'},{'prep:'}]

"""
def experimental_setup(experimental_setups):
    no_prec = {'x_train' = x_train, }
    x_train_no_prec = x_train
    x_train_no_prec = x_train
    x_train_no_prec = x_train
    x_train_no_prec = x_train
    for es in experimental_setups:
       if(es[])     
"""          
    
def print_scores(scores, name):
    print("-------",name," --------\n" )
    print("Avg. Acc ",scores_NB['test_acc'].mean(), " sd: ", scores_NB['test_acc'].std())
    print("Avg. Bal. Acc ",scores_NB['test_bal. acc'].mean(), " sd: ", scores_NB['test_bal. acc'].std())
    print("Avg. Precision ",scores_NB['test_prec.'].mean(), " sd: ", scores_NB['test_prec.'].std())
    print("Avg. Recall ",scores_NB['test_recall'].mean(), " sd: ", scores_NB['test_recall'].std())

scores_NB = cross_validate(NB_classifier, X_prep, Y_prep, cv=kfold, scoring = scoring)
print_scores(scores_NB, "scores_NB")

scores_ET = cross_validate(et_classifier, X_prep, Y_prep, cv=kfold, scoring = scoring)
print_scores(scores_ET, "scores_ET")

scores_SVC = cross_validate(SVC_classifier, X_prep , Y_prep, cv=kfold, scoring = scoring)
print_scores(scores_SVC, "scores_SVC")

scores_ridge = cross_validate(ridge_classifier, X_prep , Y_prep, cv=kfold, scoring = scoring)
print_scores(scores_ridge, "scores_RIDGE")

scores_voting = cross_validate(voting_classifier, X_prep, Y_prep, cv=kfold, scoring = scoring)
print_scores(scores_voting, "scores_VOTING")


"""
#################################################
#FINAL RESULTS: NO CROSS_VALIDATION !!!!!!!!!####
#################################################

x_train, y_train = process_data("trainWithoutDev.txt")
x_test, y_test = process_data("dev.txt")


#file = open('processed_trained_data.txt', 'w', encoding='utf-8')
#file.writelines(x_train)
#file.close()

x_train, x_test = vectorize(x_train, x_test)

#with open("variables.pickle", "wb") as f:
#    pickle.dump([x_train, y_train, x_test, y_test], f)
# with open('variables.pickle', 'rb') as f:
#     x_train, y_train, x_test, y_test = pickle.load(f)

NB_classifier.fit(x_train, y_train)
y_pred_NB = NB_classifier.predict(x_test)
print("Accuracy ComplementNB:", metrics.accuracy_score(y_test, y_pred_NB))

et_classifier.fit(x_train, y_train)
y_pred_et = et_classifier.predict(x_test)
print("Accuracy ExtraTreesClassifier:", metrics.accuracy_score(y_test, y_pred_et))

# Support Vector
SVC_classifier.fit(x_train, y_train)
y_pred_SVC = SVC_classifier.predict(x_test)
print("Accuracy SVC:", metrics.accuracy_score(y_test, y_pred_SVC))

ridge_classifier.fit(x_train, y_train)
y_pred_ridge = ridge_classifier.predict(x_test)
print("Accuracy RidgeClassifier:", metrics.accuracy_score(y_test, y_pred_ridge))

voting_classifier.fit(x_train,y_train)
y_pred_voting_classifier = voting_classifier.predict(x_test)
print("Accuracy VotingClassifier:", metrics.accuracy_score(y_test, y_pred_voting_classifier))
"""
