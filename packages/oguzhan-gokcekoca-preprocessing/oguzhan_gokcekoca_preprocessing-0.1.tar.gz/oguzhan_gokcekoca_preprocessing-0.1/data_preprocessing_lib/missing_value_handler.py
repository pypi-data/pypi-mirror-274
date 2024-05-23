import pandas as pd
from sklearn.impute import SimpleImputer

class MissingValueHandler:
    def __init__(self):
        pass

    def impute_with_mean(self, df, columns):
        imputer = SimpleImputer(strategy='mean')
        df[columns] = imputer.fit_transform(df[columns])
        return df

    def impute_with_median(self, df, columns):
        imputer = SimpleImputer(strategy='median')
        df[columns] = imputer.fit_transform(df[columns])
        return df

    def impute_with_constant(self, df, columns, constant_value):
        imputer = SimpleImputer(strategy='constant', fill_value=constant_value)
        df[columns] = imputer.fit_transform(df[columns])
        return df

    def drop_missing(self, df):
        return df.dropna()
