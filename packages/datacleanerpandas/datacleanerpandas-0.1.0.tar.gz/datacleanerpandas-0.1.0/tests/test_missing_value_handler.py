import unittest
import pandas as pd
import numpy as np
from dataPreprocessing.missing_value_handler import MissingValueHandler


class TestMissingValueHandler(unittest.TestCase):
    """
    TestMissingValueHandler is a test class for the MissingValueHandler class, ensuring the correct functionality of handling missing values.

    Methods:
        setUp():
            Initializes a sample DataFrame for testing.

        test_mean_imputation():
            Tests the mean imputation strategy.

        test_median_imputation():
            Tests the median imputation strategy.

        test_constant_imputation():
            Tests the constant imputation strategy.

        test_fill_with_mean():
            Tests filling missing values in a column with mean.

        test_fill_with_median():
            Tests filling missing values in a column with median.

        test_fill_with_mode():
            Tests filling missing values in a column with mode.

        test_drop_missing():
            Tests dropping rows with missing values in a column.

        test_invalid_strategy():
            Tests the handling of an invalid strategy.
    """

    def setUp(self):
        self.data = pd.DataFrame({
            'A': [1, 2, np.nan, 4, 5],
            'B': [np.nan, 2, 3, 4, 5]
        })

    def test_mean_imputation(self):
        handler = MissingValueHandler(strategy="mean")
        transformed = handler.fit_transform(self.data)
        expected = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [3.5, 2, 3, 4, 5]
        }, dtype=float)
        pd.testing.assert_frame_equal(transformed, expected)

    def test_median_imputation(self):
        handler = MissingValueHandler(strategy="median")
        transformed = handler.fit_transform(self.data)
        expected = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [3.5, 2, 3, 4, 5]
        }, dtype=float)
        pd.testing.assert_frame_equal(transformed, expected)

    def test_constant_imputation(self):
        handler = MissingValueHandler(strategy="constant", fill_value=0)
        transformed = handler.fit_transform(self.data)
        expected = pd.DataFrame({
            'A': [1, 2, 0, 4, 5],
            'B': [0, 2, 3, 4, 5]
        }, dtype=float)
        pd.testing.assert_frame_equal(transformed, expected)

    def test_fill_with_mean(self):
        df = MissingValueHandler.fill_with_mean(self.data.copy(), 'A')
        expected = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [np.nan, 2, 3, 4, 5]
        }, dtype=float)
        pd.testing.assert_frame_equal(df, expected)

    def test_fill_with_median(self):
        df = MissingValueHandler.fill_with_median(self.data.copy(), 'A')
        expected = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [np.nan, 2, 3, 4, 5]
        }, dtype=float)
        pd.testing.assert_frame_equal(df, expected)

    def test_fill_with_mode(self):
        df = MissingValueHandler.fill_with_mode(self.data.copy(), 'B')
        expected = pd.DataFrame({
            'A': [1, 2, np.nan, 4, 5],
            'B': [2, 2, 3, 4, 5]
        }, dtype=float)
        pd.testing.assert_frame_equal(df, expected)

    def test_drop_missing(self):
        df = MissingValueHandler.drop_missing(self.data.copy(), 'A')
        expected = pd.DataFrame({
            'A': [1, 2, 4, 5],
            'B': [np.nan, 2, 4, 5]
        }).astype({'A': 'float64', 'B': 'float64'}).reset_index(drop=True)
        pd.testing.assert_frame_equal(df.reset_index(drop=True), expected)

    def test_invalid_strategy(self):
        with self.assertRaises(ValueError):
            handler = MissingValueHandler(strategy="invalid")
            handler.fit_transform(self.data)


if __name__ == '__main__':
    unittest.main()
