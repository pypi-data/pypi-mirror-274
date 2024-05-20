import pandas as pd

class date_time_handler:
    """
       Tarih özelliklerini çıkarmak için kullanılan sınıf.

       Attributes:
           None

       Methods:
           extract_date_features(data, column): Tarih özelliklerini çıkarır.

       Usage:
           data_with_features = DateTimeHandler.extract_date_features(data, column='Date')
       """
    @staticmethod
    def extract_data_features(data, column):
        """
        Tarih özelliklerini çıkaran bir işlev.

        Argümanlar:
        data (DataFrame): Tarih özellikleri çıkarılacak veri seti.
        column (str): Tarih sütununun adı.

        Dönüş:
        DataFrame: Tarih özelliklerinin eklenmiş veri seti.
        """
        data[column] = pd.to_datetime(data[column])
        data['Year'] = data[column].dt.year
        data['Month'] = data[column].dt.month
        data['Day'] = data[column].dt.day
        data['DayOfWeek'] = data[column].dt.dayofweek
        return data
