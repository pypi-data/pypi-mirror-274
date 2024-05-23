import os
import unittest
import pandas as pd
from data_preprocessing_lib.data_type_converter import DataTypeConverter

class TestDataTypeConverter(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, './synthetic_sample_data.csv')
        
        self.df = pd.read_csv(file_path)
        self.df = self.df[['Rating', 'Genre']]
        self.converter = DataTypeConverter()

    def test_to_numeric(self):
        df_result = self.converter.to_numeric(self.df.copy(), 'Rating')
        expected_result = self.df.copy()
        expected_result['Rating'] = pd.to_numeric(expected_result['Rating'])
        
        pd.testing.assert_frame_equal(df_result, expected_result)

    def test_to_categorical(self):
        df_result = self.converter.to_categorical(self.df.copy(), 'Genre')
        expected_result = self.df.copy()
        expected_result['Genre'] = pd.Categorical(expected_result['Genre'])
        
        pd.testing.assert_frame_equal(df_result, expected_result)

if __name__ == '__main__':
    unittest.main()
