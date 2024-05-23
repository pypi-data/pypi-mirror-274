import pandas as pd

class DateTimeHandler:
    def to_datetime(self, df, column, date_format=None):
        if date_format:
            df[column] = pd.to_datetime(df[column], format=date_format, dayfirst=True)
        else:
            df[column] = pd.to_datetime(df[column], dayfirst=True)
        return df

    def extract_date_parts(self, df, column):
        df[column + '_year'] = df[column].dt.year
        df[column + '_month'] = df[column].dt.month
        df[column + '_day'] = df[column].dt.day
        return df

    def calculate_date_difference(self, df, start_column, end_column, new_column_name):
        df[new_column_name] = (df[end_column] - df[start_column]).dt.days
        return df
