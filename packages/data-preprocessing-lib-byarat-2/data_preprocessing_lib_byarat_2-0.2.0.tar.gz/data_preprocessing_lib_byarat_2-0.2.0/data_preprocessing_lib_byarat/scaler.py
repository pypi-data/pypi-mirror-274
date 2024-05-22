import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, MaxAbsScaler, PowerTransformer, QuantileTransformer

class Scaler:
    @staticmethod
    def min_max_scale(df, column):
        scaler = MinMaxScaler()
        df[column] = scaler.fit_transform(df[[column]])
        return df

    @staticmethod
    def standard_scale(df, column):
        scaler = StandardScaler()
        df[column] = scaler.fit_transform(df[[column]])
        return df

    @staticmethod
    def robust_scale(df, column):
        scaler = RobustScaler()
        df[column] = scaler.fit_transform(df[[column]])
        return df

    @staticmethod
    def max_abs_scale(df, column):
        scaler = MaxAbsScaler()
        df[column] = scaler.fit_transform(df[[column]])
        return df

    @staticmethod
    def scale_to_range(df, column, feature_range=(0, 1)):
        scaler = MinMaxScaler(feature_range=feature_range)
        df[column] = scaler.fit_transform(df[[column]])
        return df

    @staticmethod
    def log_scale(df, column):
        df[column] = np.log1p(df[column])
        return df

    @staticmethod
    def z_score(df, column):
        df[column] = (df[column] - df[column].mean()) / df[column].std()
        return df

    @staticmethod
    def box_cox_scale(df, column):
        scaler = PowerTransformer(method='box-cox')
        df[column] = scaler.fit_transform(df[[column]])
        return df

    @staticmethod
    def yeo_johnson_scale(df, column):
        scaler = PowerTransformer(method='yeo-johnson')
        df[column] = scaler.fit_transform(df[[column]])
        return df

    @staticmethod
    def quantile_transform(df, column, n_quantiles=100, output_distribution='uniform'):
        scaler = QuantileTransformer(n_quantiles=n_quantiles, output_distribution=output_distribution)
        df[column] = scaler.fit_transform(df[[column]])
        return df

    @staticmethod
    def inverse_log_scale(df, column):
        df[column] = np.expm1(df[column])
        return df

    @staticmethod
    def square_root_scale(df, column):
        df[column] = np.sqrt(df[column])
        return df

    @staticmethod
    def reciprocal_scale(df, column):
        df[column] = 1 / df[column]
        return df

# Test kodu
if __name__ == "__main__":
    data = {
        'value': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    df = pd.DataFrame(data)

    scaler = Scaler()

    # min_max_scale test
    df_min_max = scaler.min_max_scale(df.copy(), 'value')
    print("Min-Max Scale:")
    print(df_min_max)

    # standard_scale test
    df_standard = scaler.standard_scale(df.copy(), 'value')
    print("Standard Scale:")
    print(df_standard)

    # robust_scale test
    df_robust = scaler.robust_scale(df.copy(), 'value')
    print("Robust Scale:")
    print(df_robust)

    # max_abs_scale test
    df_max_abs = scaler.max_abs_scale(df.copy(), 'value')
    print("Max-Abs Scale:")
    print(df_max_abs)

    # scale_to_range test
    df_scale_range = scaler.scale_to_range(df.copy(), 'value', feature_range=(1, 2))
    print("Scale to Range (1, 2):")
    print(df_scale_range)

    # log_scale test
    df_log = scaler.log_scale(df.copy(), 'value')
    print("Log Scale:")
    print(df_log)

    # z_score test
    df_z_score = scaler.z_score(df.copy(), 'value')
    print("Z-Score:")
    print(df_z_score)

    # box_cox_scale test
    df_box_cox = scaler.box_cox_scale(df.copy(), 'value')
    print("Box-Cox Scale:")
    print(df_box_cox)

    # yeo_johnson_scale test
    df_yeo_johnson = scaler.yeo_johnson_scale(df.copy(), 'value')
    print("Yeo-Johnson Scale:")
    print(df_yeo_johnson)

    # quantile_transform test
    df_quantile = scaler.quantile_transform(df.copy(), 'value', n_quantiles=5, output_distribution='normal')
    print("Quantile Transform (Normal):")
    print(df_quantile)

    # inverse_log_scale test
    df_inverse_log = scaler.log_scale(df.copy(), 'value')  # Apply log_scale first to get log values
    df_inverse_log = scaler.inverse_log_scale(df_inverse_log.copy(), 'value')
    print("Inverse Log Scale:")
    print(df_inverse_log)

    # square_root_scale test
    df_sqrt = scaler.square_root_scale(df.copy(), 'value')
    print("Square Root Scale:")
    print(df_sqrt)

    # reciprocal_scale test
    df_reciprocal = scaler.reciprocal_scale(df.copy(), 'value')
    print("Reciprocal Scale:")
    print(df_reciprocal)
