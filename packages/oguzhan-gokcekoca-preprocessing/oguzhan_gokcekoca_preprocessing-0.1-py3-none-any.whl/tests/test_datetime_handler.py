import os
import unittest
import pandas as pd
from data_preprocessing_lib.datetime_handler import DateTimeHandler

class TestDateTimeHandler(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, './synthetic_sample_data.csv')

        self.df = pd.read_csv(file_path)
        self.df = self.df[['Release Date', 'Budget in USD', 'Rating']]
        self.df['start_date'] = self.df['Release Date']
        self.df['end_date'] = self.df['Release Date']
        self.handler = DateTimeHandler()

    def test_convert_to_datetime(self):
        df_result = self.handler.to_datetime(self.df.copy(), 'Release Date', date_format='%d/%m/%Y')
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df_result['Release Date']))
        self.assertEqual(df_result['Release Date'][0], pd.Timestamp('1985-07-07'))

    def test_extract_date_parts(self):
        df = self.handler.to_datetime(self.df.copy(), 'Release Date', date_format='%d/%m/%Y')
        df_result = self.handler.extract_date_parts(df, 'Release Date')
        expected_result = df.copy()
        expected_result['Release Date'] = pd.to_datetime(expected_result['Release Date'], dayfirst=True)
        expected_result['Release Date_year'] = expected_result['Release Date'].dt.year
        expected_result['Release Date_month'] = expected_result['Release Date'].dt.month
        expected_result['Release Date_day'] = expected_result['Release Date'].dt.day
        
        pd.testing.assert_frame_equal(df_result, expected_result)

    def test_calculate_date_difference(self):
        df = self.handler.to_datetime(self.df.copy(), 'start_date', date_format='%d/%m/%Y')
        df = self.handler.to_datetime(df, 'end_date', date_format='%d/%m/%Y')
        df_result = self.handler.calculate_date_difference(df, 'start_date', 'end_date', 'date_diff')
        
        expected_result = df.copy()
        expected_result['date_diff'] = (expected_result['end_date'] - expected_result['start_date']).dt.days
        
        pd.testing.assert_frame_equal(df_result, expected_result)

if __name__ == '__main__':
    unittest.main()
