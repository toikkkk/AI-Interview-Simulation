from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

from config import DATA_PATH
from ml.retrieval import get_ranked_questions

# -------------------------------------------------
# INISIALISASI APLIKASI
# -------------------------------------------------
app = Flask(__name__)

# CORS: izinkan akses dari frontend (localhost:5173)
# Untuk dev, paling aman pakai CORS(app) saja
CORS(app)  # kalau mau lebih strict: CORS(app, origins=["http://localhost:5173"])


def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response
# -------------------------------------------------
# LOAD DATASET SEKALI SAAT START
# -------------------------------------------------
try:
    QUESTIONS_DF = pd.read_csv(DATA_PATH)
    print(f"[INFO] Loaded questions from {DATA_PATH}, rows = {len(QUESTIONS_DF)}")
except Exception as e:
    print(f"[WARN] Gagal load {DATA_PATH}: {e}")
    QUESTIONS_DF = pd.DataFrame(columns=["id", "question", "pseudo_label"])


# -------------------------------------------------
# ROUTE: CEK SERVER
# -------------------------------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "ok",
            "questions_count": int(len(QUESTIONS_DF)),
        }
    )


# -------------------------------------------------
# ROUTE: AMBIL PERTANYAAN
# -------------------------------------------------
# Bisa dipanggil lewat:
#   POST http://localhost:5000/questions
#   POST http://localhost:5000/api/questions
@app.route("/questions", methods=["POST"])
@app.route("/api/questions", methods=["POST"])
def questions():
    """
    Body JSON yang diharapkan:
    {
      "role": "Data_Analyst" | "Data_Engineer" | "ML_Engineer",
      "level": "Junior" | "Senior",
      "description": "teks deskripsi pengalaman",
      "n": 10
    }
    """
    data = request.get_json(force=True) or {}
    role = data.get("role")
    level = data.get("level")
    description = data.get("description", "")
    n = int(data.get("n", 10))

    if not role or not level or not description:
        return (
            jsonify({"error": "role, level, dan description wajib diisi."}),
            400,
        )

    try:
        # panggil fungsi retrieval (TF-IDF + cosine similarity)
        result_df = get_ranked_questions(
            QUESTIONS_DF,
            role=role,
            level=level,
            description=description,
            n=n,
        )
    except Exception as e:
        # kalau ada error di sisi ML, jangan bikin frontend bingung
        print("[ERROR] get_ranked_questions gagal:", e)
        return (
            jsonify({"error": "Gagal memproses pertanyaan di server."}),
            500,
        )

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


# -------------------------------------------------
# MAIN
# -------------------------------------------------
if __name__ == "__main__":
    print("[INFO] URL map:", app.url_map)  # debug: lihat route apa saja yang terdaftar
    app.run(host="0.0.0.0", port=5000, debug=True)
