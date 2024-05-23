import pandas as pd

from sklearn.preprocessing import OneHotEncoder, LabelEncoder

class CategoricalEncoder:
    def __init__(self):
        self.label_encoder = LabelEncoder()
        self.one_hot_encoder = OneHotEncoder()

    def label_encode(self, df, column):
        df[column] = self.label_encoder.fit_transform(df[column])
        return df

    def one_hot_encode(self, df, column):
        encoded = self.one_hot_encoder.fit_transform(df[[column]])
        encoded_df = pd.DataFrame(encoded.toarray(), columns=self.one_hot_encoder.get_feature_names_out([column]))
        # Cast columns to integers
        encoded_df = encoded_df.astype(int)
        df = df.join(encoded_df)
        df = df.drop(column, axis=1)
        return df
