# -*- coding: utf-8 -*-
"""
PC Güvenlik Sistemi - GUI Tema Yöneticisi
ttk stil tanımlamaları
"""

from tkinter import ttk
from .constants import COLORS, FONTS


def setup_professional_theme(root):
    """Profesyonel tema ayarlarını uygula ve listbox_config döndür"""
    style = ttk.Style()
    style.theme_use('clam')
    
    colors = COLORS
    
    # Notebook (sekmeler) stili
    style.configure('TNotebook', 
                   background=colors['bg'],
                   borderwidth=0)
    
    style.configure('TNotebook.Tab',
                   background=colors['light'],
                   foreground=colors['text'],
                   padding=[20, 10],
                   font=FONTS['body_bold'])
    
    style.map('TNotebook.Tab',
             background=[('selected', colors['primary']),
                       ('active', colors['secondary'])],
             foreground=[('selected', colors['white']),
                       ('active', colors['white'])])
    
    # Button stilleri
    style.configure('Accent.TButton',
                   background=colors['accent'],
                   foreground=colors['white'],
                   font=FONTS['body_bold'],
                   padding=[15, 8])
    
    style.configure('Success.TButton',
                   background=colors['success'],
                   foreground=colors['white'],
                   font=FONTS['small_bold'],
                   padding=[12, 6])
    
    style.configure('Warning.TButton',
                   background=colors['warning'],
                   foreground=colors['white'],
                   font=FONTS['small_bold'],
                   padding=[12, 6])
    
    style.configure('Danger.TButton',
                   background=colors['danger'],
                   foreground=colors['white'],
                   font=FONTS['small_bold'],
                   padding=[12, 6])
    
    # LabelFrame stilleri
    style.configure('TLabelframe',
                   background=colors['bg'],
                   foreground=colors['text'],
                   borderwidth=2,
                   relief='solid')
    
    style.configure('TLabelframe.Label',
                   background=colors['bg'],
                   foreground=colors['primary'],
                   font=FONTS['body_bold'])
    
    # Entry stilleri
    style.configure('TEntry',
                   fieldbackground=colors['white'],
                   foreground=colors['text'],
                   borderwidth=1,
                   insertcolor=colors['accent'])
    
    # Ana pencere stili
    root.configure(bg=colors['bg'])
    
    # Listbox için özel stil (tkinter widget olduğu için)
    listbox_config = {
        'bg': colors['white'],
        'fg': colors['text'],
        'selectbackground': colors['accent'],
        'selectforeground': colors['white'],
        'font': FONTS['small'],
        'borderwidth': 1,
        'relief': 'solid',
        'highlightthickness': 1,
        'highlightcolor': colors['accent']
    }
    
    return style, listbox_config
