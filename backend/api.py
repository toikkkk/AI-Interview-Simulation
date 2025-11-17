import csv
import os
import re
from openai import OpenAI

# ======================================================
# KONFIGURASI OPENAI CLIENT
# ======================================================
import requests

# -------------------------------
# KONFIGURASI API
# -------------------------------

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)



# ======================================================
# 1. GENERATE INTERVIEW DARI AI (UNIK + AVOID DUPLIKAT)
# ======================================================
def generate_interview(role: str,
                       level: str,
                       jumlah: int = 10,
                       existing_examples: list[str] | None = None):

    exclusion_block = ""
    if existing_examples:
        joined = "\n".join(f"- {q}" for q in existing_examples[:20])
        exclusion_block = f"""
Daftar pertanyaan yang TIDAK BOLEH diulang atau diparafrase:

{joined}

JANGAN membuat pertanyaan yang sama atau mirip.
"""

    prompt = f"""
Kamu adalah interviewer profesional untuk posisi **{role.replace('_', ' ')}** tingkat **{level}**.

Tugasmu: Buat **{jumlah} pertanyaan interview** yang:
- spesifik
- teknis
- sesuai role
- unik (tidak sama dengan contoh sebelumnya)

{exclusion_block}

FORMAT WAJIB:
Pertanyaan 1: <isi>
Jawaban ideal: <maks 3 kalimat>

Pertanyaan 2: <isi>
Jawaban ideal: <maks 3 kalimat>
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Kamu interviewer profesional."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# ======================================================
# 2. EXTRACT HANYA PERTANYAAN (MANY FORMAT SUPPORT)
# ======================================================
def extract_questions_from_output(text: str) -> list[str]:
    questions = []

    for raw in text.split("\n"):
        line = raw.strip()

        if not line:
            continue
        if line.lower().startswith("jawaban"):
            continue
        if line.lower().startswith("answer"):
            continue

        # Pola 1: Pertanyaan 1:
        if re.match(r"(?i)^pertanyaan\s+\d+\s*:", line):
            q = line.split(":", 1)[1].strip()
            q = q.split(",")[0].strip()
            questions.append(q)
            continue

        # Pola 2: 1. xxx
        if re.match(r"^\d+\.\s+", line):
            q = re.sub(r"^\d+\.\s+", "", line).strip()
            q = q.split(",")[0].strip()
            questions.append(q)
            continue

        # Pola 3: 1) xxx
        if re.match(r"^\d+\)\s+", line):
            q = re.sub(r"^\d+\)\s+", "", line).strip()
            q = q.split(",")[0].strip()
            questions.append(q)
            continue

        # Pola 4: Q1:
        if re.match(r"(?i)^q\d+:", line):
            q = line.split(":", 1)[1].strip()
            q = q.split(",")[0].strip()
            questions.append(q)
            continue

    return questions


# ======================================================
# 3. LOAD CSV (1 kolom: Pertanyaan)
# ======================================================
def load_existing_questions(csv_file: str) -> set[str]:
    if not os.path.exists(csv_file):
        return set()

    existing = set()
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0].strip().lower() != "pertanyaan":
                existing.add(row[0].strip().lower())

    return existing


# ======================================================
# 4. APPEND 1 KOLOM (tidak ubah struktur CSV)
# ======================================================
def append_to_csv(csv_file: str, questions: list[str]):
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for q in questions:
            writer.writerow([q])


# ======================================================
# 5. FUNGSI UTAMA (AUTO-LOOP UNTUK LIST)
# ======================================================
def append_unique_questions(
    role,
    level,
    csv_file="backend/data/questions_raw.csv",
    jumlah=10,
    max_round=5,
):
    # ============ jika role atau level berupa LIST → LOOP otomatis ============
    if isinstance(role, list) or isinstance(level, list):
        roles = role if isinstance(role, list) else [role]
        levels = level if isinstance(level, list) else [level]

        for r in roles:
            for l in levels:
                print(f"\n=== GENERATE: {r} | {l} ===")
                append_unique_questions(
                    role=r,
                    level=l,
                    csv_file=csv_file,
                    jumlah=jumlah,
                    max_round=max_round
                )
        return

    # ============ Single role + single level ============
    print(f"\n▶ Role = {role} | Level = {level}")
    print(f"📄 CSV: {csv_file}")

    existing = load_existing_questions(csv_file)
    final_list = []

    print(f"📊 Pertanyaan lama: {len(existing)}")

    round_ke = 0

    while len(final_list) < jumlah and round_ke < max_round:
        round_ke += 1
        sisa = jumlah - len(final_list)

        print(f"🔁 Round {round_ke}: minta {sisa} pertanyaan ke AI...")

        raw_output = generate_interview(
            role=role,
            level=level,
            jumlah=sisa,
            existing_examples=list(existing)
        )

        batch = extract_questions_from_output(raw_output)
        print(f"   ➜ Model mengembalikan {len(batch)} kandidat pertanyaan")

        baru_round_ini = 0
        for q in batch:
            qc = q.lower()
            if qc in existing:
                continue
            final_list.append(q)
            existing.add(qc)
            baru_round_ini += 1

            if len(final_list) == jumlah:
                break

        print(f"   ✔ Unik round ini: {baru_round_ini}")
        print(f"   📈 Total unik: {len(final_list)} / {jumlah}\n")

    if len(final_list) == 0:
        print("❌ Tidak bisa mendapatkan pertanyaan unik.")
        return

    append_to_csv(csv_file, final_list)

    print(f"🎉 DONE → total ditambahkan: {len(final_list)} pertanyaan.")
    print(f"📌 CSV ditambahkan di baris paling bawah.\n")


# ======================================================
# 6. MAIN PROGRAM
# ======================================================
if __name__ == "__main__":

    role = ["data_science", "data_analyst", "machine_learning"]
    level = ["Junior", "Middle", "Senior"]

    csv_path = "backend/data/questions_raw.csv"

    append_unique_questions(
        role=role,
        level=level,
        csv_file=csv_path,
        jumlah=10,
        max_round=6,
    )
