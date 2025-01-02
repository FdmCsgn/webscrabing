import os
import re
import nltk
from nltk.corpus import stopwords
from unidecode import unidecode
from word2number import w2n

nltk.download('stopwords')

# Durma kelimeleri (stopwords) yükle
stop_words = set(stopwords.words('turkish'))  # Dilini istediğiniz gibi değiştirebilirsiniz.

def to_lowercase(text):
    return text.lower()

def remove_numbers(text):
    # Sayıları metne dönüştürme
    words = text.split()
    new_words = []
    for word in words:
        try:
            # Kelimeyi sayıya çevirme
            new_words.append(str(w2n.word_to_num(word)))
        except ValueError:
            # Eğer kelime bir sayı değilse olduğu gibi ekle
            new_words.append(word)
    return ' '.join(new_words)

def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)

def remove_whitespace(text):
    return re.sub(r'\s+', ' ', text).strip()

def expand_abbreviations(text):
    abbreviations = {
        "ve": "ve", "yada": "ya da", "gibi": "gibi",  # Örnek, başka kısaltmalar ekleyebilirsiniz
        "için": "için", "bahçe":"bahçe"
    }
    for abbrev, full in abbreviations.items():
        text = text.replace(abbrev, full)
    return text

def remove_stopwords(text):
    return ' '.join([word for word in text.split() if word not in stop_words])

def remove_sparse_terms(text):
    # Seyrek terimleri (çok az kullanılan kelimeler) kaldırmak için bir yöntem
    word_freq = nltk.FreqDist(text.split())
    frequent_words = [word for word, freq in word_freq.items() if freq > 1]  # Örneğin sadece 1'den fazla geçenleri tut
    return ' '.join([word for word in text.split() if word in frequent_words])

def canonicalize_text(text):
    # Diğer işlevleri birleştirerek metni normalize et
    text = to_lowercase(text)
    text = remove_numbers(text)
    text = remove_punctuation(text)
    text = remove_whitespace(text)
    text = expand_abbreviations(text)
    text = remove_stopwords(text)
    text = remove_sparse_terms(text)
    text = unidecode(text)  # Diakritik işaretlerini kaldırır
    return text

def process_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                # Metni işleyip dosyanın üzerine kaydedelim
                processed_text = canonicalize_text(text)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(processed_text)

# Klasörün yolu
directory_path = r'C:\Users\ardac\OneDrive\Masaüstü\wepscrabinsoup\indirilen_sayfalar'  # Kendi klasör yolunuzu buraya yazın
process_files_in_directory(directory_path)

