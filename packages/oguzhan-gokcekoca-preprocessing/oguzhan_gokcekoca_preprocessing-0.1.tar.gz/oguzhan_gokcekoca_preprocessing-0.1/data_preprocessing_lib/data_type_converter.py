import pandas as pd

class DataTypeConverter:
    def __init__(self):
        pass

    def to_numeric(self, df, columns):
        df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')
        return df

    def to_categorical(self, df, columns):
        df[columns] = df[columns].astype('category')
        return df

    def convert_to_categorical(self, df, columns):
        return self.to_categorical(df, columns)
