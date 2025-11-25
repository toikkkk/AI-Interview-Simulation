import yake

# =========================
# UPGRADE: tambah varian skill yang sering muncul di deskripsi CV
# =========================
SKILL_PHRASES = [
    # DA skills
    "data cleaning", "cleaning data", "visualisasi data", "eda", "exploratory data analysis",
    "ab testing", "eksperimen", "cohort analysis", "funnel analysis",
    "time series", "forecasting", "statistik deskriptif", "insight bisnis",
    "dashboard", "kpi", "retention", "conversion rate", "churn",

    # DE skills
    "etl", "extract transform load", "data pipeline", "pipeline data",
    "streaming", "stream processing", "batch processing",
    "data warehouse", "lakehouse", "data lake",
    "partitioning", "clustering", "data quality", "data governance",

    # ML skills
    "feature engineering", "hyperparameter tuning",
    "classification", "regression", "clustering",
    "fraud detection", "credit scoring", "model drift", "retraining"
]

TOOL_PHRASES = [
    "python","pandas","numpy","sql","excel","tableau","power bi","looker","looker studio",
    "airflow","spark","kafka","bigquery","google cloud storage","postgresql","mysql",
    "docker","kubernetes","mlflow","optuna","xgboost","lightgbm","fastapi","flask",
    "scikit learn","sklearn"
]

CONCEPT_PHRASES = [
    "kpi","retention","conversion rate","cac","lifetime value","churn",
    "etl","data warehouse","lakehouse","streaming",
    "classification","regression","clustering","confusion matrix","f1 score"
]

SIMPLE_STOPWORDS = {
    "dan","yang","di","ke","dari","untuk","pada","dengan","saya","kamu",
    "the","a","an","of","to","in","on","for","with","as","is","are","was","were"
}


def extract_phrases(text: str, phrases: list):
    found = []
    for p in phrases:
        if p in text:
            found.append(p)
    return found


def extract_manual_keywords(text: str) -> dict:
    """Extract keywords/skills secara manual berbasis phrase-matching (upgraded)."""
    if not text:
        return {"skills": [], "tools": [], "key_concepts": []}

    t = text.lower()

    skills = extract_phrases(t, SKILL_PHRASES)
    tools = extract_phrases(t, TOOL_PHRASES)
    concepts = extract_phrases(t, CONCEPT_PHRASES)

    def dedupe(lst):
        seen = set()
        out = []
        for x in lst:
            if x not in seen:
                out.append(x)
                seen.add(x)
        return out

    skills = dedupe(skills)
    tools = dedupe(tools)
    concepts = dedupe(concepts)


    if len(skills) == 0 and len(concepts) > 0:
        # ambil konsep yang bukan tools biar tidak dobel
        skills = [c for c in concepts if c not in tools]

    return {
        "skills": skills,
        "tools": tools,
        "key_concepts": concepts
    }


def extract_auto_keywords(text: str, top_n: int = 10):
    """Automatic keyword extraction (YAKE) dengan filtering (upgraded)."""
    if not text:
        return []

    kw_extractor = yake.KeywordExtractor(n=3, top=top_n)
    keywords = kw_extractor.extract_keywords(text)

    raw = [k[0].lower().strip() for k in keywords]

    filtered = []
    for kw in raw:
        if len(kw) < 3:
            continue
        parts = kw.split()
        if any(p in SIMPLE_STOPWORDS for p in parts):
            continue
        filtered.append(kw)

    out = []
    seen = set()
    for kw in filtered:
        if kw not in seen:
            out.append(kw)
            seen.add(kw)

    return out[:top_n]
