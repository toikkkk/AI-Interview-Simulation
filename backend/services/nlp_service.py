from nlp.nlp_processor import process_text

def run_nlp(description: str):
    """Memproses deskripsi user menggunakan NLP pipeline."""
    if not description:
        return {
            "skills": [],
            "tools": [],
            "key_concepts": [],
            "main_topic": None,
            "topic_score": 0.0,
            "secondary_topics": []
        }
    return process_text(description)
