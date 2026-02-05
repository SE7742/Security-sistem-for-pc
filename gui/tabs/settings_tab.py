# -*- coding: utf-8 -*-
"""
PC Güvenlik Sistemi - Ayarlar Sekmesi
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
import os
import re

from .base_tab import BaseTab
from ..constants import COLORS, FONTS


class SettingsTab(BaseTab):
    """Ayarlar sekmesi"""
    
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.setup_ui()
        self.add_to_notebook("⚙️ Ayarlar")
    
    def setup_ui(self):
        """Ayarlar sekmesi arayüzünü oluştur"""
        from config import TELEGRAM_BOT_TOKEN, CHAT_ID, CAMERA_INDEX
        
        # Telegram ayarları
        telegram_frame = ttk.LabelFrame(self.frame, text="📱 Telegram Bot Ayarları")
        telegram_frame.pack(fill='x', padx=20, pady=10)
        
        # Grid konfigürasyonu
        telegram_frame.grid_columnconfigure(1, weight=1)
        
        # Bot Token
        ttk.Label(telegram_frame, text="🤖 Bot Token:", 
                 font=FONTS['body_bold']).grid(row=0, column=0, sticky='w', padx=15, pady=10)
        self.token_entry = ttk.Entry(telegram_frame, width=50, show='*')
        self.token_entry.grid(row=0, column=1, padx=15, pady=10, sticky='ew')
        self.token_entry.insert(0, TELEGRAM_BOT_TOKEN)
        
        # Chat ID
        ttk.Label(telegram_frame, text="💬 Chat ID:", 
                 font=FONTS['body_bold']).grid(row=1, column=0, sticky='w', padx=15, pady=10)
        self.chat_id_entry = ttk.Entry(telegram_frame, width=50)
        self.chat_id_entry.grid(row=1, column=1, padx=15, pady=10, sticky='ew')
        self.chat_id_entry.insert(0, CHAT_ID)
        
        # Buton frame'i
        button_frame = ttk.Frame(telegram_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        ttk.Button(button_frame, text="💾 Ayarları Kaydet", 
                  command=self.save_telegram_settings,
                  style='Success.TButton').pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="🗑️ Ayarları Temizle", 
                  command=self.clear_telegram_settings,
                  style='Warning.TButton').pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="🧪 Telegram Testi", 
                  command=self._test_telegram,
                  style='Accent.TButton').pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="📸 Fotoğraf Testi", 
                  command=self._test_telegram_photo,
                  style='Accent.TButton').pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="📁 Klasör Kontrolü", 
                  command=self.check_known_faces_folder,
                  style='Accent.TButton').pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="🚀 Otomatik Başlangıç Testi", 
                  command=self.test_auto_start,
                  style='Accent.TButton').pack(side='left', padx=5)
        
        # Kamera ayarları
        camera_frame = ttk.LabelFrame(self.frame, text="Kamera Ayarları")
        camera_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(camera_frame, text="Kamera İndeksi:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.camera_index_var = tk.StringVar(value=str(CAMERA_INDEX))
        ttk.Entry(camera_frame, textvariable=self.camera_index_var, width=10).grid(row=0, column=1, padx=5, pady=5)
        
        # Otomatik başlangıç
        startup_frame = ttk.LabelFrame(self.frame, text="Otomatik Başlangıç")
        startup_frame.pack(fill='x', padx=20, pady=10)
        
        self.auto_start_var = tk.BooleanVar()
        ttk.Checkbutton(startup_frame, text="Windows başlangıcında otomatik çalıştır", 
                       variable=self.auto_start_var).pack(padx=5, pady=5)
        
        ttk.Button(startup_frame, text="Otomatik Başlangıcı Ayarla", 
                  command=self.setup_auto_start).pack(pady=5)
    
    def _test_telegram(self):
        """Telegram testi"""
        if self.telegram.test_connection():
            messagebox.showinfo("Telegram Testi", "✅ Telegram bağlantısı başarılı!")
        else:
            messagebox.showerror("Telegram Testi", "❌ Telegram bağlantısı başarısız!")
    
    def _test_telegram_photo(self):
        """Telegram fotoğraf testi"""
        try:
            if not self.telegram.bot_token or self.telegram.bot_token.strip() == "":
                messagebox.showerror("Telegram Ayarları", 
                                   "❌ Telegram bot token ayarlanmamış!")
                return
            
            if not self.telegram.chat_id or self.telegram.chat_id.strip() == "":
                messagebox.showerror("Telegram Ayarları", 
                                   "❌ Telegram chat ID ayarlanmamış!")
                return
            
            result = messagebox.askyesno(
                "Telegram Fotoğraf Testi",
                "Telegram'a test fotoğrafı gönderilecek.\n\nDevam etmek istiyor musunuz?"
            )
            
            if result:
                if self.telegram.test_photo_sending():
                    messagebox.showinfo("Telegram Fotoğraf Testi", 
                                      "✅ Telegram fotoğraf testi başarılı!")
                else:
                    messagebox.showerror("Telegram Fotoğraf Testi", 
                                       "❌ Telegram fotoğraf testi başarısız!")
        except Exception as e:
            messagebox.showerror("Hata", f"❌ Test hatası: {str(e)}")
    
    def check_known_faces_folder(self):
        """Known faces klasörünü kontrol et"""
        from config import KNOWN_FACES_DIR
        from pathlib import Path
        
        try:
            known_faces_dir = Path(KNOWN_FACES_DIR)
            
            if not known_faces_dir.exists():
                messagebox.showwarning("Klasör Kontrolü", 
                    f"❌ Klasör bulunamadı: {KNOWN_FACES_DIR}\n\n"
                    f"Klasör otomatik olarak oluşturulacak.")
                known_faces_dir.mkdir(exist_ok=True)
                return
            
            # Klasördeki dosyaları listele
            image_files = []
            other_files = []
            
            for file in known_faces_dir.glob("*"):
                if file.is_file():
                    if file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
                        image_files.append(file.name)
                    else:
                        other_files.append(file.name)
            
            # Sonuç mesajı
            message = f"📁 Klasör: {KNOWN_FACES_DIR}\n\n"
            message += f"📸 Resim dosyaları ({len(image_files)}):\n"
            
            if image_files:
                for img in image_files[:10]:  # İlk 10 dosyayı göster
                    message += f"  • {img}\n"
                if len(image_files) > 10:
                    message += f"  ... ve {len(image_files) - 10} dosya daha\n"
            else:
                message += "  (Hiç resim dosyası yok)\n"
            
            if other_files:
                message += f"\n📄 Diğer dosyalar ({len(other_files)}):\n"
                for other in other_files:
                    message += f"  • {other}\n"
            
            messagebox.showinfo("Klasör Kontrolü", message)
            
        except Exception as e:
            messagebox.showerror("Hata", f"❌ Klasör kontrolü hatası: {str(e)}")
    
    def test_auto_start(self):
        """Otomatik başlangıç testi"""
        try:
            import winreg
            
            # Registry'yi kontrol et
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            
            try:
                # PCSecurityQuickScan entry'sini kontrol et
                value, _ = winreg.QueryValueEx(key, "PCSecurityQuickScan")
                
                # startup_security.bat dosyasının varlığını kontrol et
                current_dir = os.path.dirname(os.path.abspath(__file__))
                project_dir = os.path.dirname(os.path.dirname(current_dir))
                startup_script = os.path.join(project_dir, "startup_security.bat")
                
                if os.path.exists(startup_script):
                    messagebox.showinfo("Otomatik Başlangıç Testi", 
                        "✅ Otomatik başlangıç AKTİF!\n\n"
                        f"📁 Script: {startup_script}\n"
                        f"🔧 Registry: {value}\n\n"
                        "🚀 Windows her açıldığında 8 saniye güvenlik taraması yapılacak")
                else:
                    messagebox.showwarning("Otomatik Başlangıç Testi", 
                        "⚠️ Registry'de kayıtlı ama script dosyası bulunamadı!\n\n"
                        f"📁 Aranan: {startup_script}\n"
                        f"🔧 Registry: {value}")
                
            except FileNotFoundError:
                messagebox.showinfo("Otomatik Başlangıç Testi", 
                    "ℹ️ Otomatik başlangıç PASİF\n\n"
                    "Windows açılışında güvenlik taraması yapılmayacak")
            
            winreg.CloseKey(key)
            
        except Exception as e:
            messagebox.showerror("Hata", f"❌ Otomatik başlangıç testi hatası: {str(e)}")
    
    def save_telegram_settings(self):
        """Telegram ayarlarını kalıcı olarak kaydet"""
        try:
            new_token = self.token_entry.get().strip()
            new_chat_id = self.chat_id_entry.get().strip()
            
            if not new_token or new_token == "YOUR_BOT_TOKEN_HERE":
                messagebox.showerror("Hata", "❌ Geçerli bir bot token girin!")
                return
            
            if not new_chat_id or new_chat_id == "YOUR_CHAT_ID_HERE":
                messagebox.showerror("Hata", "❌ Geçerli bir chat ID girin!")
                return
            
            # config.py dosyasını güncelle
            self._update_config_file(new_token, new_chat_id)
            
            # Telegram nesnesini güncelle
            self.telegram.bot_token = new_token
            self.telegram.chat_id = new_chat_id
            self.telegram.base_url = f"https://api.telegram.org/bot{new_token}"
            
            messagebox.showinfo("Ayarlar", "✅ Telegram ayarları kalıcı olarak kaydedildi!\n\nYeni ayarlar config.py dosyasına yazıldı.")
            logging.info("Telegram ayarları güncellendi")
            
        except Exception as e:
            messagebox.showerror("Hata", f"❌ Ayar kaydetme hatası: {str(e)}")
            logging.error(f"Telegram ayar kaydetme hatası: {e}")
    
    def _update_config_file(self, new_token, new_chat_id):
        """config.py dosyasını güncelle"""
        try:
            # config.py dosyasını oku
            with open('config.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Token güncelle
            token_pattern = r'TELEGRAM_BOT_TOKEN\s*=\s*["\'][^"\']*["\']'
            new_token_line = f'TELEGRAM_BOT_TOKEN = "{new_token}"'
            content = re.sub(token_pattern, new_token_line, content)
            
            # Chat ID güncelle  
            chat_pattern = r'CHAT_ID\s*=\s*["\'][^"\']*["\']'
            new_chat_line = f'CHAT_ID = "{new_chat_id}"'
            content = re.sub(chat_pattern, new_chat_line, content)
            
            # Dosyayı yaz
            with open('config.py', 'w', encoding='utf-8') as f:
                f.write(content)
            
            logging.info("config.py dosyası güncellendi")
            
        except Exception as e:
            raise Exception(f"Config dosyası güncellenemedi: {e}")
    
    def clear_telegram_settings(self):
        """Telegram ayarlarını temizle"""
        try:
            result = messagebox.askyesno(
                "Ayarları Temizle",
                "Telegram ayarlarını temizlemek istediğinizden emin misiniz?\n\n"
                "Bu işlem bot token ve chat ID'yi siler."
            )
            
            if result:
                # Entry'leri temizle
                self.token_entry.delete(0, tk.END)
                self.token_entry.insert(0, "")
                
                self.chat_id_entry.delete(0, tk.END)
                self.chat_id_entry.insert(0, "")
                
                # Config dosyasını güncelle
                self._update_config_file("", "")
                
                # Telegram nesnesini güncelle
                self.telegram.bot_token = ""
                self.telegram.chat_id = ""
                self.telegram.base_url = f"https://api.telegram.org/bot"
                
                messagebox.showinfo("Ayarlar", "✅ Telegram ayarları temizlendi!")
                logging.info("Telegram ayarları temizlendi")
                
        except Exception as e:
            messagebox.showerror("Hata", f"❌ Ayar temizleme hatası: {str(e)}")
            logging.error(f"Telegram ayar temizleme hatası: {e}")
    
    def load_current_settings(self):
        """Mevcut ayarları GUI'ye yükle"""
        from config import TELEGRAM_BOT_TOKEN, CHAT_ID
        
        try:
            # Token entry'yi güncelle
            self.token_entry.delete(0, tk.END)
            if TELEGRAM_BOT_TOKEN and TELEGRAM_BOT_TOKEN != "YOUR_BOT_TOKEN_HERE":
                self.token_entry.insert(0, TELEGRAM_BOT_TOKEN)
            else:
                self.token_entry.insert(0, "")
            
            # Chat ID entry'yi güncelle  
            self.chat_id_entry.delete(0, tk.END)
            if CHAT_ID and CHAT_ID != "YOUR_CHAT_ID_HERE":
                self.chat_id_entry.insert(0, CHAT_ID)
            else:
                self.chat_id_entry.insert(0, "")
            
            # Otomatik başlangıç durumunu kontrol et
            self.check_auto_start_status()
                
        except Exception as e:
            logging.error(f"Ayar yükleme hatası: {e}")
    
    def check_auto_start_status(self):
        """Otomatik başlangıç durumunu kontrol et ve GUI'yi güncelle"""
        try:
            import winreg
            
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            
            try:
                # PCSecurityQuickScan entry'sini kontrol et
                winreg.QueryValueEx(key, "PCSecurityQuickScan")
                # Eğer buraya kadar geldiyse, otomatik başlangıç aktif
                self.auto_start_var.set(True)
            except FileNotFoundError:
                # Entry bulunamadı, otomatik başlangıç pasif
                self.auto_start_var.set(False)
            
            winreg.CloseKey(key)
            
        except Exception as e:
            # Hata durumunda pasif olarak ayarla
            self.auto_start_var.set(False)
            logging.error(f"Otomatik başlangıç durumu kontrol hatası: {e}")
    
    def setup_auto_start(self):
        """Otomatik başlangıcı ayarla"""
        if self.auto_start_var.get():
            self._enable_auto_start()
        else:
            self._disable_auto_start()
    
    def _enable_auto_start(self):
        """Otomatik başlangıcı etkinleştir"""
        try:
            import winreg
            
            # Mevcut script konumu
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_dir = os.path.dirname(os.path.dirname(current_dir))
            startup_script = os.path.join(project_dir, "startup_security.bat")
            
            # startup_security.bat dosyasının varlığını kontrol et
            if not os.path.exists(startup_script):
                messagebox.showerror("Hata", f"❌ startup_security.bat dosyası bulunamadı!\n\nKonum: {startup_script}")
                return
            
            # Registry key'i aç
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            
            # Otomatik başlangıç entry'si ekle
            app_name = "PCSecurityQuickScan"
            command = f'"{startup_script}"'
            
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, command)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Otomatik Başlangıç", 
                "✅ Otomatik başlangıç etkinleştirildi!\n\n"
                "🚀 Artık Windows her açıldığında 8 saniye güvenlik taraması yapılacak\n"
                "📁 Script: startup_security.bat\n"
                "⏱️ Süre: 8 saniye hızlı tarama")
            
            logging.warning("🚀 Windows otomatik başlangıç etkinleştirildi")
            
        except Exception as e:
            messagebox.showerror("Hata", f"❌ Otomatik başlangıç ayarlanamadı: {str(e)}")
            logging.error(f"Otomatik başlangıç hatası: {e}")
    
    def _disable_auto_start(self):
        """Otomatik başlangıcı devre dışı bırak"""
        try:
            import winreg
            
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            
            try:
                winreg.DeleteValue(key, "PCSecurityQuickScan")
                messagebox.showinfo("Otomatik Başlangıç", "✅ Otomatik başlangıç devre dışı bırakıldı!")
                logging.warning("⏹️ Windows otomatik başlangıç devre dışı bırakıldı")
            except FileNotFoundError:
                messagebox.showinfo("Otomatik Başlangıç", "ℹ️ Otomatik başlangıç zaten kurulu değil")
            
            winreg.CloseKey(key)
            
        except Exception as e:
            messagebox.showerror("Hata", f"❌ Otomatik başlangıç ayarı değiştirilemedi: {str(e)}")
            logging.error(f"Otomatik başlangıç kaldırma hatası: {e}")
