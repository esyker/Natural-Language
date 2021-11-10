import re
import sys
from string import punctuation

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer, SnowballStemmer
from nltk.tokenize import word_tokenize
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import RidgeClassifier
from sklearn.naive_bayes import ComplementNB
from sklearn.svm import SVC

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


def preprocess(tokenized_line, proc='Snowball', keep_stop_words=True, punctuation_remove=True,
               proc_number=True, lower=True):
    if (not bool(proc)):
        return tokenized_line
    processor = None
    if (proc == 'Snowball'):
        processor = SnowballStemmer('english')
    elif (proc == 'Porter'):
        processor = PorterStemmer()
    elif (proc == 'Lemmatizer'):
        processor = WordNetLemmatizer()
    stop_words = stopwords.words("english")
    tokens = []
    for word in tokenized_line:
        if (keep_stop_words or (word not in stop_words)):  # default is no stop-word removal
            if (punctuation_remove):  # default is punctuation removal
                word = remove_punctuation(word)
            word = remove_letter_only(word)
            if (proc_number):
                word = process_number(word)
            if (lower):
                word = word.lower()
            if word:
                if (proc == 'Lemmatizer'):
                    word = processor.lemmatize(word)
                else:
                    word = processor.stem(word)
                tokens.append(word)
    return tokens


def process_data(file, label=True, proc='Snowball', keep_stop_words=True, punctuation_remove=True,
                 proc_number=True, lower=True):
    with open(file, "r", encoding='utf-8') as fp:
        x_data = []
        y_data = []
        for line in fp.readlines():
            tokenized_line = word_tokenize(line)
            if label:
                tokens = preprocess(tokenized_line[1:], proc, keep_stop_words, punctuation_remove,
                                    proc_number, lower)
                label = tokenized_line[0]
                y_data.append(label)
            else:
                tokens = preprocess(tokenized_line, proc, keep_stop_words, punctuation_remove,
                                    proc_number, lower)
            x_data.append(tokens)
        if label:
            return x_data, y_data
        else:
            return x_data


def vectorize(x_train, x_test, is_count=False):
    if is_count:
        vectorizer = CountVectorizer(tokenizer=lambda x: x, stop_words=None,
                                     lowercase=False)
        x_train = vectorizer.fit_transform(x_train)
        x_test = vectorizer.transform(x_test)
    else:
        vectorizer = TfidfVectorizer(sublinear_tf=True, tokenizer=lambda x: x
                                     , stop_words=None, lowercase=False)
        x_train = vectorizer.fit_transform(x_train)
        x_test = vectorizer.transform(x_test)
    return x_train, x_test


def vectorize_single(X, is_count=False):
    if is_count:
        vectorizer = CountVectorizer(tokenizer=lambda x: x, stop_words=None,
                                     lowercase=False)
        X = vectorizer.fit_transform(X)
    else:
        vectorizer = TfidfVectorizer(sublinear_tf=True, tokenizer=lambda x: x
                                     , stop_words=None, lowercase=False)
        X = vectorizer.fit_transform(X)
    return X


def output_prediction(prediction, output_file):
    with open(output_file, "w") as fp:
        for label in prediction:
            fp.write(label + '\n')


def train_and_predict(train_file, test_file, output_file):
    NB_classifier = ComplementNB()

    et_classifier = ExtraTreesClassifier(n_jobs=-1, random_state=30)

    SVC_classifier = SVC(kernel='linear')

    ridge_classifier = RidgeClassifier()

    voting_classifier = VotingClassifier(estimators=[('nb', NB_classifier), ('et', et_classifier),
                                                     ('svc', SVC_classifier), ('ridge', ridge_classifier)]
                                         , voting='hard', weights=[1, 1, 1, 1], flatten_transform=True, n_jobs=1)

    x_train, y_train = process_data(train_file)
    x_test, y_test = process_data(test_file)
    # x_test = process_data(test_file, label=False)

    x_train, x_test = vectorize(x_train, x_test)

    voting_classifier.fit(x_train, y_train)

    y_pred_voting_classifier = voting_classifier.predict(x_test)

    print(y_pred_voting_classifier)
    output_prediction(y_pred_voting_classifier, output_file)

    print("Accuracy Voting:", metrics.accuracy_score(y_test, y_pred_voting_classifier),
          "Balanced Accuracy Voting:", metrics.balanced_accuracy_score(y_test, y_pred_voting_classifier),
          "F1-Score Voting:", metrics.f1_score(y_test, y_pred_voting_classifier, average='macro'))


args = sys.argv
test_file = args[2]
train_file = args[4]
output_file = args[6]
print(test_file, train_file, output_file)

train_and_predict(train_file, test_file, output_file)
