
import pandas as pd

class OutlierHandler:
    """
        OutlierHandler is a class designed to handle outliers in a given DataFrame using the IQR (Interquartile Range) method.

        Attributes:
            method (str): The method used to detect outliers. Default is "iqr".
            threshold (float): The threshold for determining outliers. Default is 1.5.
            lower_bound (pd.Series): The lower bound for outliers, calculated based on the IQR method.
            upper_bound (pd.Series): The upper bound for outliers, calculated based on the IQR method.

        Methods:
            fit(X):
                Calculates the lower and upper bounds for the provided DataFrame X based on the specified method.

            _preserve_dtypes(original, modified):
                Ensures that the data types of the modified DataFrame match those of the original DataFrame.

            transform(X):
                Clips the values in the DataFrame X to be within the calculated lower and upper bounds, and preserves the original data types.

            fit_transform(X):
                Combines the fit and transform methods to first calculate the bounds and then clip the values in one step.
    """
    def __init__(self, method="iqr", threshold=1.5):
        self.method = method
        self.threshold = threshold
        self.lower_bound = None
        self.upper_bound = None

    def fit(self, X):
        if self.method == "iqr":
            numeric_cols = X.select_dtypes(include=['number'])
            Q1 = numeric_cols.quantile(0.25)
            Q3 = numeric_cols.quantile(0.75)
            IQR = Q3 - Q1
            self.lower_bound = Q1 - self.threshold * IQR
            self.upper_bound = Q3 + self.threshold * IQR
        else:
            raise ValueError("Invalid method: choose 'iqr'")
        return self

    def transform(self, X):
        if self.lower_bound is not None and self.upper_bound is not None:
            X.loc[:, self.lower_bound.index] = X[self.lower_bound.index].clip(lower=self.lower_bound, upper=self.upper_bound, axis=1)
        return X

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
