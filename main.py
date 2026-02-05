# -*- coding: utf-8 -*-
"""
PC Güvenlik Sistemi - Ana Uygulama
Yüz tanıma ile güvenlik sistemi

Özellikler:
- Gerçek zamanlı yüz tespiti
- Kayıtlı yüz tanıma
- Telegram bildirimleri
- Otomatik başlangıç
"""

import sys
import os
import logging
import argparse
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Pillow uyumluluk katmanı (9.1.0 öncesi sürümler için)
try:
    LANCZOS = Image.Resampling.LANCZOS
except AttributeError:
    LANCZOS = Image.LANCZOS

import threading
import cv2
import time

# Yerel modüller
from face_detector import FaceDetector
from face_database import FaceDatabase
from telegram_notifier import TelegramNotifier
from config import *

# GUI modülleri
from gui.constants import WINDOW_WIDTH, WINDOW_HEIGHT, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT, COLORS, FONTS, STATUS_UPDATE_INTERVAL
from gui.theme import setup_professional_theme
from gui.tabs import MainTab, PersonManagementTab, SettingsTab, DetectionsTab, LogTab

# Logging ayarları
def setup_logging():
    """Logging sistemini kur"""
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
    
    # Eski logları temizle (7 günden eski)
    cleanup_old_logs()
    
    log_filename = os.path.join(LOGS_DIR, f"security_{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def cleanup_old_logs():
    """Eski log dosyalarını temizle (7 günden eski)"""
    try:
        import glob
        from datetime import timedelta
        
        # 7 gün önceki tarih
        cutoff_date = datetime.now() - timedelta(days=7)
        
        # Log dosyalarını bul
        log_pattern = os.path.join(LOGS_DIR, "security_*.log")
        log_files = glob.glob(log_pattern)
        
        deleted_count = 0
        for log_file in log_files:
            try:
                # Dosya tarihini al
                file_time = datetime.fromtimestamp(os.path.getmtime(log_file))
                
                # Eski dosyaları sil
                if file_time < cutoff_date:
                    os.remove(log_file)
                    deleted_count += 1
                    
            except (OSError, IOError):
                continue  # Hata durumunda devam et
        
        if deleted_count > 0:
            print(f"🗑️ {deleted_count} eski log dosyası temizlendi")
            
    except (OSError, IOError):
        pass  # Hata durumunda sessizce devam et


class SecuritySystemGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🛡️ PC Güvenlik Sistemi v1.1")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(True, True)
        self.root.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        
        # Pencere ikonunu ayarla (varsa)
        try:
            self.root.iconbitmap('icon.ico')
        except (FileNotFoundError, tk.TclError):
            pass  # İkon dosyası yoksa geç
        
        # Pencereyi merkeze al
        self.center_window()
        
        # Sistem bileşenleri
        self.face_detector = FaceDetector()
        self.face_db = FaceDatabase()
        self.telegram = TelegramNotifier()
        
        # GUI durumu
        self.is_monitoring = False
        self.monitoring_thread = None
        
        # Tema ve stil
        self.style, self.listbox_config = setup_professional_theme(self.root)
        
        # GUI'yi kur
        self.setup_gui()
        self.load_current_settings()
        self.update_status()
    
    def center_window(self):
        """Pencereyi ekranın ortasına konumlandır"""
        self.root.update_idletasks()
        
        # Ekran boyutunu al
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Merkez koordinatları hesapla
        x = (screen_width - WINDOW_WIDTH) // 2
        y = (screen_height - WINDOW_HEIGHT) // 2
        
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}')
    
    def setup_gui(self):
        """GUI arayüzünü oluştur"""
        # Notebook (sekmeler)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Sekmeleri oluştur
        self.main_tab = MainTab(notebook, self)
        self.person_tab = PersonManagementTab(notebook, self)
        self.settings_tab = SettingsTab(notebook, self)
        self.detections_tab = DetectionsTab(notebook, self)
        self.log_tab = LogTab(notebook, self)
    
    def start_monitoring(self):
        """İzlemeyi başlat"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.main_tab.start_button.config(state='disabled')
            self.main_tab.stop_button.config(state='normal')
            
            # İzleme thread'ini başlat
            self.monitoring_thread = threading.Thread(target=self._monitoring_worker, daemon=True)
            self.monitoring_thread.start()
            
            self.main_tab.update_info("İzleme başlatıldı...")
            logging.warning("🚀 Güvenlik sistemi izleme başlatıldı")
    
    def stop_monitoring(self):
        """İzlemeyi durdur"""
        if self.is_monitoring:
            self.is_monitoring = False
            self.face_detector.is_running = False
            
            self.main_tab.start_button.config(state='normal')
            self.main_tab.stop_button.config(state='disabled')
            
            # Kamera görüntüsünü temizle
            self.main_tab.camera_label.configure(
                image="", 
                text="🔌 Kamera Kapalı\n\n'İzlemeyi Başlat' butonuna tıklayın",
                bg='black', fg='white'
            )
            self.main_tab.camera_label.image = None
            
            self.main_tab.update_info("İzleme durduruldu...")
            logging.warning("⏹️ Güvenlik sistemi izleme durduruldu")
    
    def _monitoring_worker(self):
        """İzleme worker thread'i"""
        try:
            # Kamera görüntüsü güncellemesi için callback ekle
            self.face_detector.set_frame_callback(self._update_camera_display)
            self.face_detector.run_detection()
        except Exception as e:
            logging.error(f"İzleme hatası: {str(e)}")
            self.root.after(0, lambda: self.main_tab.update_info(f"İzleme hatası: {str(e)}"))
        finally:
            self.root.after(0, self.stop_monitoring)
    
    def _update_camera_display(self, frame):
        """Kamera görüntüsünü GUI'de güncelle"""
        from gui.constants import CAMERA_DISPLAY_WIDTH
        
        try:
            height, width = frame.shape[:2]
            new_width = CAMERA_DISPLAY_WIDTH
            new_height = int(height * new_width / width)
            
            resized_frame = cv2.resize(frame, (new_width, new_height))
            rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            
            # PIL Image'e çevir
            pil_image = Image.fromarray(rgb_frame)
            photo = ImageTk.PhotoImage(pil_image)
            
            # GUI'yi güncelle (main thread'de)
            self.root.after(0, lambda: self._update_camera_label(photo))
            
        except Exception as e:
            logging.error(f"Kamera görüntüsü güncelleme hatası: {e}")
    
    def _update_camera_label(self, photo):
        """Kamera label'ını güncelle (main thread'de)"""
        self.main_tab.camera_label.configure(image=photo, text="")
        self.main_tab.camera_label.image = photo  # Referansı tut
    
    def load_current_settings(self):
        """Mevcut ayarları GUI'ye yükle"""
        self.settings_tab.load_current_settings()
    
    def update_status(self):
        """Durumu güncelle (Modern kartlar)"""
        try:
            # Kayıtlı kişi sayısı
            known_count = self.face_db.get_known_faces_count()
            self.main_tab.known_faces_card_label.config(text=f"{known_count} kişi kayıtlı")
            
            # Sistem durumu
            if self.is_monitoring:
                self.main_tab.status_card_label.config(text="🔴 İzleme Aktif", fg=COLORS['danger'])
            else:
                self.main_tab.status_card_label.config(text="🟢 Sistem Hazır", fg=COLORS['success'])
            
            # Son tespit (temp klasöründen)
            try:
                from pathlib import Path
                temp_dir = Path(TEMP_DIR)
                if temp_dir.exists():
                    detection_files = list(temp_dir.glob("unknown_*faces_*.jpg"))
                    if detection_files:
                        latest_file = max(detection_files, key=lambda x: x.stat().st_mtime)
                        file_time = datetime.fromtimestamp(latest_file.stat().st_mtime)
                        time_str = file_time.strftime("%H:%M")
                        self.main_tab.last_detection_card_label.config(text=f"Son tespit: {time_str}")
                    else:
                        self.main_tab.last_detection_card_label.config(text="Henüz tespit yok")
                else:
                    self.main_tab.last_detection_card_label.config(text="Henüz tespit yok")
            except (OSError, IOError):
                self.main_tab.last_detection_card_label.config(text="Henüz tespit yok")
            
        except Exception as e:
            logging.error(f"Status güncelleme hatası: {e}")
        
        # Periyodik güncelleme
        self.root.after(STATUS_UPDATE_INTERVAL, self.update_status)
    
    def on_closing(self):
        """Pencere kapatılırken"""
        if self.is_monitoring:
            if messagebox.askokcancel("Çıkış", "İzleme aktif. Yine de çıkmak istiyor musunuz?"):
                self.stop_monitoring()
                self.root.after(1000, self.root.destroy)
        else:
            self.root.destroy()
    
    def run(self):
        """GUI'yi çalıştır"""
        self.person_tab.refresh_person_list()
        self.detections_tab.refresh_detections_list()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


def main():
    """Ana fonksiyon"""
    parser = argparse.ArgumentParser(description='PC Güvenlik Sistemi')
    parser.add_argument('--silent', action='store_true', help='Sessiz mod (GUI olmadan)')
    parser.add_argument('--add-person', action='store_true', help='Yeni kişi ekleme modu')
    parser.add_argument('--quick-scan', action='store_true', help='Hızlı güvenlik taraması (8 saniye)')
    parser.add_argument('--scan-duration', type=int, default=8, help='Tarama süresi (saniye)')
    
    args = parser.parse_args()
    
    # Logging'i kur
    setup_logging()
    
    logging.info("PC Güvenlik Sistemi başlatılıyor...")
    
    try:
        if args.add_person:
            # Sadece kişi ekleme modu
            detector = FaceDetector()
            detector.add_known_person_interactive()
            
        elif args.quick_scan:
            # Hızlı güvenlik taraması modu
            detector = FaceDetector()
            result = detector.run_quick_scan(args.scan_duration)
            
            # Sonucu döndür (Windows Task Scheduler için)
            sys.exit(1 if result else 0)
            
        elif args.silent:
            # Sessiz mod - sadece tespit
            detector = FaceDetector()
            detector.run_detection()
            
        else:
            # GUI modu
            app = SecuritySystemGUI()
            app.run()
            
    except KeyboardInterrupt:
        logging.info("Program kullanıcı tarafından durduruldu")
    except Exception as e:
        logging.error(f"Program hatası: {str(e)}")
        messagebox.showerror("Hata", f"Program hatası: {str(e)}")
    
    logging.info("PC Güvenlik Sistemi kapatıldı")


if __name__ == "__main__":
    main()
