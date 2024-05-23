import os
import unittest
import pandas as pd
from data_preprocessing_lib.missing_value_handler import MissingValueHandler

class TestMissingValueHandler(unittest.TestCase):
    def setUp(self):
        file_path = './synthetic_sample_data.csv'
        self.df = pd.read_csv(file_path)
        self.df = self.df[['Budget in USD', 'Rating']]
        self.df.loc[0, 'Budget in USD'] = None
        self.df.loc[1, 'Rating'] = None
        self.handler = MissingValueHandler()

    def test_impute_with_mean(self):
        df_with_nan = self.df.copy()
        budget_mean = df_with_nan['Budget in USD'].mean()
        rating_mean = df_with_nan['Rating'].mean()

        df_result = self.handler.impute_with_mean(df_with_nan.copy(), ['Budget in USD', 'Rating'])
        df_result['Rating'] = df_result['Rating'].astype('float64')

        expected_result = df_with_nan.copy()
        expected_result.loc[0, 'Budget in USD'] = budget_mean
        expected_result.loc[1, 'Rating'] = rating_mean

        # Handle remaining NaNs (if any)
        expected_result = expected_result.fillna({
            'Budget in USD': budget_mean,
            'Rating': rating_mean
        })

        pd.testing.assert_frame_equal(df_result, expected_result)

    def test_impute_with_median(self):
        df_with_nan = self.df.copy()
        budget_median = df_with_nan['Budget in USD'].median()
        rating_median = df_with_nan['Rating'].median()

        df_result = self.handler.impute_with_median(df_with_nan.copy(), ['Budget in USD', 'Rating'])
        df_result['Rating'] = df_result['Rating'].astype('float64')

        expected_result = df_with_nan.copy()
        expected_result.loc[0, 'Budget in USD'] = budget_median
        expected_result.loc[1, 'Rating'] = rating_median

        # Handle remaining NaNs (if any)
        expected_result = expected_result.fillna({
            'Budget in USD': budget_median,
            'Rating': rating_median
        })

        pd.testing.assert_frame_equal(df_result, expected_result)

    def test_impute_with_constant(self):
        constant_value = 0
        df_with_nan = self.df.copy()

        df_result = self.handler.impute_with_constant(df_with_nan.copy(), ['Budget in USD', 'Rating'], constant_value)
        df_result['Rating'] = df_result['Rating'].astype('float64')

        expected_result = df_with_nan.copy()
        expected_result.loc[0, 'Budget in USD'] = constant_value
        expected_result.loc[1, 'Rating'] = constant_value

        # Handle remaining NaNs (if any)
        expected_result = expected_result.fillna({
            'Budget in USD': constant_value,
            'Rating': constant_value
        })

        pd.testing.assert_frame_equal(df_result, expected_result)

    def test_drop_missing(self):
        df_with_nan = self.df.copy()

        df_result = self.handler.drop_missing(df_with_nan.copy())

        expected_result = df_with_nan.dropna()

        pd.testing.assert_frame_equal(df_result, expected_result)

if __name__ == '__main__':
    unittest.main()
