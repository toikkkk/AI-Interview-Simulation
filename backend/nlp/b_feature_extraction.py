import yake
from typing import Set, Tuple

# Setup Corpus Keywords (Metode 10 - Manual)
# Ini adalah kamus kita untuk NER kustom
SKILL_KEYWORDS = {
    # Basic programming & scripting
    "python", "r", "sql", "scala", "java", "golang", "bash",

    # Python DS Libraries
    "pandas", "numpy", "matplotlib", "seaborn", "scikit-learn",
    "statsmodels", "pyspark", "tensorflow", "keras", "pytorch",
    "transformers", "nltk", "spacy", "sastrawi",

    # Machine Learning skills
    "machine learning", "deep learning", "nlp", "computer vision",
    "clustering", "classification", "regression",
    "supervised", "unsupervised", "reinforcement learning",
    "feature engineering", "feature selection", "model evaluation",
    "hyperparameter tuning",

    # Data Analysis
    "analisis", "analisis data", "statistik", "exploratory data analysis",
    "eda", "data cleaning", "data wrangling",

    # Cloud & MLOps / deployment
    "mlops", "ci/cd", "containerization", "deployment",
}

TOOL_KEYWORDS = {
    # BI Tools
    "excel", "power bi", "tableau", "looker studio", "looker",

    # Databases
    "mysql", "postgresql", "sql server", "oracle", "bigquery",
    "snowflake", "redshift", "mongodb", "elasticsearch",

    # Data Engineer Tools
    "airflow", "spark", "hadoop", "kafka", "dbt",
    "databricks", "glue", "synapse", "lakehouse",

    # ML Tools
    "tensorflow", "pytorch", "keras", "sklearn", "scikitlearn",
    "huggingface", "autogluon", "lightgbm", "xgboost", "catboost",

    # DevOps Tools
    "docker", "kubernetes", "git", "github", "gitlab",
    "jenkins", "terraform",

    # Environments
    "jupyter", "google colab", "vscode", "rstudio", "dbeaver",
}

CONCEPT_KEYWORDS = {
    # ML Core Concepts
    "overfitting", "underfitting", "bias variance", "cross validation",
    "train test split", "confusion matrix", "precision", "recall",
    "f1 score", "roc auc", "regularization", "normalisasi", "standardisasi",
    "one hot encoding", "feature importance",

    # Statistical concepts
    "uji hipotesis", "hypothesis testing", "t-test", "anova",
    "p-value", "confidence interval", "probabilitas",

    # Data Engineering
    "etl", "elt", "batch processing", "stream processing",
    "data pipeline", "data warehouse", "data lake", "lakehouse",

    # NLP Concepts
    "tokenisasi", "stemming", "lemmatization", "named entity recognition",
    "embedding", "word2vec", "tf-idf",

    # Business / product data
    "churn rate", "retention", "cohort analysis",
    "customer segmentation", "forecasting",
}


def extract_manual_keywords(text_stemmed: str) -> Tuple[Set[str], Set[str], Set[str]]:
    """
    Implementasi Metode 6/10 (NER Kustom berbasis kamus).
    Mencari keywords dari corpus kita di teks yang sudah di-stem.
    """
    found_skills = set()
    found_tools = set()
    found_concepts = set()
    
    # Metode 1 (Tokenisasi sederhana)
    tokens_stemmed = text_stemmed.split() 
    
    for token in tokens_stemmed:
        if token in SKILL_KEYWORDS:
            found_skills.add(token)
        if token in TOOL_KEYWORDS:
            found_tools.add(token)

    # Untuk konsep (yang mungkin 2 kata), kita cari di seluruh teks
    # Ini adalah implementasi N-gram sederhana (Metode 7)
    for concept in CONCEPT_KEYWORDS:
        if concept in text_stemmed:
            found_concepts.add(concept)
            
    return found_skills, found_tools, found_concepts


def extract_auto_keywords(text_stemmed: str) -> Set[str]:
    """
    Implementasi Metode 8 (YAKE Keyword Extraction) & 7 (N-gram).
    Mencari keyword otomatis.
    """
    found_concepts_auto = set()
    language = "id"
    max_ngram_size = 2 # Metode 7 (Bigram)
    deduplication_threshold = 0.9
    num_of_keywords = 5 
    
    yake_extractor = yake.KeywordExtractor(
        lan=language, 
        n=max_ngram_size, 
        dedupLim=deduplication_threshold, 
        top=num_of_keywords, 
        features=None
    )
    
    keywords = yake_extractor.extract_keywords(text_stemmed)
    
    for kw, score in keywords:
        print(f"YAKE menemukan keyword baru: '{kw}' (Score: {score:.4f})")
        found_concepts_auto.add(kw)
        
    return found_concepts_auto