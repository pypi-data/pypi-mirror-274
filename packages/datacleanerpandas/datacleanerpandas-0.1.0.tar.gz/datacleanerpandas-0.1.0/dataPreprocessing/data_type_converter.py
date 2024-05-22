import pandas as pd


class DataTypeConverter:
    """
    DataTypeConverter is a class for performing data type conversions on DataFrame columns.

    Methods:
        to_numeric(df, column, errors='coerce'):
            Converts a column in the DataFrame to numeric values, coercing errors by default.

        to_categorical(df, column):
            Converts a column in the DataFrame to categorical values.

        to_datetime(df, column, date_format=None):
            Converts a column in the DataFrame to datetime objects based on the provided format.
    """

    @staticmethod
    def to_numeric(df, column, errors='coerce'):
        df[column] = pd.to_numeric(df[column], errors=errors)
        return df

    @staticmethod
    def to_categorical(df, column):
        df[column] = df[column].astype('category')
        return df

    @staticmethod
    def to_datetime(df, column, date_format=None):
        df[column] = pd.to_datetime(df[column], format=date_format, errors='coerce')
        return df
