import re

def clean_text(text: str) -> str:
    """
    Fungsi cleaning untuk teks:
    - lowercase
    - hapus URL
    - hapus simbol
    - rapikan spasi
    """
    if text is None:
        return ""

    s = str(text).lower()                          # ubah jadi huruf kecil
    s = re.sub(r"http\S+|www\.\S+", " ", s)        # hapus URL
    s = re.sub(r"[^a-z0-9\s_+\-]", " ", s)         # buang simbol
    s = re.sub(r"\s+", " ", s).strip()             # rapikan spasi
    return s
