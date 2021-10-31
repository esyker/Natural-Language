import pickle
from string import punctuation

import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import RidgeClassifier
from sklearn.naive_bayes import ComplementNB
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import VotingClassifier

# stemmer = SnowballStemmer('english')
stemmer = PorterStemmer()
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
    processed_line = ""
    stop_words = stopwords.words("english")
    for word in tokenized_line:
        if word not in stop_words:
            word = remove_punctuation(word)
            word = remove_letter_only(word)
            word = process_number(word)
            if word:
                word = stemmer.stem(word)
                processed_line += word + " "
    return processed_line


def process_data(file):
    with open(file, "r", encoding='utf-8') as fp:
        x_data = []
        y_data = []
        for line in fp.readlines():
            tokenized_line = word_tokenize(line)
            processed_line = preprocess(tokenized_line[1:])
            x_data.append(processed_line)
            y_data.append(tokenized_line[0])
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


x_train, y_train = process_data("trainWithoutDev.txt")
x_test, y_test = process_data("dev.txt")

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

et_classifier = ExtraTreesClassifier()
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
                                     ('svc', SVC_classifier), ('ada',adaboost_classifier)]
                         , voting='soft', weights=[3,1,4,2],flatten_transform=True)
voting_classifier.fit(x_train,y_train)
y_pred_voting_classifier = voting_classifier.predict(x_test)
print("Accuracy VotingClassifier:", metrics.accuracy_score(y_test, y_pred_voting_classifier))
