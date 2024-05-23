class FeatureEngineer:
    def __init__(self, df):
        self.df = df

    def add_interaction_term(self, column1, column2, new_column_name):
        self.df[new_column_name] = self.df[column1] * self.df[column2]
        return self.df

    def add_polynomial_terms(self, column, degree=2):
        for i in range(2, degree + 1):
            self.df[f'{column}_power_{i}'] = self.df[column] ** i
        return self.df
