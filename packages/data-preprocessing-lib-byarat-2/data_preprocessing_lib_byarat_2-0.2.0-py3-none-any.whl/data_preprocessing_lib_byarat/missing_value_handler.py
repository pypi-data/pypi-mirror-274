import pandas as pd
from sklearn.impute import KNNImputer

class MissingValueHandler:
    @staticmethod
    def impute_with_mean(df, column):
        mean_value = df[column].mean()
        df[column].fillna(mean_value, inplace=True)
        return df

    @staticmethod
    def impute_with_median(df, column):
        median_value = df[column].median()
        df[column].fillna(median_value, inplace=True)
        return df

    @staticmethod
    def impute_with_constant(df, column, constant):
        df[column].fillna(constant, inplace=True)
        return df

    @staticmethod
    def drop_missing(df, column):
        df.dropna(subset=[column], inplace=True)
        return df

    @staticmethod
    def impute_with_mode(df, column):
        mode_value = df[column].mode()[0]
        df[column].fillna(mode_value, inplace=True)
        return df

    @staticmethod
    def forward_fill(df, column):
        df[column].fillna(method='ffill', inplace=True)
        return df

    @staticmethod
    def backward_fill(df, column):
        df[column].fillna(method='bfill', inplace=True)
        return df

    @staticmethod
    def impute_knn(df, columns, n_neighbors=5):
        imputer = KNNImputer(n_neighbors=n_neighbors)
        df[columns] = imputer.fit_transform(df[columns])
        return df

    @staticmethod
    def mark_missing(df, column):
        df[column + '_missing'] = df[column].isnull()
        return df

    @staticmethod
    def impute_group_mean(df, group_col, column):
        df[column] = df.groupby(group_col)[column].transform(lambda x: x.fillna(x.mean()))
        return df

    @staticmethod
    def impute_group_median(df, group_col, column):
        df[column] = df.groupby(group_col)[column].transform(lambda x: x.fillna(x.median()))
        return df

    @staticmethod
    def impute_group_mode(df, group_col, column):
        df[column] = df.groupby(group_col)[column].transform(lambda x: x.fillna(x.mode()[0]))
        return df

# Test kodu
if __name__ == "__main__":
    data = {
        'group': ['A', 'A', 'B', 'B', 'C', 'C'],
        'value': [1, None, 3, 4, None, 6],
        'value2': [None, 2, 3, None, 5, 6]
    }
    df = pd.DataFrame(data)

    handler = MissingValueHandler()

    # impute_with_mean test
    df_mean_imputed = handler.impute_with_mean(df.copy(), 'value')
    print("Impute with Mean:")
    print(df_mean_imputed)

    # impute_with_median test
    df_median_imputed = handler.impute_with_median(df.copy(), 'value')
    print("Impute with Median:")
    print(df_median_imputed)

    # impute_with_constant test
    df_constant_imputed = handler.impute_with_constant(df.copy(), 'value', 99)
    print("Impute with Constant:")
    print(df_constant_imputed)

    # drop_missing test
    df_dropped = handler.drop_missing(df.copy(), 'value')
    print("Drop Missing:")
    print(df_dropped)

    # impute_with_mode test
    df_mode_imputed = handler.impute_with_mode(df.copy(), 'value')
    print("Impute with Mode:")
    print(df_mode_imputed)

    # forward_fill test
    df_forward_filled = handler.forward_fill(df.copy(), 'value')
    print("Forward Fill:")
    print(df_forward_filled)

    # backward_fill test
    df_backward_filled = handler.backward_fill(df.copy(), 'value')
    print("Backward Fill:")
    print(df_backward_filled)

    # impute_knn test
    df_knn_imputed = handler.impute_knn(df.copy(), ['value', 'value2'], n_neighbors=2)
    print("Impute with KNN:")
    print(df_knn_imputed)

    # mark_missing test
    df_marked_missing = handler.mark_missing(df.copy(), 'value')
    print("Mark Missing:")
    print(df_marked_missing)

    # impute_group_mean test
    df_group_mean_imputed = handler.impute_group_mean(df.copy(), 'group', 'value')
    print("Impute Group Mean:")
    print(df_group_mean_imputed)

    # impute_group_median test
    df_group_median_imputed = handler.impute_group_median(df.copy(), 'group', 'value')
    print("Impute Group Median:")
    print(df_group_median_imputed)

    # impute_group_mode test
    df_group_mode_imputed = handler.impute_group_mode(df.copy(), 'group', 'value')
    print("Impute Group Mode:")
    print(df_group_mode_imputed)
