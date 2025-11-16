from typing import List, Dict
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from .preprocessing import clean_text


# mapping role & level dari UI ke label CSV
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
    # bikin label final, misal: Data_Analyst + Junior → Data_Analyst_Junior
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

    # bangun label target (misal: Data_Analyst_Junior)
    label = build_label(role, level)

    # filter pertanyaan berdasarkan pseudo_label
    if "pseudo_label" in df.columns:
        sub = df[df["pseudo_label"].str.lower() == label.lower()]
        if sub.empty:
            sub = df.copy()                 # fallback jika label tidak ditemukan
    else:
        sub = df.copy()

    sub = sub.reset_index(drop=True)

    # ---------- TF-IDF untuk pertanyaan ----------
    vec = TfidfVectorizer(
        preprocessor=clean_text,            # cleaning teks
        ngram_range=(1, 2),                 # unigram + bigram
        max_features=20000,
    )
    X = vec.fit_transform(sub["question"].astype(str))  # vector pertanyaan

    # ---------- TF-IDF untuk deskripsi user ----------
    qv = vec.transform([description])       # vector user input

    # ---------- COSINE SIMILARITY ----------
    sims = linear_kernel(qv, X).ravel()     # similarity user ↔ pertanyaan

    # ambil top-N pertanyaan
    n = max(1, min(n, len(sub)))
    order = sims.argsort()[::-1][:n]

    sub = sub.iloc[order].copy()
    sub["score"] = sims[order]              # simpan nilai similarity
    return sub