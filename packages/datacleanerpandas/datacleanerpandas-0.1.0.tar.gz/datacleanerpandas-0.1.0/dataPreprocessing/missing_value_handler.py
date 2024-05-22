import pandas as pd
import numpy as np


class MissingValueHandler:
    """
    MissingValueHandler is a class for handling missing values in DataFrame columns using various strategies.

    Methods:
        __init__(self, strategy="mean", fill_value=None):
            Initializes the MissingValueHandler with the specified strategy.

        fit(self, X):
            Fits the handler to the DataFrame.

        transform(self, X):
            Transforms the DataFrame by applying the missing value handling strategy.

        fit_transform(self, X):
            Fits the handler and transforms the DataFrame.

        fill_with_mean(df, column):
            Fills missing values in the specified column with the mean of the column.

        fill_with_median(df, column):
            Fills missing values in the specified column with the median of the column.

        fill_with_mode(df, column):
            Fills missing values in the specified column with the mode of the column.

        drop_missing(df, column):
            Drops rows with missing values in the specified column.
    """

    def __init__(self, strategy="mean", fill_value=None):
        self.strategy = strategy
        self.fill_value = fill_value

    def fit(self, X):
        if self.strategy == "mean":
            self.fill_value = X.mean()
        elif self.strategy == "median":
            self.fill_value = X.median()
        elif self.strategy == "constant":
            if self.fill_value is None:
                raise ValueError("fill_value must be provided for constant strategy")
        else:
            raise ValueError("Invalid strategy: choose from 'mean', 'median', 'constant'")
        return self

    def transform(self, X):
        return X.fillna(self.fill_value)

    def fit_transform(self, X):
        return self.fit(X).transform(X)

    @staticmethod
    def fill_with_mean(df, column):
        df[column] = df[column].fillna(df[column].mean()).astype(df[column].dtype)
        return df

    @staticmethod
    def fill_with_median(df, column):
        df[column] = df[column].fillna(df[column].median()).astype(df[column].dtype)
        return df

    @staticmethod
    def fill_with_mode(df, column):
        df[column] = df[column].fillna(df[column].mode()[0]).astype(df[column].dtype)
        return df

    @staticmethod
    def drop_missing(df, column):
        df = df.dropna(subset=[column])
        return df
