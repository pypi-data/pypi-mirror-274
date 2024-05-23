class OutlierHandler:
    def __init__(self):
        pass

    def detect_outliers_iqr(self, df, column, threshold=1.5):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        return outliers

    def remove_outliers_iqr(self, df, column, threshold=1.5):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

    def remove_outliers(self, df, column, method='iqr', threshold=1.5):
        if method == 'iqr':
            return self.remove_outliers_iqr(df, column, threshold)
        else:
            raise ValueError("Invalid method. Supported methods: 'iqr'.")

