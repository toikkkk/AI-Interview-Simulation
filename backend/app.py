from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

from config.config import DATA_PATH
from services.question_service import get_questions_service
from services.analysis_service import get_analysis_service

app = Flask(__name__)
CORS(app)

# Load dataset
try:
    QUESTIONS_DF = pd.read_csv(DATA_PATH)
    print(f"[INFO] Loaded dataset: {len(QUESTIONS_DF)} rows")
except Exception as e:
    print("[ERROR] Failed loading dataset:", e)
    QUESTIONS_DF = pd.DataFrame(columns=["id", "question", "pseudo_label"])


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "question_count": len(QUESTIONS_DF)
    })


# ===============================
# 1) ENDPOINT — GET QUESTIONS
# ===============================
@app.route("/api/questions", methods=["POST"])
def api_questions():
    data = request.get_json(force=True)
    role = data.get("role")
    level = data.get("level")
    description = data.get("description")
    n = int(data.get("n", 10))

    if not role or not level or not description:
        return jsonify({"error": "role, level, description wajib diisi"}), 400

    result = get_questions_service(
        QUESTIONS_DF,
        role=role,
        level=level,
        description=description,
        n=n
    )

    return jsonify(result)


# ===============================
# 2) ENDPOINT — ANALYSIS
# ===============================
@app.route("/api/textmining/analysis", methods=["POST"])
def api_analysis():
    data = request.get_json(force=True)
    
    result = get_analysis_service(
    df=QUESTIONS_DF,
    role=data.get("role"),
    level=data.get("level"),
    description=data.get("description"),
    n=data.get("n")  # <-- TAMBAH INI
    )

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
