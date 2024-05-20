import pandas as pd
import numpy as np
class data_type_converter:
    """
       Veri tipini dönüştürmek için kullanılan sınıf.

       Attributes:
           None

       Methods:
           convert_to_numeric(data, columns): Belirli sütunları sayısal veri tipine dönüştürür.

       Usage:
           numeric_data = DataTypeConverter.convert_to_numeric(data, columns=['A', 'B'])
       """
    @staticmethod
    def convert_to_numeric(data, columns):
        """
        Belirli sütunları sayısal veri tipine dönüştüren bir işlev.

        Argümanlar:
        data (DataFrame): Veri seti.
        columns (list): Sayısal veri tipine dönüştürülecek sütunların listesi.

        Dönüş:
        DataFrame: Veri tipi dönüştürülmüş veri seti.
        """
        for column in columns:
            # Sadece sayısal veri içeren sütunları dönüştür
            if not pd.api.types.is_numeric_dtype(data[column]):
                data[column] = pd.to_numeric(data[column], errors='coerce')
        return data

    @staticmethod
    def convert_to_categorical(data, columns):
        """
        Belirli sütunları kategorik veri tipine dönüştüren bir işlev.

        Argümanlar:
        data (DataFrame): Veri seti.
        columns (list): Kategorik veri tipine dönüştürülecek sütunların listesi.

        Dönüş:
        DataFrame: Veri tipi dönüştürülmüş veri seti.
        """
        data[columns] = data[columns].astype('category')
        return data
