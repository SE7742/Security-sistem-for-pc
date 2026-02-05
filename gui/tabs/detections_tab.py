# -*- coding: utf-8 -*-
"""
PC Güvenlik Sistemi - Tespit Edilen Fotoğraflar Sekmesi
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
import os
import subprocess
from datetime import datetime
from PIL import Image, ImageTk

from .base_tab import BaseTab
from ..constants import COLORS, FONTS, DETECTION_THUMBNAIL_SIZE

# Pillow uyumluluk
try:
    LANCZOS = Image.Resampling.LANCZOS
except AttributeError:
    LANCZOS = Image.LANCZOS


class DetectionsTab(BaseTab):
    """Tespit edilen fotoğraflar sekmesi"""
    
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.setup_ui()
        self.add_to_notebook("📸 Tespit Edilen Fotoğraflar")
    
    def setup_ui(self):
        """Tespit edilen fotoğraflar sekmesi arayüzünü oluştur"""
        # Ana container
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Sol taraf: Fotoğraf listesi
        list_frame = ttk.LabelFrame(main_container, text="Bilinmeyen Kişi Tespitleri")
        list_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Listbox ve scrollbar
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.detections_listbox = tk.Listbox(list_container, **self.listbox_config)
        detections_scrollbar = ttk.Scrollbar(list_container, orient='vertical', 
                                           command=self.detections_listbox.yview)
        self.detections_listbox.configure(yscrollcommand=detections_scrollbar.set)
        
        # Listbox'a seçim eventi ekle
        self.detections_listbox.bind('<<ListboxSelect>>', self.on_detection_select)
        
        self.detections_listbox.pack(side='left', fill='both', expand=True)
        detections_scrollbar.pack(side='right', fill='y')
        
        # Sağ taraf: Fotoğraf önizleme
        detection_photo_frame = ttk.LabelFrame(main_container, text="Tespit Fotoğrafı")
        detection_photo_frame.pack(side='right', fill='y', padx=(10, 0))
        
        # Fotoğraf label'ı
        self.detection_photo_label = ttk.Label(detection_photo_frame, text="Bir tespit seçin", 
                                              background='lightgray', width=30)
        self.detection_photo_label.pack(padx=10, pady=10)
        
        # Fotoğraf bilgileri
        self.detection_info_label = ttk.Label(detection_photo_frame, text="", wraplength=250)
        self.detection_info_label.pack(padx=10, pady=(0, 10))
        
        # Butonlar
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(button_frame, text="🔄 Listeyi Yenile", 
                  command=self.refresh_detections_list).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="🗑️ Seçili Fotoğrafı Sil", 
                  command=self.delete_selected_detection,
                  style='Danger.TButton').pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="🧹 Tüm Fotoğrafları Temizle", 
                  command=self.clear_all_detections,
                  style='Warning.TButton').pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="📁 Klasörü Aç", 
                  command=self.open_temp_folder,
                  style='Accent.TButton').pack(side='left', padx=5)
    
    def refresh_detections_list(self):
        """Tespit listesini yenile"""
        from config import TEMP_DIR
        from pathlib import Path
        
        self.detections_listbox.delete(0, tk.END)
        
        try:
            temp_dir = Path(TEMP_DIR)
            
            if temp_dir.exists():
                # Tespit dosyalarını bul (tarih sırasına göre)
                detection_files = []
                for file in temp_dir.glob("unknown_*faces_*.jpg"):
                    detection_files.append(file)
                
                # Tarih sırasına göre sırala (yeni önce)
                detection_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                
                for file in detection_files:
                    # Dosya adından bilgi çıkar
                    name = file.stem
                    parts = name.split('_')
                    
                    if len(parts) >= 3:
                        face_count = parts[1].replace('faces', '')
                        timestamp = parts[2] + '_' + parts[3] if len(parts) > 3 else parts[2]
                        
                        # Tarihi okunabilir hale getir
                        try:
                            dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                            readable_date = dt.strftime("%d.%m.%Y %H:%M:%S")
                        except ValueError:
                            readable_date = timestamp
                        
                        display_text = f"{readable_date} - {face_count} bilinmeyen kişi"
                    else:
                        display_text = file.name
                    
                    self.detections_listbox.insert(tk.END, display_text)
                    
        except Exception as e:
            logging.error(f"Tespit listesi yenileme hatası: {e}")
    
    def on_detection_select(self, event):
        """Tespit seçildiğinde fotoğrafını göster"""
        from config import TEMP_DIR
        from pathlib import Path
        
        try:
            selection = self.detections_listbox.curselection()
            
            if not selection:
                self.clear_detection_preview()
                return
            
            # Seçili indeksi al
            selected_index = selection[0]
            
            # Dosya listesini tekrar al (aynı sırayla)
            temp_dir = Path(TEMP_DIR)
            
            detection_files = []
            for file in temp_dir.glob("unknown_*faces_*.jpg"):
                detection_files.append(file)
            
            detection_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            if selected_index < len(detection_files):
                selected_file = detection_files[selected_index]
                self.show_detection_photo(selected_file)
            
        except Exception as e:
            logging.error(f"Tespit seçme hatası: {e}")
            self.clear_detection_preview()
    
    def show_detection_photo(self, file_path):
        """Tespit fotoğrafını göster"""
        try:
            # Resmi yükle ve boyutlandır
            pil_image = Image.open(file_path)
            
            # Oranı koruyarak boyutlandır
            pil_image.thumbnail(DETECTION_THUMBNAIL_SIZE, LANCZOS)
            
            # PhotoImage'e çevir
            photo = ImageTk.PhotoImage(pil_image)
            
            # Label'ı güncelle
            self.detection_photo_label.configure(image=photo, text="")
            self.detection_photo_label.image = photo
            
            # Dosya bilgilerini göster
            file_size = file_path.stat().st_size
            file_size_kb = file_size / 1024
            
            # Dosya adından bilgi çıkar
            name = file_path.stem
            parts = name.split('_')
            
            info_text = f"Dosya: {file_path.name}\n"
            info_text += f"Boyut: {file_size_kb:.1f} KB\n"
            
            if len(parts) >= 3:
                face_count = parts[1].replace('faces', '')
                timestamp = parts[2] + '_' + parts[3] if len(parts) > 3 else parts[2]
                
                try:
                    dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                    readable_date = dt.strftime("%d.%m.%Y %H:%M:%S")
                    info_text += f"Tarih: {readable_date}\n"
                except ValueError:
                    pass
                
                info_text += f"Bilinmeyen kişi sayısı: {face_count}"
            
            self.detection_info_label.configure(text=info_text)
            
        except Exception as e:
            logging.error(f"Tespit fotoğrafı gösterme hatası: {e}")
            self.clear_detection_preview()
    
    def clear_detection_preview(self):
        """Tespit önizlemesini temizle"""
        self.detection_photo_label.configure(image="", text="Bir tespit seçin")
        self.detection_photo_label.image = None
        self.detection_info_label.configure(text="")
    
    def delete_selected_detection(self):
        """Seçili tespit fotoğrafını sil"""
        from config import TEMP_DIR
        from pathlib import Path
        
        try:
            selection = self.detections_listbox.curselection()
            
            if not selection:
                messagebox.showwarning("Uyarı", "Lütfen silmek istediğiniz tespit fotoğrafını seçin.")
                return
            
            # Onay iste
            result = messagebox.askyesno(
                "Fotoğraf Silme Onayı", 
                "Seçili tespit fotoğrafını silmek istediğinizden emin misiniz?"
            )
            
            if result:
                selected_index = selection[0]
                
                # Dosyayı bul ve sil
                temp_dir = Path(TEMP_DIR)
                
                detection_files = []
                for file in temp_dir.glob("unknown_*faces_*.jpg"):
                    detection_files.append(file)
                
                detection_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                
                if selected_index < len(detection_files):
                    selected_file = detection_files[selected_index]
                    selected_file.unlink()
                    
                    messagebox.showinfo("Başarılı", "✅ Fotoğraf başarıyla silindi!")
                    self.refresh_detections_list()
                    self.clear_detection_preview()
                    
        except Exception as e:
            messagebox.showerror("Hata", f"❌ Fotoğraf silme hatası: {str(e)}")
            logging.error(f"Tespit silme hatası: {e}")
    
    def clear_all_detections(self):
        """Tüm tespit fotoğraflarını temizle"""
        from config import TEMP_DIR
        from pathlib import Path
        
        try:
            result = messagebox.askyesno(
                "Tüm Fotoğrafları Sil", 
                "TÜM tespit fotoğraflarını silmek istediğinizden emin misiniz?\n\n"
                "Bu işlem geri alınamaz!"
            )
            
            if result:
                temp_dir = Path(TEMP_DIR)
                
                deleted_count = 0
                for file in temp_dir.glob("unknown_*faces_*.jpg"):
                    file.unlink()
                    deleted_count += 1
                
                messagebox.showinfo("Başarılı", f"✅ {deleted_count} fotoğraf silindi!")
                self.refresh_detections_list()
                self.clear_detection_preview()
                
        except Exception as e:
            messagebox.showerror("Hata", f"❌ Toplu silme hatası: {str(e)}")
            logging.error(f"Toplu silme hatası: {e}")
    
    def open_temp_folder(self):
        """Temp klasörünü dosya gezgininde aç"""
        from config import TEMP_DIR
        
        try:
            subprocess.Popen(f'explorer "{os.path.abspath(TEMP_DIR)}"')
        except Exception as e:
            messagebox.showerror("Hata", f"❌ Klasör açma hatası: {str(e)}")
