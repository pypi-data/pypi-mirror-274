import unittest
import nltk
import pandas as pd
from data_preprocessing_lib.text_cleaner import TextCleaner

class TestTextCleaner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nltk.download('stopwords')

    def setUp(self):
        file_path = './synthetic_sample_data.csv'
        self.df = pd.read_csv(file_path)
        
        if 'Summary' not in self.df.columns:
            raise KeyError("Column 'Summary' not found in the CSV file.")
        
        self.df = self.df[['Summary']]
        
        self.cleaner = TextCleaner()

    def test_to_lowercase(self):
        df_result = self.cleaner.to_lowercase(self.df.copy(), 'Summary')
        expected_result = self.df.copy()
        expected_result['Summary'] = expected_result['Summary'].str.lower()
        pd.testing.assert_frame_equal(df_result, expected_result)

    def test_remove_punctuation(self):
        df_result = self.cleaner.remove_punctuation(self.df.copy(), 'Summary')
        expected_result = self.df.copy()
        expected_result['Summary'] = expected_result['Summary'].str.replace(r'[^\w\s]', '', regex=True)
        
        pd.testing.assert_frame_equal(df_result, expected_result)

if __name__ == '__main__':
    unittest.main()
