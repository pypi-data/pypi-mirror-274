from sklearn.preprocessing import MinMaxScaler, StandardScaler
import pandas as pd

class Scaler:
    @staticmethod
    def min_max_scale(df, column):
        scaler = MinMaxScaler()
        df[column] = scaler.fit_transform(df[[column]])
        return df

    @staticmethod
    def standard_scale(df, column):
        scaler = StandardScaler()
        df[column] = scaler.fit_transform(df[[column]])
        return df