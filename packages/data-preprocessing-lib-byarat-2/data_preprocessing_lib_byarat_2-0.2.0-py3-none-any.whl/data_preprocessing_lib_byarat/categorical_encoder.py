import pandas as pd
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder


class CategoricalEncoder:
    @staticmethod
    def one_hot_encode(df, column):
        return pd.get_dummies(df, columns=[column])

    @staticmethod
    def label_encode(df, column):
        df[column] = df[column].astype('category').cat.codes
        return df
    @staticmethod
    def ordinal_encode(df, column, categories='auto'):
        encoder = OrdinalEncoder(categories=[categories] if categories != 'auto' else 'auto')
        df[column] = encoder.fit_transform(df[[column]])
        return df

    @staticmethod
    def frequency_encode(df, column):
        freq = df[column].value_counts() / len(df)
        df[column + '_freq_encode'] = df[column].map(freq)
        return df

    @staticmethod
    def target_encode(df, column, target):
        mean_target = df.groupby(column)[target].mean()
        df[column + '_target_encode'] = df[column].map(mean_target)
        return df

    @staticmethod
    def binary_encode(df, column):
        encoder = LabelEncoder()
        df[column] = encoder.fit_transform(df[column])
        max_label = df[column].max() + 1
        num_bits = max_label.bit_length()
        for i in range(num_bits):
            df[f'{column}_bin_{i}'] = df[column].apply(lambda x: (x >> i) & 1)
        df.drop(columns=[column], inplace=True)
        return df
    

if __name__ == "__main__":
    data = {
        'category': ['A', 'B', 'A', 'C', 'B', 'A'],
        'target': [1, 2, 1, 3, 2, 1]
    }
    df = pd.DataFrame(data)

    encoder = CategoricalEncoder()
    
    df_one_hot = encoder.one_hot_encode(df.copy(), 'category')
    print("One-Hot Encoding:")
    print(df_one_hot)
    
    df_label = encoder.label_encode(df.copy(), 'category')
    print("Label Encoding:")
    print(df_label)
    
    df_ordinal = encoder.ordinal_encode(df.copy(), 'category', categories=['A', 'B', 'C'])
    print("Ordinal Encoding:")
    print(df_ordinal)
    
    df_freq = encoder.frequency_encode(df.copy(), 'category')
    print("Frequency Encoding:")
    print(df_freq)
    
    df_target = encoder.target_encode(df.copy(), 'category', 'target')
    print("Target Encoding:")
    print(df_target)
    
    df_binary = encoder.binary_encode(df.copy(), 'category')
    print("Binary Encoding:")
    print(df_binary)