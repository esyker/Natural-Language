from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import  LogisticRegressionCV
from spacy_preprocessing import TextPreprocessor
# ... assuming data split X_train, X_test ...

clf  = Pipeline(steps=[
        ('normalize': TextPreprocessor(n_jobs=-1), 
        ('features', TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
        ('classifier', LogisticRegressionCV(cv=5,solver='saga',scoring='accuracy', n_jobs=-1, verbose=1))
    ])

clf.fit(X_train, y_train)
clf.predict(X_test)
