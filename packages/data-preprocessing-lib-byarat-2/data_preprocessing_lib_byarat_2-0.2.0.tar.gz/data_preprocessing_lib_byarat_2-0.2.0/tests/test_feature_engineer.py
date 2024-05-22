import unittest
import pandas as pd
import numpy as np
from data_preprocessing_lib_byarat import FeatureEngineer

class TestFeatureEngineer(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            'budget_column': [100, 200, 300],
            'date_column': ['2020-01-01', '2021-01-01', '2022-01-01'],
            'value': [10, 20, 30],
            'category': ['A', 'B', 'A']
        })

    def test_normalize_budget_by_year(self):
        df_result = FeatureEngineer.normalize_budget_by_year(self.df.copy(), 'budget_column', 'date_column')
        self.assertIn('normalized_budget', df_result.columns)

    def test_extract_date_parts(self):
        df_result = FeatureEngineer.extract_date_parts(self.df.copy(), 'date_column')
        self.assertIn('year', df_result.columns)
        self.assertIn('month', df_result.columns)
        self.assertIn('day', df_result.columns)

    def test_create_feature(self):
        df_result = FeatureEngineer.create_feature(self.df.copy(), 'value_squared', lambda row: row['value'] ** 2)
        self.assertIn('value_squared', df_result.columns)
        self.assertEqual(df_result['value_squared'].iloc[0], 100)

    def test_normalize_budget(self):
        df_result = FeatureEngineer.normalize_budget(self.df.copy(), 'budget_column', 'date_column')
        self.assertIn('normalized_budget', df_result.columns)

    def test_day_of_year(self):
        df_result = FeatureEngineer.day_of_year(self.df.copy(), 'date_column')
        self.assertIn('day_of_year', df_result.columns)

    def test_conditional_feature(self):
        df_result = FeatureEngineer.conditional_feature(self.df.copy(), 'high_value', lambda df: df['value'] > 15, 1, 0)
        self.assertIn('high_value', df_result.columns)
        self.assertEqual(df_result['high_value'].iloc[0], 0)
        self.assertEqual(df_result['high_value'].iloc[1], 1)

    def test_create_dummies(self):
        df_result = FeatureEngineer.create_dummies(self.df.copy(), 'category')
        self.assertIn('category_A', df_result.columns)
        self.assertIn('category_B', df_result.columns)

    def test_log_transform(self):
        df_result = FeatureEngineer.log_transform(self.df.copy(), 'value')
        self.assertIn('value_log', df_result.columns)

    def test_interaction_terms(self):
        df_result = FeatureEngineer.interaction_terms(self.df.copy(), ['value', 'budget_column'])
        self.assertIn('value_x_budget_column', df_result.columns)

    def test_polynomial_features(self):
        df_result = FeatureEngineer.polynomial_features(self.df.copy(), 'value', degree=3)
        self.assertIn('value_pow_2', df_result.columns)
        self.assertIn('value_pow_3', df_result.columns)

    def test_moving_average(self):
        df_result = FeatureEngineer.moving_average(self.df.copy(), 'value', window=2)
        self.assertIn('value_moving_avg', df_result.columns)

    def test_label_encode(self):
        df_result = FeatureEngineer.label_encode(self.df.copy(), 'category')
        self.assertIn('category_encoded', df_result.columns)

    def test_diff_features(self):
        df_result = FeatureEngineer.diff_features(self.df.copy(), 'value', periods=1)
        self.assertIn('value_diff', df_result.columns)

    def test_lag_features(self):
        df_result = FeatureEngineer.lag_features(self.df.copy(), 'value', lags=2)
        self.assertIn('value_lag_1', df_result.columns)
        self.assertIn('value_lag_2', df_result.columns)

    def test_cumulative_sum(self):
        df_result = FeatureEngineer.cumulative_sum(self.df.copy(), 'value')
        self.assertIn('value_cumsum', df_result.columns)

    def test_binary_threshold(self):
        df_result = FeatureEngineer.binary_threshold(self.df.copy(), 'value', 15)
        self.assertIn('value_binary', df_result.columns)

    def test_sqrt_transform(self):
        df_result = FeatureEngineer.sqrt_transform(self.df.copy(), 'value')
        self.assertIn('value_sqrt', df_result.columns)

    def test_exp_transform(self):
        df_result = FeatureEngineer.exp_transform(self.df.copy(), 'value')
        self.assertIn('value_exp', df_result.columns)

    def test_inverse_transform(self):
        df_result = FeatureEngineer.inverse_transform(self.df.copy(), 'value')
        self.assertIn('value_inverse', df_result.columns)

    def test_sin_transform(self):
        df_result = FeatureEngineer.sin_transform(self.df.copy(), 'value')
        self.assertIn('value_sin', df_result.columns)

    def test_cos_transform(self):
        df_result = FeatureEngineer.cos_transform(self.df.copy(), 'value')
        self.assertIn('value_cos', df_result.columns)

    def test_standard_scale(self):
        df_result = FeatureEngineer.standard_scale(self.df.copy(), 'value')
        self.assertIn('value_standard_scaled', df_result.columns)

    def test_min_max_scale(self):
        df_result = FeatureEngineer.min_max_scale(self.df.copy(), 'value')
        self.assertIn('value_min_max_scaled', df_result.columns)

    def test_median(self):
        df_result = FeatureEngineer.median(self.df.copy(), 'value')
        self.assertIn('value_median', df_result.columns)

    def test_mode(self):
        df_result = FeatureEngineer.mode(self.df.copy(), 'value')
        self.assertIn('value_mode', df_result.columns)

if __name__ == '__main__':
    unittest.main()
