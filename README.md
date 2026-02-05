# PC Güvenlik Sistemi

Yüz tanıma teknolojisi ile çalışan Windows güvenlik sistemi.

## Özellikler

- **Yüz Tanıma**: OpenCV + LBPH tabanlı, hafif ve hızlı
- **Telegram Bildirimi**: Bilinmeyen kişi tespitinde anlık uyarı
- **Otomatik Başlangıç**: Windows açılışında 8 saniye güvenlik taraması
- **Kullanıcı Arayüzü**: Kolay yönetim için GUI

## Kurulum

### 1. Bağımlılıkları Kur

```bash
pip install -r requirements.txt
```

### 2. Ayarları Yapılandır

```bash
# env.example dosyasını .env olarak kopyala
copy env.example .env

# .env dosyasını düzenle ve token'larını gir
notepad .env
```

### 3. Çalıştır

```bash
python main.py
```

## Telegram Bot Kurulumu

1. Telegram'da [@BotFather](https://t.me/BotFather) ile konuşun
2. `/newbot` komutu ile bot oluşturun
3. Token'ı kopyalayın
4. [@userinfobot](https://t.me/userinfobot) ile Chat ID öğrenin
5. `.env` dosyasına token ve chat ID'yi yazın

## Kullanım

| Komut | Açıklama |
|-------|----------|
| `python main.py` | GUI ile başlat |
| `python main.py --quick-scan` | 8 saniye hızlı tarama |
| `python main.py --add-person` | Yeni kişi ekle |
| `python main.py --silent` | Arka planda çalıştır |

## Gereksinimler

- Python 3.8+
- Windows 10/11
- Webcam
- İnternet bağlantısı

## Lisans

MIT License