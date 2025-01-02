# 🌐 Web Kazıma (Web Scraping) Projesi

Beautiful Soup kullanarak web sayfalarından veri çıkarma ve toplama rehberi.

## 📚 Beautiful Soup Nedir?

Beautiful Soup, Python'da web sayfalarını parse etmek ve veri çıkarmak için kullanılan güçlü bir kütüphanedir. HTML ve XML dosyalarını parse ederek içerilerinden istediğimiz verileri çıkarmamızı sağlar.

## 🛠️ Temel Kurulum

```python
# Gerekli kütüphanelerin kurulumu
pip install beautifulsoup4
pip install requests
pip install lxml

# Temel importlar
from bs4 import BeautifulSoup
import requests
import os
import time
```

## 🔍 Temel Kullanım Örnekleri

### 1. Web Sayfasını Çekme
```python
# Web sayfasına istek atma
url = "https://example.com"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
```

### 2. Metin Verisi Çıkarma
```python
# Başlıkları çekme
titles = soup.find_all('h1')
for title in titles:
    print(title.text.strip())

# Paragrafları çekme
paragraphs = soup.find_all('p')
for p in paragraphs:
    print(p.text.strip())
```

### 3. Görsel Çıkarma
```python
# Resimleri çekme ve kaydetme
images = soup.find_all('img')
for img in images:
    img_url = img.get('src')
    if img_url:
        img_data = requests.get(img_url).content
        with open(f'images/{img_url.split("/")[-1]}', 'wb') as f:
            f.write(img_data)
```

## 🎯 Veri Çıkarma Teknikleri

### 1. CSS Seçiciler
```python
# Class ile seçme
content = soup.find('div', class_='content')

# ID ile seçme
header = soup.find('div', id='header')

# Multiple seçiciler
links = soup.select('div.content a')
```

### 2. Özel Filtreler
```python
# Lambda fonksiyonları ile filtreleme
specific_divs = soup.find_all('div', attrs={
    'class': lambda x: x and 'specific-class' in x
})
```

## 🛡️ Best Practices ve Dikkat Edilmesi Gerekenler

1. **Rate Limiting**
```python
# İstekler arasına gecikme ekleme
import time

def scrape_with_delay(urls, delay=2):
    for url in urls:
        response = requests.get(url)
        # İşlemler...
        time.sleep(delay)  # Saniye cinsinden bekleme
```

2. **Hata Yönetimi**
```python
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Hata oluştu: {e}")
```

3. **User-Agent Belirtme**
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
response = requests.get(url, headers=headers)
```

## 📂 Veri Saklama Stratejileri

### 1. Dosya Sistemi
```python
# Metin verilerini kaydetme
with open('data.txt', 'w', encoding='utf-8') as f:
    f.write(extracted_text)

# Görselleri kaydetme
def save_image(img_url, folder='images'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    response = requests.get(img_url)
    file_name = os.path.join(folder, img_url.split('/')[-1])
    with open(file_name, 'wb') as f:
        f.write(response.content)
```

### 2. Veritabanı Entegrasyonu
```python
import sqlite3

def save_to_db(data):
    conn = sqlite3.connect('scraping.db')
    c = conn.cursor()
    c.execute('''INSERT INTO scraped_data 
                 (title, content, url) 
                 VALUES (?, ?, ?)''', 
                 (data['title'], data['content'], data['url']))
    conn.commit()
    conn.close()
```

## 🔄 Dinamik İçerik İşleme

### 1. JavaScript İçeriği
```python
from selenium import webdriver

def get_dynamic_content(url):
    driver = webdriver.Chrome()
    driver.get(url)
    # Sayfanın yüklenmesini bekle
    time.sleep(2)
    page_source = driver.page_source
    driver.quit()
    return BeautifulSoup(page_source, 'html.parser')
```

## 📊 Veri Temizleme ve İşleme

```python
def clean_text(text):
    # Gereksiz boşlukları temizle
    text = ' '.join(text.split())
    # HTML karakterlerini çöz
    text = BeautifulSoup(text, 'html.parser').get_text()
    return text.strip()
```

## 🚫 Etik ve Yasal Konular

1. `robots.txt` dosyasına uyma
2. Rate limiting uygulama
3. Telif haklarına saygı gösterme
4. Kişisel verileri koruma
5. Site kullanım şartlarına uyma

## 🔍 Performans Optimizasyonu

1. **Asenkron İstekler**
```python
import asyncio
import aiohttp

async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

async def scrape_multiple_pages(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

2. **Multiprocessing**
```python
from multiprocessing import Pool

def scrape_url(url):
    return requests.get(url).text

with Pool(4) as p:
    results = p.map(scrape_url, urls)
```
