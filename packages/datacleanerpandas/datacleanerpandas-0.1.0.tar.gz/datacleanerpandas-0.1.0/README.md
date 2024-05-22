 Data Preprocessing Library

## Overview

This repository contains a comprehensive data preprocessing library for handling various data transformation tasks, including categorical encoding, data type conversion, date-time handling, feature engineering, missing value handling, outlier handling, scaling, and text cleaning. The library is designed to be modular, allowing for easy integration into data pipelines.

## Modules

### 1. CategoricalEncoder

A class for performing label encoding and one-hot encoding on DataFrame columns.

- **Methods**:
  - `label_encode(df, column)`: Performs label encoding on the specified column.
  - `one_hot_encode(df, column)`: Performs one-hot encoding on the specified column.

### 2. DataTypeConverter

A class for performing data type conversions on DataFrame columns.

- **Methods**:
  - `to_numeric(df, column, errors='coerce')`: Converts a column to numeric values.
  - `to_categorical(df, column)`: Converts a column to categorical values.
  - `to_datetime(df, column, date_format=None)`: Converts a column to datetime objects.

### 3. DateTimeHandler

A class for performing date and time manipulations on DataFrame columns.

- **Methods**:
  - `convert_to_datetime(df, column, format)`: Converts a column to datetime objects.
  - `extract_date_component(df, column, component)`: Extracts a specific date component from a datetime column.
  - `calculate_date_difference(df, column1, column2, unit)`: Calculates the difference between two datetime columns.
  - `add_to_date(df, column, amount, unit)`: Adds a specified amount of time to a datetime column.

### 4. FeatureEngineer

A class for creating new features from existing DataFrame columns.

- **Methods**:
  - `add_difference(df, col1, col2, new_col_name)`: Adds a new column which is the difference between `col1` and `col2`.
  - `add_product(df, col1, col2, new_col_name)`: Adds a new column which is the product of `col1` and `col2`.
  - `add_sum(df, col1, col2, new_col_name)`: Adds a new column which is the sum of `col1` and `col2`.
  - `add_square(df, col, new_col_name)`: Adds a new column which is the square of the values in `col`.

### 5. MissingValueHandler

A class for handling missing values in DataFrame columns using various strategies.

- **Methods**:
  - `__init__(self, strategy="mean", fill_value=None)`: Initializes the MissingValueHandler with the specified strategy.
  - `fit(self, X)`: Fits the handler to the DataFrame.
  - `transform(self, X)`: Transforms the DataFrame by applying the missing value handling strategy.
  - `fit_transform(self, X)`: Fits the handler and transforms the DataFrame.
  - `fill_with_mean(df, column)`: Fills missing values in the specified column with the mean.
  - `fill_with_median(df, column)`: Fills missing values in the specified column with the median.
  - `fill_with_mode(df, column)`: Fills missing values in the specified column with the mode.
  - `drop_missing(df, column)`: Drops rows with missing values in the specified column.

### 6. OutlierHandler

A class for handling outliers in a DataFrame using the IQR (Interquartile Range) method.

- **Methods**:
  - `__init__(self, method="iqr", threshold=1.5)`: Initializes the OutlierHandler with the specified method and threshold.
  - `fit(self, X)`: Calculates the lower and upper bounds for outliers.
  - `transform(self, X)`: Clips the values in the DataFrame to be within the calculated bounds.
  - `fit_transform(self, X)`: Combines the fit and transform methods.

### 7. Scaler

A class for scaling numeric data using either StandardScaler or MinMaxScaler.

- **Methods**:
  - `__init__(self, method="standard")`: Initializes the Scaler with the specified method.
  - `fit(self, X)`: Fits the scaler to the DataFrame.
  - `transform(self, X)`: Transforms the DataFrame using the fitted scaler.
  - `fit_transform(self, X)`: Fits the scaler and transforms the DataFrame.

### 8. TextCleaner

A class for performing text cleaning operations such as removing stopwords, punctuation, and lemmatizing words.

- **Methods**:
  - `__init__(self, remove_stopwords=True, lemmatize=True)`: Initializes the TextCleaner with the specified options.
  - `clean(self, text)`: Cleans the input text by performing the specified operations.

## Installation

To use this library, clone the repository and install the required packages:

```sh
git clone <repository-url>
cd <repository-directory>
pip install -r requirements.txt