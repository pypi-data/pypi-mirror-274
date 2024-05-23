import os
import unittest
import pandas as pd

from data_preprocessing_lib.categorical_encoder import CategoricalEncoder

class TestCategoricalEncoder(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, './synthetic_sample_data.csv')
        self.df = pd.read_csv(file_path)
        self.df = self.df[['Genre']]
        self.encoder = CategoricalEncoder()

    def test_label_encode(self):
        encoded_df = self.encoder.label_encode(self.df.copy(), 'Genre')
        genres = sorted(self.df['Genre'].unique())
        genre_to_label = {genre: idx for idx, genre in enumerate(genres)}
        expected_result = self.df.replace({'Genre': genre_to_label})
        pd.testing.assert_frame_equal(encoded_df, expected_result)

    def test_one_hot_encode(self):
        encoded_df = self.encoder.one_hot_encode(self.df.copy(), 'Genre')
        expected_result = pd.get_dummies(self.df, columns=['Genre'], prefix='Genre').astype(int)
        pd.testing.assert_frame_equal(encoded_df, expected_result)

if __name__ == '__main__':
    unittest.main()
