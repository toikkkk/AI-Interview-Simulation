import React from "react";

function TextMiningFinalModal({ data, onClose }) {
  if (!data) return null;

  return (
    <div className="tm-backdrop">
      <div className="tm-card">

        <div className="tm-header">
          <h2>Analisis Text Mining</h2>
          <button className="tm-close" onClick={onClose}>✕</button>
        </div>

        <p className="tm-desc">
          Berikut alasan sistem memilih 7 pertanyaan untuk interview Anda berdasarkan
          kesamaan teks dan bobot TF-IDF dari deskripsi pengalaman Anda.
        </p>

        {/* RANKING SIMILARITY */}
        <h3 className="tm-section-title">Ranking Kesamaan</h3>
        <div className="ranking-list">
          {data.top_questions.map((q, i) => (
            <div key={i} className="ranking-item">
              <span>{i + 1}.</span>
              <span className="rank-question">{q.question}</span>
              <span className="rank-score">{(q.score * 100).toFixed(1)}%</span>
            </div>
          ))}
        </div>

        {/* TOKEN TF-IDF */}
        <h3 className="tm-section-title">Kata / N-gram Dominan (TF-IDF)</h3>
        <div className="tokens-list">
          {data.wordcloud.map((item, i) => (
            <div key={i} className="token-item">
              <span>{i + 1}. {item.word}</span>
              <span className="token-weight">{item.weight.toFixed(4)}</span>
            </div>
          ))}
        </div>

        {/* PENJELASAN */}
        <h3 className="tm-section-title">Penjelasan Sistem</h3>
        <p className="tm-explanation">
          Sistem mendeteksi kata-kata dominan seperti{" "}
          <b>{data.wordcloud.slice(0, 3).map(w => w.word).join(", ")}</b>.
          Kata tersebut memiliki bobot tinggi sehingga berkaitan kuat dengan 
          pertanyaan seperti:
          <b> {data.top_questions[0].question}</b>.
        </p>

      </div>
    </div>
  );
}

export default TextMiningFinalModal;
