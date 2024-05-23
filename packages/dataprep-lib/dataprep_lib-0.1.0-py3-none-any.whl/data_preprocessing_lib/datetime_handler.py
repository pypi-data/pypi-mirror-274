import pandas as pd

class DateTimeHandler:
    @staticmethod
    def extract_date_parts(df, date_col):
        df[date_col] = pd.to_datetime(df[date_col])
        df['year'] = df[date_col].dt.year
        df['month'] = df[date_col].dt.month
        df['day'] = df[date_col].dt.day
        return df