# PC GÃ¼venlik Sistemi

YÃ¼z tanÄ±ma teknolojisi ile Ã§alÄ±ÅŸan Windows gÃ¼venlik sistemi.

## Ã–zellikler

- **YÃ¼z TanÄ±ma**: OpenCV + LBPH tabanlÄ±, hafif ve hÄ±zlÄ±
- **Telegram Bildirimi**: Bilinmeyen kiÅŸi tespitinde anlÄ±k uyarÄ±
- **Otomatik BaÅŸlangÄ±Ã§**: Windows aÃ§Ä±lÄ±ÅŸÄ±nda 8 saniye gÃ¼venlik taramasÄ±
- **KullanÄ±cÄ± ArayÃ¼zÃ¼**: Kolay yÃ¶netim iÃ§in GUI

## Kurulum

### 1. BaÄŸÄ±mlÄ±lÄ±klarÄ± Kur

`ash
pip install -r requirements.txt
`

### 2. AyarlarÄ± YapÄ±landÄ±r

`ash
# env.example dosyasÄ±nÄ± .env olarak kopyala
copy env.example .env

# .env dosyasÄ±nÄ± dÃ¼zenle ve token'larÄ±nÄ± gir
notepad .env
`

### 3. Ã‡alÄ±ÅŸtÄ±r

`ash
python main.py
`

## Telegram Bot Kurulumu

1. Telegram'da [@BotFather](https://t.me/BotFather) ile konuÅŸun
2. `/newbot` komutu ile bot oluÅŸturun
3. Token'Ä± kopyalayÄ±n
4. [@userinfobot](https://t.me/userinfobot) ile Chat ID Ã¶ÄŸrenin
5. `.env` dosyasÄ±na token ve chat ID'yi yazÄ±n

## KullanÄ±m

| Komut | AÃ§Ä±klama |
|-------|----------|
| `python main.py` | GUI ile baÅŸlat |
| `python main.py --quick-scan` | 8 saniye hÄ±zlÄ± tarama |
| `python main.py --add-person` | Yeni kiÅŸi ekle |
| `python main.py --silent` | Arka planda Ã§alÄ±ÅŸtÄ±r |

## Gereksinimler

- Python 3.8+
- Windows 10/11
- Webcam
- Ä°nternet baÄŸlantÄ±sÄ±

## Lisans

MIT License