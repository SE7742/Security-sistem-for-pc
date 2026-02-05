# -*- coding: utf-8 -*-
"""
PC Güvenlik Sistemi - Log Sekmesi
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

from .base_tab import BaseTab
from ..constants import COLORS, FONTS


class LogTab(BaseTab):
    """Log sekmesi"""
    
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.setup_ui()
        self.add_to_notebook("📋 Loglar")
    
    def setup_ui(self):
        """Log sekmesi arayüzünü oluştur"""
        # Log metin alanı
        log_container = ttk.Frame(self.frame)
        log_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.log_text = tk.Text(log_container, wrap='word')
        log_scrollbar = ttk.Scrollbar(log_container, orient='vertical', 
                                     command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side='left', fill='both', expand=True)
        log_scrollbar.pack(side='right', fill='y')
        
        # Log butonları
        log_button_frame = ttk.Frame(self.frame)
        log_button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(log_button_frame, text="Logları Yenile", 
                  command=self.refresh_logs).pack(side='left', padx=5)
        
        ttk.Button(log_button_frame, text="Logları Temizle", 
                  command=self.clear_logs).pack(side='left', padx=5)
    
    def refresh_logs(self):
        """Logları yenile"""
        from config import LOGS_DIR
        
        try:
            log_file = os.path.join(LOGS_DIR, f"security_{datetime.now().strftime('%Y%m%d')}.log")
            
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(tk.END, content)
                self.log_text.see(tk.END)
            else:
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(tk.END, "Log dosyası bulunamadı.")
                
        except Exception as e:
            messagebox.showerror("Hata", f"❌ Loglar yüklenemedi: {str(e)}")
    
    def clear_logs(self):
        """Logları temizle"""
        self.log_text.delete(1.0, tk.END)
