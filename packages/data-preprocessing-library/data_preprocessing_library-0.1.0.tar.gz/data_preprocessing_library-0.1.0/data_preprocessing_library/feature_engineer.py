class feature_engineer:
    """
       Veri setine yeni özellikler eklemek için kullanılan sınıf.

       Attributes:
           None

       Methods:
           create_new_features(data): Veri setine yeni özellikler ekler.

       Usage:
           data_with_new_features = FeatureEngineer.create_new_features(data)
       """
    @staticmethod
    def create_new_features(data):
        """
        Yeni özellikler oluşturan bir işlev.

        Argümanlar:
        data (DataFrame): Özellik mühendisliği için kullanılacak veri seti.

        Dönüş:
        DataFrame: Yeni özelliklerin eklenmiş veri seti.
        """
        data['NewFeature'] = data['Feature1'] + data['Feature2']  # Örnek olarak iki sütunu toplama
        return data