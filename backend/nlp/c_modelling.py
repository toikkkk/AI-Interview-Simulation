def find_main_topic(text: str):
    """Topic modelling rule-based + scoring (upgraded, tetap ringan)."""
    t = text.lower()

    TOPIC_RULES = {
        "Data Analyst": {
            "keywords": ["kpi","dashboard","eda","ab testing","cohort","retention","conversion","insight","visualisasi data",
            "tableau","power bi","looker","cohort","conversion","retention","kpi","dashboard","tableau","power bi","looker","ab testing"],
            "weight": 1.0
        },
        "Data Engineer": {
            "keywords": ["etl","pipeline","data pipeline","airflow","spark","kafka","bigquery","lakehouse","data warehouse","streaming",
                         "batch processing","mysql","postgresql","bigquery","data warehouse","lakehouse","spark","airflow","kafka","pipelines"],
            "weight": 1.2
        },
        "ML Engineer": {
            "keywords": ["model","training","feature engineering","xgboost","lightgbm","mlflow","optuna","drift","deployment","classification",
                         "regression","training","classification","regression","tuning","xgboost","mlflow","model drift","deployment"],
            "weight": 1.1
        }
    }

    scores = {}
    for topic, rule in TOPIC_RULES.items():
        s = 0.0
        for kw in rule["keywords"]:
            if kw in t:
                s += rule["weight"]
        scores[topic] = s

    best_topic = max(scores, key=scores.get) if scores else None
    best_score = scores.get(best_topic, 0.0)

    return best_topic, best_score


def find_secondary_topics(text: str, main_topic: str):
    """Cari topik sekunder yang juga muncul di teks (upgraded)."""
    t = text.lower()

    TOPIC_KEYWORDS = {
        "Data Analyst": ["kpi","dashboard","eda","ab testing","cohort","retention","conversion","visualisasi data"],
        "Data Engineer": ["etl","pipeline","airflow","spark","kafka","bigquery","lakehouse","data warehouse","streaming"],
        "ML Engineer": ["model","training","feature engineering","xgboost","mlflow","optuna","deployment","drift"]
    }

    result = []
    for topic, kws in TOPIC_KEYWORDS.items():
        if topic == main_topic:
            continue
        if any(kw in t for kw in kws):
            result.append(topic)

    return result
