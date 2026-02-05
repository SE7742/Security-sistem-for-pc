@echo off
chcp 65001 >nul
echo ============================================================
echo PC Güvenlik Sistemi - Test Scripti
echo ============================================================
echo.

echo [1/5] Python versiyonu kontrol ediliyor...
python --version
if errorlevel 1 (
    echo HATA: Python bulunamadı! Lütfen Python yükleyin.
    pause
    exit /b 1
)
echo.

echo [2/5] Bağımlılık versiyonları kontrol ediliyor...
echo.
python -c "import cv2; print('  OpenCV:', cv2.__version__)"
python -c "import numpy; print('  NumPy:', numpy.__version__)"
python -c "import PIL; print('  Pillow:', PIL.__version__)"
python -c "import requests; print('  Requests:', requests.__version__)"
echo.

echo [3/5] config.py kontrol ediliyor...
if not exist "config.py" (
    echo config.py bulunamadı, config.example.py kopyalanıyor...
    copy config.example.py config.py
)
echo config.py mevcut.
echo.

echo [4/5] Modül import testleri...
python -c "from face_database import FaceDatabase; print('  FaceDatabase OK')"
python -c "from telegram_notifier import TelegramNotifier; print('  TelegramNotifier OK')"
python -c "from face_detector import FaceDetector; print('  FaceDetector OK')"
echo.

echo [5/5] Tam sistem testi çalıştırılıyor...
echo.
python test_system.py
echo.

echo ============================================================
echo Test tamamlandı!
echo ============================================================
pause
