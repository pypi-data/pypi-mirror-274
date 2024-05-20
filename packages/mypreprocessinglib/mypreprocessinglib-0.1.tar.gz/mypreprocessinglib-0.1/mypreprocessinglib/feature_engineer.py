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
    def create_new_features(data, column1='MevcutSutun1', column2='MevcutSutun2'):
        """
        Yeni özellikler oluşturan bir işlev.

        Argümanlar:
        data (DataFrame): Özellik mühendisliği için kullanılacak veri seti.
        column1 (str): Yeni özellik oluşturmak için kullanılacak mevcut sütun adı 1.
        column2 (str): Yeni özellik oluşturmak için kullanılacak mevcut sütun adı 2.

        Dönüş:
        DataFrame: Yeni özelliklerin eklenmiş veri seti.
        """
        data['NewFeature'] = data[column1] + data[column2]  # Örnek olarak iki sütunu toplama
        return data