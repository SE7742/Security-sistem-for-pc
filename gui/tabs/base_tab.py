# -*- coding: utf-8 -*-
"""
PC Güvenlik Sistemi - Base Tab Sınıfı
Tüm sekmelerin temel sınıfı
"""

import tkinter as tk
from tkinter import ttk


class BaseTab:
    """Tüm sekmelerin temel sınıfı"""
    
    def __init__(self, parent, app):
        """
        Args:
            parent: Notebook widget
            app: Ana uygulama referansı (SecuritySystemGUI)
        """
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent)
        
    def add_to_notebook(self, text):
        """Sekmeyi notebook'a ekle"""
        self.parent.add(self.frame, text=text)
    
    @property
    def face_detector(self):
        return self.app.face_detector
    
    @property
    def face_db(self):
        return self.app.face_db
    
    @property
    def telegram(self):
        return self.app.telegram
    
    @property
    def listbox_config(self):
        return self.app.listbox_config
