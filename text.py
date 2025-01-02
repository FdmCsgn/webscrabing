import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import re

# URL ve klasör tanımları
base_url = "https://gardenlux-tr.decorexpro.com/hozyajstvo/pchelovodstvo/pihtovoe-maslo-ot-kleschey-obrabotka-i-lechenie-pchel.html"
output_folder = "Kenelerden köknar yağı"
image_folder = os.path.join(output_folder, "images")
text_file = os.path.join(output_folder, "content.txt")

# Klasörleri oluştur
os.makedirs(image_folder, exist_ok=True)

# Sayfayı indir ve BeautifulSoup ile ayrıştır
response = requests.get(base_url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# 1. Metin İçeriği Çekme
with open(text_file, "w", encoding="utf-8") as file:
    # Tüm paragraf <p> etiketlerini bul
    paragraphs = soup.find_all("p")
    for p in paragraphs:
        text = p.get_text(strip=True)
        if text:
            file.write(text + "\n\n")
    print(f"Metinler kaydedildi: {text_file}")

# 2. Görselleri İndirme
img_tags = soup.find_all("img")
for img in img_tags:
    img_src = img.get("src")  # Görselin kaynağı
    if img_src:
        # Görsel URL'sini tam URL'ye dönüştür
        img_url = urljoin(base_url, img_src)
        print(f"İndiriliyor: {img_url}")

        try:
            # Görseli indir
            img_data = requests.get(img_url).content

            # Geçerli bir dosya adı oluştur
            img_name = os.path.basename(img_src)
            img_name = re.sub(r'[<>:"/\\|?*]', '_', img_name)  # Geçersiz karakterleri temizle
            file_path = os.path.join(image_folder, img_name)

            # Görseli kaydet
            with open(file_path, "wb") as f:
                f.write(img_data)
            print(f"Görsel kaydedildi: {file_path}")
        except Exception as e:
            print(f"Görsel indirilemedi: {img_url}, Hata: {e}")
