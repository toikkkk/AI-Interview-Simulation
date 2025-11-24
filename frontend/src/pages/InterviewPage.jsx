import React from "react";
import TextMiningFinalModal from "../components/TextMiningFinalModal.jsx";

function prettyRole(role) {
  if (role === "Data_Analyst") return "Data Analyst";
  if (role === "Data_Engineer") return "Data Engineer";
  if (role === "ML_Engineer") return "ML Engineer";
  return role;
}

function InterviewPage({
  questions,
  role,
  level,
  answers,
  isInterviewDone,
  finalAnalysisData,
  isFinalAnalysisOpen,
  onOpenFinalAnalysis,
  onCloseFinalAnalysis
}) {

  return (
    <div className="card interview-panel">

      <div className="interview-header">
        <div>
          <div className="interview-header-title">Status Interview</div>
          <div className="card-subtitle">
            {isInterviewDone ? "Interview selesai. Berikut hasilnya." : "Belum ada interview yang berjalan."}
          </div>
        </div>

        <div className="interview-chip">
          <span>{prettyRole(role)}</span> · <span>{level}</span>
        </div>
      </div>

      {/* TOMBOL ANALISIS */}
      {isInterviewDone && finalAnalysisData && (
        <button className="tm-button" onClick={onOpenFinalAnalysis}>
          Lihat Analisis Text Mining
        </button>
      )}

      {/* DAFTAR PERTANYAAN */}
      {isInterviewDone && (
        <ul className="questions-list">
          {questions.map((q, idx) => (
            <li key={idx} className="question-item">
              <div className="question-meta">Pertanyaan {idx + 1}</div>
              <strong>{q.question}</strong>
              <div style={{ marginTop: 8, fontSize: 13 }}>
                <div style={{ color: "#6b7280" }}>Jawaban:</div>
                <div>{answers[idx] || "(Tidak ada jawaban)"}</div>
              </div>
            </li>
          ))}
        </ul>
      )}

      {/* MODAL FINAL */}
      {isFinalAnalysisOpen && finalAnalysisData && (
        <TextMiningFinalModal
          isOpen={isFinalAnalysisOpen}
          onClose={onCloseFinalAnalysis}
          nlp={finalAnalysisData.nlp}
          tfidf={finalAnalysisData.tfidf}
          similarity={finalAnalysisData.similarity}
          wordcloudImage={finalAnalysisData.wordcloud}
        />
      )}
    </div>
  );
}

export default InterviewPage;
