from sklearn.preprocessing import StandardScaler, MinMaxScaler

class Scaler:
    def __init__(self):
        self.standard_scaler = StandardScaler()
        self.min_max_scaler = MinMaxScaler()

    def standard_scale(self, df, columns=None):
        if columns is None:
            columns = df.columns
        df[columns] = self.standard_scaler.fit_transform(df[columns])
        return df

    def min_max_scale(self, df, columns=None):
        if columns is None:
            columns = df.columns
        df[columns] = self.min_max_scaler.fit_transform(df[columns])
        return df
