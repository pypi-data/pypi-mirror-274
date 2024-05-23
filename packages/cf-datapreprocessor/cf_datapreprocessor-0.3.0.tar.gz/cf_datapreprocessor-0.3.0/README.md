# cf_datapreprocessor

cf_datapreprocessor is a Python package that simplifies data preprocessing steps for machine learning projects. This package provides various data preprocessing tools, including handling missing values, detecting and correcting outliers, data scaling, text cleaning, encoding categorical data, and more.

## Installation

To install the package, follow these steps:

```sh
pip install cf_datapreprocessor
Usage
1. Handling Missing Values (missing_value_handler)
You can fill missing values with mean, median, or a constant value, or you can remove the missing data.

python
Kodu kopyala
from dataPreprocessor.missing_value_handler import missing_value_handler

handler = missing_value_handler()

# Impute with mean
df = handler.impute_mean(df, 'column_name')

# Impute with median
df = handler.impute_median(df, 'column_name')

# Impute with a constant value
df = handler.impute_constant(df, 'column_name', value=0)

# Remove missing data
df = handler.delete_missing(df, 'column_name')
2. Handling Outliers (outlier_handler)
You can detect and remove outliers using the IQR (Interquartile Range) method.

python
Kodu kopyala
from dataPreprocessor.outlier_handler import outlier_handler

handler = outlier_handler()
df = handler.iqr_outliers(df, 'column_name')
3. Data Scaling (scaler)
You can scale your data using Min-Max scaling or standard scaling methods.

python
Kodu kopyala
from dataPreprocessor.scaler import scaler

scaler = scaler()

# Min-Max scaling
df = scaler.min_max_scale(df, 'column_name')

# Standard scaling
df = scaler.standard_scale(df, 'column_name')
4. Text Cleaning (text_cleaner)
You can clean text data by removing stopwords and applying lemmatization.

python
Kodu kopyala
from dataPreprocessor.text_cleaner import text_cleaner

cleaner = text_cleaner()

# Clean a single text entry
clean_text = cleaner.clean_text("Your text data here.")

# Clean a DataFrame column
df = cleaner.clean_column(df, 'text_column')
5. Feature Engineering (feature_engineer)
You can create new features or add new columns using existing columns.

python
Kodu kopyala
from dataPreprocessor.feature_engineer import feature_engineer

engineer = feature_engineer()

# Create a new feature
df = engineer.create_feature(df, 'new_column', lambda df: df['column1'] + df['column2'])

# Add columns
df['new_column'] = engineer.add_columns(df, 'column1', 'column2')
6. Data Type Conversion (data_type_converter)
You can convert column data types to numeric or categorical types.

python
Kodu kopyala
from dataPreprocessor.data_type_converter import data_type_converter

converter = data_type_converter()

# Convert to numeric type
df = converter.to_numeric(df, 'column_name')

# Convert to categorical type
df = converter.to_categorical(df, 'column_name')
7. Encoding Categorical Data (categorical_encoder)
You can encode categorical data using One-Hot Encoding or Label Encoding methods.

python
Kodu kopyala
from dataPreprocessor.categorical_encoder import categorical_encoder

encoder = categorical_encoder()

# One-Hot Encoding
df = encoder.one_hot_encode(df, 'categorical_column')

# Label Encoding
df = encoder.label_encode(df, 'categorical_column')
8. Handling Date and Time Data (datetime_handler)
You can process date and time data and extract various components.

python
Kodu kopyala
from dataPreprocessor.datetime_handler import datetime_handler

handler = datetime_handler()

# Extract date parts
df = handler.extract_date_parts(df, 'date_column')
Requirements
You will need the following Python libraries to use this package:

pandas
numpy
scikit-learn
nltk
Contact
If you have any questions or would like to contribute, please contact:

Fatmanur Caliskan: fatmanur.caliskan@stu.fsm.edu.tr
Cihan Yilmaz: cihan.yilmaz@stu.fsm.edu.tr

Kodu kopyala

Feel free to further customize the content as needed.