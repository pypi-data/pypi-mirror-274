import pandas as pd
class DataTypeConverter:
    def __init__(self, df):
        self.df = df

    def to_numeric(self, columns):
        for column in columns:
            self.df[column] = pd.to_numeric(self.df[column], errors='coerce')
        return self.df

    def to_categorical(self, columns):
        for column in columns:
            self.df[column] = self.df[column].astype('category')
        return self.df