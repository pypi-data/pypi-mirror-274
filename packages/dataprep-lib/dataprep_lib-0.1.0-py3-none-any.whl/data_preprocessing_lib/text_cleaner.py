import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

class TextCleaner:
    @staticmethod
    def clean_text(text):
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        words = word_tokenize(text)
        words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
        return ' '.join(words)

    @staticmethod
    def clean_column(df, column):
        df[column] = df[column].apply(TextCleaner.clean_text)
        return df