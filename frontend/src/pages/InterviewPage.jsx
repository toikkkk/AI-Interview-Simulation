import React from "react";

function InterviewPage({ questions, role, level }) {
  if (!questions || questions.length === 0) {
    return <p>Belum ada pertanyaan yang ditampilkan.</p>;
  }

  return (
    <div style={{ marginTop: "24px" }}>
      <h2>
        Pertanyaan untuk {role} ({level})
      </h2>
      <ol>
        {questions.map((q, index) => (
          <li key={q.id ?? index} style={{ marginBottom: "8px" }}>
            {q.question}
            {typeof q.score === "number" && (
              <span style={{ color: "#888", fontSize: "0.8rem" }}>
                {" "}
                (score: {q.score.toFixed(3)})
              </span>
            )}
          </li>
        ))}
      </ol>
    </div>
  );
}

export default InterviewPage;
