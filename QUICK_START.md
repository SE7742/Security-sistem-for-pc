# Hızlı Başlangıç

PC Güvenlik Sistemi'ni kurmak için bu adımları takip edin.

## 1. Kurulum

```bash
# Bağımlılıkları kur
pip install -r requirements.txt

# Kurulumu test et
python test_system.py
```

## 2. Telegram Bot Oluşturma

1. Telegram'da **@BotFather** ile konuşun
2. `/newbot` komutu gönderin
3. Bot adı ve kullanıcı adı belirleyin
4. **Token'ı** kopyalayın (örn: `123456:ABC-xyz...`)

5. **@userinfobot** ile konuşun
6. **Chat ID'nizi** kopyalayın (örn: `987654321`)

## 3. Ayar Dosyası Oluşturma

```bash
# env.example dosyasını .env olarak kopyala
copy env.example .env

# .env dosyasını aç ve düzenle
notepad .env
```

`.env` dosyasına token ve chat ID'nizi yazın:

```
TELEGRAM_BOT_TOKEN=123456:ABC-xyz...
CHAT_ID=987654321
```

## 4. İlk Kişiyi Ekleme

### Kamera ile:
```bash
python main.py --add-person
```

### Dosyadan:
Fotoğrafı `known_faces/isim.jpg` olarak kaydedin.

## 5. Sistemi Başlatma

```bash
# GUI ile başlat
python main.py

# Hızlı tarama (8 saniye)
python main.py --quick-scan
```

## Sorun Giderme

| Sorun | Çözüm |
|-------|-------|
| Kamera açılmıyor | `.env`'de `CAMERA_INDEX=1` deneyin |
| Telegram çalışmıyor | Token ve Chat ID'yi kontrol edin |
| Yüz tanınmıyor | Daha kaliteli fotoğraf ekleyin |

## Yardım

- Sistem testi: `python test_system.py`
- Telegram testi: `python test_telegram.py`
