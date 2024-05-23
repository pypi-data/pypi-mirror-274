import pandas as pd

class DataTypeConverter:
    @staticmethod
    def to_numeric(df, column):
        df[column] = pd.to_numeric(df[column], errors='coerce')
        return df

    @staticmethod
    def to_categorical(df, column):
        df[column] = df[column].astype('category')
        return df