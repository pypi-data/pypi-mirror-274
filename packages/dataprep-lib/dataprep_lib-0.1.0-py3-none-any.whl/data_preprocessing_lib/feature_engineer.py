import pandas as pd

class FeatureEngineer:
    @staticmethod
    def normalize_budget_by_year(df, budget_col, date_col):
        df[date_col] = pd.to_datetime(df[date_col])
        df['year'] = df[date_col].dt.year
        yearly_budget = df.groupby('year')[budget_col].transform('mean')
        df['normalized_budget'] = df[budget_col] / yearly_budget
        return df

    @staticmethod
    def extract_date_parts(df, date_col):
        df[date_col] = pd.to_datetime(df[date_col])
        df['year'] = df[date_col].dt.year
        df['month'] = df[date_col].dt.month
        df['day'] = df[date_col].dt.day
        return df