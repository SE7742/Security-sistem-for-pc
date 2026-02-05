@echo off
echo ========================================
echo PC Guvenlik Sistemi - EXE Olusturucu
echo ========================================
echo.

REM Python kontrolü
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo HATA: Python bulunamadi!
    echo Lutfen Python 3.8+ surumunu yukleyin: https://python.org
    pause
    exit /b 1
)

echo Python bulundu.
echo.

REM Build script'i çalıştır
echo EXE dosyasi olusturuluyor...
echo Bu islem 5-10 dakika surebilir...
echo.

python build_exe.py

echo.
echo ========================================
echo BUILD TAMAMLANDI!
echo ========================================
echo.
echo Olusturulan dosyalar:
echo - dist\PC-Security-System.exe
echo - Release klasoru (zip'lemek icin)
echo.
pause
