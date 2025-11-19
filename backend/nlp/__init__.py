
"""
Inisialisasi ringan untuk package NLP.

- HANYA memuat Sastrawi (stemmer + stopword remover)
- TIDAK memuat stanza
- TIDAK memuat sentence-transformers / torch

Ini supaya server Flask bisa jalan tanpa crash karena
masalah DLL PyTorch di Windows.
"""

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

print("--- MEMUAT MODEL NLP RINGAN (SASTRAWI) ---")

# Setup Sastrawi (stemmer & stopword)
stemmer = StemmerFactory().create_stemmer()
stopword_remover = StopWordRemoverFactory().create_stop_word_remover()

print("Model Sastrawi (Stemmer, Stopword) berhasil dimuat.")
print("--- INISIALISASI NLP RINGAN SELESAI ---")