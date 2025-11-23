"""
Modul pemodelan topik (versi ringan, tanpa sentence-transformers / torch).

Pendekatan:
- Kita definisikan beberapa "tema" topik pekerjaan terkait data/ML.
- Setiap tema punya daftar kata kunci.
- Kita hitung skor tema berdasarkan kemunculan kata kunci di teks.
- Topik utama = tema dengan skor tertinggi.
- Topik sekunder = tema lain dengan skor non-zero, diurutkan dari skor tertinggi.

Kelebihan:
- Tidak butuh PyTorch, sentence-transformers, atau model besar.
- Aman untuk lingkungan Windows yang sering bermasalah dengan DLL torch.
"""

from typing import List, Tuple, Dict


TOPIC_THEMES = [
    {
        "name": "Data Analysis & BI",
        "keywords": [
            "analisis", "analisis data", "data analysis", "statistik",
            "statistical", "eda", "exploratory", "data cleaning",
            "missing value", "cleaning", "grafik", "visualisasi",
            "chart", "insight", "metrik", "power bi", "tableau",
            "dashboard", "excel"
        ],
    },
    {
        "name": "Machine Learning & AI",
        "keywords": [
            "machine learning", "deep learning", "supervised", "unsupervised",
            "regression", "classification", "clustering", "model",
            "training", "testing", "predict", "overfitting", "underfitting",
            "dataset", "feature", "algoritma", "evaluasi", "akurasi",
            "precision", "recall", "f1", "feature importance"
        ],
    },
    {
        "name": "Data Engineering & Pipelines",
        "keywords": [
            "etl", "elt", "data pipeline", "pipeline", "airflow",
            "spark", "hadoop", "data warehouse", "ingestion", "datalake",
            "bigquery", "snowflake", "orchestrator"
        ],
    },
    {
        "name": "Software Engineering",
        "keywords": [
            "api", "rest", "fastapi", "flask", "django",
            "docker", "kubernetes", "git", "testing",
            "ci/cd", "deploy", "deployment", "microservice"
        ],
    },
    {
        "name": "Statistics & Experimentation",
        "keywords": [
            "statistik", "hipotesis", "hypothesis", "uji t",
            "p-value", "confidence", "sampling", "bayes",
            "variance", "distribusi", "anova", "experiment"
        ],
    },
]



def _score_themes(text: str) -> List[Tuple[str, int]]:
    """
    Hitung skor masing-masing tema berdasarkan kemunculan kata kunci
    (count substring sederhana, case-insensitive).
    """
    text_low = text.lower()
    scores: List[Tuple[str, int]] = []

    for theme in TOPIC_THEMES:
        name = theme["name"]
        score = 0
        for kw in theme["keywords"]:
            if not kw:
                continue
            # hitung jumlah kemunculan keyword dalam teks
            score += text_low.count(kw.lower())
        scores.append((name, score))

    return scores


def find_main_topic(text_stopped: str) -> Tuple[str, float]:
    """
    Menentukan topik utama berdasarkan skor tema tertinggi.
    Mengembalikan:
    - nama topik
    - skor normalisasi sederhana (0.0 - 1.0) berdasarkan rasio terhadap total skor.
    """
    scores = _score_themes(text_stopped)

    total = sum(s for _, s in scores)
    if total == 0:
        # tidak ada keyword yang nyantol
        return "Umum / Tidak Terklasifikasi", 0.0

    # cari tema dengan skor tertinggi
    scores_sorted = sorted(scores, key=lambda x: x[1], reverse=True)
    top_name, top_score = scores_sorted[0]

    # normalisasi sederhana: porsi skor tema ini terhadap total
    normalized = top_score / total if total > 0 else 0.0

    return top_name, float(normalized)


def find_secondary_topics(text_stemmed: str) -> List[str]:
    """
    Mengembalikan daftar topik sekunder.
    Diambil dari tema lain yang punya skor > 0, diurutkan dari skor tertinggi,
    kecuali topik utama.
    """
    scores = _score_themes(text_stemmed)
    # buang yang skor 0
    non_zero = [(name, s) for name, s in scores if s > 0]

    if not non_zero:
        return []

    # urutkan dari skor tertinggi
    sorted_scores = sorted(non_zero, key=lambda x: x[1], reverse=True)

    # ambil nama topik saja, skip yang pertama kalau dianggap topik utama
    # (asumsi find_main_topic dipanggil dengan teks yang sama)
    secondary = [name for name, _ in sorted_scores[1:]]

    return secondary