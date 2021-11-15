import matplotlib.pyplot as plt
import numpy as np
from nltk import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud

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
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import VotingClassifier
from string import punctuation

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


def read_data(file):
    with open(file, "r", encoding='utf-8') as fp:
        x_data = []
        y_data = []
        for line in fp.readlines():
            tokens = line.split()
            x_data.append(' '.join(token for token in tokens[1:]))
            y_data.append(tokens[0])
        return x_data, y_data

def stats(x_train,y_train):
    labels = dict()
    terms = dict()
    for label in y_train:
        if label not in labels:
            labels[label]=1
        else:
            labels[label]+=1
    for sentence in x_train:
        tokens = word_tokenize(sentence)
        for token in tokens:
                if token not in terms:
                    terms[token]=1
                else:
                    terms[token]+=1          
    return labels, terms

def terms_by_label(x_train,y_train,label):
    terms = dict()
    stop_words = stopwords.words('english')
    for i in range(len(y_train)):
        if y_train[i]!=label:
            continue
        sentence = x_train[i]
        tokens = word_tokenize(sentence)
        for token in tokens:
            if token not in stop_words:
                if token not in terms:
                    terms[token]=1
                else:
                    terms[token]+=1          
    return terms
    

def piechart_labels(labels):
    sizes = labels.values()
    labels = labels.keys()
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

def barchart_terms(terms, title):
    sorted_terms = sorted(terms.items(), key=lambda term_value: term_value[1])
    print(sorted_terms[-10:])
    values =[]
    terms_word =[]
    for i in range(20):
        print(sorted_terms[-i])
        values.append(sorted_terms[-i-1][1])
        terms_word.append(sorted_terms[-i-1][0])
    plt.bar(np.arange(len(values)),values,align='center',alpha = 0.5)
    plt.xticks(np.arange(len(values)),terms_word, rotation = 75)
    plt.ylabel('Count')
    plt.xlabel('Term')
    plt.title(title)
    plt.show()

def plotWordCloud(tokens_dict):
    cloud=WordCloud(width=int(400*1.5), height=int(200*1.5))
    cloud=cloud.fit_words(tokens_dict)
    fig=plt.imshow(cloud)
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.rcParams["axes.grid"] = False
    plt.show()

def calculate_overlap(dict1,dict2):
    overlap_terms=0
    for key in dict1:
        if key in dict2:
            overlap_terms+=1
    return overlap_terms

def overlapping_terms(geography, music, history, literature, science):
    print("geography_terms", len(geography.keys()))
    print("music_terms", len(music.keys()))
    print("history", len(history.keys()))
    print("literature",len(literature.keys()))
    print("science",len(science.keys()))
    print("geography_music",calculate_overlap(geography,music))
    print("geography_history",calculate_overlap(geography,history))
    print("geography_literature",calculate_overlap(geography,literature))
    print("geography_science",calculate_overlap(geography,science))
    print("music_history",calculate_overlap(music,history))
    print("music_literature",calculate_overlap(music,literature))
    print("music_science",calculate_overlap(music,science))
    print("history_literature",calculate_overlap(history,literature))
    print("history_science",calculate_overlap(history,science))
    print("literature_science",calculate_overlap(literature,science))
    return

if __name__ == "__main__":
    #x_train, y_train = read_data("trainWithoutDev.txt")
    x_train, y_train = process_data("trainWithoutDev.txt")
    #labels, terms = stats(x_train,y_train)
    science = terms_by_label(x_train,y_train,"SCIENCE")
    music = terms_by_label(x_train,y_train,"MUSIC")
    history =terms_by_label(x_train,y_train,"HISTORY")
    geography = terms_by_label(x_train,y_train,"GEOGRAPHY")
    literature = terms_by_label(x_train,y_train,"LITERATURE")
    overlapping_terms(geography, music, history, literature, science)
    #plotWordCloud(terms)
    #barchart_terms(terms, "Term Distribution without preprocessing")
    