# -*- coding: utf-8 -*-
"""
PC Güvenlik Sistemi - İlk Kurulum Scripti
GitHub'dan indirdikten sonra çalıştırılacak kurulum scripti
"""

import os
import sys
import shutil
import json
from datetime import datetime

def create_directories():
    """Gerekli klasörleri oluştur"""
    directories = ['known_faces', 'logs', 'temp']
    
    print("📁 Klasörler oluşturuluyor...")
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ {directory}/ klasörü oluşturuldu")
        else:
            print(f"ℹ️  {directory}/ klasörü zaten mevcut")

def setup_config():
    """Config dosyasını ayarla"""
    print("\n⚙️  Konfigürasyon dosyası ayarlanıyor...")
    
    if os.path.exists('config.py'):
        print("ℹ️  config.py zaten mevcut, atlanıyor...")
        return
    
    if not os.path.exists('config.example.py'):
        print("❌ config.example.py bulunamadı!")
        return False
    
    # Örnek dosyayı kopyala
    shutil.copy2('config.example.py', 'config.py')
    print("✅ config.py oluşturuldu (config.example.py'den)")
    
    print("\n🔧 Şimdi config.py dosyasını düzenlemeniz gerekiyor:")
    print("   1. Telegram bot token'ınızı girin")
    print("   2. Chat ID'nizi girin")
    print("   3. Diğer ayarları isteğe göre değiştirin")
    
    return True

def create_gitignore():
    """GitHub için .gitignore oluştur"""
    print("\n📝 .gitignore dosyası oluşturuluyor...")
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Kişisel ayarlar
config.py
*.pkl

# Kullanıcı verileri
known_faces/
logs/
temp/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Geçici dosyalar
*.tmp
*.temp
*.log

# Güvenlik
*.key
*.pem
*.crt
"""
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print("✅ .gitignore oluşturuldu")

def create_user_data_template():
    """Kullanıcı için örnek veri şablonu oluştur"""
    print("\n👤 Kullanıcı veri şablonu oluşturuluyor...")
    
    # known_faces klasörüne README ekle
    readme_content = """# Kayıtlı Kişi Fotoğrafları

Bu klasöre kendi fotoğraflarınızı ve güvenilir kişilerin fotoğraflarını ekleyin.

## 📸 Fotoğraf Gereksinimleri:

- **Format**: JPG, JPEG, PNG
- **Kalite**: Net ve yüksek çözünürlüklü
- **Yüz**: Tek kişi, yüz net görünür
- **Aydınlatma**: İyi aydınlatılmış
- **Boyut**: Minimum 200x200 piksel

## 📝 Dosya Adlandırma:

- Dosya adı = Kişinin ismi
- Örnek: `ahmet.jpg`, `ayse.png`, `mehmet_bey.jpg`
- Türkçe karakter kullanabilirsiniz

## 🔄 Fotoğraf Ekleme Yöntemleri:

### Yöntem 1: Manuel Ekleme
1. Fotoğrafı bu klasöre kopyalayın
2. İsme göre yeniden adlandırın
3. Programı yeniden başlatın

### Yöntem 2: Program İle Ekleme
1. `python main.py --add-person` komutunu çalıştırın
2. Kameraya bakarak fotoğraf çektirin
3. İsim girin

### Yöntem 3: GUI İle Ekleme
1. `python main.py` ile programı açın
2. "Kişi Yönetimi" sekmesine gidin
3. "Yeni Kişi Ekle" butonunu kullanın

## ⚠️ Önemli Notlar:

- Bu klasör GitHub'a yüklenmez (.gitignore ile korunur)
- Kişisel verileriniz sadece kendi bilgisayarınızda kalır
- Düzenli yedekleme yapmanız önerilir
"""
    
    with open('known_faces/README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ known_faces/README.md oluşturuldu")

def create_quick_start_guide():
    """Hızlı başlangıç rehberi oluştur"""
    print("\n📖 Hızlı başlangıç rehberi oluşturuluyor...")
    
    guide_content = """# 🚀 Hızlı Başlangıç Rehberi

Bu rehber, PC Güvenlik Sistemi'ni ilk kez kuranlar içindir.

## 1️⃣ İlk Kurulum (Sadece Bir Kez)

### Python Kurulumu
```bash
# Python yüklü mü kontrol et
python --version

# Yoksa python.org'dan indirin
```

### Bağımlılıkları Kur
```bash
# Windows için otomatik kurulum
install.bat

# Manuel kurulum
pip install -r requirements.txt
```

### Kurulumu Test Et
```bash
python test_system.py
```

## 2️⃣ Telegram Bot Kurulumu

### Bot Oluştur
1. Telegram'da @BotFather ile konuşun
2. `/newbot` komutu ile bot oluşturun
3. Bot adı ve kullanıcı adı verin
4. Token'ı kopyalayın

### Chat ID Öğren
1. @userinfobot ile konuşun
2. Chat ID'nizi kopyalayın

### Config Ayarla
1. `config.py` dosyasını açın
2. Token ve Chat ID'yi yapıştırın
3. Dosyayı kaydedin

## 3️⃣ İlk Kişiyi Ekle

### Seçenek A: Kamera ile
```bash
python main.py --add-person
```

### Seçenek B: Dosya ile
1. Fotoğrafı `known_faces/` klasörüne koyun
2. `isim.jpg` formatında adlandırın

## 4️⃣ Sistemi Başlat

### GUI Modu (Önerilen)
```bash
python main.py
```

### Sessiz Mod
```bash
python main.py --silent
```

## 5️⃣ Otomatik Başlangıç (Opsiyonel)

1. GUI'yi açın: `python main.py`
2. "Ayarlar" sekmesine gidin
3. "Otomatik başlangıç" seçeneğini işaretleyin
4. "Ayarla" butonuna tıklayın

## 🆘 Sorun Giderme

### Kamera Açılmıyor
- Kamera başka program tarafından kullanılıyor olabilir
- `config.py`'de `CAMERA_INDEX = 1` deneyin

### Yüz Tanınmıyor
- Fotoğraf kalitesini kontrol edin
- Daha fazla fotoğraf ekleyin
- `FACE_RECOGNITION_TOLERANCE` değerini artırın

### Telegram Çalışmıyor
- Token ve Chat ID'yi kontrol edin
- Bot'un aktif olduğundan emin olun
- Internet bağlantısını kontrol edin

## 📞 Yardım

- Detaylı bilgi: `README.md`
- Test araçları: `python test_system.py`
- GitHub Issues: Sorun bildirimi için
"""
    
    with open('QUICK_START.md', 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("✅ QUICK_START.md oluşturuldu")

def create_version_info():
    """Sürüm bilgisi oluştur"""
    version_info = {
        "version": "1.0.0",
        "release_date": datetime.now().strftime("%Y-%m-%d"),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "features": [
            "Real-time face detection",
            "Face recognition with OpenCV",
            "Telegram notifications",
            "GUI interface",
            "Auto-startup support",
            "Multi-user support"
        ],
        "requirements": {
            "python": ">=3.8",
            "opencv-python": "4.8.1.78",
            "face-recognition": "1.3.0",
            "numpy": "1.24.3"
        }
    }
    
    with open('version.json', 'w', encoding='utf-8') as f:
        json.dump(version_info, f, indent=4, ensure_ascii=False)
    
    print("✅ version.json oluşturuldu")

def main():
    """Ana kurulum fonksiyonu"""
    print("=" * 60)
    print("🛡️  PC GÜVENLİK SİSTEMİ - İLK KURULUM")
    print("=" * 60)
    print(f"⏰ Kurulum zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # 1. Klasörleri oluştur
        create_directories()
        
        # 2. Config ayarla
        setup_config()
        
        # 3. .gitignore oluştur
        create_gitignore()
        
        # 4. Kullanıcı şablonları oluştur
        create_user_data_template()
        
        # 5. Hızlı rehber oluştur
        create_quick_start_guide()
        
        # 6. Sürüm bilgisi oluştur
        create_version_info()
        
        print("\n" + "=" * 60)
        print("🎉 KURULUM TAMAMLANDI!")
        print("=" * 60)
        
        print("\n📋 Sonraki Adımlar:")
        print("1. 📝 config.py dosyasını düzenleyin")
        print("2. 🤖 Telegram bot kurulumu yapın (QUICK_START.md)")
        print("3. 👤 İlk kişiyi ekleyin: python main.py --add-person")
        print("4. 🚀 Sistemi başlatın: python main.py")
        
        print("\n📖 Yardım Dosyaları:")
        print("- QUICK_START.md : Hızlı başlangıç rehberi")
        print("- README.md      : Detaylı kullanım kılavuzu")
        print("- known_faces/README.md : Fotoğraf ekleme rehberi")
        
        print("\n🧪 Sistem Testi:")
        print("python test_system.py")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ Kurulum hatası: {e}")
        print("Lütfen hata mesajını kontrol edin ve tekrar deneyin.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    input("\nDevam etmek için Enter tuşuna basın...")
    sys.exit(0 if success else 1)
