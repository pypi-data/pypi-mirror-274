from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import pandas as pd

class categorical_encoder:
    """
       Kategorik değişkenleri kodlamak için kullanılan sınıf.

       Attributes:
           None

       Methods:
           one_hot_encode(data, columns): One-hot encoding uygular.

       Usage:
           encoded_data = CategoricalEncoder.one_hot_encode(data, columns=['A', 'B'])
       """

    @staticmethod
    def one_hot_encode(data, columns):
        """
        One-hot encoding işlemi uygulayan bir işlev.

        Argümanlar:
        data (DataFrame): Kodlanacak veri seti.
        columns (list): One-hot encoding uygulanacak sütunların listesi.

        Dönüş:
        DataFrame: One-hot encoding uygulanmış veri seti.
        """
        encoder = OneHotEncoder(drop='first', sparse=False)
        encoded_data = pd.DataFrame(encoder.fit_transform(data[columns]))
        data = data.drop(columns, axis=1)
        encoded_data.columns = encoder.get_feature_names_out(columns)
        return pd.concat([data, encoded_data], axis=1)

    @staticmethod
    def label_encode(data, column):
        """
        Label encoding işlemi uygulayan bir işlev.

        Argümanlar:
        data (DataFrame): Kodlanacak veri seti.
        column (str): Label encoding uygulanacak sütun adı.

        Dönüş:
        DataFrame: Label encoding uygulanmış veri seti.
        """
        encoder = LabelEncoder()
        data[column] = encoder.fit_transform(data[column])
        return data
