import yake
from typing import Set, Tuple

# Setup Corpus Keywords (Metode 10 - Manual)
# Ini adalah kamus kita untuk NER kustom
SKILL_KEYWORDS = {"python", "sql", "machine learning", "data science", "sains data", "visualisasi", "pandas", "numpy", "scikit-learn", "nlp", "text mining", "deep learning", "etl", "analisis"}
TOOL_KEYWORDS = {"tableau", "powerbi", "power bi", "airflow", "docker", "git", "github", "excel", "postgresql", "mysql", "google colab", "vscode", "dbeaver", "rstudio"}
CONCEPT_KEYWORDS = {"churn rate", "analisis churn", "a/b testing", "data warehouse", "data lake", "deteksi anomali", "rekomendasi", "forecasting", "klaster", "clustering", "sentimen", "realtime", "analisis uang"}


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