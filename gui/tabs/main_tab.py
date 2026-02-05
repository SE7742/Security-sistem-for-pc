# -*- coding: utf-8 -*-
"""
PC Güvenlik Sistemi - Ana Kontrol Sekmesi
"""

import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import time
import threading
import logging
from datetime import datetime
from PIL import Image, ImageTk

from .base_tab import BaseTab
from ..constants import COLORS, FONTS, CAMERA_DISPLAY_WIDTH, QUICK_SCAN_DURATION


class MainTab(BaseTab):
    """Ana kontrol sekmesi"""
    
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.setup_ui()
        self.add_to_notebook("🏠 Ana Kontrol")
    
    def setup_ui(self):
        """Ana kontrol sekmesi arayüzünü oluştur"""
        # Header bölümü
        header_frame = tk.Frame(self.frame, bg=COLORS['primary'], height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Başlık ve logo alanı
        title_container = tk.Frame(header_frame, bg=COLORS['primary'])
        title_container.pack(expand=True, fill='both')
        
        title_label = tk.Label(title_container, 
                              text="🛡️ PC GÜVENLİK SİSTEMİ", 
                              font=FONTS['title'],
                              bg=COLORS['primary'], fg='white')
        title_label.pack(pady=25)
        
        # Ana içerik container
        content_frame = ttk.Frame(self.frame)
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Durum kartları (3 kolonlu)
        status_container = ttk.Frame(content_frame)
        status_container.pack(fill='x', pady=(0, 20))
        
        # Sistem durumu kartı
        self.status_card_label = self._create_status_card(
            status_container, "🔴 Sistem Durumu", "Sistem Hazır", 0)
        
        # Kayıtlı kişi kartı  
        self.known_faces_card_label = self._create_status_card(
            status_container, "👥 Kayıtlı Kişiler", "0 kişi", 1)
        
        # Son tespit kartı
        self.last_detection_card_label = self._create_status_card(
            status_container, "📸 Son Tespit", "Henüz tespit yok", 2)
        
        # Ana kontrol butonları
        control_frame = ttk.LabelFrame(content_frame, text="🎮 Sistem Kontrolü")
        control_frame.pack(fill='x', pady=(0, 20))
        
        button_container = ttk.Frame(control_frame)
        button_container.pack(pady=20)
        
        self.start_button = ttk.Button(button_container, 
                                      text="🚀 İzlemeyi Başlat", 
                                      command=self.app.start_monitoring,
                                      style='Success.TButton')
        self.start_button.pack(side='left', padx=10)
        
        self.stop_button = ttk.Button(button_container, 
                                     text="⏹️ İzlemeyi Durdur", 
                                     command=self.app.stop_monitoring,
                                     style='Danger.TButton',
                                     state='disabled')
        self.stop_button.pack(side='left', padx=10)
        
        # İki kolonlu layout
        dual_column = ttk.Frame(content_frame)
        dual_column.pack(fill='both', expand=True)
        
        # Sol kolon: Test butonları
        left_column = ttk.Frame(dual_column)
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        test_frame = ttk.LabelFrame(left_column, text="🧪 Test İşlemleri")
        test_frame.pack(fill='x', pady=(0, 10))
        
        test_button_container = ttk.Frame(test_frame)
        test_button_container.pack(pady=15)
        
        ttk.Button(test_button_container, text="📹 Kamera Testi", 
                  command=self.test_camera,
                  style='Accent.TButton').pack(pady=5, fill='x')
        
        ttk.Button(test_button_container, text="📱 Telegram Testi", 
                  command=self.test_telegram,
                  style='Accent.TButton').pack(pady=5, fill='x')
        
        ttk.Button(test_button_container, text="📸 Telegram Fotoğraf Testi", 
                  command=self.test_telegram_photo,
                  style='Accent.TButton').pack(pady=5, fill='x')
        
        ttk.Button(test_button_container, text=f"⚡ {QUICK_SCAN_DURATION} Saniye Hızlı Tarama", 
                  command=self.run_quick_scan_test,
                  style='Warning.TButton').pack(pady=5, fill='x')
        
        # Sağ kolon: Kamera görüntüsü
        right_column = ttk.Frame(dual_column)
        right_column.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        camera_frame = ttk.LabelFrame(right_column, text="📹 Canlı Kamera Görüntüsü")
        camera_frame.pack(fill='both', expand=True)
        
        # Kamera container
        camera_container = tk.Frame(camera_frame, bg='black')
        camera_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.camera_label = tk.Label(camera_container, 
                                    text="🔌 Kamera Kapalı\n\n'İzlemeyi Başlat' butonuna tıklayın", 
                                    bg='black', fg='white',
                                    font=FONTS['heading'],
                                    justify='center')
        self.camera_label.pack(expand=True)
        
        # Bilgi alanı
        info_frame = ttk.LabelFrame(self.frame, text="Sistem Bilgileri")
        info_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.info_text = tk.Text(info_frame, height=6, wrap='word')
        scrollbar = ttk.Scrollbar(info_frame, orient='vertical', command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        
        self.info_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def _create_status_card(self, parent, title, value, column):
        """Modern durum kartı oluştur"""
        card_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        card_frame.grid(row=0, column=column, padx=10, pady=10, sticky='ew')
        
        # Grid ağırlıkları
        parent.grid_columnconfigure(column, weight=1)
        
        # Kart içeriği
        title_label = tk.Label(card_frame, 
                              text=title,
                              font=FONTS['body_bold'],
                              bg='white', fg=COLORS['primary'])
        title_label.pack(pady=(15, 5))
        
        value_label = tk.Label(card_frame,
                              text=value, 
                              font=FONTS['heading'],
                              bg='white', fg=COLORS['secondary'])
        value_label.pack(pady=(0, 15))
        
        return value_label
    
    def test_camera(self):
        """Kamera testi"""
        from config import CAMERA_INDEX
        try:
            cap = cv2.VideoCapture(CAMERA_INDEX)
            
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    messagebox.showinfo("Kamera Testi", "✅ Kamera başarıyla test edildi!")
                else:
                    messagebox.showerror("Kamera Testi", "❌ Kameradan görüntü alınamadı!")
            else:
                messagebox.showerror("Kamera Testi", "❌ Kamera açılamadı!")
            
            cap.release()
            
        except Exception as e:
            messagebox.showerror("Kamera Testi", f"❌ Kamera testi hatası: {str(e)}")
    
    def test_telegram(self):
        """Telegram testi"""
        if self.telegram.test_connection():
            messagebox.showinfo("Telegram Testi", "✅ Telegram bağlantısı başarılı!")
        else:
            messagebox.showerror("Telegram Testi", "❌ Telegram bağlantısı başarısız!")
    
    def test_telegram_photo(self):
        """Telegram fotoğraf testi"""
        try:
            # Önce ayarları kontrol et
            if not self.telegram.bot_token or self.telegram.bot_token.strip() == "":
                messagebox.showerror("Telegram Ayarları", 
                                   "❌ Telegram bot token ayarlanmamış!\n\n"
                                   "Lütfen 'Ayarlar' sekmesinden Telegram bot token'ını girin.")
                return
            
            if not self.telegram.chat_id or self.telegram.chat_id.strip() == "":
                messagebox.showerror("Telegram Ayarları", 
                                   "❌ Telegram chat ID ayarlanmamış!\n\n"
                                   "Lütfen 'Ayarlar' sekmesinden Telegram chat ID'yi girin.")
                return
            
            result = messagebox.askyesno(
                "Telegram Fotoğraf Testi",
                "Telegram'a test fotoğrafı gönderilecek.\n\n"
                "Bu test fotoğraf gönderme işlevinin çalışıp çalışmadığını kontrol eder.\n\n"
                "Devam etmek istiyor musunuz?"
            )
            
            if result:
                if self.telegram.test_photo_sending():
                    messagebox.showinfo("Telegram Fotoğraf Testi", 
                                      "✅ Telegram fotoğraf testi başarılı!\n\n"
                                      "Test fotoğrafı Telegram'a gönderildi.\n"
                                      "Telegram'ınızı kontrol edin.")
                else:
                    messagebox.showerror("Telegram Fotoğraf Testi", 
                                       "❌ Telegram fotoğraf testi başarısız!\n\n"
                                       "Logları kontrol edin veya ayarları gözden geçirin.")
        except Exception as e:
            messagebox.showerror("Hata", f"❌ Test hatası: {str(e)}")
    
    def run_quick_scan_test(self):
        """Hızlı tarama testi (GUI'den)"""
        try:
            # Kullanıcıya bilgi ver
            result = messagebox.askyesno(
                "Hızlı Güvenlik Taraması",
                f"{QUICK_SCAN_DURATION} saniye hızlı güvenlik taraması başlatılacak.\n\n"
                "Bu test Windows açılışında yapılan otomatik taramayı simüle eder.\n\n"
                "Devam etmek istiyor musunuz?"
            )
            
            if not result:
                return
            
            # Ana pencereyi gizle
            self.app.root.withdraw()
            
            # Bilgi penceresi
            info_window = tk.Toplevel()
            info_window.title("⚡ Hızlı Tarama")
            info_window.geometry("500x300")
            info_window.resizable(False, False)
            
            # Merkeze al
            x = (info_window.winfo_screenwidth() - 500) // 2
            y = (info_window.winfo_screenheight() - 300) // 2
            info_window.geometry(f"500x300+{x}+{y}")
            
            # İçerik
            tk.Label(info_window, text="⚡ Hızlı Güvenlik Taraması",
                    font=FONTS['subtitle']).pack(pady=20)
            
            status_label = tk.Label(info_window, text="Başlatılıyor...",
                                   font=FONTS['body'])
            status_label.pack(pady=10)
            
            progress_label = tk.Label(info_window, text=f"0/{QUICK_SCAN_DURATION} saniye",
                                     font=FONTS['small'])
            progress_label.pack(pady=5)
            
            # İptal butonu
            def cancel_scan():
                info_window.destroy()
                self.app.root.deiconify()
            
            tk.Button(info_window, text="❌ İptal", 
                     command=cancel_scan).pack(pady=10)
            
            # Taramayı thread'de çalıştır
            def run_scan():
                try:
                    from face_detector import FaceDetector
                    detector = FaceDetector()
                    
                    # Progress güncellemesi için callback
                    def update_progress(elapsed, total):
                        info_window.after(0, lambda: status_label.config(text=f"Tarama devam ediyor..."))
                        info_window.after(0, lambda: progress_label.config(text=f"{elapsed:.1f}/{total} saniye"))
                    
                    # Tarama süresi boyunca progress güncelle
                    start_time = time.time()
                    
                    while time.time() - start_time < QUICK_SCAN_DURATION:
                        elapsed = time.time() - start_time
                        update_progress(elapsed, QUICK_SCAN_DURATION)
                        time.sleep(0.1)
                    
                    # Gerçek hızlı tarama çalıştır
                    result = detector.run_quick_scan(QUICK_SCAN_DURATION)
                    
                    # Sonuç göster
                    info_window.after(0, lambda: self._show_scan_result(result, info_window))
                    
                except Exception as e:
                    info_window.after(0, lambda: messagebox.showerror("Hata", f"Tarama hatası: {e}"))
                    info_window.after(0, lambda: cancel_scan())
            
            # Thread başlat
            scan_thread = threading.Thread(target=run_scan, daemon=True)
            scan_thread.start()
            
        except Exception as e:
            messagebox.showerror("Hata", f"❌ Hızlı tarama başlatılamadı: {str(e)}")
            self.app.root.deiconify()
    
    def _show_scan_result(self, unknown_detected, info_window):
        """Tarama sonucunu göster"""
        from config import TEMP_DIR
        from pathlib import Path
        
        try:
            info_window.destroy()
            
            if unknown_detected:
                # Önce Telegram'a bildirim gönder
                self._send_telegram_alert_for_scan()
                
                # Bilinmeyen kişi tespit edildi - Daha detaylı uyarı
                result_window = tk.Toplevel()
                result_window.title("🚨 Güvenlik Uyarısı!")
                result_window.geometry("600x400")
                result_window.resizable(False, False)
                
                # Merkeze al
                x = (result_window.winfo_screenwidth() - 600) // 2
                y = (result_window.winfo_screenheight() - 400) // 2
                result_window.geometry(f"600x400+{x}+{y}")
                
                # Başlık
                tk.Label(result_window, text="🚨 GÜVENLİK UYARISI! 🚨",
                        font=FONTS['subtitle'], fg='red').pack(pady=20)
                
                # Ana mesaj
                main_text = """BİLİNMEYEN KİŞİ TESPİT EDİLDİ!

📸 Fotoğraf kaydedildi
📱 Telegram bildirimi gönderildi  
📋 Log kaydı oluşturuldu

⚠️ Bu durum güvenlik riski oluşturabilir.
Lütfen durumu kontrol edin."""
                
                tk.Label(result_window, text=main_text,
                        font=FONTS['body'], justify='left').pack(pady=20, padx=20)
                
                # Bilgi kutusu
                info_frame = tk.Frame(result_window, bg='#FFF3CD', relief='solid', borderwidth=1)
                info_frame.pack(pady=20, padx=20, fill='x')
                
                tk.Label(info_frame, text="💡 Bilgi:",
                        font=FONTS['body_bold'], bg='#FFF3CD').pack(pady=(10, 5))
                
                tk.Label(info_frame, text="Tespit edilen fotoğrafları 'Tespit Edilen Fotoğraflar' sekmesinden görüntüleyebilirsiniz.",
                        font=FONTS['small'], bg='#FFF3CD', wraplength=500).pack(pady=(0, 10))
                
                # Butonlar
                button_frame = tk.Frame(result_window)
                button_frame.pack(pady=20)
                
                def close_and_continue():
                    result_window.destroy()
                    self.app.root.deiconify()
                
                tk.Button(button_frame, text="✅ Anladım", 
                         command=close_and_continue,
                         font=FONTS['body_bold'],
                         bg='#28A745', fg='white',
                         padx=20, pady=10).pack(side='left', padx=10)
                
                # 10 saniye sonra otomatik kapat
                result_window.after(10000, close_and_continue)
                
            else:
                # Güvenlik sorunu yok - Kısa mesaj
                messagebox.showinfo(
                    "✅ Güvenlik Taraması Tamamlandı",
                    "Güvenlik taraması başarıyla tamamlandı.\n\n"
                    "• Kayıtlı kişiler tespit edildi\n"
                    "• Bilinmeyen kişi bulunamadı\n"
                    "• Sistem güvenli\n\n"
                    "Bu Windows açılışında otomatik olarak yapılan taramadır."
                )
                self.app.root.deiconify()
        
        except Exception as e:
            messagebox.showerror("Hata", f"Sonuç gösterme hatası: {e}")
            self.app.root.deiconify()
    
    def _send_telegram_alert_for_scan(self):
        """Hızlı tarama sonucu için Telegram bildirimi gönder"""
        from config import TEMP_DIR
        from pathlib import Path
        
        try:
            temp_dir = Path(TEMP_DIR)
            
            if temp_dir.exists():
                # En son tespit dosyasını bul
                detection_files = list(temp_dir.glob("unknown_*faces_*.jpg"))
                if detection_files:
                    # En yeni dosyayı al
                    latest_file = max(detection_files, key=lambda x: x.stat().st_mtime)
                    
                    # Telegram'a bildirim gönder
                    success = self.telegram.notify_unknown_person(str(latest_file), skip_cooldown=True)
                    
                    if success:
                        logging.info("✅ Hızlı tarama Telegram bildirimi gönderildi")
                    else:
                        logging.error("❌ Hızlı tarama Telegram bildirimi başarısız")
                else:
                    logging.warning("⚠️ Tespit edilen fotoğraf bulunamadı")
            else:
                logging.warning("⚠️ Temp klasörü bulunamadı")
                
        except Exception as e:
            logging.error(f"❌ Telegram bildirim hatası: {e}")
    
    def update_info(self, message):
        """Bilgi alanını güncelle"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.info_text.insert(tk.END, formatted_message)
        self.info_text.see(tk.END)
        
        # Maksimum 1000 satır tut
        from .base_tab import BaseTab
        from ..constants import MAX_LOG_LINES
        lines = int(self.info_text.index('end-1c').split('.')[0])
        if lines > MAX_LOG_LINES:
            self.info_text.delete(1.0, f"{lines-MAX_LOG_LINES}.0")
