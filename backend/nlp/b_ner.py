# backend/nlp/b_ner.py

from typing import Set

# Coba import stanza, tapi jangan bikin seluruh app crash kalau gagal
try:
    import stanza

    _STANZA_AVAILABLE = True
except Exception as e:
    print("[WARN] Tidak bisa import stanza, fitur NER ORG dimatikan. Detail:", e)
    stanza = None
    _STANZA_AVAILABLE = False

_nlp_pipeline = None


def _get_pipeline():
    """
    Inisialisasi lazy Stanza pipeline untuk NER.
    Kalau stanza tidak tersedia atau inisialisasi gagal, kembalikan None.
    """
    global _nlp_pipeline

    if not _STANZA_AVAILABLE:
        return None

    if _nlp_pipeline is not None:
        return _nlp_pipeline

    try:
        # Sesuaikan bahasa kalau mau (misal 'id' untuk bahasa Indonesia)
        # stanza.download("en")  # butuh koneksi internet saat pertama kali
        _nlp_pipeline = stanza.Pipeline(
            "en",
            processors="tokenize,ner",
            tokenize_pretokenized=False,
        )
        return _nlp_pipeline
    except Exception as e:
        print("[WARN] Gagal inisialisasi pipeline stanza, NER ORG dimatikan. Detail:", e)
        _nlp_pipeline = None
        return None


def extract_entities(text: str) -> Set[str]:
    """
    Ekstrak entitas organisasi (ORG) dari teks menggunakan Stanza.
    Kalau stanza/torch bermasalah, akan mengembalikan set kosong
    dan mencetak peringatan, tanpa menjatuhkan server Flask.
    """
    if not _STANZA_AVAILABLE:
        # stanza tidak bisa di-import, disable NER
        return set()

    nlp = _get_pipeline()
    if nlp is None:
        return set()

    doc = nlp(text)
    orgs = set()

    for ent in doc.ents:
        if ent.type == "ORG":
            orgs.add(ent.text)

    return orgs
