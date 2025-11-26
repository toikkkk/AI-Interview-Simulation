# services/analysis_service.py  (PATCHED / DIPERBAIKI)

from ml.preprocessing import clean_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np

from services.nlp_service import run_nlp
from ml.retrieval import build_label

import io
import base64


def _try_build_wordcloud_image(freq_dict):
    """
    Coba buat wordcloud PNG base64.
    Pakai backend non-GUI (Agg) supaya aman di Flask/thread.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")  # <<< TAMBAHAN PENTING

        from wordcloud import WordCloud
        import matplotlib.pyplot as plt
        import io, base64

        wc = WordCloud(
            width=800,
            height=400,
            background_color="white"
        ).generate_from_frequencies(freq_dict)

        buf = io.BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout(pad=0)

        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        b64 = base64.b64encode(buf.read()).decode("utf-8")
        return f"data:image/png;base64,{b64}"

    except Exception:
        return None


# STOPWORDS sederhana (Indo + English) untuk filter TF-IDF output

STOPWORDS = set([
    
    # STOPWORDS INDONESIA UMUM
    
    "dan","yang","di","ke","dari","untuk","pada","dengan","atau","itu","ini",
    "saya","kami","kamu","dia","mereka","sebagai","dalam","agar","karena",
    "oleh","tentang","tanpa","hingga","sampai","sejak","antara","selama",
    "jika","kalau","maka","jadi","bahwa","adalah","ialah","yakni","yaitu",
    "lebih","kurang","paling","sangat","cukup","banyak","sedikit","beberapa",
    "semua","setiap","tiap","para","dapat","bisa","mampu","harus","akan",
    "telah","sudah","belum","masih","pernah","sering","kadang","selalu",
    "namun","tetapi","tapi","padahal","sehingga","sementara","lalu","kemudian",
    "atau","dan","dll","dsb","etc",

    "pengalaman","tahun","bulan","intern","magang","selama","memiliki",
    "pernah","tugas","proyek","project","pekerjaan","tim","membuat",
    "menggunakan","melakukan","membangun","menyusun","menangani",
    "mengerjakan","menjalankan","menyelesaikan","menyampaikan",
    "memberikan","melaporkan","meningkatkan","memperbaiki","melanjutkan",
    "menganalisis","bertanggungjawab","kolaborasi","berkolaborasi",
    "berkoordinasi","mengembangkan","menyusun","mengelola","mengatur",
    "sebagai","dalam","selain","untuk","sebuah","pada","adalah","yang",
    "dan","atau","itu","ini","terhadap","melalui","serta","menyimpan",
    "menyajikan","digunakan","menggunakan","memakai","menjalankan",
    "pengguna","mengolah","mengelompokkan","mengevaluasi", 

    # kata tanya / penghubung
    "apa","siapa","kapan","dimana","mengapa","kenapa","bagaimana","berapa",
    "apakah","yangmana","dari mana","ke mana",

    
    # KATA KERJA UMUM CV (TIDAK INFORMATIF)
    
    "menggunakan","melakukan","mengerjakan","menangani","membuat","membangun",
    "merancang","mengembangkan","menyusun","mengelola","mengatur","memimpin",
    "menganalisis","mengolah","memproses","meningkatkan","memperbaiki",
    "berkolaborasi","berkoordinasi","mendukung","membantu","bertanggungjawab",
    "memastikan","menjalankan","memantau","menyelesaikan","menyajikan",
    "menyampaikan","menulis","mengimplementasikan","memvalidasi",
    "melaporkan","mengoptimalkan","mengintegrasikan","men-deploy","deploy",

    # kata kerja bahasa Inggris CV
    "using","use","used","do","did","doing","done","make","made","build","built",
    "develop","developed","design","designed","manage","managed","lead","led",
    "analyze","analyzed","process","processed","implement","implemented",
    "support","supported","collaborate","collaborated","coordinate","coordinated",
    "ensure","ensured","monitor","monitored","optimize","optimized",
    "report","reported","deliver","delivered",

    
    # STOPWORDS INGGRIS UMUM
    
    "the","a","an","to","of","in","on","for","with","and","or","is","are",
    "was","were","be","been","being","it","this","that","these","those",
    "as","at","by","from","into","about","over","under","between","within",
    "while","when","where","why","how","what","who","whom","which",
    "more","most","less","very","just","only","also","still","already",
    "yet","not","no","yes",

    
    # FILLER / GENERIC WORK WORDS
    # (sering muncul tapi kurang spesifik)
    
    "pengalaman","project","proyek","tugas","pekerjaan","kerja","bekerja","tim",
    "team","member","anggota","company","perusahaan","client","klien",
    "tahun","bulan","minggu","hari","waktu","proses","hasil","target",
    "laporan","report","presentasi","presentation",

    
    # ANGKA / SIMBOL UMUM (opsional)
    
    "1","2","3","4","5","6","7","8","9","0"
])


def _valid_term(term: str) -> bool:
    """Filter term TF-IDF agar yang ditampilkan relevan."""
    t = term.strip().lower()
    if not t:
        return False
    if t in STOPWORDS:
        return False
    if len(t) <= 1:        # buang token 1 huruf
        return False
    if t.isdigit():        # buang angka doang
        return False
    return True


def get_analysis_service(df, role, level, description, n=None):
    """Menghasilkan analisis text mining + NLP. (kompatibel dengan frontend)"""

    if df.empty:
        return {"error": "Dataset pertanyaan kosong"}

    label = build_label(role, level)

    subset = df[df["pseudo_label"].str.lower() == label.lower()]
    if subset.empty:
        subset = df.copy()
    subset = subset.reset_index(drop=True)

    
    # TOP-K: prioritas dari request n, fallback dari level
    
    if n is not None:
        try:
            top_k = int(n)
        except:
            top_k = 5
    else:
        lvl = str(level or "").strip().lower()
        top_k = 3 if "junior" in lvl else 5

    
    # POOL UNTUK RANKING TOP-K
    # kalau subset kurang dari top_k → pakai full df
    
    rank_pool = subset if len(subset) >= top_k else df.copy()
    rank_pool = rank_pool.reset_index(drop=True)

    
    # TF-IDF UNTUK rank_pool
    
    vec = TfidfVectorizer(preprocessor=clean_text, ngram_range=(1, 2))
    X = vec.fit_transform(rank_pool["question"])
    qv = vec.transform([description])

    sims = linear_kernel(qv, X).ravel()
    order = sims.argsort()[::-1][:top_k]

    
    # TOP QUESTIONS + similarity (ikut top_k)
    
    top_questions = [{
        "question": rank_pool.loc[i, "question"],
        "score": float(sims[i])
    } for i in order]

    similarity = [
        {"score": float(sims[i]), "question": rank_pool.loc[i, "question"]}
        for i in order
    ]

    
    # USER TF-IDF KEYWORDS (rapi, tanpa override)
    
    feature_names = vec.get_feature_names_out()
    arr = qv.toarray()[0]

    sorted_idx = np.argsort(arr)[::-1]

    valid_idx = []
    for i in sorted_idx:
        if arr[i] <= 0:
            continue
        term = feature_names[i]
        if _valid_term(term):
            valid_idx.append(i)
        if len(valid_idx) >= 10:
            break

    keywords = [feature_names[i] for i in valid_idx]
    wordcloud_data = [{"word": feature_names[i], "weight": float(arr[i])} for i in valid_idx]
    tfidf = [{"term": feature_names[i], "weight": float(arr[i])} for i in valid_idx]

    # wordcloud image base64
    freq_dict = {d["word"]: d["weight"] for d in wordcloud_data}
    wordcloud_image = _try_build_wordcloud_image(freq_dict)

    # similarity matrix (top_k x top_k) 
    Xm = X[order]
    matrix = linear_kernel(Xm, Xm).tolist()

    nlp_result = run_nlp(description)
    
    # RANKING TABLE (TF-IDF + NLP SMART MATCHING)
   
    ranked_table = []
    for idx, i in enumerate(order):

        question_text = rank_pool.loc[i, "question"].lower()

        
        # NLP MATCHING LOGIC
        

        match_score = 0

        if nlp_result:

            # 3 poin untuk SKILLS
            for t in nlp_result.get("skills", []):
                if isinstance(t, str) and t.lower() in question_text:
                    match_score += 3

            # 2 poin untuk TOOLS
            for t in nlp_result.get("tools", []):
                if isinstance(t, str) and t.lower() in question_text:
                    match_score += 2

            # 2 poin untuk CONCEPTS
            for t in nlp_result.get("key_concepts", []):
                if isinstance(t, str) and t.lower() in question_text:
                    match_score += 2

            # 1 poin untuk AUTO KEYWORDS
            for t in nlp_result.get("auto_keywords", []):
                if isinstance(t, str) and t.lower() in question_text:
                    match_score += 1

        # Normalisasi NLP strength biar 0–1
        max_possible = 3*len(nlp_result.get("skills", [])) \
                     + 2*len(nlp_result.get("tools", [])) \
                     + 2*len(nlp_result.get("key_concepts", [])) \
                     + 1*len(nlp_result.get("auto_keywords", []))

        if max_possible == 0:
            nlp_strength = 0
        else:
            nlp_strength = match_score / max_possible   # 0–1 but scalable

        
        # FINAL SCORING
        
        # FINAL SCORING (TF-IDF + NLP BOOST)

        tfidf_raw = float(sims[i])

        nlp_boost = (
                     (match_score * 0.30)    
                    )
# Final score lebih besar dari TF-IDF
        final_score = tfidf_raw + nlp_boost

# ------------------------------


        ranked_table.append({
            "rank": idx + 1,
            "id": int(rank_pool.loc[i, "id"]) if "id" in rank_pool.columns else None,
            "question": rank_pool.loc[i, "question"],
            "tfidf_raw": tfidf_raw,
            "match_nlp": match_score,
            "nlp_strength": nlp_strength,
            "final_score": final_score
            })


    return {
        "top_questions": top_questions,
        "user_keywords": keywords,
        "similarity_matrix": matrix,
        "nlp": nlp_result,

        "wordcloud_data": wordcloud_data,
        "ranked_table": ranked_table,

        "tfidf": tfidf,
        "similarity": similarity,
        "wordcloud": wordcloud_image
    }
