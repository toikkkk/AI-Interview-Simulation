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
    
    # DATA ANALYST – JUNIOR
    
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

# Load raw CSV berisi pertanyaan mentah
def load_raw_csv(path: str) -> pd.DataFrame:
    print(">> Cek file:", path)
    if not os.path.exists(path):
        raise FileNotFoundError(f"File tidak ditemukan: {path}")

    questions = []
    with open(path, "r", encoding="utf-8-sig", errors="ignore") as f:
        lines = [line.strip() for line in f if line.strip()]

    # cek dan lewati header
    if lines and "pertanyaan" in lines[0].lower():
        lines = lines[1:]

    for line in lines:
        q = line.rstrip(",").strip()              # buang koma berlebih
        if q:
            questions.append(q)

    # bikin dataframe raw
    df = pd.DataFrame({"question": questions})
    df.insert(0, "id", df.index + 1)
    return df


# PROSES UTAMA PSEUDO-LABELING
def pseudo_label(df: pd.DataFrame) -> pd.DataFrame:
    questions = df["question"].tolist()

    # gabungkan pertanyaan + seed (supaya vektor TF-IDF seragam)
    all_texts = questions + list(SEEDS.values())

    # ---------- TF-IDF ----------
    vec = TfidfVectorizer(
        preprocessor=clean_text,     # gunakan teks yang sudah dibersihkan
        ngram_range=(1, 2),          # unigram + bigram
        max_features=30000
    )
    X_all = vec.fit_transform(all_texts)          # fit TF-IDF untuk semua teks

    Xq = X_all[:len(df)]                          # vektor pertanyaan
    seed_vecs = {label: vec.transform([seed])     # vektor tiap seed
                  for label, seed in SEEDS.items()}

    labels = []
    scores = []
    second_labels = []
    second_scores = []

    # ---------- COSINE SIMILARITY ----------
    # pilih label dengan skor similarity tertinggi
    for i in range(Xq.shape[0]):
        sims = {label: float(linear_kernel(seed_vecs[label], Xq[i])[0, 0])
                for label in SEEDS}

        sorted_sims = sorted(sims.items(), key=lambda x: x[1], reverse=True)

        best_lbl, best_score = sorted_sims[0]     # label paling mirip
        snd_lbl, snd_score = sorted_sims[1]       # label kedua

        labels.append(best_lbl)
        scores.append(best_score)
        second_labels.append(snd_lbl)
        second_scores.append(snd_score)

    # tambahkan hasil ke dataframe
    df["pseudo_label"] = labels
    df["pseudo_score"] = scores
    df["second_label"] = second_labels
    df["second_score"] = second_scores
    return df


# MAIN EXECUTION
if __name__ == "__main__":
    # path input & output
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    RAW_PATH = os.path.join(BASE_DIR, "backend", "data", "questions_raw.csv")
    OUT_PATH = os.path.join(BASE_DIR, "backend", "data", "questions_labeled.csv")

    df_raw = load_raw_csv(RAW_PATH)
    df_labeled = pseudo_label(df_raw)

    df_labeled.to_csv(OUT_PATH, index=False)      # simpan hasil pseudo-labeling
    print("Pseudo-labeling selesai!")