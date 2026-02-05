# -*- coding: utf-8 -*-
"""
PC Güvenlik Sistemi - GUI Sabitleri
Tüm magic number'lar ve UI sabitleri burada tanımlanır
"""

# Pencere boyutları
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

# Kamera görüntü boyutları
CAMERA_DISPLAY_WIDTH = 320

# Thumbnail boyutları
PERSON_THUMBNAIL_SIZE = (200, 200)
DETECTION_THUMBNAIL_SIZE = (300, 300)

# Zamanlama (milisaniye)
STATUS_UPDATE_INTERVAL = 1000  # 1 saniye
AUTO_CLOSE_ALERT_TIMEOUT = 10000  # 10 saniye

# Hızlı tarama
QUICK_SCAN_DURATION = 8  # saniye

# Log sınırları
MAX_LOG_LINES = 1000

# Yüz tanıma
FACE_RECOGNITION_CONFIDENCE_THRESHOLD = 80
CONSECUTIVE_UNKNOWN_FRAMES = 10
MAX_PHOTOS_PER_DAY = 3

# Renkler (GUI için)
COLORS = {
    'primary': '#2C3E50',      # Koyu mavi-gri (güvenlik)
    'secondary': '#34495E',    # Orta gri  
    'accent': '#3498DB',       # Mavi (vurgu)
    'success': '#27AE60',      # Yeşil (başarılı)
    'warning': '#F39C12',      # Turuncu (uyarı)
    'danger': '#E74C3C',       # Kırmızı (tehlike)
    'light': '#ECF0F1',        # Açık gri
    'white': '#FFFFFF',        # Beyaz
    'dark': '#2C3E50',         # Koyu
    'text': '#2C3E50',         # Metin rengi
    'bg': '#F8F9FA'            # Arka plan
}

# Fontlar
FONTS = {
    'title': ('Segoe UI', 18, 'bold'),
    'subtitle': ('Segoe UI', 14, 'bold'),
    'heading': ('Segoe UI', 12, 'bold'),
    'body': ('Segoe UI', 10),
    'body_bold': ('Segoe UI', 10, 'bold'),
    'small': ('Segoe UI', 9),
    'small_bold': ('Segoe UI', 9, 'bold'),
}
