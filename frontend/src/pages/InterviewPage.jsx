import React from "react";

function prettyRole(role) {
  if (role === "Data_Analyst") return "Data Analyst";
  if (role === "Data_Engineer") return "Data Engineer";
  if (role === "ML_Engineer") return "ML Engineer";
  return role;
}

function InterviewPage({ questions, role, level, currentIndex }) {
  const total = questions.length;

  return (
    <div className="card interview-panel">
      <div className="interview-header">
        <div>
          <div className="interview-header-title">Status interview</div>
          <div className="card-subtitle">
            {total === 0
              ? "Belum ada sesi interview yang berjalan."
              : "Sedang berjalan sesi tanya-jawab berbasis profilmu."}
          </div>
        </div>
        <div className="interview-chip">
          <span>{prettyRole(role)}</span>
          <span>·</span>
          <span>{level}</span>
          {total > 0 && (
            <>
              <span>·</span>
              <span>
                {currentIndex + 1}/{total}
              </span>
            </>
          )}
        </div>
      </div>

      {total === 0 ? (
        <p className="field-hint">
          Klik <strong>Mulai Interview</strong> di panel kiri untuk memulai.
        </p>
      ) : (
        <p className="field-hint">
          Pertanyaan sedang ditampilkan di popup. Kamu dapat menutup popup
          kapan saja, lalu melanjutkan lagi dengan membuka sesi baru.
        </p>
      )}
    </div>
  );
}

export default InterviewPage;
