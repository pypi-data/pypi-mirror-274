import unittest
import pandas as pd
import numpy as np
from mypreprocessinglib.missing_value_handler import missing_value_handler
from mypreprocessinglib.feature_engineer import feature_engineer
from mypreprocessinglib.date_time_handler import date_time_handler
from mypreprocessinglib.data_type_converter import data_type_converter
from mypreprocessinglib.categorical_encoder import categorical_encoder


class test_data_preprocessing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Verinizi burada yükleyin
        dosya_yolu = r"C:\Users\Dell\Desktop\synthetic_sample_data (1).csv"
        cls.data = pd.read_csv(dosya_yolu)

    def test_detect_missing_values(self):
        missing_handler = missing_value_handler()
        result = missing_handler.detect_missing_values(self.data)

        # Beklenen sonucu hesapla
        expected_result = self.data.isnull().sum()

        self.assertTrue(result.equals(expected_result))


    def test_fill_missing_values(self):
        numeric_columns = self.data.select_dtypes(include=['number']).columns
        filled_data = self.data.copy()
        filled_data[numeric_columns] = filled_data[numeric_columns].fillna(filled_data[numeric_columns].mean())
        self.assertFalse(filled_data.isnull().values.any())

    def test_remove_missing_values(self):
        cleaned_data = missing_value_handler.remove_missing_values(self.data)
        self.assertFalse(cleaned_data.isnull().values.any())


    def test_create_new_features(self):
        # Test için bir veri seti oluşturun veya başlatın
        data = pd.DataFrame({
            'Movie Id': [1, 2, 3],
            'Genre': ['Action', 'Comedy', 'Drama'],
            'Release Date': ['2022-01-01', '2022-02-01', '2022-03-01'],
            'Rating': [8.5, 7.2, 6.9],
            'Summary': ['Action movie', 'Comedy movie', 'Drama movie'],
            'Shooting Location': ['USA', 'UK', 'Canada'],
            'Budget in USD': [1000000, 2000000, 1500000],
            'Awards': [3, 1, 2],
            'Popular': [True, False, True]
        })

        # 'Release Date' sütununu 'Date' adıyla bir tarih sütununa dönüştürün
        data['Date'] = pd.to_datetime(data['Release Date'], format='%Y-%m-%d')

        # 'Date' sütununu kullanarak özellikleri çıkarın
        data_with_features = date_time_handler.extract_data_features(data, column='Date')

        # Çıkarılan özelliklerin doğru şekilde eklenip eklenmediğini kontrol edin
        self.assertTrue('Year' in data_with_features.columns)
        self.assertTrue('Month' in data_with_features.columns)
        self.assertTrue('Day' in data_with_features.columns)
        self.assertTrue('DayOfWeek' in data_with_features.columns)

        # Yeni özelliklerin oluşturulduğunu kontrol edin
        data_with_new_feature = feature_engineer.create_new_features(data, column1='Budget in USD', column2='Awards')
        self.assertTrue('NewFeature' in data_with_new_feature.columns)

    def test_extract_data_features(self):
        pass

    def test_convert_to_numeric(self):
        # Önceki ve sonraki veri setlerini yazdırarak dönüşümü kontrol edin
        print("Original DataFrame:")
        print(self.data)

        # Mevcut sütun adlarını kontrol edin
        print("Existing columns:")
        print(self.data.columns)

        # Mevcut sütun adlarına uygun olarak sadece var olan sütunları seçin
        columns_to_convert = ['Budget in USD', 'Awards', 'Popular']

        # Sütunları sayısal veri türüne dönüştürün
        numeric_data = data_type_converter.convert_to_numeric(self.data, columns=columns_to_convert)

        print("Numeric DataFrame:")
        print(numeric_data)

        # Dönüştürülen DataFrame'in veri türlerini kontrol edin
        print("Data Types:")
        print(numeric_data.dtypes)

        # Sütunların doğru şekilde dönüştürüldüğünü kontrol edin
        for column in columns_to_convert:
          self.assertTrue(pd.api.types.is_numeric_dtype(numeric_data[column]))

    if __name__ == '__main__':
        unittest.main()
