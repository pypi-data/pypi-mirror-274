import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')

class TextCleaner:
    def __init__(self, df, text_column):
        self.df = df
        self.text_column = text_column

    def remove_stopwords(self):
        stop_words = set(stopwords.words('english'))
        self.df[self.text_column] = self.df[self.text_column].apply(
            lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words])
        )
        return self.df

    def to_lowercase(self):
        self.df[self.text_column] = self.df[self.text_column].str.lower()
        return self.df

    def remove_punctuation(self):
        self.df[self.text_column] = self.df[self.text_column].apply(lambda x: re.sub(r'[^\w\s]', '', x))
        return self.df

    def lemmatize(self):
        lemmatizer = WordNetLemmatizer()
        self.df[self.text_column] = self.df[self.text_column].apply(
            lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x.split()])
        )
        return self.df
