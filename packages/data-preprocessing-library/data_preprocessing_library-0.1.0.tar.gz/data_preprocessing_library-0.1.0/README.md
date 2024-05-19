import pandas as pd
import numpy as np
from data_preprocessing_library.missing_value_handler import missing_value_handler
from data_preprocessing_library.outlier_handler import outlier_handler
from data_preprocessing_library.scaler import scaler
from data_preprocessing_library.text_cleaner import text_cleaner
from data_preprocessing_library.feature_engineer import feature_engineer
from data_preprocessing_library.data_type_converter import data_type_converter
from data_preprocessing_library.categorical_encoder import categorical_encoder
from data_preprocessing_library.data_time_handler import data_time_handler

# Example usage
data = pd.DataFrame({'A': [1, 2, np.nan, 4], 'B': [np.nan, 6, 7, 8]})
missing_handler = missing_value_handler()
missing_values = missing_handler.detect_missing_values(data)
print(missing_values)

# Example usage
data = pd.DataFrame({'A': [1, 2, 100, 4], 'B': [5, 6, 7, 800]})
outliers = outlier_handler.detect_outliers(data)
print(outliers)

# Example usage
data = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [4, 3, 2, 1]})
scaled_data = scaler.standardize_data(data)
print(scaled_data)

# Example usage
text = "This is a sample text, with punctuation and stopwords!"
cleaned_text = text_cleaner.clean_text(text)
print(cleaned_text)

# Example usage
data = pd.DataFrame({'Feature1': [1, 2, 3], 'Feature2': [4, 5, 6]})
data_with_new_feature = feature_engineer.create_new_features(data)
print(data_with_new_feature)

# Example usage
data = pd.DataFrame({'A': ['1', '2', '3'], 'B': ['4', '5', '6']})
numeric_data = data_type_converter.convert_to_numeric(data, columns=['A', 'B'])
print(numeric_data)

# Example usage
data = pd.DataFrame({'A': ['cat', 'dog', 'bird'], 'B': ['red', 'blue', 'green']})
encoded_data = categorical_encoder.one_hot_encode(data, columns=['A', 'B'])
print(encoded_data)

# Example usage
data = pd.DataFrame({'Date': ['2023-01-01', '2023-02-01', '2023-03-01']})
data_with_features = data_time_handler.extract_date_features(data, column='Date')
print(data_with_features)