import unittest
import pandas as pd
from data_preprocessing_lib_byarat import DateTimeHandler

class TestDateTimeHandler(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            'datetime_column': [
                '2020-01-01 00:00:00',
                '2021-06-15 12:30:45',
                '2022-12-31 23:59:59'
            ]
        })

    def test_extract_date_parts(self):
        df_result = DateTimeHandler.extract_date_parts(self.df.copy(), 'datetime_column')
        self.assertIn('year', df_result.columns)
        self.assertIn('month', df_result.columns)
        self.assertIn('day', df_result.columns)
        self.assertIn('hour', df_result.columns)
        self.assertIn('minute', df_result.columns)
        self.assertIn('second', df_result.columns)
        self.assertIn('day_of_week', df_result.columns)
        self.assertIn('day_of_year', df_result.columns)
        self.assertIn('week_of_year', df_result.columns)
        self.assertIn('quarter', df_result.columns)

    def test_extract_year(self):
        df_result = DateTimeHandler.extract_year(self.df.copy(), 'datetime_column')
        self.assertIn('year', df_result.columns)

    def test_extract_month(self):
        df_result = DateTimeHandler.extract_month(self.df.copy(), 'datetime_column')
        self.assertIn('month', df_result.columns)

    def test_extract_day(self):
        df_result = DateTimeHandler.extract_day(self.df.copy(), 'datetime_column')
        self.assertIn('day', df_result.columns)

    def test_extract_hour(self):
        df_result = DateTimeHandler.extract_hour(self.df.copy(), 'datetime_column')
        self.assertIn('hour', df_result.columns)

    def test_extract_minute(self):
        df_result = DateTimeHandler.extract_minute(self.df.copy(), 'datetime_column')
        self.assertIn('minute', df_result.columns)

    def test_extract_second(self):
        df_result = DateTimeHandler.extract_second(self.df.copy(), 'datetime_column')
        self.assertIn('second', df_result.columns)

    def test_extract_day_of_week(self):
        df_result = DateTimeHandler.extract_day_of_week(self.df.copy(), 'datetime_column')
        self.assertIn('day_of_week', df_result.columns)

    def test_extract_day_of_year(self):
        df_result = DateTimeHandler.extract_day_of_year(self.df.copy(), 'datetime_column')
        self.assertIn('day_of_year', df_result.columns)

    def test_extract_week_of_year(self):
        df_result = DateTimeHandler.extract_week_of_year(self.df.copy(), 'datetime_column')
        self.assertIn('week_of_year', df_result.columns)

    def test_extract_quarter(self):
        df_result = DateTimeHandler.extract_quarter(self.df.copy(), 'datetime_column')
        self.assertIn('quarter', df_result.columns)

    def test_extract_elapsed_time(self):
        self.df['end_datetime_column'] = [
            '2020-01-02 00:00:00',
            '2021-06-16 12:30:45',
            '2023-01-01 23:59:59'
        ]
        df_result = DateTimeHandler.extract_elapsed_time(
            self.df.copy(),
            'datetime_column',
            'end_datetime_column',
            'elapsed_time'
        )
        self.assertIn('elapsed_time', df_result.columns)
        self.assertAlmostEqual(df_result['elapsed_time'].iloc[0], 86400.0)
        self.assertAlmostEqual(df_result['elapsed_time'].iloc[1], 86400.0)
        self.assertAlmostEqual(df_result['elapsed_time'].iloc[2], 31536000.0)

if __name__ == '__main__':
    unittest.main()
