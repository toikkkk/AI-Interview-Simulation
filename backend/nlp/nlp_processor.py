from .a_preprocessing import run_preprocessing
from .b_feature_extraction import extract_manual_keywords, extract_auto_keywords
from .b_ner import extract_entities
from .c_modelling import find_main_topic, find_secondary_topics


def process_text(text: str) -> dict:
    """
    Orkestrator pipeline NLP:
    - Preprocessing (case folding, stopword, stemming)
    - Ekstraksi keyword manual & otomatis
    - Ekstraksi entitas organisasi (ORG) dengan Stanza
    - Analisis topik utama & topik-topik sekunder
    Mengembalikan dict siap di-JSON-kan oleh Flask.
    """

    print("Memulai pipeline NLP (Flask integration)...")

    # --- A. Pre-processing ---
    text_stopped, text_stemmed = run_preprocessing(text)
    print(f"[NLP] Teks setelah stemming: {text_stemmed}")

    # --- B. Ekstraksi Fitur ---
    # 1) Keyword manual berbasis kamus (skills, tools, concepts)
    skills, tools, concepts = extract_manual_keywords(text_stemmed)
    print(f"[NLP] Skills manual: {skills}")
    print(f"[NLP] Tools manual: {tools}")
    print(f"[NLP] Concepts manual: {concepts}")

    # 2) Keyword otomatis dengan YAKE
    auto_concepts = extract_auto_keywords(text_stemmed)
    print(f"[NLP] Concepts otomatis (YAKE): {auto_concepts}")

    # 3) Entitas organisasi (ORG) dari Stanza (jika tersedia)
    org_entities = extract_entities(text.lower())
    print(f"[NLP] Entities ORG (Stanza): {org_entities}")

    # --- C. Analisis Topik (Topic Modelling) ---
    # 1) Topik utama berbasis Sentence-Transformers
    main_topic, topic_score = find_main_topic(text_stopped)
    print(f"[NLP] Topik utama: {main_topic} (score={topic_score})")

    # 2) Topik-topik sekunder (LDA)
    secondary_topics = find_secondary_topics(text_stemmed)
    print(f"[NLP] Topik sekunder: {secondary_topics}")

    # --- D. Finalisasi Hasil ---
    # Gabungkan tools dengan entitas ORG
    final_tools = tools.union(org_entities)

    # Gabungkan concept manual + otomatis
    final_concepts = concepts.union(auto_concepts)

    # Hapus konsep yang tumpang tindih dengan tools dan skills
    final_concepts = final_concepts - final_tools - skills

    result = {
        "skills": sorted(list(skills)),
        "tools": sorted(list(final_tools)),
        "key_concepts": sorted(list(final_concepts)),
        "main_topic": main_topic,
        "topic_score": topic_score,
        "secondary_topics": secondary_topics,
    }

    print(f"[NLP] Hasil final: {result}")
    return result
