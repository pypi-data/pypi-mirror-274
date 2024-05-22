import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

class CategoricalEncoder:
    def __init__(self, df):
        self.df = df

    def one_hot_encode(self, column):
        encoder = OneHotEncoder(sparse_output=False)
        encoded = encoder.fit_transform(self.df[[column]])
        encoded_df = pd.DataFrame(encoded, columns=[f"{column}_{cat}" for cat in encoder.categories_[0]])
        self.df = pd.concat([self.df, encoded_df], axis=1).drop(columns=[column])
        return self.df

    def label_encode(self, column):
        encoder = LabelEncoder()
        self.df[column] = encoder.fit_transform(self.df[column])
        return self.df