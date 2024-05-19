import pandas as pd

class outlier_handler:
    @staticmethod
    def detect_outliers(data, threshold=3):
        """
        IQR yöntemini kullanarak aykırı değerleri tespit eden işlev.

        Argümanlar:
        data (DataFrame): Aykırı değerleri tespit etmek için kullanılacak veri seti.

        Dönüş:
        DataFrame: Aykırı değerlerin tespit edildiği bir DataFrame.
        """
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR)))
        return outliers


    @staticmethod
    def handle_outliers(data, method='drop'):
        """
        Aykırı değerleri ele alacak bir işlev.

        Argümanlar:
        data (DataFrame): Aykırı değerleri ele almak için kullanılacak veri seti.
        method (str, optional): Aykırı değerleri ele alma yöntemi. 'drop' (silme) veya 'replace' (değiştirme). Varsayılan olarak 'drop'.

        Dönüş:
        DataFrame: Aykırı değerlerin ele alındığı veri seti.
        """
        outliers = outlier_handler.detect_outliers_iqr(data)
        if method == 'drop':
            cleaned_data = data[~outliers.any(axis=1)]
        elif method == 'replace':
            cleaned_data = data.mask(outliers, data.median())
        else:
            raise ValueError("Geçersiz aykırı değer ele alma yöntemi!")
        return cleaned_data