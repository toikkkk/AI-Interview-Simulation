import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from ml.preprocessing import clean_text


def build_label(role: str, level: str) -> str:
    role_fixed = role.replace(" ", "_")
    label = f"{role_fixed}_{level}"
    return label.title()



def get_ranked_questions(df, role, level, description, n=10):
    """TF-IDF retrieval sesuai label + fallback jika pertanyaan label kurang."""

    if df.empty:
        return df.head(0)

    label = build_label(role, level)
    subset = df[df["pseudo_label"].astype(str) == label]

    if subset.empty:
        subset = df.copy()

    subset = subset.reset_index(drop=True)

    # ===== FIT TF-IDF SEKALI DI SUBSET =====
    vectorizer = TfidfVectorizer(preprocessor=clean_text, ngram_range=(1, 2))
    X_subset = vectorizer.fit_transform(subset["question"])
    qv = vectorizer.transform([description])

    scores_subset = linear_kernel(qv, X_subset).ravel()
    subset["score"] = scores_subset
    subset = subset.sort_values(by="score", ascending=False)

    top_subset = subset.head(n)

    # ===== FALLBACK JIKA JUMLAH < n =====
    if len(top_subset) < n:
        needed = n - len(top_subset)

        remaining_pool = df[~df["id"].isin(top_subset["id"])].copy()
        remaining_pool = remaining_pool.reset_index(drop=True)

        # ⚠️ PENTING: JANGAN FIT LAGI
        X_remaining = vectorizer.transform(remaining_pool["question"])

        scores_remaining = linear_kernel(qv, X_remaining).ravel()
        remaining_pool["score"] = scores_remaining
        remaining_pool = remaining_pool.sort_values(by="score", ascending=False)

        top_extra = remaining_pool.head(needed)

        top_subset = pd.concat([top_subset, top_extra], ignore_index=True)

    return top_subset
