import unittest
import pandas as pd
from data_preprocessing_lib_byarat import DataTypeConverter

class TestDataTypeConverter(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            'numeric_column': ['1', '2', 'invalid', '4'],
            'category_column': [1, 2, 3, 4],
            'datetime_column': ['2020-01-01', '2021-01-01', 'invalid date', '2022-01-01']
        })

    def test_to_numeric(self):
        df_result = DataTypeConverter.to_numeric(self.df.copy(), 'numeric_column')
        self.assertTrue(pd.api.types.is_numeric_dtype(df_result['numeric_column']))
        self.assertTrue(df_result['numeric_column'].isnull().iloc[2])

    def test_to_categorical(self):
        df_result = DataTypeConverter.to_categorical(self.df.copy(), 'category_column')
        self.assertTrue(pd.api.types.is_categorical_dtype(df_result['category_column']))

    def test_to_datetime(self):
        df_result = DataTypeConverter.to_datetime(self.df.copy(), 'datetime_column')
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df_result['datetime_column']))
        self.assertTrue(df_result['datetime_column'].isnull().iloc[2])

if __name__ == '__main__':
    unittest.main()
