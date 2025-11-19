from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

from config import DATA_PATH
from ml.retrieval import get_ranked_questions
from nlp.nlp_processor import process_text

app = Flask(__name__)
CORS(app)                                    # izinkan akses dari frontend

# load dataset pertanyaan hasil pseudo-labeling
try:
    QUESTIONS_DF = pd.read_csv(DATA_PATH)
    print(f"[INFO] Loaded questions from {DATA_PATH}, rows = {len(QUESTIONS_DF)}")
except Exception as e:
    print(f"[WARN] Gagal load {DATA_PATH}: {e}")
    QUESTIONS_DF = pd.DataFrame(columns=["id", "question", "pseudo_label"])


# health check endpoint
@app.route("/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "ok",
            "questions_count": int(len(QUESTIONS_DF)),
        }
    )


# endpoint utama untuk memberikan pertanyaan
@app.route("/api/questions", methods=["POST", "OPTIONS"])
def api_questions():

    if request.method == "OPTIONS":          # handle preflight (CORS)
        return ("", 204)

    data = request.get_json(force=True) or {}

    role = data.get("role")
    level = data.get("level")
    description = data.get("description", "")
    n = int(data.get("n", 10))

    # validasi input
    if not role or not level or not description:
        return jsonify({"error": "role, level, dan description wajib diisi."}), 400

    # panggil text mining retrieval
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

    # konversi dataframe → json
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
@app.route("/api/textmining/analysis", methods=["POST"])
def textmining_analysis():
    from ml.preprocessing import clean_text
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import linear_kernel
    import numpy as np

    data = request.get_json(force=True)

    role = data.get("role")
    level = data.get("level")
    description = data.get("description", "")

    if QUESTIONS_DF.empty:
        return jsonify({"error": "Dataset kosong"}), 500

    # ambil semua pertanyaan sesuai role-level → atau fallback
    from ml.retrieval import build_label
    label = build_label(role, level)

    df = QUESTIONS_DF.copy()
    subset = df[df["pseudo_label"].str.lower() == label.lower()]
    if subset.empty:
        subset = df.copy()

    subset = subset.reset_index(drop=True)

    # ambil hanya 7 teratas
    top_n = 7

    # TF-IDF
    vec = TfidfVectorizer(preprocessor=clean_text, ngram_range=(1, 2))
    X = vec.fit_transform(subset["question"])
    qv = vec.transform([description])

    sims = linear_kernel(qv, X).ravel()
    order = sims.argsort()[::-1][:top_n]

    top_questions = []
    for idx in order:
        top_questions.append({
            "question": subset.loc[idx, "question"],
            "score": float(sims[idx])
        })

    # n-gram extraction
    feature_names = vec.get_feature_names_out()
    top_indices = np.argsort(qv.toarray()[0])[::-1][:15]
    user_keywords = [feature_names[i] for i in top_indices]

    # buat word weight untuk wordcloud
    wc = [{"word": feature_names[i], "weight": float(qv.toarray()[0][i])}
          for i in top_indices]

    # similarity matrix top-7
    Xm = X[order]
    matrix = linear_kernel(Xm, Xm).tolist()

    return jsonify({
        "top_questions": top_questions,
        "user_keywords": user_keywords,
        "wordcloud": wc,
        "similarity_matrix": matrix
    })



@app.route("/api/nlp/analyze", methods=["POST", "OPTIONS"])
def api_nlp_analyze():
    """Analisis NLP lengkap (skills, tools, konsep, dan topik) dari deskripsi kandidat.

    Body JSON:
    {
        "text": "deskripsi kandidat"
    }
    """
    if request.method == "OPTIONS":
        # Untuk preflight CORS (CORS preflight request dari browser)
        return ("", 204)

    data = request.get_json(force=True) or {}
    text = data.get("text", "")

    if not text or not text.strip():
        return jsonify({"error": "field 'text' wajib diisi."}), 400

    try:
        result = process_text(text)
    except Exception as e:
        print("[ERROR] process_text gagal:", e)
        return jsonify({"error": "Gagal memproses NLP di server."}), 500

    return jsonify(result)


if __name__ == "__main__":
    print("[INFO] URL map:", app.url_map)
    app.run(host="0.0.0.0", port=5001, debug=True)  # server backend berjalan di port 5001