from sklearn.preprocessing import StandardScaler, MinMaxScaler

class Scaler:
    def __init__(self, df):
        self.df = df

    def standard_scaler(self, columns):
        scaler = StandardScaler()
        self.df[columns] = scaler.fit_transform(self.df[columns])

    def min_max_scaler(self, columns):
        scaler = MinMaxScaler()
        self.df[columns] = scaler.fit_transform(self.df[columns])
