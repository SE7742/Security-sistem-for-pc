@echo off
echo ========================================
echo PC Guvenlik Sistemi Kurulum Scripti
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

REM Pip güncellemesi
echo Pip guncelleniyor...
python -m pip install --upgrade pip

REM Bağımlılıkları kur
echo.
echo Bagimliliklar yukleniyor...
echo Bu islem birkaç dakika surebilir...
echo.

pip install opencv-python==4.8.1.78
if %errorlevel% neq 0 goto error

pip install face-recognition==1.3.0
if %errorlevel% neq 0 goto error

pip install numpy==1.24.3
if %errorlevel% neq 0 goto error

pip install Pillow==10.0.1
if %errorlevel% neq 0 goto error

pip install requests==2.31.0
if %errorlevel% neq 0 goto error

pip install python-telegram-bot==20.6
if %errorlevel% neq 0 goto error

echo.
echo dlib kuruluyor... (Bu uzun surebilir)
pip install dlib==19.24.2
if %errorlevel% neq 0 (
    echo.
    echo UYARI: dlib kurulumunda sorun yasandi.
    echo Visual Studio Build Tools gerekebilir.
    echo Indirme linki: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo.
    echo Yine de devam etmek istiyor musunuz? (y/n)
    set /p choice=
    if /i "%choice%" neq "y" goto error
)

pip install cmake==3.27.7
if %errorlevel% neq 0 goto error

REM Klasörleri oluştur
echo.
echo Klasorler olusturuluyor...
if not exist "known_faces" mkdir known_faces
if not exist "logs" mkdir logs
if not exist "temp" mkdir temp

echo.
echo ========================================
echo KURULUM TAMAMLANDI!
echo ========================================
echo.
echo Sonraki adimlar:
echo 1. config.py dosyasini duzenleyin (Telegram ayarlari)
echo 2. python main.py komutu ile programi calistirin
echo 3. Ilk kayitli kisileri ekleyin
echo.
echo Kullanim:
echo - GUI modu:          python main.py
echo - Sessiz mod:        python main.py --silent
echo - Kisi ekleme:       python main.py --add-person
echo.
echo Detayli bilgi icin README.md dosyasini okuyun.
echo.
pause
exit /b 0

:error
echo.
echo ========================================
echo KURULUM HATASI!
echo ========================================
echo.
echo Kurulum sirasinda hata olustu.
echo Lutfen hata mesajlarini kontrol edin.
echo.
echo Yardim icin:
echo - README.md dosyasini okuyun
echo - GitHub Issues bolumunu kontrol edin
echo.
pause
exit /b 1
