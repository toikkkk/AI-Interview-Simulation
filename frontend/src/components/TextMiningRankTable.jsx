import React from "react";

export default function TextMiningRankTable({ table }) {
  if (!table || table.length === 0) return null;

  return (
    <div style={{
      background: "white",
      border: "1px solid #e5e7eb",
      borderRadius: "12px",
      padding: "14px 16px",
      marginBottom: "16px"
    }}>
      <h3 style={{ marginBottom: "12px", fontWeight: 600 }}>
        📊 Detail Ranking Pertanyaan
      </h3>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#f3f4f6" }}>
            <th style={th}>Rank</th>
            <th style={th}>ID</th>
            <th style={th}>Pertanyaan</th>
            <th style={th}>TF-IDF</th>
            <th style={th}>Final Score</th>
          </tr>
        </thead>

        <tbody>
          {table.map((row, i) => (
            <tr key={i} style={{ borderBottom: "1px solid #e5e7eb" }}>
              <td style={td}>{row.rank}</td>
              <td style={td}>{row.id}</td>
              <td style={td}>{row.question}</td>
              <td style={td}>{row.tfidf_raw.toFixed(4)}</td>
              <td style={{ ...td, fontWeight: 600 }}>
                {row.final_score.toFixed(4)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const th = {
  padding: "10px",
  fontSize: "13px",
  textAlign: "left",
  fontWeight: 600
};

const td = {
  padding: "10px",
  fontSize: "13px",
  color: "#374151"
};
