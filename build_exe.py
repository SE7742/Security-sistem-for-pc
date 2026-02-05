# -*- coding: utf-8 -*-
"""
PC Güvenlik Sistemi - PyInstaller Build Script
Bu script ile projeyi tek .exe dosyası haline getirebilirsiniz.
"""

import os
import sys
import shutil
import subprocess
from datetime import datetime

def install_pyinstaller():
    """PyInstaller'ı kur"""
    print("📦 PyInstaller kuruluyor...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller kuruldu")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller kurulumu başarısız: {e}")
        return False

def create_spec_file():
    """PyInstaller spec dosyası oluştur"""
    print("📝 Spec dosyası oluşturuluyor...")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.example.py', '.'),
        ('README.md', '.'),
        ('QUICK_START.md', '.'),
        ('known_faces/README.md', 'known_faces/'),
        ('version.json', '.'),
    ],
    hiddenimports=[
        'PIL._tkinter_finder',
        'pkg_resources.py2_warn',
        'cv2',
        'face_recognition',
        'numpy',
        'requests',
        'telegram',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'threading',
        'queue',
        'datetime',
        'json',
        'logging',
        'os',
        'sys',
        'pickle',
        'base64',
        'io'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PC-Security-System',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI modu için False
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  # İkon dosyanız varsa
)
'''
    
    with open('pc_security.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ pc_security.spec oluşturuldu")

def build_exe():
    """EXE dosyasını oluştur"""
    print("🔨 EXE dosyası oluşturuluyor...")
    print("⏰ Bu işlem birkaç dakika sürebilir...")
    
    try:
        # Spec dosyası ile build et
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller", 
            "--clean", 
            "pc_security.spec"
        ])
        
        print("✅ EXE dosyası başarıyla oluşturuldu!")
        print("📁 Dosya konumu: dist/PC-Security-System.exe")
        
        # Dosya boyutunu göster
        exe_path = "dist/PC-Security-System.exe"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"📊 Dosya boyutu: {size_mb:.1f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ EXE oluşturma başarısız: {e}")
        return False

def create_installer_script():
    """Kullanıcı için kurulum scripti oluştur"""
    print("📋 Kullanıcı kurulum scripti oluşturuluyor...")
    
    installer_content = '''@echo off
echo ========================================
echo PC Güvenlik Sistemi - Kurulum
echo ========================================
echo.

REM Klasörleri oluştur
if not exist "known_faces" mkdir known_faces
if not exist "logs" mkdir logs
if not exist "temp" mkdir temp

REM Config dosyasını kopyala
if not exist "config.py" (
    if exist "config.example.py" (
        copy "config.example.py" "config.py"
        echo ✅ config.py oluşturuldu
    )
)

echo.
echo ========================================
echo KURULUM TAMAMLANDI!
echo ========================================
echo.
echo Sonraki adımlar:
echo 1. config.py dosyasını düzenleyin (Telegram ayarları)
echo 2. PC-Security-System.exe dosyasını çalıştırın
echo.
echo Kullanım:
echo - Çift tıklayarak çalıştırın
echo - Veya komut satırından: PC-Security-System.exe
echo.
pause
'''
    
    with open('dist/install.bat', 'w', encoding='utf-8') as f:
        f.write(installer_content)
    
    # Config örneği de kopyala
    if os.path.exists('config.example.py'):
        shutil.copy2('config.example.py', 'dist/')
    
    if os.path.exists('README.md'):
        shutil.copy2('README.md', 'dist/')
    
    if os.path.exists('QUICK_START.md'):
        shutil.copy2('QUICK_START.md', 'dist/')
    
    print("✅ Kurulum scripti oluşturuldu: dist/install.bat")

def create_release_package():
    """Release paketi oluştur"""
    print("📦 Release paketi hazırlanıyor...")
    
    release_dir = f"PC-Security-System-v1.0-{datetime.now().strftime('%Y%m%d')}"
    
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    
    os.makedirs(release_dir)
    
    # Dosyaları kopyala
    files_to_copy = [
        'dist/PC-Security-System.exe',
        'dist/install.bat',
        'dist/config.example.py',
        'dist/README.md',
        'dist/QUICK_START.md'
    ]
    
    for file_path in files_to_copy:
        if os.path.exists(file_path):
            shutil.copy2(file_path, release_dir)
    
    # Klasörleri oluştur
    os.makedirs(f"{release_dir}/known_faces", exist_ok=True)
    os.makedirs(f"{release_dir}/logs", exist_ok=True)
    os.makedirs(f"{release_dir}/temp", exist_ok=True)
    
    # README kopyala
    if os.path.exists('known_faces/README.md'):
        shutil.copy2('known_faces/README.md', f"{release_dir}/known_faces/")
    
    print(f"✅ Release paketi hazır: {release_dir}/")
    print(f"📁 Bu klasörü zip'leyerek dağıtabilirsiniz")

def main():
    """Ana build fonksiyonu"""
    print("=" * 60)
    print("🛡️  PC GÜVENLİK SİSTEMİ - EXE BUILD SCRIPT")
    print("=" * 60)
    print(f"⏰ Build zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. PyInstaller'ı kur
    if not install_pyinstaller():
        return False
    
    # 2. Spec dosyası oluştur
    create_spec_file()
    
    # 3. EXE oluştur
    if not build_exe():
        return False
    
    # 4. Kurulum scripti oluştur
    create_installer_script()
    
    # 5. Release paketi oluştur
    create_release_package()
    
    print("\n" + "=" * 60)
    print("🎉 BUILD TAMAMLANDI!")
    print("=" * 60)
    
    print("\n📋 Oluşturulan Dosyalar:")
    print("- dist/PC-Security-System.exe   : Ana program")
    print("- dist/install.bat              : Kullanıcı kurulum scripti")
    print("- PC-Security-System-v1.0-*/    : Dağıtım paketi")
    
    print("\n🚀 Dağıtım:")
    print("1. Release klasörünü zip'leyin")
    print("2. GitHub Releases'e yükleyin")
    print("3. Kullanıcılar sadece zip'i indirip çalıştıracak!")
    
    print("\n💡 Kullanıcı Deneyimi:")
    print("1. Zip dosyasını indir ve aç")
    print("2. install.bat çalıştır")
    print("3. config.py düzenle")
    print("4. PC-Security-System.exe çalıştır")
    print("5. Bitti! ✅")
    
    return True

if __name__ == "__main__":
    success = main()
    input("\nDevam etmek için Enter tuşuna basın...")
    sys.exit(0 if success else 1)
