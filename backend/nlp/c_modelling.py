def find_main_topic(text: str):
    """Rule-based topic modelling (sederhana)."""
    t = text.lower()

    topic_rules = {
        "data cleaning": ["cleaning", "bersih", "preprocessing"],
        "data analysis": ["analisis", "analysis", "statistik"],
        "machine learning": ["model", "training", "prediksi", "classification"],
        "visualization": ["dashboard", "visual", "grafik"],
        "database": ["sql", "query", "database"]
    }

    best_topic = None
    best_score = 0

    for topic, keywords in topic_rules.items():
        score = sum(1 for k in keywords if k in t)
        if score > best_score:
            best_topic = topic
            best_score = score

    return best_topic, best_score


def find_secondary_topics(text: str, main_topic: str):
    """Secondary topics (yang tidak menjadi topik utama)."""
    t = text.lower()
    result = []

    all_topics = {
        "data cleaning": ["cleaning", "bersih", "preprocessing"],
        "data analysis": ["analisis", "analysis", "statistik"],
        "machine learning": ["model", "training", "prediksi", "classification"],
        "visualization": ["dashboard", "visual", "grafik"],
        "database": ["sql", "query", "database"]
    }

    for topic, keywords in all_topics.items():
        if topic == main_topic:
            continue
        if any(k in t for k in keywords):
            result.append(topic)

    return result
