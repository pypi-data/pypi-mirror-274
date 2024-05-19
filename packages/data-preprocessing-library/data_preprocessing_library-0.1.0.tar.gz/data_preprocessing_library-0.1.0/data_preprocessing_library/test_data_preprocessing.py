import unittest
import pandas as pd
import numpy as np
from data_preprocessing_library.missing_value_handler import missing_value_handler
from data_preprocessing_library.feature_engineer import feature_engineer
from data_preprocessing_library.data_time_handler import data_time_handler
from data_preprocessing_library.data_type_converter import data_type_converter
from data_preprocessing_library.categorical_encoder import categorical_encoder


def main():
    # Excel dosyasını yükle
    file_path = 'synthetic_sample_data (1).csv'
    data = pd.read_excel(file_path)


class test_data_preprocessing(unittest.TestCase):

    def test_detect_missing_values(self):
        data = pd.DataFrame({'A': [1, 2, np.nan, 4], 'B': [np.nan, 6, 7, 8]})
        missing_handler = missing_value_handler()  # Değişiklik burada
        result = missing_handler.detect_missing_values(data)  # Değişiklik burada
        expected_result = pd.Series({'A': 1, 'B': 1})  # Beklenen eksik değer sayısı
        self.assertTrue(result.equals(expected_result))

    def test_fill_missing_values(self):
        data = pd.DataFrame({'A': [1, 2, np.nan, 4], 'B': [np.nan, 6, 7, 8]})
        filled_data = missing_value_handler.fill_missing_values(data)
        # Eksik değerlerin doldurulması bekleniyor
        self.assertFalse(filled_data.isnull().values.any())

    def test_remove_missing_values(self):
        data = pd.DataFrame({'A': [1, 2, np.nan, 4], 'B': [np.nan, 6, 7, 8]})
        cleaned_data = missing_value_handler.remove_missing_values(data)
        # Eksik değerlerin kaldırılması bekleniyor
        self.assertFalse(cleaned_data.isnull().values.any())

    def test_create_new_features(self):
        data = pd.DataFrame({'Feature1': [1, 2, 3], 'Feature2': [4, 5, 6]})
        data_with_new_feature = feature_engineer.create_new_features(data)
        # Yeni özelliklerin eklenip eklenmediğini kontrol etme
        self.assertTrue('NewFeature' in data_with_new_feature.columns)

    def test_extract_date_features(self):
        data = pd.DataFrame({'Date': ['2023-01-01', '2023-02-01', '2023-03-01']})
        data_with_features = data_time_handler.extract_date_features(data, column='Date')
        # Tarih özelliklerinin doğru şekilde eklenip eklenmediğini kontrol etme
        self.assertTrue('Year' in data_with_features.columns)
        self.assertTrue('Month' in data_with_features.columns)
        self.assertTrue('Day' in data_with_features.columns)
        self.assertTrue('DayOfWeek' in data_with_features.columns)

    def test_convert_to_numeric(self):
        # Test veri setini oluşturun
        data = pd.DataFrame({'A': ['1', '2', '3'], 'B': ['4', '5', '6']})

        # Önceki ve sonraki veri setlerini yazdırarak dönüşümü kontrol edin
        print("Original DataFrame:")
        print(data)

        # Sütunları sayısal veri türüne dönüştürün
        numeric_data = data_type_converter.convert_to_numeric(data, columns=['A', 'B'])

        print("Numeric DataFrame:")
        print(numeric_data)

        # Dönüştürülen DataFrame'in veri türlerini kontrol edin
        print("Data Types:")
        print(numeric_data.dtypes)

        # Sütunların doğru şekilde dönüştürüldüğünü kontrol edin
        self.assertTrue(numeric_data.dtypes['A'] in [np.float64, np.int64])
        self.assertTrue(numeric_data.dtypes['B'] in [np.float64, np.int64])

    if _name_ == '_main_':
        unittest.main()
