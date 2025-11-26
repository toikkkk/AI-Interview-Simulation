import React from "react";
import TextMiningRankTable from "./TextMiningRankTable";

const chipStyle = {
  padding: "6px 12px",
  borderRadius: "999px",
  background: "#eef2ff",
  color: "#374151",
  fontSize: "13px",
  marginRight: "8px",
  marginBottom: "8px",
  display: "inline-block",
};

const sectionCard = {
  background: "#ffffff",
  border: "1px solid #e5e7eb",
  borderRadius: "12px",
  padding: "14px 16px",
  marginBottom: "16px",
};

export default function TextMiningFinalModal({
  isOpen,
  onClose,
  nlp,
  tfidf,
  similarity,
  rankedTable,
  wordcloudImage,
}) {

  if (!isOpen) return null;

  return (
    <div className="tm-backdrop">
      <div className="tm-card">
        <div className="tm-header">
          <h2>Analisis Text Mining</h2>
          <button className="tm-close" onClick={onClose}>
            ✕
          </button>
        </div>

        <p className="tm-desc">
          Berikut visualisasi bagaimana sistem memilih <b> pertanyaan</b> paling relevan, serta
          bagaimana <b>NLP</b> memproses deskripsi kamu.
        </p>

        {/* =====================
            SIMILARITY SCORES
        ====================== */}
        <h3 className="tm-section-title">Skor Similarity</h3>
        <div>
          {similarity?.map((item, idx) => (
            <div key={idx} className="bar-row">
              <div className="bar-label">Q{idx + 1}</div>
              <div className="bar-container">
                <div
                  className="bar-fill bar-blue"
                  style={{ width: `${(item.score * 100).toFixed(1)}%` }}
                ></div>
              </div>
              <div className="bar-score">{(item.score * 100).toFixed(1)}%</div>
            </div>
          ))}
        </div>

        {/* =====================
            WORDCLOUD
        ====================== */}
        <h3 className="tm-section-title">Wordcloud</h3>

        {wordcloudImage ? (
          <img
            src={wordcloudImage}
            alt="wordcloud"
            style={{
              width: "100%",
              borderRadius: "12px",
              border: "1px solid #e5e7eb",
              marginBottom: "16px",
            }}
          />
        ) : (
          <p>Tidak ada wordcloud.</p>
        )}

        {/* =====================
            TF-IDF TOKENS
        ====================== */}
        <h3 className="tm-section-title">Kata / N-gram Dominan (TF-IDF)</h3>

        <div style={sectionCard}>
          {tfidf?.map((item, i) => (
            <div
              key={i}
              style={{
                display: "flex",
                justifyContent: "space-between",
                padding: "4px 0",
              }}
            >
              <span>{i + 1}. {item.term}</span>
              <span style={{ color: "#2563eb", fontWeight: "600" }}>
                {item.weight.toFixed(4)}
              </span>
            </div>
          ))}
        </div>

          {/* =====================
      DETAIL RANKING
===================== */}
<TextMiningRankTable table={rankedTable} />

        {/* ============================
              PREMIUM NLP ANALYSIS
        ============================= */}
        <h3 className="tm-section-title">Hasil Analisis NLP</h3>

        {/* Skills */}
        <div style={sectionCard}>
          <h4 style={{ margin: "0 0 8px" }}>🔥 Skill yang Terdeteksi</h4>
          {nlp?.skills?.length > 0 ? (
            nlp.skills.map((s, idx) => (
              <span key={idx} style={chipStyle}>{s}</span>
            ))
          ) : (
            <p style={{ fontSize: "14px", color: "#6b7280" }}>Tidak ada skill terdeteksi.</p>
          )}
        </div>

        {/* Tools */}
        <div style={sectionCard}>
          <h4 style={{ margin: "0 0 8px" }}>🛠 Tools yang Disebut</h4>
          {nlp?.tools?.length > 0 ? (
            nlp.tools.map((t, idx) => (
              <span key={idx} style={chipStyle}>{t}</span>
            ))
          ) : (
            <p style={{ fontSize: "14px", color: "#6b7280" }}>Tidak ada tools terdeteksi.</p>
          )}
        </div>

        {/* Key Concepts */}
        <div style={sectionCard}>
          <h4 style={{ margin: "0 0 8px" }}>🔍 Konsep / Key Concepts</h4>
          {nlp?.key_concepts?.length > 0 ? (
            nlp.key_concepts.map((k, idx) => (
              <span key={idx} style={chipStyle}>{k}</span>
            ))
          ) : (
            <p style={{ fontSize: "14px", color: "#6b7280" }}>Tidak ada konsep terdeteksi.</p>
          )}
        </div>

        {/* Main topic */}
        <div style={sectionCard}>
          <h4 style={{ margin: "0 0 8px" }}>📘 Topik Utama</h4>
          {nlp?.main_topic ? (
            <span style={chipStyle}>{nlp.main_topic}</span>
          ) : (
            <p style={{ fontSize: "14px", color: "#6b7280" }}>Tidak ada topik utama.</p>
          )}
        </div>

        {/* Secondary topics */}
        <div style={sectionCard}>
          <h4 style={{ margin: "0 0 8px" }}>📗 Topik Sekunder</h4>
          {nlp?.secondary_topics?.length > 0 ? (
            nlp.secondary_topics.map((t, idx) => (
              <span key={idx} style={chipStyle}>{t}</span>
            ))
          ) : (
            <p style={{ fontSize: "14px", color: "#6b7280" }}>Tidak ada topik sekunder.</p>
          )}
        </div>
      </div>
    </div>
  );
}
