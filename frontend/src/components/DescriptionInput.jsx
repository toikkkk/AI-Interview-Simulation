import React from "react";

function DescriptionInput({ value, onChange }) {
  return (
    <div className="field-group">
      <label className="field-label">
        Deskripsi pengalamanmu (CV singkat)
      </label>
      <p className="field-hint">
        Contoh: &quot;2 tahun sebagai Data Analyst, sering membuat dashboard
        marketing, SQL, sedikit A/B testing.&quot;
      </p>
      <textarea
        className="textarea-input"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Tuliskan tech stack, jenis proyek, tanggung jawab utama..."
      />
    </div>
  );
}

export default DescriptionInput;
