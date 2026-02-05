# -*- coding: utf-8 -*-
"""
Telegram Entegrasyonu Test Scripti
"""

import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_notifier import TelegramNotifier
from config import TELEGRAM_BOT_TOKEN, CHAT_ID

def test_basic_connection():
    """Temel bağlantı testi"""
    print("🔍 Telegram bağlantısı test ediliyor...")
    
    notifier = TelegramNotifier()
    
    if notifier.test_connection():
        print("✅ Telegram bağlantısı başarılı!")
        return True
    else:
        print("❌ Telegram bağlantısı başarısız!")
        return False

def test_simple_message():
    """Basit mesaj gönderme testi"""
    print("\n📤 Test mesajı gönderiliyor...")
    
    notifier = TelegramNotifier()
    
    message = "🧪 Test Mesajı\n\nPC Güvenlik Sistemi Telegram entegrasyonu test ediliyor.\n\nTarih: " + str(datetime.now())
    
    success = notifier.send_message(message)
    
    if success:
        print("✅ Test mesajı başarıyla gönderildi!")
        print("📱 Telegram'ınızı kontrol edin")
        return True
    else:
        print("❌ Test mesajı gönderilemedi!")
        return False

def test_unknown_person_notification():
    """Bilinmeyen kişi bildirimi testi"""
    print("\n🚨 Bilinmeyen kişi bildirimi test ediliyor...")
    
    notifier = TelegramNotifier()
    
    # Test için sahte bir fotoğraf yolu (gerçek dosya olmasa da çalışır)
    test_image_path = "test_detection.jpg"
    
    # Test görüntüsü oluştur
    import cv2
    import numpy as np
    
    # Basit test görüntüsü oluştur
    test_image = np.zeros((300, 400, 3), dtype=np.uint8)
    cv2.putText(test_image, "TEST DETECTION", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(test_image, "Unknown Person Alert", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
    cv2.imwrite(test_image_path, test_image)
    
    # Bildirim gönder
    success = notifier.notify_unknown_person(test_image_path)
    
    # Test dosyasını sil
    if os.path.exists(test_image_path):
        os.remove(test_image_path)
    
    if success:
        print("✅ Bilinmeyen kişi bildirimi başarıyla gönderildi!")
        print("📱 Telegram'ınızda fotoğraflı uyarı mesajını göreceksiniz")
        return True
    else:
        print("❌ Bilinmeyen kişi bildirimi gönderilemedi!")
        return False

def test_system_start_notification():
    """Sistem başlangıç bildirimi testi"""
    print("\n🚀 Sistem başlangıç bildirimi test ediliyor...")
    
    notifier = TelegramNotifier()
    success = notifier.notify_system_start()
    
    if success:
        print("✅ Sistem başlangıç bildirimi gönderildi!")
        return True
    else:
        print("❌ Sistem başlangıç bildirimi gönderilemedi!")
        return False

def main():
    """Ana test fonksiyonu"""
    print("=" * 60)
    print("🤖 TELEGRAM ENTEGRASYONİ TEST SÜİTİ")
    print("=" * 60)
    print(f"⏰ Test zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("📋 Mevcut ayarlar:")
    print(f"  🤖 Bot Token: {TELEGRAM_BOT_TOKEN[:20]}..." if TELEGRAM_BOT_TOKEN != "YOUR_BOT_TOKEN_HERE" else "  ❌ Bot Token ayarlanmamış!")
    print(f"  💬 Chat ID: {CHAT_ID}" if CHAT_ID != "YOUR_CHAT_ID_HERE" else "  ❌ Chat ID ayarlanmamış!")
    print()
    
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("❌ Telegram ayarları yapılmamış!")
        print("Lütfen önce config.py dosyasında TELEGRAM_BOT_TOKEN ve CHAT_ID ayarlayın.")
        return
    
    tests = [
        ("Temel Bağlantı", test_basic_connection),
        ("Basit Mesaj", test_simple_message),
        ("Sistem Başlangıcı", test_system_start_notification),
        ("Bilinmeyen Kişi Uyarısı", test_unknown_person_notification),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"🧪 Test: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test hatası: {e}")
            results.append((test_name, False))
        print("-" * 40)
    
    # Sonuçlar
    print("\n" + "=" * 60)
    print("📊 TEST SONUÇLARI")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ BAŞARILI" if result else "❌ BAŞARISIZ"
        print(f"{test_name:<25} : {status}")
        if result:
            passed += 1
    
    total = len(results)
    print(f"\n📈 Toplam: {passed}/{total} test başarılı ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 Tüm testler başarılı! Telegram entegrasyonu çalışıyor.")
        print("✅ Artık güvenle sistemi kullanabilirsiniz.")
    elif passed > 0:
        print(f"\n⚠️ {total-passed} test başarısız. Bazı özellikler çalışmayabilir.")
        print("🔧 Ayarlarınızı kontrol edin ve tekrar deneyin.")
    else:
        print("\n❌ Hiçbir test başarılı değil. Telegram entegrasyonu çalışmıyor.")
        print("🔧 Bot token ve chat ID'yi kontrol edin.")

if __name__ == "__main__":
    main()
