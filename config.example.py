# ⚠️ GÜVENLİK UYARISI: ÖRNEK DOSYA - KİŞİSEL BİLGİ GİRMEYİN!
# Bu dosyayı config.py olarak kopyalayın ve kendi ayarlarınızı girin
# Bu dosya GitHub'a yüklenecek, gerçek bilgilerinizi buraya yazmayın!
#
# NOT: Artık .env dosyası da destekleniyor!
# Önce .env dosyasından okur, yoksa buradaki değerleri kullanır.

import os

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False

# .env dosyasını yükle (varsa)
load_dotenv()

# Helper fonksiyon: .env'den oku, yoksa varsayılan değeri kullan
def get_env(key, default=None, type_func=str):
    """Environment variable oku, yoksa varsayılan değeri döndür"""
    value = os.getenv(key, default)
    if value is None:
        return default
    if type_func == bool:
        if isinstance(value, bool):
            return value
        return str(value).lower() in ('true', '1', 'yes', 'on')
    if type_func == int:
        try:
            return int(value)
        except ValueError:
            return default
    if type_func == float:
        try:
            return float(value)
        except ValueError:
            return default
    if type_func == tuple:
        if isinstance(value, tuple):
            return value
        # Tuple formatı: "(0, 255, 0)" veya "0,255,0"
        try:
            value = str(value).strip('()')
            return tuple(map(int, value.split(',')))
        except ValueError:
            return default
    return value

# ===========================================
# TELEGRAM BOT AYARLARI
# ===========================================
# Telegram Bot Father'dan alacağınız bilgiler
# Önce .env dosyasından okur, yoksa buradaki değeri kullanır
TELEGRAM_BOT_TOKEN = get_env("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")  # Örnek: "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
CHAT_ID = get_env("CHAT_ID", "YOUR_CHAT_ID_HERE")  # Örnek: "123456789"

# Telegram bot kurulumu için:
# 1. @BotFather ile konuşun
# 2. /newbot komutu ile bot oluşturun
# 3. Token'ı yukarıya yazın
# 4. Chat ID için @userinfobot kullanın

# ===========================================
# KAMERA AYARLARI
# ===========================================
CAMERA_INDEX = get_env("CAMERA_INDEX", 0, int)  # Varsayılan kamera (genellikle 0, sorun olursa 1 deneyin)
FRAME_WIDTH = get_env("FRAME_WIDTH", 640, int)
FRAME_HEIGHT = get_env("FRAME_HEIGHT", 480, int)

# ===========================================
# YÜZ TANIMA AYARLARI
# ===========================================
FACE_RECOGNITION_TOLERANCE = get_env("FACE_RECOGNITION_TOLERANCE", 0.6, float)  # Düşük değer = daha sıkı eşleşme (0.4-0.8 arası önerilir)
FACE_DETECTION_SCALE_FACTOR = get_env("FACE_DETECTION_SCALE_FACTOR", 1.1, float)
MIN_NEIGHBORS = get_env("MIN_NEIGHBORS", 5, int)

# ===========================================
# DOSYA YOLLARI (Otomatik oluşturulur)
# ===========================================
KNOWN_FACES_DIR = get_env("KNOWN_FACES_DIR", "known_faces")
LOGS_DIR = get_env("LOGS_DIR", "logs")
TEMP_DIR = get_env("TEMP_DIR", "temp")

# ===========================================
# SİSTEM AYARLARI
# ===========================================
DETECTION_INTERVAL = get_env("DETECTION_INTERVAL", 1, int)  # Saniye cinsinden tespit aralığı
NOTIFICATION_COOLDOWN = get_env("NOTIFICATION_COOLDOWN", 30, int)  # Saniye cinsinden bildirim soğuma süresi
LOG_LEVEL = get_env("LOG_LEVEL", "INFO")  # DEBUG, INFO, WARNING, ERROR

# ===========================================
# GÖRSEL AYARLAR
# ===========================================
# Renkler (BGR formatında)
GREEN_COLOR = get_env("GREEN_COLOR", (0, 255, 0), tuple)  # Kayıtlı kişi için yeşil
RED_COLOR = get_env("RED_COLOR", (0, 0, 255), tuple)    # Bilinmeyen kişi için kırmızı
BLUE_COLOR = get_env("BLUE_COLOR", (255, 0, 0), tuple)   # Mavi
WHITE_COLOR = get_env("WHITE_COLOR", (255, 255, 255), tuple)

# Font ayarları
FONT = 0  # cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.6
FONT_THICKNESS = 2

# ===========================================
# GELİŞMİŞ AYARLAR
# ===========================================
# Performans ayarları
MAX_FACE_DISTANCE = get_env("MAX_FACE_DISTANCE", 0.6, float)  # Yüz tanıma için maksimum mesafe
RESIZE_FRAME = get_env("RESIZE_FRAME", True, bool)  # Frame'i küçült (performans için)
RESIZE_WIDTH = get_env("RESIZE_WIDTH", 320, int)  # Küçültülmüş frame genişliği

# Güvenlik ayarları
SAVE_UNKNOWN_FACES = get_env("SAVE_UNKNOWN_FACES", True, bool)  # Bilinmeyen yüzlerin fotoğrafını kaydet
MAX_TEMP_FILES = get_env("MAX_TEMP_FILES", 100, int)  # Temp klasöründe maksimum dosya sayısı
AUTO_CLEANUP_DAYS = get_env("AUTO_CLEANUP_DAYS", 7, int)  # Kaç gün sonra temp dosyaları sil

# Bildirim ayarları
SEND_PHOTO_WITH_NOTIFICATION = get_env("SEND_PHOTO_WITH_NOTIFICATION", True, bool)  # Bildirim ile birlikte fotoğraf gönder
NOTIFICATION_SOUND = get_env("NOTIFICATION_SOUND", True, bool)  # Sistem bildirimi sesi
MULTIPLE_FACE_ALERT = get_env("MULTIPLE_FACE_ALERT", True, bool)  # Birden fazla yüz tespitinde uyar
