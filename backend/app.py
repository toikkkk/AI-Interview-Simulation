from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

from config import DATA_PATH
from ml.retrieval import get_ranked_questions

app = Flask(__name__)

CORS(app)

try:
    QUESTIONS_DF = pd.read_csv(DATA_PATH)
    print(f"[INFO] Loaded questions from {DATA_PATH}, rows = {len(QUESTIONS_DF)}")
except Exception as e:
    print(f"[WARN] Gagal load {DATA_PATH}: {e}")
    QUESTIONS_DF = pd.DataFrame(columns=["id", "question", "pseudo_label"])



# ROUTE: HEALTH

@app.route("/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "ok",
            "questions_count": int(len(QUESTIONS_DF)),
        }
    )



# ROUTE: AMBIL PERTANYAAN

# HANYA 1 ENDPOINT: /api/questions
@app.route("/api/questions", methods=["POST", "OPTIONS"])
def api_questions():
    # handle preflight OPTIONS dulu
    if request.method == "OPTIONS":
        # response kosong tapi lewat @after_request tetap kena header CORS
        return ("", 204)

    data = request.get_json(force=True) or {}
    role = data.get("role")
    level = data.get("level")
    description = data.get("description", "")
    n = int(data.get("n", 10))

    if not role or not level or not description:
        return jsonify({"error": "role, level, dan description wajib diisi."}), 400

    try:
        result_df = get_ranked_questions(
            QUESTIONS_DF,
            role=role,
            level=level,
            description=description,
            n=n,
        )
    except Exception as e:
        print("[ERROR] get_ranked_questions gagal:", e)
        return jsonify({"error": "Gagal memproses pertanyaan di server."}), 500

    questions = []
    for _, row in result_df.iterrows():
        q = {
            "id": int(row["id"]) if "id" in row else None,
            "question": row["question"],
            "label": row.get("pseudo_label"),
            "score": float(row.get("score", 0.0)),
        }
        questions.append(q)

    return jsonify(
        {
            "role": role,
            "level": level,
            "count": len(questions),
            "questions": questions,
        }
    )


if __name__ == "__main__":
    print("[INFO] URL map:", app.url_map)
    app.run(host="0.0.0.0", port=5001, debug=True)  # <-- GANTI JADI 5001