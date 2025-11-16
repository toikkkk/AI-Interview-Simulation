import React from "react";

function prettyRole(role) {
  if (role === "Data_Analyst") return "Data Analyst";
  if (role === "Data_Engineer") return "Data Engineer";
  if (role === "ML_Engineer") return "ML Engineer";
  return role;
}

function InterviewPage({ questions, role, level, currentIndex, answers, isInterviewDone }) {
  const total = questions.length;

  return (
    <div className="card interview-panel">
      <div className="interview-header">
        <div>
          <div className="interview-header-title">Status interview</div>
          <div className="card-subtitle">
            {total === 0
              ? "Belum ada sesi interview yang berjalan."
              : isInterviewDone
              ? "Interview selesai. Berikut ringkasannya."
              : "Sedang berjalan sesi tanya-jawab berbasis profilmu."}
          </div>
        </div>

        <div className="interview-chip">
          <span>{prettyRole(role)}</span>
          <span>·</span>
          <span>{level}</span>

          {total > 0 && !isInterviewDone && (
            <>
              <span>·</span>
              <span>
                {currentIndex + 1}/{total}
              </span>
            </>
          )}
        </div>
      </div>

      {/* BELUM MULAI INTERVIEW */}
      {total === 0 && (
        <p className="field-hint">
          Klik <strong>Mulai Interview</strong> di panel kiri untuk memulai.
        </p>
      )}

      {/* INTERVIEW SEDANG BERJALAN */}
      {total > 0 && !isInterviewDone && (
        <p className="field-hint">
          Pertanyaan sedang ditampilkan di popup. Kamu dapat menutup popup
          kapan saja, lalu melanjutkan lagi dengan membuka sesi baru.
        </p>
      )}

      {/* INTERVIEW SUDAH SELESAI — TAMPILKAN RINGKASAN */}
      {isInterviewDone && total > 0 && (
        <div style={{ marginTop: "12px" }}>
          <ul className="questions-list">
            {questions.map((q, idx) => (
              <li key={idx} className="question-item">
                <div className="question-meta">Pertanyaan {idx + 1}</div>
                <div><strong>{q.question}</strong></div>

                <div style={{ marginTop: 8, color: "#9ca3af" }}>
                  <span style={{ fontSize: 13 }}>Jawaban:</span>
                  <div style={{ marginTop: 4 }}>
                    {answers[idx] && answers[idx].trim() !== ""
                      ? answers[idx]
                      : "(Tidak ada jawaban)"}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default InterviewPage;
