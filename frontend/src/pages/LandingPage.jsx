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

  const handleStartInterview = async () => {
    setError("");

    if (!description.trim()) {
      setError("Deskripsi pengalaman tidak boleh kosong.");
      return;
    }

    const payload = {
      role,
      level,
      description,
      n: 10,
    };

    try {
      setLoading(true);
      console.log("[DEBUG] Payload yang dikirim:", payload);

      // Panggil backend Flask
      const res = await fetch("http://localhost:5001/api/questions", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    role,
    level,
    description,
    n: 10,
  }),
});



      const contentType = res.headers.get("content-type") || "";
      const rawBody = await res.text();

      console.log("[DEBUG] Status backend:", res.status, res.statusText);
      console.log("[DEBUG] Body backend:", rawBody);

      if (!res.ok) {
        let errMsg = `HTTP ${res.status}`;

        // Kalau backend kirim JSON {error: "..."}
        if (contentType.includes("application/json")) {
          try {
            const errData = JSON.parse(rawBody);
            if (errData.error) errMsg = errData.error;
          } catch (e) {
            console.warn("[DEBUG] Gagal parse JSON error:", e);
          }
        }

        throw new Error(errMsg);
      }

      let data = {};
      if (contentType.includes("application/json")) {
        try {
          data = JSON.parse(rawBody);
        } catch (e) {
          console.warn("[DEBUG] Gagal parse JSON sukses:", e);
        }
      }

      console.log("[DEBUG] Data sukses:", data);
      setQuestions(data.questions || []);
    } catch (err) {
      console.error("[DEBUG] Error di handleStartInterview:", err);
      setError(err.message || "Gagal mengambil pertanyaan");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "24px", fontFamily: "sans-serif" }}>
      <h1>AI Mock Interview</h1>
      <p style={{ maxWidth: "600px" }}>
        Pilih role dan level, lalu tuliskan deskripsi pengalamanmu. Sistem akan
        menyesuaikan pertanyaan interview berdasarkan profilmu.
      </p>

      <RoleSelector value={role} onChange={setRole} />
      <LevelSelector value={level} onChange={setLevel} />
      <DescriptionInput value={description} onChange={setDescription} />

      {error && (
        <p style={{ color: "red", marginBottom: "8px" }}>
          Error: {error}
        </p>
      )}

      <button
        onClick={handleStartInterview}
        disabled={loading}
        style={{
          padding: "10px 18px",
          fontWeight: "bold",
          cursor: loading ? "not-allowed" : "pointer",
          marginBottom: "24px",
        }}
      >
        {loading ? "Mengambil pertanyaan..." : "Mulai Interview"}
      </button>

      <InterviewPage questions={questions} role={role} level={level} />
    </div>
  );
}

// 🔥 INI YANG WAJIB ADA supaya bisa di-import sebagai default
export default LandingPage;
