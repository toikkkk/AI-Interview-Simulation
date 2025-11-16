import React, { useState } from "react";
import RoleSelector from "../components/RoleSelector.jsx";
import LevelSelector from "../components/LevelSelector.jsx";
import DescriptionInput from "../components/DescriptionInput.jsx";
import InterviewPage from "./InterviewPage.jsx";

function LandingPage() {
  const [role, setRole] = useState("Data_Analyst");
  const [level, setLevel] = useState("Junior");
  const [description, setDescription] = useState("");
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [currentIndex, setCurrentIndex] = useState(0);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [answers, setAnswers] = useState({});

  // ------------------------------------------------
  // MULAI INTERVIEW
  // ------------------------------------------------
  const handleStartInterview = async () => {
    setError("");

    if (!description.trim()) {
      setError("Deskripsi pengalaman tidak boleh kosong.");
      return;
    }

    const questionCount = level === "Junior" ? 3 : 5;

    const payload = {
      role,
      level,
      description,
      n: questionCount,
    };

    try {
      setLoading(true);
      console.log("[DEBUG] Payload yang dikirim:", payload);

      const res = await fetch("http://localhost:5001/api/questions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        let msg = `HTTP ${res.status}`;
        try {
          const dataErr = await res.json();
          if (dataErr.error) msg = dataErr.error;
        } catch {
          /* ignore */
        }
        throw new Error(msg);
      }

      const data = await res.json();
      console.log("[DEBUG] Data sukses:", data);

      const qs = data.questions || [];
      setQuestions(qs);
      setCurrentIndex(0);
      setAnswers({});

      if (qs.length > 0) {
        setIsModalOpen(true);
      }
    } catch (err) {
      console.error("[DEBUG] Error di handleStartInterview:", err);
      setError(err.message || "Gagal mengambil pertanyaan");
    } finally {
      setLoading(false);
    }
  };

  // ------------------------------------------------
  // JAWABAN & NEXT
  // ------------------------------------------------
  const handleAnswerChange = (value) => {
    setAnswers((prev) => ({
      ...prev,
      [currentIndex]: value,
    }));
  };

  const handleNextQuestion = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex((idx) => idx + 1);
    } else {
      setIsModalOpen(false);
      console.log("[DEBUG] Semua jawaban:", answers);
    }
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const currentQuestion =
    questions.length > 0 ? questions[currentIndex] : null;

  return (
    <>
      {/* HEADER TENGAH */}
      <div className="app-header">
        <div className="app-title-block">
          <div className="app-badge">
            <span className="app-badge-dot" />
            <span>KELOMPOK I</span>
          </div>
          <h1>AI Mock Interview</h1>
          <p>
            Pilih role dan level, lalu tuliskan deskripsi pengalamanmu.
            Pertanyaan akan disesuaikan dengan profil yang kamu isi.
          </p>
        </div>
      </div>

      {/* LAYOUT UTAMA: FORM (KIRI) + STATUS (KANAN) */}
      <div className="main-layout">
        {/* FORM CARD */}
        <div className="card">
          <div className="card-header">
            <div>
              <div className="card-title">Konfigurasi sesi</div>
              <div className="card-subtitle">
                Junior akan mendapat 3 pertanyaan, Senior mendapat 5
                pertanyaan.
              </div>
            </div>
          </div>

          <RoleSelector value={role} onChange={setRole} />
          <LevelSelector value={level} onChange={setLevel} />
          <DescriptionInput value={description} onChange={setDescription} />

          {error && <p className="error-text">Error: {error}</p>}

          <button
            onClick={handleStartInterview}
            disabled={loading}
            className="primary-btn"
          >
            {loading ? "Mengambil pertanyaan..." : "Mulai Interview"}
            {!loading && <span>→</span>}
          </button>
        </div>

        {/* PANEL STATUS */}
        <InterviewPage
          questions={questions}
          role={role}
          level={level}
          currentIndex={currentIndex}
        />
      </div>

      {/* MODAL JAWABAN */}
      {isModalOpen && currentQuestion && (
        <div className="modal-backdrop">
          <div className="modal-card">
            <div className="modal-header">
              <div className="modal-title">Pertanyaan interview</div>
              <div className="modal-progress">
                {currentIndex + 1} / {questions.length} pertanyaan
              </div>
            </div>

            <p className="modal-question">{currentQuestion.question}</p>

            <textarea
              className="modal-answer"
              placeholder="Tulis jawabanmu di sini..."
              value={answers[currentIndex] || ""}
              onChange={(e) => handleAnswerChange(e.target.value)}
            />

            <div className="modal-actions">
              <button className="modal-btn" onClick={handleCloseModal}>
                Tutup
              </button>
              <button
                className="modal-btn primary"
                onClick={handleNextQuestion}
              >
                {currentIndex < questions.length - 1 ? "Next" : "Selesai"}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default LandingPage;
