# -*- coding: utf-8 -*-
"""
PC Güvenlik Sistemi - Kişi Yönetimi Sekmesi
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import logging
import os
from PIL import Image, ImageTk

from .base_tab import BaseTab
from ..constants import COLORS, FONTS, PERSON_THUMBNAIL_SIZE

# Pillow uyumluluk
try:
    LANCZOS = Image.Resampling.LANCZOS
except AttributeError:
    LANCZOS = Image.LANCZOS


class PersonManagementTab(BaseTab):
    """Kişi yönetimi sekmesi"""
    
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.setup_ui()
        self.add_to_notebook("👥 Kişi Yönetimi")
    
    def setup_ui(self):
        """Kişi yönetimi sekmesi arayüzünü oluştur"""
        # Ana container (yatay bölünmüş)
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Sol taraf: Kişi listesi
        list_frame = ttk.LabelFrame(main_container, text="Kayıtlı Kişiler")
        list_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Listbox ve scrollbar
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.person_listbox = tk.Listbox(list_container, **self.listbox_config)
        person_scrollbar = ttk.Scrollbar(list_container, orient='vertical', 
                                        command=self.person_listbox.yview)
        self.person_listbox.configure(yscrollcommand=person_scrollbar.set)
        
        # Listbox'a seçim eventi ekle
        self.person_listbox.bind('<<ListboxSelect>>', self.on_person_select)
        
        self.person_listbox.pack(side='left', fill='both', expand=True)
        person_scrollbar.pack(side='right', fill='y')
        
        # Sağ taraf: Fotoğraf önizleme
        photo_frame = ttk.LabelFrame(main_container, text="Fotoğraf Önizleme")
        photo_frame.pack(side='right', fill='y', padx=(10, 0))
        
        # Fotoğraf label'ı
        self.photo_label = ttk.Label(photo_frame, text="Bir kişi seçin", 
                                    background='lightgray', width=25)
        self.photo_label.pack(padx=10, pady=10)
        
        # Fotoğraf bilgileri
        self.photo_info_label = ttk.Label(photo_frame, text="", wraplength=200)
        self.photo_info_label.pack(padx=10, pady=(0, 10))
        
        # Butonlar
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(button_frame, text="📷 Kamera ile Ekle", 
                  command=self.add_person_camera,
                  style='Success.TButton').pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="📁 Dosyadan Ekle", 
                  command=self.add_person_file,
                  style='Accent.TButton').pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="🔄 Listeyi Yenile", 
                  command=self.refresh_person_list).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="🗑️ Seçili Kişiyi Sil", 
                  command=self.delete_selected_person,
                  style='Danger.TButton').pack(side='left', padx=5)
    
    def add_person_camera(self):
        """Kamera ile kişi ekleme"""
        self.app.root.withdraw()  # Ana pencereyi gizle
        
        try:
            self.face_detector.add_known_person_interactive()
            
            # Kişi eklendikten sonra modeli yeniden yükle
            try:
                if hasattr(self.face_detector, '_load_known_faces'):
                    self.face_detector._load_known_faces()
                    logging.info("🔄 Yüz tanıma modeli yeniden yüklendi (kameradan ekleme)")
                
                # Face database'i de yeniden yükle
                self.face_detector.face_db.load_known_faces()
                logging.info("🔄 Yüz veritabanı yeniden yüklendi (kameradan ekleme)")
                
            except Exception as reload_error:
                logging.error(f"❌ Model yeniden yükleme hatası: {reload_error}")
            
        finally:
            self.app.root.deiconify()  # Ana pencereyi göster
            self.refresh_person_list()
            self.app.update_status()  # Durum kartlarını güncelle
    
    def add_person_file(self):
        """Dosyadan kişi ekleme"""
        file_path = filedialog.askopenfilename(
            title="Kişi fotoğrafı seçin",
            filetypes=[("Resim dosyaları", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if file_path:
            name = simpledialog.askstring("Kişi Adı", "Kişinin adını girin:")
            
            if name and name.strip():
                if self.face_db.add_person(file_path, name.strip()):
                    messagebox.showinfo("Başarılı", f"✅ {name} başarıyla eklendi!")
                    
                    # Yüz tanıma modelini yeniden yükle
                    try:
                        if hasattr(self.face_detector, '_load_known_faces'):
                            self.face_detector._load_known_faces()
                            logging.info("🔄 Yüz tanıma modeli yeniden yüklendi (yeni kişi)")
                        
                        # Face database'i de yeniden yükle
                        self.face_detector.face_db.load_known_faces()
                        logging.info("🔄 Yüz veritabanı yeniden yüklendi (yeni kişi)")
                        
                    except Exception as reload_error:
                        logging.error(f"❌ Model yeniden yükleme hatası: {reload_error}")
                    
                    self.refresh_person_list()
                    
                    # Eklenen kişiyi seç ve fotoğrafını göster
                    for i in range(self.person_listbox.size()):
                        if self.person_listbox.get(i) == name.strip():
                            self.person_listbox.selection_set(i)
                            self.show_person_photo(name.strip())
                            break
                    
                    # Durum kartlarını güncelle
                    self.app.update_status()
                else:
                    messagebox.showerror("Hata", "❌ Kişi eklenemedi! Resimde yüz bulunamadı.")
    
    def refresh_person_list(self):
        """Kişi listesini yenile"""
        self.person_listbox.delete(0, tk.END)
        
        for name in self.face_db.get_known_names():
            self.person_listbox.insert(tk.END, name)
    
    def on_person_select(self, event):
        """Kişi seçildiğinde fotoğrafını göster"""
        try:
            # Seçili öğeyi al
            selection = self.person_listbox.curselection()
            
            if not selection:
                self.clear_photo_preview()
                return
            
            # Seçili kişinin adını al
            selected_index = selection[0]
            person_name = self.person_listbox.get(selected_index)
            
            # Kişinin fotoğrafını bul ve göster
            self.show_person_photo(person_name)
            
        except Exception as e:
            logging.error(f"Kişi seçme hatası: {e}")
            self.clear_photo_preview()
    
    def show_person_photo(self, person_name):
        """Kişinin fotoğrafını göster"""
        from config import KNOWN_FACES_DIR
        from pathlib import Path
        
        try:
            known_faces_dir = Path(KNOWN_FACES_DIR)
            
            # Desteklenen formatlar
            supported_formats = ('.jpg', '.jpeg', '.png', '.bmp')
            
            # Kişinin fotoğrafını bul
            found_photo = None
            for image_file in known_faces_dir.glob("*"):
                if image_file.suffix.lower() in supported_formats:
                    # Dosya adından kişi ismini al
                    name_parts = image_file.stem.split('_')
                    file_person_name = name_parts[0] if name_parts else image_file.stem
                    
                    if file_person_name == person_name:
                        found_photo = image_file
                        break
            
            if found_photo:
                # Resmi yükle ve boyutlandır
                pil_image = Image.open(found_photo)
                
                # Oranı koruyarak boyutlandır
                pil_image.thumbnail(PERSON_THUMBNAIL_SIZE, LANCZOS)
                
                # PhotoImage'e çevir
                photo = ImageTk.PhotoImage(pil_image)
                
                # Label'ı güncelle
                self.photo_label.configure(image=photo, text="")
                self.photo_label.image = photo  # Referansı tut
                
                # Dosya bilgilerini göster
                file_size = found_photo.stat().st_size
                file_size_kb = file_size / 1024
                
                info_text = f"Kişi: {person_name}\n"
                info_text += f"Dosya: {found_photo.name}\n"
                info_text += f"Boyut: {file_size_kb:.1f} KB\n"
                info_text += f"Format: {found_photo.suffix.upper()}"
                
                self.photo_info_label.configure(text=info_text)
                
            else:
                # Fotoğraf bulunamadı
                self.clear_photo_preview()
                self.photo_info_label.configure(text=f"'{person_name}' için\nfotoğraf bulunamadı")
                
        except Exception as e:
            logging.error(f"Fotoğraf gösterme hatası: {e}")
            self.clear_photo_preview()
            self.photo_info_label.configure(text="Fotoğraf yükleme\nhatası")
    
    def clear_photo_preview(self):
        """Fotoğraf önizlemesini temizle"""
        self.photo_label.configure(image="", text="Bir kişi seçin")
        self.photo_label.image = None
        self.photo_info_label.configure(text="")
    
    def delete_selected_person(self):
        """Seçili kişiyi sil"""
        from config import KNOWN_FACES_DIR
        from pathlib import Path
        
        try:
            # Seçili öğeyi al
            selection = self.person_listbox.curselection()
            
            if not selection:
                messagebox.showwarning("Uyarı", "Lütfen silmek istediğiniz kişiyi seçin.")
                return
            
            # Seçili kişinin adını al
            selected_index = selection[0]
            person_name = self.person_listbox.get(selected_index)
            
            # Onay iste
            result = messagebox.askyesno(
                "Kişi Silme Onayı", 
                f"'{person_name}' adlı kişiyi ve tüm fotoğraflarını silmek istediğinizden emin misiniz?\n\n"
                "Bu işlem geri alınamaz!"
            )
            
            if result:
                # Kişiyi sil
                success, message = self.face_db.delete_person(person_name)
                
                if success:
                    # Klasör kontrolü yap
                    known_faces_dir = Path(KNOWN_FACES_DIR)
                    remaining_files = []
                    
                    if known_faces_dir.exists():
                        for file in known_faces_dir.glob("*"):
                            if file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                                name_parts = file.stem.split('_')
                                file_person_name = name_parts[0] if name_parts else file.stem
                                if file_person_name == person_name:
                                    remaining_files.append(file.name)
                    
                    if remaining_files:
                        messagebox.showwarning("Uyarı", 
                            f"⚠️ {person_name} silindi ancak bazı dosyalar hala klasörde:\n\n"
                            f"{chr(10).join(remaining_files)}\n\n"
                            f"Bu dosyaları manuel olarak silebilirsiniz.")
                        logging.warning(f"⚠️ Silme sonrası kalan dosyalar: {remaining_files}")
                    else:
                        messagebox.showinfo("Başarılı", f"✅ {person_name} başarıyla silindi!\n\n{message}")
                    
                    # Listeyi yenile
                    self.refresh_person_list()
                    
                    # Fotoğraf önizlemesini temizle
                    self.clear_photo_preview()
                    
                    # Yüz tanıma modelini yeniden yükle (ZORUNLU)
                    try:
                        if hasattr(self.face_detector, '_load_known_faces'):
                            self.face_detector._load_known_faces()
                        
                        # Face database'i de yeniden yükle
                        self.face_detector.face_db.load_known_faces()
                        
                        # Durum kartlarını güncelle
                        self.app.update_status()
                        
                    except Exception as reload_error:
                        logging.error(f"❌ Model yeniden yükleme hatası: {reload_error}")
                        messagebox.showwarning("Uyarı", f"Kişi silindi ancak yüz tanıma modeli güncellenemedi.\nProgramı yeniden başlatın.")
                else:
                    messagebox.showerror("Hata", f"❌ Silme işlemi başarısız!\n\n{message}")
                    
        except Exception as e:
            messagebox.showerror("Hata", f"❌ Kişi silme hatası: {str(e)}")
            logging.error(f"Kişi silme hatası: {e}")
