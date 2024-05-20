import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class scaler:

    @staticmethod
    def standardize_data(data):
        """
        Veriyi standartlaştıran bir işlev.

        Argümanlar:
        data (DataFrame): Standartlaştırılacak veri seti.

        Dönüş:
        DataFrame: Standartlaştırılmış veri seti.
        """
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)
        return pd.DataFrame(scaled_data, columns=data.columns)

    @staticmethod
    def normalize_data(data):
        """
        Veriyi normalize eden bir işlev.

        Argümanlar:
        data (DataFrame): Normalize edilecek veri seti.

        Dönüş:
        DataFrame: Normalize edilmiş veri seti.
        """
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(data)
        return pd.DataFrame(scaled_data, columns=data.columns)
