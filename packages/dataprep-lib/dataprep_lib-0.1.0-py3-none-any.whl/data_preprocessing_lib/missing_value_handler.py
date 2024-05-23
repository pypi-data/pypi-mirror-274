import pandas as pd

class MissingValueHandler:
    @staticmethod
    def impute_with_mean(df, column):
        mean_value = df[column].mean()
        df[column].fillna(mean_value, inplace=True)
        return df

    @staticmethod
    def impute_with_median(df, column):
        median_value = df[column].median()
        df[column].fillna(median_value, inplace=True)
        return df

    @staticmethod
    def impute_with_constant(df, column, constant):
        df[column].fillna(constant, inplace=True)
        return df

    @staticmethod
    def drop_missing(df, column):
        df.dropna(subset=[column], inplace=True)
        return df