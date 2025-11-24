from ml.retrieval import get_ranked_questions

def get_questions_service(df, role, level, description, n):
    ranked_df = get_ranked_questions(
        df=df,
        role=role,
        level=level,
        description=description,
        n=n
    )

    questions = []
    for _, row in ranked_df.iterrows():
        questions.append({
            "id": int(row["id"]),
            "question": row["question"],
            "label": row["pseudo_label"],
            "score": float(row["score"]),
        })

    return {
        "role": role,
        "level": level,
        "count": len(questions),
        "questions": questions,
    }
