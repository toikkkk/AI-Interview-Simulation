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
  const [answers, setAnswers] = useState({});
  const [currentIndex, setCurrentIndex] = useState(0);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isInterviewDone, setIsInterviewDone] = useState(false);

  const [finalAnalysisData, setFinalAnalysisData] = useState(null);
  const [isFinalAnalysisOpen, setIsFinalAnalysisOpen] = useState(false);

  const [loading, setLoading] = useState(false);

  // ====== Fetch Analisis Text Mining Akhir ======
  const fetchFinalTextMiningAnalysis = async () => {
    const payload = { role, level, description };

    const res = await fetch("http://localhost:5001/api/textmining/analysis", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    setFinalAnalysisData(data);
  };

  // ====== Mulai Interview ======
  const handleStartInterview = async () => {
    if (!description.trim()) return;

    const questionCount = level === "Junior" ? 3 : 5;

    const payload = { role, level, description, n: questionCount };

    setLoading(true);

    const res = await fetch("http://localhost:5001/api/questions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    setQuestions(data.questions || []);
    setCurrentIndex(0);
    setAnswers({});
    setIsInterviewDone(false);
    setIsFinalAnalysisOpen(false);

    if (data.questions.length > 0) {
      setIsModalOpen(true);
    }

    setLoading(false);
  };

  // ====== Next Pertanyaan ======
  const handleNextQuestion = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(i => i + 1);
    } else {
      setIsModalOpen(false);
      setIsInterviewDone(true);
      fetchFinalTextMiningAnalysis();
    }
  };

  return (
    <>
      <div className="app-header">
        <div className="app-title-block">
          <div className="app-badge">KELOMPOK I</div>
          <h1>AI Mock Interview</h1>
          <p>Isi deskripsi pengalamanmu, lalu sistem akan membuatkan pertanyaan interview.</p>
        </div>
      </div>

      <div className="main-layout">

        {/* FORM */}
        <div className="card">
          <div className="card-title">Konfigurasi Interview</div>

          <RoleSelector value={role} onChange={setRole} />
          <LevelSelector value={level} onChange={setLevel} />
          <DescriptionInput value={description} onChange={setDescription} />

          <button
            className="primary-btn"
            onClick={handleStartInterview}
            disabled={loading}
          >
            {loading ? "Mengambil pertanyaan..." : "Mulai Interview"}
          </button>
        </div>

        {/* PANEL STATUS */}
        <InterviewPage
          questions={questions}
          role={role}
          level={level}
          currentIndex={currentIndex}
          answers={answers}
          isInterviewDone={isInterviewDone}
          finalAnalysisData={finalAnalysisData}
          isFinalAnalysisOpen={isFinalAnalysisOpen}
          onOpenFinalAnalysis={() => setIsFinalAnalysisOpen(true)}
          onCloseFinalAnalysis={() => setIsFinalAnalysisOpen(false)}
        />
      </div>

      {/* POPUP JAWAB PERTANYAAN */}
      {isModalOpen && questions[currentIndex] && (
        <div className="modal-backdrop">
          <div className="modal-card">

            <div className="modal-header">
              <div className="modal-title">Pertanyaan</div>
              <div className="modal-progress">
                {currentIndex + 1}/{questions.length}
              </div>
            </div>

            <p className="modal-question">{questions[currentIndex].question}</p>

            <textarea
              className="modal-answer"
              value={answers[currentIndex] || ""}
              onChange={(e) =>
                setAnswers(prev => ({ ...prev, [currentIndex]: e.target.value }))
              }
              placeholder="Tulis jawabanmu..."
            />

            <div className="modal-actions">
              <button className="modal-btn primary" onClick={handleNextQuestion}>
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
