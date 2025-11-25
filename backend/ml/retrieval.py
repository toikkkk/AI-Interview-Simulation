from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from ml.preprocessing import clean_text

# NLP helper (dipakai buat re-ranking)
from services.nlp_service import run_nlp


def build_label(role: str, level: str) -> str:
    """
    Generate label EXACTLY like CSV:
    Data_Analyst_Junior
    Data_Analyst_Senior
    ML_Engineer_Junior
    Data_Engineer_Senior
    """
    role_fixed = role.replace(" ", "_")
    label = f"{role_fixed}_{level}"
    return label.title()


def _extract_user_terms(description: str) -> set:
    """
    Ambil term penting dari NLP:
    skills + tools + key_concepts + auto_keywords
    """
    nlp = run_nlp(description)
    terms = []
    terms += nlp.get("skills", [])
    terms += nlp.get("tools", [])
    terms += nlp.get("key_concepts", [])
    terms += nlp.get("auto_keywords", [])

    norm_terms = []
    for t in terms:
        if not t:
            continue
        tt = str(t).lower().strip()
        if len(tt) >= 2:
            norm_terms.append(tt)

    return set(norm_terms)


def _nlp_match_count(question: str, user_terms: set) -> int:
    """
    Hitung berapa term user muncul di pertanyaan.
    Match sederhana (substring).
    """
    q = str(question).lower()
    c = 0
    for t in user_terms:
        if t in q:
            c += 1
    return c


def get_ranked_questions(df, role, level, description, n=10, nlp_boost=True, alpha=0.05):
    """
    TF-IDF retrieval + NLP re-ranking (tanpa menghilangkan retrieval).
    - nlp_boost: aktifkan bonus NLP
    - alpha: bobot bonus per term match (kecil agar TF-IDF tetap dominan)
    """

    if df is None or df.empty:
        return df.head(0)

    # 1) Label sesuai CSV
    label = build_label(role, level)

    # 2) Filter subset label
    subset = df[df["pseudo_label"].astype(str) == label]

    # fallback kalau subset kosong
    if subset.empty:
        subset = df.copy()

    subset = subset.reset_index(drop=True)

    # 3) TF-IDF similarity (retrieval utama)
    vectorizer = TfidfVectorizer(preprocessor=clean_text, ngram_range=(1, 2))
    X = vectorizer.fit_transform(subset["question"])
    qv = vectorizer.transform([description])

    scores = linear_kernel(qv, X).ravel()
    subset["score_raw"] = scores   # skor TF-IDF asli
    subset["score"] = scores       # skor final default = TF-IDF

    # 4) NLP re-ranking (bonus kecil)
    if nlp_boost:
        user_terms = _extract_user_terms(description)

        if len(user_terms) > 0:
            subset["nlp_match"] = subset["question"].apply(
                lambda q: _nlp_match_count(q, user_terms)
            )
            subset["score"] = subset["score_raw"] + alpha * subset["nlp_match"]
        else:
            subset["nlp_match"] = 0

    # 5) Sorting pakai skor final
    subset = subset.sort_values(by="score", ascending=False)

    return subset.head(n)
