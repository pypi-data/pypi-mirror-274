import pandas as pd

class DataTypeConverter:
    @staticmethod
    def to_numeric(df, column):
        df[column] = pd.to_numeric(df[column], errors='coerce')
        return df

    @staticmethod
    def to_categorical(df, column):
        df[column] = df[column].astype('category')
        return df
    
    @staticmethod
    def to_datetime(df, column):
        df[column] = pd.to_datetime(df[column], errors='coerce')
        return df
    
if __name__ == "__main__":
    data = {
        'numeric_str': ['1', '2', 'three', '4', '5'],
        'categorical_str': ['a', 'b', 'a', 'c', 'b'],
        'datetime_str': ['2020-01-01', '2021-06-15', 'invalid_date', '2023-12-31', '']
    }
    df = pd.DataFrame(data)

    converter = DataTypeConverter()

    # to_numeric test
    df_numeric = converter.to_numeric(df.copy(), 'numeric_str')
    print("Numeric Conversion:")
    print(df_numeric)

    # to_categorical test
    df_categorical = converter.to_categorical(df.copy(), 'categorical_str')
    print("Categorical Conversion:")
    print(df_categorical)

    # to_datetime test
    df_datetime = converter.to_datetime(df.copy(), 'datetime_str')
    print("Datetime Conversion:")
    print(df_datetime)