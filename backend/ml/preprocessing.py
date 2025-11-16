import re

def clean_text(text: str) -> str:
    """
    Preprocessing sederhana untuk text classification / retrieval:
    - lowercase
    - buang URL
    - buang karakter non-alfanumerik
    - rapikan spasi
    """
    if text is None:
        return ""
    s = str(text).lower()
    s = re.sub(r"http\S+|www\.\S+", " ", s)          # hapus URL
    s = re.sub(r"[^a-z0-9\s_+\-]", " ", s)          # sisakan huruf, angka, spasi
    s = re.sub(r"\s+", " ", s).strip()
    return s
