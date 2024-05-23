import unittest
import pandas as pd
from data_preprocessing_lib.outlier_handler import OutlierHandler

class TestOutlierHandler(unittest.TestCase):
    def setUp(self):
        file_path = './synthetic_sample_data.csv'
        self.df = pd.read_csv(file_path)
        if 'Budget in USD' not in self.df.columns:
            raise KeyError("Column 'Budget in USD' not found in the CSV file.")
        
        self.df = self.df[['Budget in USD']]
        self.handler = OutlierHandler()

    def test_remove_outliers(self):
        df_result = self.handler.remove_outliers(self.df.copy(), 'Budget in USD').reset_index(drop=True)
        
        Q1 = self.df['Budget in USD'].quantile(0.25)
        Q3 = self.df['Budget in USD'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        expected_result = self.df[(self.df['Budget in USD'] >= lower_bound) & (self.df['Budget in USD'] <= upper_bound)].reset_index(drop=True)
        
        pd.testing.assert_frame_equal(df_result, expected_result)

if __name__ == '__main__':
    unittest.main()
