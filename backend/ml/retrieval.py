from typing import List, Dict
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from .preprocessing import clean_text

# mapping teks dari UI → label di CSV
ROLE_MAP = {
    "data_analyst": "Data_Analyst",
    "data analyst": "Data_Analyst",
    "data-analyst": "Data_Analyst",

    "data_engineer": "Data_Engineer",
    "data engineer": "Data_Engineer",
    "data-engineer": "Data_Engineer",

    "ml_engineer": "ML_Engineer",
    "machine learning engineer": "ML_Engineer",
    "ml engineer": "ML_Engineer",
}

LEVEL_MAP = {
    "junior": "Junior",
    "senior": "Senior",
}

def build_label(role: str, level: str) -> str:
    base = ROLE_MAP.get(role.lower(), role.replace(" ", "_"))
    lev = LEVEL_MAP.get(level.lower(), level)
    return f"{base}_{lev}"

def get_ranked_questions(
    df: pd.DataFrame,
    role: str,
    level: str,
    description: str,
    n: int = 10,
) -> pd.DataFrame:
    """
    Pilih N pertanyaan terbaik berdasarkan:
    - role + level (filter pseudo_label)
    - kemiripan TF-IDF + cosine terhadap deskripsi user
    """
    if df.empty:
        return df

    label = build_label(role, level)

    # 1) filter by label (kalau tidak ada, fallback pakai semua)
    if "pseudo_label" in df.columns:
        sub = df[df["pseudo_label"].str.lower() == label.lower()]
        if sub.empty:
            sub = df.copy()
    else:
        sub = df.copy()

    sub = sub.reset_index(drop=True)

    # 2) TF-IDF di subset pertanyaan
    vec = TfidfVectorizer(
        preprocessor=clean_text,
        ngram_range=(1, 2),
        max_features=20000,
    )
    X = vec.fit_transform(sub["question"].astype(str))

    # 3) vektorkan deskripsi user & hitung cosine
    qv = vec.transform([description])
    sims = linear_kernel(qv, X).ravel()  # cosine similarity

    # 4) ambil Top-N
    n = max(1, min(n, len(sub)))
    order = sims.argsort()[::-1][:n]
    sub = sub.iloc[order].copy()
    sub["score"] = sims[order]
    return sub
