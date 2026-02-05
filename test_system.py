# -*- coding: utf-8 -*-
"""
PC Güvenlik Sistemi Test Scripti
Sistem bileşenlerini test eder
"""

import os
import sys
import logging
from datetime import datetime

def test_imports():
    """Gerekli modüllerin import edilebilirliğini test et (Lite Mod)"""
    print("🔍 Import testleri yapılıyor (Lite Mod)...")
    
    try:
        import cv2
        print("✅ OpenCV import edildi")
        
        # OpenCV contrib modülünü kontrol et (LBPH için gerekli)
        if hasattr(cv2, 'face'):
            print("✅ OpenCV face modülü (LBPH) mevcut")
        else:
            print("⚠️ OpenCV face modülü bulunamadı - opencv-contrib-python kurun")
            return False
    except ImportError as e:
        print(f"❌ OpenCV import hatası: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy import edildi")
    except ImportError as e:
        print(f"❌ NumPy import hatası: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests import edildi")
    except ImportError as e:
        print(f"❌ Requests import hatası: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow import edildi")
    except ImportError as e:
        print(f"❌ Pillow import hatası: {e}")
        return False
    
    try:
        import tkinter as tk
        print("✅ Tkinter import edildi")
    except ImportError as e:
        print(f"❌ Tkinter import hatası: {e}")
        return False
    
    return True

def test_camera():
    """Kamera erişimini test et"""
    print("\n📹 Kamera testi yapılıyor...")
    
    try:
        import cv2
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Kamera açılamadı")
            return False
        
        ret, frame = cap.read()
        
        if not ret:
            print("❌ Kameradan görüntü alınamadı")
            cap.release()
            return False
        
        height, width = frame.shape[:2]
        print(f"✅ Kamera başarılı - Çözünürlük: {width}x{height}")
        
        cap.release()
        return True
        
    except Exception as e:
        print(f"❌ Kamera test hatası: {e}")
        return False

def test_face_detection():
    """Yüz tespit fonksiyonunu test et (Lite Mod - OpenCV Haar Cascade)"""
    print("\n👤 Yüz tespit testi yapılıyor (Lite Mod)...")
    
    try:
        import cv2
        import numpy as np
        
        # Haar Cascade yükle
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        if face_cascade.empty():
            print("❌ Haar Cascade yüklenemedi")
            return False
        
        print("✅ Haar Cascade yüklendi")
        
        # Test görüntüsü oluştur (basit bir yüz benzeri pattern)
        test_image = np.zeros((200, 200, 3), dtype=np.uint8)
        cv2.circle(test_image, (100, 100), 80, (255, 255, 255), -1)  # Yüz
        cv2.circle(test_image, (80, 80), 10, (0, 0, 0), -1)   # Sol göz
        cv2.circle(test_image, (120, 80), 10, (0, 0, 0), -1)  # Sağ göz
        cv2.ellipse(test_image, (100, 120), (20, 10), 0, 0, 180, (0, 0, 0), 2)  # Ağız
        
        # Gri tonlamaya çevir
        gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        
        # Yüz tespit dene
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        print(f"✅ Yüz tespit fonksiyonu çalışıyor")
        print(f"   Test görüntüsünde {len(faces)} yüz tespit edildi")
        
        # LBPH tanıyıcıyı test et
        if hasattr(cv2, 'face'):
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            print("✅ LBPH yüz tanıyıcı oluşturulabilir")
        else:
            print("⚠️ LBPH yüz tanıyıcı mevcut değil")
        
        return True
        
    except Exception as e:
        print(f"❌ Yüz tespit test hatası: {e}")
        return False

def test_directories():
    """Gerekli klasörlerin varlığını test et"""
    print("\n📁 Klasör yapısı testi yapılıyor...")
    
    required_dirs = ['known_faces', 'logs', 'temp']
    all_exist = True
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name} klasörü mevcut")
        else:
            print(f"❌ {dir_name} klasörü bulunamadı")
            all_exist = False
    
    return all_exist

def test_config():
    """Konfigürasyon dosyasını test et"""
    print("\n⚙️  Konfigürasyon testi yapılıyor...")
    
    try:
        import config
        
        # Temel ayarların varlığını kontrol et
        required_attrs = [
            'TELEGRAM_BOT_TOKEN', 'CHAT_ID', 'CAMERA_INDEX',
            'FRAME_WIDTH', 'FRAME_HEIGHT', 'FACE_RECOGNITION_TOLERANCE'
        ]
        
        missing_attrs = []
        for attr in required_attrs:
            if not hasattr(config, attr):
                missing_attrs.append(attr)
        
        if missing_attrs:
            print(f"❌ Eksik konfigürasyon: {', '.join(missing_attrs)}")
            return False
        
        print("✅ Konfigürasyon dosyası geçerli")
        
        # Telegram ayarlarını kontrol et
        if config.TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            print("⚠️  Telegram bot token ayarlanmamış")
        else:
            print("✅ Telegram bot token ayarlanmış")
        
        if config.CHAT_ID == "YOUR_CHAT_ID_HERE":
            print("⚠️  Telegram chat ID ayarlanmamış")
        else:
            print("✅ Telegram chat ID ayarlanmış")
        
        return True
        
    except ImportError as e:
        print(f"❌ Config import hatası: {e}")
        return False
    except Exception as e:
        print(f"❌ Config test hatası: {e}")
        return False

def test_local_modules():
    """Yerel modülleri test et"""
    print("\n🧩 Yerel modül testleri yapılıyor...")
    
    modules = [
        ('face_database', 'FaceDatabase'),
        ('telegram_notifier', 'TelegramNotifier'),
        ('face_detector', 'FaceDetector')
    ]
    
    all_ok = True
    
    for module_name, class_name in modules:
        try:
            module = __import__(module_name)
            cls = getattr(module, class_name)
            print(f"✅ {module_name}.{class_name} import edildi")
        except ImportError as e:
            print(f"❌ {module_name} import hatası: {e}")
            all_ok = False
        except AttributeError as e:
            print(f"❌ {module_name}.{class_name} bulunamadı: {e}")
            all_ok = False
        except Exception as e:
            print(f"❌ {module_name} test hatası: {e}")
            all_ok = False
    
    return all_ok

def main():
    """Ana test fonksiyonu"""
    print("=" * 50)
    print("🛡️  PC GÜVENLİK SİSTEMİ TEST SCRIPTI")
    print("=" * 50)
    print(f"⏰ Test zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Python Modül İmportları", test_imports),
        ("Kamera Erişimi", test_camera),
        ("Yüz Tespit Fonksiyonu", test_face_detection),
        ("Klasör Yapısı", test_directories),
        ("Konfigürasyon", test_config),
        ("Yerel Modüller", test_local_modules)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔬 {test_name} testi başlatılıyor...")
        print("-" * 40)
        
        try:
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name} testi BAŞARILI")
            else:
                print(f"❌ {test_name} testi BAŞARISIZ")
                
        except Exception as e:
            print(f"💥 {test_name} testi HATA: {e}")
            results.append((test_name, False))
    
    # Sonuç özeti
    print("\n" + "=" * 50)
    print("📊 TEST SONUÇLARI")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ BAŞARILI" if result else "❌ BAŞARISIZ"
        print(f"{test_name:.<30} {status}")
    
    print("-" * 50)
    print(f"Toplam: {passed}/{total} test başarılı")
    
    if passed == total:
        print("\n🎉 TÜM TESTLER BAŞARILI!")
        print("Sistem kurulumu tamamlanmış ve çalışmaya hazır.")
        print("\nSonraki adımlar:")
        print("1. config.py dosyasında Telegram ayarlarını yapın")
        print("2. known_faces/ klasörüne kayıtlı kişi fotoğrafları ekleyin")
        print("3. python main.py komutu ile programı çalıştırın")
    else:
        print(f"\n⚠️  {total - passed} TEST BAŞARISIZ!")
        print("Lütfen başarısız testlerdeki sorunları çözün.")
        print("Yardım için README.md dosyasını kontrol edin.")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
