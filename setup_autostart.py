# -*- coding: utf-8 -*-
"""
PC Güvenlik Sistemi - Otomatik Başlangıç Kurulumu
Windows başlangıcına hızlı güvenlik taramasını ekler
"""

import os
import sys
import winreg
import shutil
from datetime import datetime

def setup_windows_startup():
    """Windows başlangıcına otomatik güvenlik taramasını ekle"""
    try:
        # Mevcut script konumu
        current_dir = os.path.dirname(os.path.abspath(__file__))
        startup_script = os.path.join(current_dir, "startup_security.bat")
        
        # Registry key'i aç
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        
        # Otomatik başlangıç entry'si ekle
        app_name = "PCSecurityQuickScan"
        command = f'"{startup_script}"'
        
        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
        
        print("✅ Otomatik başlangıç başarıyla kuruldu!")
        print(f"📁 Konum: {startup_script}")
        print("🚀 Artık Windows her açıldığında 5 saniye güvenlik taraması yapılacak")
        print()
        print("📋 Nasıl çalışır:")
        print("1. Windows açılır")
        print("2. 5 saniye güvenlik taraması başlar")
        print("3. Sadece kırmızı (bilinmeyen) kişi varsa fotoğraf + Telegram")
        print("4. Yeşil (kayıtlı) kişi varsa hiçbir şey yapmaz")
        print("5. Tarama biter, sistem kapanır")
        print()
        print("⚠️ Kaldırmak için: python setup_autostart.py --remove")
        
        return True
        
    except Exception as e:
        print(f"❌ Otomatik başlangıç kurulumu başarısız: {e}")
        return False

def remove_windows_startup():
    """Windows başlangıcından otomatik güvenlik taramasını kaldır"""
    try:
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        
        try:
            winreg.DeleteValue(key, "PCSecurityQuickScan")
            print("✅ Otomatik başlangıç başarıyla kaldırıldı!")
        except FileNotFoundError:
            print("ℹ️ Otomatik başlangıç zaten kurulu değil")
        
        winreg.CloseKey(key)
        return True
        
    except Exception as e:
        print(f"❌ Otomatik başlangıç kaldırma başarısız: {e}")
        return False

def test_quick_scan():
    """Hızlı taramayı test et"""
    print("🧪 Hızlı güvenlik taraması test ediliyor...")
    print("⏱️ 5 saniye sürecek, lütfen bekleyin...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "main.py", "--quick-scan"], 
                              capture_output=True, text=True, timeout=30)
        
        print("\n📊 Test Sonucu:")
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print(f"Exit Code: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ Test başarılı - Kayıtlı kişi tespit edildi veya kimse yok")
        elif result.returncode == 1:
            print("🚨 Test başarılı - Bilinmeyen kişi tespit edildi!")
        else:
            print("❌ Test başarısız - Hata oluştu")
            
    except subprocess.TimeoutExpired:
        print("⏰ Test zaman aşımına uğradı")
    except Exception as e:
        print(f"❌ Test hatası: {e}")

def main():
    """Ana fonksiyon"""
    print("=" * 60)
    print("🛡️ PC GÜVENLİK SİSTEMİ - OTOMATİK BAŞLANGIÇ KURULUMU")
    print("=" * 60)
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--remove":
        # Kaldırma modu
        remove_windows_startup()
    elif len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Test modu
        test_quick_scan()
    else:
        # Kurulum modu
        print("Bu script Windows başlangıcına otomatik güvenlik taraması ekler.")
        print()
        
        choice = input("Otomatik başlangıcı kurmak istiyor musunuz? (y/n): ")
        
        if choice.lower() in ['y', 'yes', 'e', 'evet']:
            if setup_windows_startup():
                print("\n🎯 Kurulum tamamlandı!")
                print("\nTest etmek ister misiniz?")
                test_choice = input("Hızlı taramayı test et? (y/n): ")
                
                if test_choice.lower() in ['y', 'yes', 'e', 'evet']:
                    test_quick_scan()
            else:
                print("\n❌ Kurulum başarısız!")
        else:
            print("Kurulum iptal edildi.")

if __name__ == "__main__":
    main()
