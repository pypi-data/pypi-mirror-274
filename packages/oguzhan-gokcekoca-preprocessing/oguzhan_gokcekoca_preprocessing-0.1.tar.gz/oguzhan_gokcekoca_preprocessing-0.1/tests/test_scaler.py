import unittest
import pandas as pd
from data_preprocessing_lib.scaler import Scaler

class TestScaler(unittest.TestCase):
    def setUp(self):
        file_path = './synthetic_sample_data.csv'
        self.df = pd.read_csv(file_path)
        
        if 'Budget in USD' not in self.df.columns or 'Rating' not in self.df.columns:
            raise KeyError("Required columns not found in the CSV file.")
        
        self.df = self.df[['Budget in USD', 'Rating']]
        self.scaler = Scaler()

    def test_min_max_scale(self):
        df_result = self.scaler.min_max_scale(self.df.copy())
        expected_result = self.df.copy()
        for column in expected_result.columns:
            min_value = expected_result[column].min()
            max_value = expected_result[column].max()
            expected_result[column] = (expected_result[column] - min_value) / (max_value - min_value)
        
        pd.testing.assert_frame_equal(df_result, expected_result)

if __name__ == '__main__':
    unittest.main()
