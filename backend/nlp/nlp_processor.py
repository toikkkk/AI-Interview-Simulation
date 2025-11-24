from nlp.a_preprocessing import run_preprocessing
from nlp.b_feature_extraction import extract_manual_keywords, extract_auto_keywords
from nlp.b_ner import extract_entities
from nlp.c_modelling import find_main_topic, find_secondary_topics


def process_text(text: str):
    """Pipeline lengkap NLP untuk memproses deskripsi user."""

    if not text:
        return {
            "skills": [],
            "tools": [],
            "key_concepts": [],
            "auto_keywords": [],
            "entities": [],
            "main_topic": None,
            "topic_score": 0,
            "secondary_topics": []
        }

    clean = run_preprocessing(text)

    manual = extract_manual_keywords(clean)
    auto_kw = extract_auto_keywords(clean)
    ner = extract_entities(text)

    topic, score = find_main_topic(clean)
    secondary = find_secondary_topics(clean, topic)

    return {
        "skills": manual["skills"],
        "tools": manual["tools"],
        "key_concepts": manual["key_concepts"],
        "auto_keywords": auto_kw,
        "entities": ner.get("org", []),
        "main_topic": topic,
        "topic_score": score,
        "secondary_topics": secondary
    }
