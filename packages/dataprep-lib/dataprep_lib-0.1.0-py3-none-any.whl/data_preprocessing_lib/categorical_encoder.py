import pandas as pd

class CategoricalEncoder:
    @staticmethod
    def one_hot_encode(df, column):
        return pd.get_dummies(df, columns=[column])

    @staticmethod
    def label_encode(df, column):
        df[column] = df[column].astype('category').cat.codes
        return df