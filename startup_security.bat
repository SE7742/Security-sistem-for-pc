@echo off
REM PC Güvenlik Sistemi - Otomatik Başlangıç Scripti
REM Bu script Windows başlangıcında otomatik çalışır

REM Script konumuna git
cd /d "%~dp0"

REM Log dosyası
set LOG_FILE=logs\startup_%date:~6,4%%date:~3,2%%date:~0,2%.log

REM Başlangıç log'u
echo [%date% %time%] Otomatik güvenlik taraması başlatılıyor... >> %LOG_FILE%

REM Hızlı güvenlik taraması çalıştır (8 saniye)
python main.py --quick-scan --scan-duration 8

REM Sonuç kodu kontrol et
if %errorlevel% equ 1 (
    echo [%date% %time%] UYARI: Bilinmeyen kişi tespit edildi! >> %LOG_FILE%
) else (
    echo [%date% %time%] Güvenlik taraması tamamlandı - Sorun yok >> %LOG_FILE%
)

REM Script tamamlandı
echo [%date% %time%] Otomatik güvenlik taraması tamamlandı >> %LOG_FILE%

REM Pencereyi kapat
exit /b 0
