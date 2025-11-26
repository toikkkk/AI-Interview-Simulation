import re
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Normalisasi istilah umum CV (Indo-Inggris / variasi penulisan)
NORMALIZE_MAP = {
    "a b testing": "ab testing",
    "a/b testing": "ab testing",
    "ab-test": "ab testing",
    "exploratory data analysis": "eda",
    "exploratory data": "eda",
    "data visualization": "visualisasi data",
    "visualization": "visualisasi data",
    "powerbi": "power bi",
    "looker studio": "looker",
    "ml ops": "mlops",
    "m l ops": "mlops",
    "ci cd": "cicd",
    "ci/cd": "cicd",
    "pub sub": "pubsub",
    "gcs": "google cloud storage",
    "ltv": "lifetime value",
    "cac": "customer acquisition cost",
    "crm": "customer relationship management",
}

# Daftar istilah teknis yang tidak boleh di-stem
TECH_TERMS_SET = {
    "python","pandas","numpy","sql","tableau","power bi","looker","airflow","spark","kafka",
    "bigquery","postgresql","mysql","flask","fastapi","docker","kubernetes","mlflow","optuna",
    "xgboost","lightgbm","svm","knn","etl","eda","ab testing","cicd","mlops","api","dag",
    "window function","cte","cross validation","data lineage","feature engineering",
    "logistic regression","random forest","svm","xgboost","lightgbm",
    "churn","forecasting","cohort","funnel","hyperparameter","optuna","mlflow"
}


def normalize_terms(text: str) -> str:
    t = text
    for k, v in NORMALIZE_MAP.items():
        t = t.replace(k, v)
    return t


def run_preprocessing(text: str) -> str:
    """Basic preprocessing (upgraded): casefolding, cleaning, normalisasi istilah, stemming aman."""
    if not text:
        return ""

    # Lowercase
    text = text.lower().strip()

    # Normalisasi istilah/variasi penulisan
    text = normalize_terms(text)

    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)

    # Remove numbers
    text = re.sub(r"\d+", " ", text)

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Remove extra whitespace
    text = " ".join(text.split())

    # Tokenize
    tokens = text.split()

    # Stemming (Sastrawi) tapi aman untuk istilah teknis
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    safe_tokens = []
    for w in tokens:
        if w in TECH_TERMS_SET:
            safe_tokens.append(w)
        else:
            safe_tokens.append(stemmer.stem(w))

    return " ".join(safe_tokens)
