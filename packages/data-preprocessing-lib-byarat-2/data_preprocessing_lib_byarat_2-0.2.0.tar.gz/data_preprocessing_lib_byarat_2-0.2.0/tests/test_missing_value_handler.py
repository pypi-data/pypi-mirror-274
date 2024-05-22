import unittest
import pandas as pd
from sklearn.impute import KNNImputer
from data_preprocessing_lib_byarat import MissingValueHandler

class TestMissingValueHandler(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            'A': [1, 2, None, 4, None],
            'B': [None, 1, None, 3, 4],
            'C': ['a', 'b', 'a', None, 'b']
        })

    def test_impute_with_mean(self):
        df_result = MissingValueHandler.impute_with_mean(self.df.copy(), 'A')
        self.assertAlmostEqual(df_result['A'].mean(), 2.75)

    def test_impute_with_median(self):
        df_result = MissingValueHandler.impute_with_median(self.df.copy(), 'A')
        self.assertAlmostEqual(df_result['A'].median(), 2.0)

    def test_impute_with_constant(self):
        df_result = MissingValueHandler.impute_with_constant(self.df.copy(), 'A', 0)
        self.assertEqual(df_result['A'].iloc[2], 0)

    def test_drop_missing(self):
        df_result = MissingValueHandler.drop_missing(self.df.copy(), 'A')
        self.assertEqual(df_result.shape[0], 3)

    def test_impute_with_mode(self):
        df_result = MissingValueHandler.impute_with_mode(self.df.copy(), 'C')
        self.assertEqual(df_result['C'].iloc[3], 'a')

    def test_forward_fill(self):
        df_result = MissingValueHandler.forward_fill(self.df.copy(), 'A')
        self.assertEqual(df_result['A'].iloc[2], 2)

    def test_backward_fill(self):
        df_result = MissingValueHandler.backward_fill(self.df.copy(), 'A')
        self.assertEqual(df_result['A'].iloc[2], 4)

    def test_impute_knn(self):
        df_result = MissingValueHandler.impute_knn(self.df.copy(), ['A', 'B'])
        self.assertFalse(df_result[['A', 'B']].isnull().values.any())

    def test_mark_missing(self):
        df_result = MissingValueHandler.mark_missing(self.df.copy(), 'A')
        self.assertIn('A_missing', df_result.columns)
        self.assertTrue(df_result['A_missing'].iloc[2])
        self.assertFalse(df_result['A_missing'].iloc[0])

    def test_impute_group_mean(self):
        df_result = MissingValueHandler.impute_group_mean(self.df.copy(), 'C', 'A')
        self.assertFalse(df_result['A'].isnull().values.any())

    def test_impute_group_median(self):
        df_result = MissingValueHandler.impute_group_median(self.df.copy(), 'C', 'A')
        self.assertFalse(df_result['A'].isnull().values.any())

    def test_impute_group_mode(self):
        df_result = MissingValueHandler.impute_group_mode(self.df.copy(), 'C', 'A')
        self.assertFalse(df_result['A'].isnull().values.any())

if __name__ == '__main__':
    unittest.main()
