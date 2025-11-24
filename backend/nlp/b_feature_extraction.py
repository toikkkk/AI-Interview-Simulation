import yake

def extract_manual_keywords(text: str) -> dict:
    """Extract simple keywords/skills manually."""
    skills = []
    tools = []
    concepts = []

    # Define keyword groups
    skill_list = ["python", "sql", "excel", "machine learning", "analysis", "cleaning", "etl"]
    tool_list = ["tableau", "power bi", "jupyter", "mysql", "postgresql"]
    concept_list = ["regresi", "klasifikasi", "clustering", "statistik", "dashboard"]

    t = text.lower()

    for w in skill_list:
        if w in t:
            skills.append(w)

    for w in tool_list:
        if w in t:
            tools.append(w)

    for w in concept_list:
        if w in t:
            concepts.append(w)

    return {
        "skills": skills,
        "tools": tools,
        "key_concepts": concepts
    }


def extract_auto_keywords(text: str, top_n: int = 10):
    """Automatic keyword extraction (YAKE)."""
    kw_extractor = yake.KeywordExtractor(n=1, top=top_n)
    keywords = kw_extractor.extract_keywords(text)
    return [k[0] for k in keywords]
