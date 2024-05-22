import unittest
import pandas as pd
from dataPreprocessing.data_type_converter import DataTypeConverter


class TestDataTypeConverter(unittest.TestCase):
    """
    TestDataTypeConverter is a test class for the DataTypeConverter class, ensuring the correct functionality of data type conversions.

    Methods:
        setUp():
            Initializes a sample DataFrame for testing.

        test_to_numeric():
            Tests the conversion of a column to numeric values.

        test_to_categorical():
            Tests the conversion of a column to categorical values.

        test_to_datetime():
            Tests the conversion of a column to datetime objects.
    """

    def setUp(self):
        self.data = pd.DataFrame({
            'numeric_str': ['1', '2', '3', 'invalid'],
            'categorical_str': ['A', 'B', 'A', 'C'],
            'date_str': ['2023-05-19', '2024-05-19', 'invalid', '2025-05-19']
        })

    def test_to_numeric(self):
        df = DataTypeConverter.to_numeric(self.data.copy(), 'numeric_str')
        self.assertTrue(pd.api.types.is_numeric_dtype(df['numeric_str']))
        self.assertTrue(df['numeric_str'].isna().iloc[3])

    def test_to_categorical(self):
        df = DataTypeConverter.to_categorical(self.data.copy(), 'categorical_str')
        self.assertTrue(isinstance(df['categorical_str'].dtype, pd.CategoricalDtype))

    def test_to_datetime(self):
        df = DataTypeConverter.to_datetime(self.data.copy(), 'date_str', date_format='%Y-%m-%d')
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df['date_str']))
        self.assertTrue(df['date_str'].isna().iloc[2])


if __name__ == '__main__':
    unittest.main()
