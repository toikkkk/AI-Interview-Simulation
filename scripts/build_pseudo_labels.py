import os
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


# PREPROCESSING SEDERHANA

def clean_text(text: str) -> str:
    if text is None:
        return ""
    s = str(text).lower()
    s = re.sub(r"http\S+|www\.\S+", " ", s)           # hapus url
    s = re.sub(r"[^a-z0-9\s]", " ", s)                # sisakan huruf dan angka
    s = re.sub(r"\s+", " ", s).strip()                # rapikan spasi
    return s


# SEED DESKRIPSI (ROLE x LEVEL)
# Boleh kamu tambah kata2 Indonesia kalau mau makin relevan

SEEDS = {
    # -------------------------------------------------
    # DATA ANALYST – JUNIOR
    # -------------------------------------------------
    "Data_Analyst_Junior": """
        analisis data, analisis deskriptif, statistik deskriptif, rata rata, mean, median, modus,
        eksplorasi data, eksploratory data analysis, eda, membersihkan data, data cleaning,
        missing value, nilai hilang, duplikat, outlier, deteksi outlier,
        excel, spreadsheet, pivot table, vlookup,
        sql dasar, basic sql, select, where, group by, order by, join sederhana,
        visualisasi data, data visualization, grafik, chart, bar chart, line chart, pie chart,
        dashboard, laporan, report, insight bisnis, menjelaskan hasil analisis,
        query sederhana, filter data, agregasi data
    """,

    # -------------------------------------------------
    # DATA ANALYST – SENIOR
    
    "Data_Analyst_Senior": """
        business metrics, metrik bisnis, kpi, key performance indicator,
        a b testing, eksperimen, uji hipotesis, hypothesis testing, p value,
        cohort analysis, segmentasi pelanggan, customer segmentation,
        time series analysis, analisis deret waktu, forecasting, peramalan,
        regresi linier, regresi logistik, korelasi, causal inference,
        root cause analysis, analisis akar masalah,
        advanced sql, window function, cte, subquery kompleks, optimasi query,
        storytelling dengan data, presentasi ke stakeholder, rekomendasi bisnis,
        bi tools, power bi, tableau, looker, metabase,
        merancang dashboard, memvalidasi kualitas data, data governance
    """,

    
    # DATA ENGINEER – JUNIOR
    
    "Data_Engineer_Junior": """
        etl, extract transform load, pipeline data, data pipeline,
        ingest data, integrasi data, integrasi sumber data,
        sql, join, index, indeks, foreign key, primary key,
        database relasional, relational database, mysql, postgresql, sql server,
        data warehouse dasar, schema star, schema snowflake,
        cleaning data, menangani missing value, outlier, tipe data,
        batch processing, pemrosesan batch,
        file csv, json, parquet, format data,
        script python sederhana untuk olah data, pandas,
        meng schedule job, cron sederhana, workflow dasar
    """,

    
    # DATA ENGINEER – SENIOR
    
    "Data_Engineer_Senior": """
        distributed systems, sistem terdistribusi, big data,
        spark, hadoop, hive, flink,
        streaming data, stream processing, kafka, kinesis, pub sub,
        data lake, data lakehouse, delta lake, iceberg,
        orkestrasi, orchestration, airflow, dagster, prefect,
        pipeline skala besar, high throughput, low latency,
        optimasi query, partitioning, bucketing, indexing lanjutan,
        reliabilitas, reliability, fault tolerance, resiliency,
        monitoring pipeline, alerting, observability,
        data governance, lineage, catalog, audit,
        desain arsitektur data, data platform, cloud, aws, gcp, azure,
        best practice, standardisasi pipeline, code review untuk pipeline
    """,

    
    # ML ENGINEER – JUNIOR
    
    "ML_Engineer_Junior": """
        machine learning, pembelajaran mesin,
        supervised learning, unsupervised learning,
        regresi, regression, klasifikasi, classification,
        train test split, validation set, cross validation,
        feature engineering, normalisasi, standardisasi,
        algoritma dasar, logistic regression, decision tree, random forest, knn, svm,
        overfitting, underfitting, regularisasi,
        confusion matrix, accuracy, precision, recall, f1 score, roc auc,
        hyperparameter, hyperparameter tuning, grid search, random search,
        scikit learn, sklearn, pipeline model, evaluasi model,
        eksperimen model kecil, menyimpan model, pickle, joblib
    """,

    
    # ML ENGINEER – SENIOR
    
    "ML_Engineer_Senior": """
        mlops, produksi model, production machine learning,
        deployment model, rest api, batch inference, online inference,
        ci cd untuk model, continuous integration, continuous deployment,
        monitoring model, monitoring performa, data drift, concept drift,
        feature store, feature pipeline, data versioning, dvc,
        kubernetes, docker, container, scaling, autoscaling,
        latency, throughput, optimasi inference, quantization, pruning,
        model registry, model versioning,
        experiment tracking, mlflow, wandb,
        pipeline end to end, from data ingestion to serving,
        arsitektur sistem ml, desain solusi, trade off antara akurasi dan biaya,
        kolaborasi dengan data scientist dan software engineer
    """,
}


# LOAD CSV RAW  (DISAMAKAN DENGAN FILE-MU)

def load_raw_csv(path: str) -> pd.DataFrame:
    print(">> Cek file:", path)
    if not os.path.exists(path):
        raise FileNotFoundError(f"File tidak ditemukan: {path}")
    print("   - size:", os.path.getsize(path), "bytes")

    questions = []
    with open(path, "r", encoding="utf-8-sig", errors="ignore") as f:
        lines = [line.strip() for line in f if line.strip()]

    # kalau baris pertama adalah header (mis. 'Pertanyaan'), lewati
    if lines and "pertanyaan" in lines[0].lower():
        lines = lines[1:]

    for line in lines:
        # buang koma di ujung kalau ada
        q = line.rstrip(",").strip()
        if q:
            questions.append(q)

    df = pd.DataFrame({"question": questions})
    df.insert(0, "id", df.index + 1)

    print("   - jumlah baris:", len(df))
    return df



# FUNGSI UTAMA PSEUDO-LABEL

# 1) TF-IDF vectorization untuk teks pertanyaan + seed
# 2) Hitung cosine similarity terhadap setiap seed
# 3) Ambil label dengan skor similarity tertinggi sebagai pseudo_label

def pseudo_label(df: pd.DataFrame) -> pd.DataFrame:
    questions = df["question"].tolist()

    # Gabungkan semua pertanyaan + seed
    # Tujuannya agar TF-IDF dibentuk di "kosakata" yang sama.
    all_texts = questions + list(SEEDS.values())

     # ---------- TEXT MINING: TF-IDF ----------
    vec = TfidfVectorizer(
        preprocessor=clean_text, # pakai fungsi cleaning di atas
        ngram_range=(1, 2),      # unigram + bigram
        max_features=30000,
    )
    X_all = vec.fit_transform(all_texts)

    # Vektor pertanyaan ada di bagian awal
    Xq = X_all[:len(df)]

    # Vektor seed dihitung dengan vectorizer yang sama
    seed_vecs = {label: vec.transform([seed]) for label, seed in SEEDS.items()}

    labels = []
    scores = []
    second_labels = []
    second_scores = []

    # TEXT MINING: COSINE SIMILARITY 
    # Untuk setiap pertanyaan, hitung kemiripan (cosine similarity)
    # ke masing-masing seed, lalu pilih label dengan skor tertinggi.
    for i in range(Xq.shape[0]):
        sims = {
            label: float(linear_kernel(seed_vecs[label], Xq[i])[0, 0])
            for label in SEEDS
        }
        # Sorting skor tertinggi → (label, skor)
        sorted_sims = sorted(sims.items(), key=lambda x: x[1], reverse=True)

        # Label terbaik = kandidat pseudo_label
        best_lbl, best_score = sorted_sims[0]

        # Label kedua (opsional, berguna untuk analisis manual)
        snd_lbl, snd_score = sorted_sims[1]

        labels.append(best_lbl)
        scores.append(best_score)
        second_labels.append(snd_lbl)
        second_scores.append(snd_score)

    # Tambahkan kolom hasil pseudo-labeling ke dataframe

    df["pseudo_label"] = labels
    df["pseudo_score"] = scores
    df["second_label"] = second_labels
    df["second_score"] = second_scores
    return df


# MAIN EKSEKUSI SCRIPT

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # .../ai_mock_project
    RAW_PATH = os.path.join(BASE_DIR, "backend", "data", "questions_raw.csv")
    OUT_PATH = os.path.join(BASE_DIR, "backend", "data", "questions_labeled.csv")

    print("\n🔍 Membaca CSV RAW dari:", RAW_PATH)
    df_raw = load_raw_csv(RAW_PATH)
    print("✔ Total pertanyaan:", len(df_raw))

    print("\n🏷 Melakukan pseudo-labeling...")
    df_labeled = pseudo_label(df_raw)

    df_labeled.to_csv(OUT_PATH, index=False)

    print("\n✅ PSEUDO-LABEL BERHASIL DIBUAT!")
    print("➡ File disimpan ke:", OUT_PATH)
    print("\nContoh hasil:")
    print(df_labeled.head(10))
