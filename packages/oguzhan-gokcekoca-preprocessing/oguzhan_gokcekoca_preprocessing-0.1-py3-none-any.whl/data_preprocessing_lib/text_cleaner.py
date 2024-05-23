import pandas as pd
import string
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class TextCleaner:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def remove_stopwords(self, text):
        return ' '.join(word for word in text.split() if word.lower() not in self.stop_words)

    def to_lowercase(self, df, column):
        df[column] = df[column].str.lower()
        return df

    def remove_punctuation(self, df, column):
        df[column] = df[column].apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))
        return df


    def lemmatize_text(self, text):
        return ' '.join(self.lemmatizer.lemmatize(word) for word in text.split())
