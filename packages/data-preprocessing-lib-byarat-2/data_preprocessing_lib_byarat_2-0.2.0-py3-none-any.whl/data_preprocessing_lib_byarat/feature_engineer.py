import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler

class FeatureEngineer:
    @staticmethod
    def normalize_budget_by_year(df, budget_col, date_col):
        df[date_col] = pd.to_datetime(df[date_col])
        df['year'] = df[date_col].dt.year
        yearly_budget = df.groupby('year')[budget_col].transform('mean')
        df['normalized_budget'] = df[budget_col] / yearly_budget
        return df

    @staticmethod
    def extract_date_parts(df, date_col):
        df[date_col] = pd.to_datetime(df[date_col])
        df['year'] = df[date_col].dt.year
        df['month'] = df[date_col].dt.month
        df['day'] = df[date_col].dt.day
        return df

    @staticmethod
    def create_feature(df, new_column, func, *args):
        df[new_column] = df.apply(lambda row: func(row, *args), axis=1)
        return df

    @staticmethod
    def normalize_budget(df, column, year_column):
        df[year_column] = pd.to_numeric(df[year_column], errors='coerce')
        df['normalized_budget'] = df.apply(lambda row: row[column] / (2024 - row[year_column]), axis=1)
        return df

    @staticmethod
    def day_of_year(df, date_col):
        df[date_col] = pd.to_datetime(df[date_col])
        df['day_of_year'] = df[date_col].dt.dayofyear
        return df

    @staticmethod
    def conditional_feature(df, new_column, condition, value_if_true, value_if_false):
        df[new_column] = np.where(condition(df), value_if_true, value_if_false)
        return df

    @staticmethod
    def create_dummies(df, column):
        dummies = pd.get_dummies(df[column], prefix=column)
        df = pd.concat([df, dummies], axis=1)
        return df

    @staticmethod
    def log_transform(df, column):
        df[column + '_log'] = np.log1p(df[column])
        return df

    @staticmethod
    def interaction_terms(df, columns):
        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):
                df[columns[i] + '_x_' + columns[j]] = df[columns[i]] * df[columns[j]]
        return df

    @staticmethod
    def polynomial_features(df, column, degree=2):
        for power in range(2, degree + 1):
            df[column + f'_pow_{power}'] = df[column] ** power
        return df

    @staticmethod
    def moving_average(df, column, window):
        df[column + '_moving_avg'] = df[column].rolling(window=window).mean()
        return df

    @staticmethod
    def label_encode(df, column):
        le = LabelEncoder()
        df[column + '_encoded'] = le.fit_transform(df[column])
        return df

    @staticmethod
    def diff_features(df, column, periods=1):
        df[column + '_diff'] = df[column].diff(periods=periods)
        return df

    @staticmethod
    def lag_features(df, column, lags=1):
        for lag in range(1, lags + 1):
            df[column + f'_lag_{lag}'] = df[column].shift(lag)
        return df

    @staticmethod
    def cumulative_sum(df, column):
        df[column + '_cumsum'] = df[column].cumsum()
        return df

    @staticmethod
    def binary_threshold(df, column, threshold):
        df[column + '_binary'] = (df[column] > threshold).astype(int)
        return df

    @staticmethod
    def sqrt_transform(df, column):
        df[column + '_sqrt'] = np.sqrt(df[column])
        return df

    @staticmethod
    def exp_transform(df, column):
        df[column + '_exp'] = np.exp(df[column])
        return df

    @staticmethod
    def inverse_transform(df, column):
        df[column + '_inverse'] = 1 / df[column]
        return df

    @staticmethod
    def sin_transform(df, column):
        df[column + '_sin'] = np.sin(df[column])
        return df

    @staticmethod
    def cos_transform(df, column):
        df[column + '_cos'] = np.cos(df[column])
        return df

    @staticmethod
    def standard_scale(df, column):
        scaler = StandardScaler()
        df[column + '_standard_scaled'] = scaler.fit_transform(df[[column]])
        return df

    @staticmethod
    def min_max_scale(df, column):
        scaler = MinMaxScaler()
        df[column + '_min_max_scaled'] = scaler.fit_transform(df[[column]])
        return df

    @staticmethod
    def median(df, column):
        df[column + '_median'] = df[column].median()
        return df

    @staticmethod
    def mode(df, column):
        df[column + '_mode'] = df[column].mode()[0]
        return df

# Test kodu
if __name__ == "__main__":
    data = {
        'budget': [100000, 200000, 150000, 300000],
        'release_date': ['2020-01-01', '2021-01-01', '2022-01-01', '2023-01-01'],
        'genre': ['Action', 'Comedy', 'Action', 'Drama']
    }
    df = pd.DataFrame(data)

    feature_engineer = FeatureEngineer()

    # normalize_budget_by_year test
    df_normalized = feature_engineer.normalize_budget_by_year(df.copy(), 'budget', 'release_date')
    print("Normalize Budget by Year:")
    print(df_normalized)

    # extract_date_parts test
    df_date_parts = feature_engineer.extract_date_parts(df.copy(), 'release_date')
    print("Extract Date Parts:")
    print(df_date_parts)

    # create_feature test
    df_new_feature = feature_engineer.create_feature(df.copy(), 'budget_plus_1000', lambda row: row['budget'] + 1000)
    print("Create Feature:")
    print(df_new_feature)

    # extract_date_parts to create 'year' column before normalize_budget test
    df = feature_engineer.extract_date_parts(df.copy(), 'release_date')
    df_normalized_budget = feature_engineer.normalize_budget(df.copy(), 'budget', 'year')
    print("Normalize Budget:")
    print(df_normalized_budget)

    # day_of_year test
    df_day_of_year = feature_engineer.day_of_year(df.copy(), 'release_date')
    print("Day of Year:")
    print(df_day_of_year)

    # conditional_feature test
    df_conditional = feature_engineer.conditional_feature(df.copy(), 'high_budget', lambda df: df['budget'] > 150000, 'High', 'Low')
    print("Conditional Feature:")
    print(df_conditional)

    # create_dummies test
    df_dummies = feature_engineer.create_dummies(df.copy(), 'genre')
    print("Create Dummies:")
    print(df_dummies)

    # log_transform test
    df_log = feature_engineer.log_transform(df.copy(), 'budget')
    print("Log Transform:")
    print(df_log)

    # interaction_terms test
    df_interaction = feature_engineer.interaction_terms(df.copy(), ['budget', 'year'])
    print("Interaction Terms:")
    print(df_interaction)

    # polynomial_features test
    df_poly = feature_engineer.polynomial_features(df.copy(), 'budget', degree=3)
    print("Polynomial Features:")
    print(df_poly)

    # moving_average test
    df_moving_avg = feature_engineer.moving_average(df.copy(), 'budget', window=2)
    print("Moving Average:")
    print(df_moving_avg)

    # label_encode test
    df_label_encoded = feature_engineer.label_encode(df.copy(), 'genre')
    print("Label Encoding:")
    print(df_label_encoded)

    # diff_features test
    df_diff = feature_engineer.diff_features(df.copy(), 'budget', periods=1)
    print("Diff Features:")
    print(df_diff)

    # lag_features test
    df_lag = feature_engineer.lag_features(df.copy(), 'budget', lags=2)
    print("Lag Features:")
    print(df_lag)

    # cumulative_sum test
    df_cumsum = feature_engineer.cumulative_sum(df.copy(), 'budget')
    print("Cumulative Sum:")
    print(df_cumsum)

    # binary_threshold test
    df_binary = feature_engineer.binary_threshold(df.copy(), 'budget', threshold=150000)
    print("Binary Threshold:")
    print(df_binary)

    # sqrt_transform test
    df_sqrt = feature_engineer.sqrt_transform(df.copy(), 'budget')
    print("Sqrt Transform:")
    print(df_sqrt)

    # exp_transform test
    df_exp = feature_engineer.exp_transform(df.copy(), 'budget')
    print("Exp Transform:")
    print(df_exp)

    # inverse_transform test
    df_inverse = feature_engineer.inverse_transform(df.copy(), 'budget')
    print("Inverse Transform:")
    print(df_inverse)

    # sin_transform test
    df_sin = feature_engineer.sin_transform(df.copy(), 'budget')
    print("Sin Transform:")
    print(df_sin)

    # cos_transform test
    df_cos = feature_engineer.cos_transform(df.copy(), 'budget')
    print("Cos Transform:")
    print(df_cos)

    # standard_scale test
    df_standard_scaled = feature_engineer.standard_scale(df.copy(), 'budget')
    print("Standard Scale:")
    print(df_standard_scaled)

    # min_max_scale test
    df_min_max_scaled = feature_engineer.min_max_scale(df.copy(), 'budget')
    print("Min-Max Scale:")
    print(df_min_max_scaled)

    # median test
    df_median = feature_engineer.median(df.copy(), 'budget')
    print("Median:")
    print(df_median)

    # mode test
    df_mode = feature_engineer.mode(df.copy(), 'budget')
    print("Mode:")
    print(df_mode)
