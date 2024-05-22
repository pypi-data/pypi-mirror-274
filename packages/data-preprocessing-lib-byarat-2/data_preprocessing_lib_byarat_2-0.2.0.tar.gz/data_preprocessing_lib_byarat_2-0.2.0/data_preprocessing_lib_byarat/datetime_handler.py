import pandas as pd

class DateTimeHandler:
    @staticmethod
    def extract_date_parts(df, date_col):
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df['year'] = df[date_col].dt.year
        df['month'] = df[date_col].dt.month
        df['day'] = df[date_col].dt.day
        df['hour'] = df[date_col].dt.hour
        df['minute'] = df[date_col].dt.minute
        df['second'] = df[date_col].dt.second
        df['day_of_week'] = df[date_col].dt.dayofweek
        df['day_of_year'] = df[date_col].dt.dayofyear
        df['week_of_year'] = df[date_col].dt.isocalendar().week
        df['quarter'] = df[date_col].dt.quarter
        return df

    @staticmethod
    def extract_year(df, column):
        df[column] = pd.to_datetime(df[column], errors='coerce')
        df['year'] = df[column].dt.year
        return df

    @staticmethod
    def extract_month(df, column):
        df[column] = pd.to_datetime(df[column], errors='coerce')
        df['month'] = df[column].dt.month
        return df

    @staticmethod
    def extract_day(df, column):
        df[column] = pd.to_datetime(df[column], errors='coerce')
        df['day'] = df[column].dt.day
        return df

    @staticmethod
    def extract_hour(df, column):
        df[column] = pd.to_datetime(df[column], errors='coerce')
        df['hour'] = df[column].dt.hour
        return df

    @staticmethod
    def extract_minute(df, column):
        df[column] = pd.to_datetime(df[column], errors='coerce')
        df['minute'] = df[column].dt.minute
        return df

    @staticmethod
    def extract_second(df, column):
        df[column] = pd.to_datetime(df[column], errors='coerce')
        df['second'] = df[column].dt.second
        return df

    @staticmethod
    def extract_day_of_week(df, column):
        df[column] = pd.to_datetime(df[column], errors='coerce')
        df['day_of_week'] = df[column].dt.dayofweek
        return df

    @staticmethod
    def extract_day_of_year(df, column):
        df[column] = pd.to_datetime(df[column], errors='coerce')
        df['day_of_year'] = df[column].dt.dayofyear
        return df

    @staticmethod
    def extract_week_of_year(df, column):
        df[column] = pd.to_datetime(df[column], errors='coerce')
        df['week_of_year'] = df[column].dt.isocalendar().week
        return df

    @staticmethod
    def extract_quarter(df, column):
        df[column] = pd.to_datetime(df[column], errors='coerce')
        df['quarter'] = df[column].dt.quarter
        return df

    @staticmethod
    def extract_elapsed_time(df, start_column, end_column, new_column):
        df[start_column] = pd.to_datetime(df[start_column], errors='coerce')
        df[end_column] = pd.to_datetime(df[end_column], errors='coerce')
        df[new_column] = (df[end_column] - df[start_column]).dt.total_seconds()
        return df

# Test kodu
if __name__ == "__main__":
    data = {
        'date': ['2020-01-01 12:34:56', '2021-06-15 08:15:27', 'invalid_date', '2023-12-31 23:59:59', ''],
        'start_date': ['2020-01-01 08:00:00', '2021-06-15 07:00:00', '2022-09-10 16:00:00', '2023-12-31 20:00:00', ''],
        'end_date': ['2020-01-01 10:00:00', '2021-06-15 09:00:00', '2022-09-10 18:00:00', '2023-12-31 22:00:00', '']
    }
    df = pd.DataFrame(data)

    datetime_handler = DateTimeHandler()

    # extract_date_parts test
    df_parts = datetime_handler.extract_date_parts(df.copy(), 'date')
    print("Extract Date Parts:")
    print(df_parts.to_string(index=False))

    # extract_year test
    df_year = datetime_handler.extract_year(df.copy(), 'date')
    print("Extract Year:")
    print(df_year.to_string(index=False))

    # extract_month test
    df_month = datetime_handler.extract_month(df.copy(), 'date')
    print("Extract Month:")
    print(df_month.to_string(index=False))

    # extract_day test
    df_day = datetime_handler.extract_day(df.copy(), 'date')
    print("Extract Day:")
    print(df_day.to_string(index=False))

    # extract_hour test
    df_hour = datetime_handler.extract_hour(df.copy(), 'date')
    print("Extract Hour:")
    print(df_hour.to_string(index=False))

    # extract_minute test
    df_minute = datetime_handler.extract_minute(df.copy(), 'date')
    print("Extract Minute:")
    print(df_minute.to_string(index=False))

    # extract_second test
    df_second = datetime_handler.extract_second(df.copy(), 'date')
    print("Extract Second:")
    print(df_second.to_string(index=False))

    # extract_day_of_week test
    df_day_of_week = datetime_handler.extract_day_of_week(df.copy(), 'date')
    print("Extract Day of Week:")
    print(df_day_of_week.to_string(index=False))

    # extract_day_of_year test
    df_day_of_year = datetime_handler.extract_day_of_year(df.copy(), 'date')
    print("Extract Day of Year:")
    print(df_day_of_year.to_string(index=False))

    # extract_week_of_year test
    df_week_of_year = datetime_handler.extract_week_of_year(df.copy(), 'date')
    print("Extract Week of Year:")
    print(df_week_of_year.to_string(index=False))

    # extract_quarter test
    df_quarter = datetime_handler.extract_quarter(df.copy(), 'date')
    print("Extract Quarter:")
    print(df_quarter.to_string(index=False))

    # extract_elapsed_time test
    df_elapsed_time = datetime_handler.extract_elapsed_time(df.copy(), 'start_date', 'end_date', 'elapsed_seconds')
    print("Extract Elapsed Time:")
    print(df_elapsed_time.to_string(index=False))
