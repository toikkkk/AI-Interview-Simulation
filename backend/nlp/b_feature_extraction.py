import yake

# =========================
# UPGRADE: tambah varian skill yang sering muncul di deskripsi CV
# =========================
SKILL_PHRASES = [
    # DA skills
    "data cleaning","cleaning data","data wrangling","preprocessing data",
    "eda","exploratory data analysis","analisis deskriptif","statistik deskriptif",
    "visualisasi data","data visualization","kpi","business insight",
    "ab testing","hypothesis testing","cohort analysis","funnel analysis",
    "churn analysis","retention analysis","forecasting","time series",
    "segmentation","customer segmentation",

    # DE skills
    "etl","etl pipeline","data pipeline","extract transform load",
    "batch processing","stream processing","streaming pipeline",
    "data warehouse","data lake","lakehouse","delta lake",
    "big data","distributed system","data lineage","schema design",
    "data validation","data quality","orchestration","workflow",

    # ML skills
    "feature engineering","hyperparameter tuning","model training",
    "cross validation","classification","regression","clustering",
    "model deployment","model monitoring","model drift","retraining",
    "fraud detection","credit scoring"
]

TOOL_PHRASES = [
    # Python stack
    "python","pandas","numpy","sql","mysql","postgresql","bigquery",
    "tableau","power bi","looker","looker studio",

    # Data engineer tools
    "airflow","spark","kafka","gcs","google cloud storage",
    "github actions","docker","docker compose","kubernetes",

    # ML stack
    "scikit learn","sklearn","xgboost","lightgbm",
    "mlflow","optuna","fastapi","flask"
]

CONCEPT_PHRASES = [
    # DA
    "kpi","retention","conversion rate","cac","ltv","lifetime value",
    "correlation","time series","forecasting",

    # DE
    "etl","data warehouse","lakehouse","streaming","batch",

    # ML
    "classification","regression","clustering",
    "confusion matrix","recall","precision","f1 score"
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
