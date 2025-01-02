import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Ana URL ve sayfa numarası
base_url = 'https://gardenlux-tr.decorexpro.com/hozyajstvo/'

# Sayfa numarasını arttırarak birden fazla sayfayı gezme
for page_num in range(1, 42):  # 1'den 2'ye kadar olan sayfaları al
    page_url = f"{base_url}page/{page_num}"

    # Sayfayı al
    response = requests.get(page_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Sayfadaki tüm linkleri bul
    for a_tag in soup.find_all('a', class_='box__title'):
        linkler = a_tag.get('href')

        if linkler:
            # Göreli URL'yi tam URL'ye dönüştür
            href = urljoin(base_url, linkler)
            print(f"Link: {href}")

            try:
                # Linkin HTML içeriğini al
                response = requests.get(href)
                response.raise_for_status()  # Hata durumunda exception fırlat
                soup = BeautifulSoup(response.text, "html.parser")

                # Sayfanın başlığını al ve geçersiz karakterleri temizle
                page_title = soup.title.get_text() if soup.title else "Başlık Bulunamadı"
                file_name = re.sub(r'[\\/*?:"<>|]', '_', page_title)  # Geçersiz karakterleri '_' ile değiştir
                file_name = file_name.replace(" ", "_")  # Boşlukları da '_' ile değiştir

                # Dosya yolu ve klasörü oluştur
                folder_path = os.path.join("indirilen_sayfalar", file_name)

                # Klasör yoksa oluştur
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                # Dosya yolunu tam olarak oluştur
                file_path = os.path.join(folder_path, f"{file_name}.txt")

                # Sayfadaki metni al (örneğin başlık ve içerik)
                page_content = soup.get_text()

                # Sayfa içeriğini dosyaya kaydet
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(f"Sayfa Başlığı: {page_title}\n\n")
                    file.write(f"Sayfa İçeriği:\n{page_content}\n\n")

                print(f"Metin kaydedildi: {file_path}")

                # Sayfadaki tüm <img> etiketlerini bul
                img_tags = soup.find_all("img")
                for img in img_tags:
                    img_src = img.get("src")
                    if img_src:  # Eğer 'src' varsa
                        img_url = urljoin(base_url, img_src)  # Tam URL'yi oluştur
                        print(f"İndiriliyor: {img_url}")

                        try:
                            # Görseli indir
                            img_data = requests.get(img_url).content

                            # Görsel dosya ismini oluştur
                            img_name = os.path.basename(img_url)
                            img_path = os.path.join(folder_path, img_name)

                            # Görseli kaydet
                            with open(img_path, "wb") as img_file:
                                img_file.write(img_data)
                            print(f"Görsel kaydedildi: {img_path}")

                            # Görseli metin dosyasına ekle
                            with open(file_path, "a", encoding="utf-8") as file:
                                file.write(f"Görsel: {img_url}\n")

                        except requests.exceptions.RequestException as e:
                            print(f"Görsel indirilemedi: {img_url}, Hata: {e}")

            except requests.exceptions.RequestException as e:
                print(f"Linke gidilemedi: {href}, Hata: {e}")
