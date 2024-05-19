import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string

class missing_value_handler:
    @staticmethod
    def detect_missing_values(data):
        """
        Veri setindeki eksik değerleri tespit eden bir işlev.

        Argümanlar:
        data (DataFrame): Eksik değerleri tespit etmek için kullanılacak veri seti.

        Dönüş:
        Series: Sütun başına eksik değer sayısı.
        """
        missing_values = data.isnull().sum()
        return missing_values

    @staticmethod
    def fill_missing_values(data, strategy='mean',  value=None):
        """
        Eksik değerleri dolduran bir işlev.

        Argümanlar:
        data (DataFrame): Eksik değerleri doldurmak için kullanılacak veri seti.
        strategy (str, optional): Doldurma stratejisi. Varsayılan olarak 'mean' (ortalama).

        Dönüş:
        DataFrame: Eksik değerlerin doldurulmuş hali.
        """
        if strategy == 'mean':
            filled_data = data.fillna(data.mean())
        elif strategy == 'median':
            filled_data = data.fillna(data.median())
        elif strategy == 'constant':
            if value is None:
                raise ValueError("Sabit bir değer belirtmelisiniz.")
            filled_data = data.fillna(value)
        elif strategy == 'drop':
            filled_data = data.dropna()
        else:
            raise ValueError("Geçersiz doldurma stratejisi!")

        return filled_data

    @staticmethod
    def remove_missing_values(data):
        """
        Eksik değerleri içeren satırları veya sütunları kaldıran bir işlev.

        Argümanlar:
        data (DataFrame): Eksik değerleri kaldırmak için kullanılacak veri seti.

        Dönüş:
        DataFrame: Eksik değerlerin kaldırıldığı veri seti.
        """
        cleaned_data = data.dropna()
        return cleaned_data