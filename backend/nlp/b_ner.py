# b_ner.py — versi aman & ringan TANPA stanza & TANPA torch

def extract_entities(text: str):
    """
    NER dimatikan untuk mencegah dependency torch & stanza.
    Tetap mengembalikan struktur yang sama agar kompatibel.
    """
    return {
        "org": []   # tidak ada extract ORG, tetap aman
    }
