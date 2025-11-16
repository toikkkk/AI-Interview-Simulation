import React from "react";

function DescriptionInput({ value, onChange }) {
  return (
    <div style={{ marginBottom: "16px" }}>
      <label style={{ fontWeight: "bold", display: "block", marginBottom: 4 }}>
        Deskripsi pengalamanmu (CV singkat)
      </label>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        rows={5}
        style={{ width: "100%", maxWidth: "600px", padding: "8px" }}
        placeholder="Contoh: Saya pernah membuat dashboard penjualan, analisis data bisnis dengan SQL dan Excel..."
      />
    </div>
  );
}

export default DescriptionInput;
