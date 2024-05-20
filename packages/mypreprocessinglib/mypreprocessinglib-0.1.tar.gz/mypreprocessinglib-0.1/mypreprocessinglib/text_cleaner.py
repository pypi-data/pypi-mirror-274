# TextCleaner.py

import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


class text_cleaner:
    @staticmethod
    def clean_text(text, tokenize=True):
        """
        Metni temizleyen bir işlev.

        Argümanlar:
        text (str): Temizlenecek metin.

        Dönüş:
        str: Temizlenmiş metin.
        """
        # Küçük harfe dönüştürme
        text = text.lower()
        # Noktalama işaretlerini kaldırma
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Stopwords'leri kaldırma
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)

        filtered_words = [word for word in word_tokens if word not in stop_words]
        # Lemmatizasyon
        lemmatizer = WordNetLemmatizer()
        cleaned_text = ' '.join([lemmatizer.lemmatize(word) for word in filtered_words])
        return cleaned_text

