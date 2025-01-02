import pandas as pd
from nltk.tokenize import word_tokenize
import nltk

# 'punkt' tokenizer'ını indir
nltk.download('punkt')

# 'punkt_tab' kaynağını indir
nltk.download('punkt_tab')


# Dosya yolunu tam olarak belirtin
file_path = "C:/Users/ardac/OneDrive/Masaüstü/wepscrabinsoup/tokenized_files/1_aylık_3_ve_6_aylık_buzağıları_besleme__normlar_planlar.txt"

# Dosyayı oku
df = pd.read_csv(file_path, header=None, sep='\r\n', engine='python', names=['hastalıklar'])

# 'lowercase' sütununu ekleyelim
df['lowercase'] = df['hastalıklar'].apply(lambda x: x.lower())

# Tokenize işlemi
df['tokens'] = df['lowercase'].apply(lambda x: word_tokenize(x))

# Tokenize edilmiş metni yazdıralım
print(df['tokens'])

# Token'ları birleştirip tüm metni görmek için
df['joined_tokens'] = df['tokens'].apply(lambda x: ' '.join(x))
print(df['joined_tokens'])

df['joined_tokens'].to_csv('tokenized_data.csv', index=False, header=True)

