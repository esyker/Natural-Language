import nltk
from nltk import pos_tag
from nltk import word_tokenize
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from nltk_preprocessing import Preprocess
import numpy as np

#show all possible tags
print(nltk.help.upenn_tagset())

sent_list = ["Hello World", "I am Diogo", "I did not learn much in school",
             "They refuse to permit us to obtain the refuse permit"]

tokenized_sent_list =[]

def pos_tag_sentence(sent,sent_list):
    text = word_tokenize(sent)
    tags = pos_tag(text)
    sent_list.append(tags)

preprocessor = Preprocess()
label_encoder = LabelEncoder()

for sent in sent_list:
    pos_tag_sentence(sent, tokenized_sent_list)

flat_list = [item[1] for sublist in tokenized_sent_list for item in sublist]
print(flat_list)
encoded_no_preprocess = label_encoder.fit_transform(flat_list)

tokenized_sent_list = []

for i in range(len(sent_list)):
    sent_list[i]=preprocessor.preprocess(sent_list[i])
    
for sent in sent_list:
    pos_tag_sentence(sent, tokenized_sent_list)

#print(tokenized_sent_list)
#tokenized_sent_list = np.array(tokenized_sent_list, dtype='object')

    
flat_list = [item[1] for sublist in tokenized_sent_list for item in sublist]
print(flat_list)
encoded_preprocessed = label_encoder.fit_transform(flat_list)

