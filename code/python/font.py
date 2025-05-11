# src/font.py

import matplotlib.font_manager as fm

def get_font_synonyms(ext):
    return fm.get_fontext_synonyms(ext)
