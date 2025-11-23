"""
Pipeline lengkap NLP + Pembacaan CSV
Terhubung dengan __init__.py yang memuat Sastrawi
"""

import pandas as pd

# Import modul NLP internal
from backend.nlp.a_preprocessing import run_preprocessing
from backend.nlp.b_feature_extraction import extract_manual_keywords, extract_auto_keywords
from backend.nlp.b_ner import extract_entities
from backend.nlp.c_modelling import find_main_topic, find_secondary_topics


# ==========================================================
# ⚡ PROCESS TEXT UTAMA
# ==========================================================
def process_text(text: str) -> dict:
    """
    Orkestrator pipeline NLP:
    - Preprocessing
    - Ekstraksi keyword manual & otomatis
    - Ekstraksi entitas organisasi (NER)
    - Analisis topik
    """

    print("\nMemulai pipeline NLP...")

    # --- A. Preprocessing ---
    text_stopped, text_stemmed = run_preprocessing(text)
    print(f"[NLP] Teks setelah stemming: {text_stemmed}")

    # --- B. Ekstraksi keyword manual ---
    skills, tools, concepts = extract_manual_keywords(text_stemmed)
    print(f"[NLP] Skills manual: {skills}")
    print(f"[NLP] Tools manual: {tools}")
    print(f"[NLP] Concepts manual: {concepts}")

    # --- C. Ekstraksi keyword otomatis (YAKE) ---
    auto_concepts = extract_auto_keywords(text_stemmed)
    print(f"[NLP] Concepts otomatis (YAKE): {auto_concepts}")

    # --- D. Entity Recognition (ORG) ---
    org_entities = extract_entities(text.lower())
    print(f"[NLP] Entities ORG (Stanza): {org_entities}")

    # --- E. Topic Modelling ---
    main_topic, topic_score = find_main_topic(text_stopped)
    print(f"[NLP] Topik utama: {main_topic} (score={topic_score})")

    secondary_topics = find_secondary_topics(text_stemmed)
    print(f"[NLP] Topik sekunder: {secondary_topics}")

    # --- Finalisasi ---
    final_tools = tools.union(org_entities)
    final_concepts = concepts.union(auto_concepts)
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


# ==========================================================
# ⚡ PROCESS CSV → JALANKAN NLP UNTUK SETIAP BARIS
# ==========================================================
def process_csv(csv_path: str, text_column: str):
    """
    Membaca CSV, memproses setiap baris menggunakan process_text()
    """
    df = pd.read_csv(csv_path)

    if text_column not in df.columns:
        raise ValueError(
            f"Kolom '{text_column}' tidak ditemukan! Kolom tersedia: {df.columns}"
        )

    results = []

    for idx, text in df[text_column].fillna("").items():
        print(f"\n=== Memproses baris {idx} ===")
        r = process_text(str(text))

        results.append({
            "index": idx,
            "text": text,
            "skills": ", ".join(r["skills"]),
            "tools": ", ".join(r["tools"]),
            "key_concepts": ", ".join(r["key_concepts"]),
            "main_topic": r["main_topic"],
            "topic_score": r["topic_score"],
            "secondary_topics": ", ".join(r["secondary_topics"]),
        })

    return pd.DataFrame(results)


# ==========================================================
# ⚡ SIMPAN CSV HASIL
# ==========================================================
def save_results(df: pd.DataFrame, output_path: str):
    df.to_csv(output_path, index=False)
    print(f"\nHasil NLP disimpan ke: {output_path}")


# ==========================================================
# ⚡ RUNNER
# ==========================================================
if __name__ == "__main__":
    print(">>> MEMPROSES CSV INTERVIEW <<<")

    input_csv = "backend/data/questions_raw.csv"     # ubah sesuai file kamu
    output_csv = "backend/data/questions_processed.csv"

    df_output = process_csv(input_csv, text_column="Pertanyaan")  # ubah kolom sesuai CSV kamu
    save_results(df_output, output_csv)

    print("\n>>> SELESAI <<<")
