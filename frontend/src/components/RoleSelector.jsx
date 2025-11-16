import React from "react";

const ROLE_OPTIONS = [
  { value: "Data_Analyst", label: "Data Analyst" },
  { value: "Data_Engineer", label: "Data Engineer" },
  { value: "ML_Engineer", label: "ML Engineer" },
];

function RoleSelector({ value, onChange }) {
  return (
    <div className="field-group">
      <label className="field-label">Pilih role</label>
      <p className="field-hint">
        Role ini akan memengaruhi fokus pertanyaan teknis dan studi kasus.
      </p>
      <select
        className="select-input"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        {ROLE_OPTIONS.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  );
}

export default RoleSelector;
