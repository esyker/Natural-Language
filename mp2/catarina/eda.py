import matplotlib.pyplot as plt
import numpy as np
from nltk import word_tokenize
from nltk.corpus import stopwords

def stats(x_train,y_train):
    labels = dict()
    terms = dict()
    stop_words = stopwords.words('english')
    for label in y_train:
        if label not in labels:
            labels[label]=1
        else:
            labels[label]+=1
    for sentence in x_train:
        tokens = word_tokenize(sentence)
        for token in tokens:
            if token not in stop_words:
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
    plt.xticks(np.arange(len(values)),terms_word, rotation = 45)
    plt.ylabel('Count')
    plt.xlabel('Term')
    plt.title(title)
    plt.show()