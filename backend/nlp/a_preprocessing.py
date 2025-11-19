import re
from . import stemmer, stopword_remover # Impor dari __init__.py di folder ini
from typing import Tuple

def run_preprocessing(text: str) -> Tuple[str, str]:
    """
    Menjalankan pipeline preprocessing (Metode 2, 3, 4).
    Mengembalikan dua string:
    1. text_stopped: Teks bersih untuk Analisis Topik (Metode 11)
    2. text_stemmed: Teks bersih + kata dasar untuk Ekstraksi Keyword
    """
    
    # Metode 2: Case Folding
    text_lower = text.lower()
    
    # Hapus karakter non-alfanumerik sederhana
    text_clean = re.sub(r'[^a-z0-9\s]', '', text_lower)

    # Metode 3: Stopword Removal (Sastrawi)
    text_stopped = stopword_remover.remove(text_clean)
    
    # Metode 4: Stemming (Sastrawi)
    # Kita stem teks yang *sudah* di-stopword
    text_stemmed = stemmer.stem(text_stopped)
    
    return text_stopped, text_stemmed