import React from "react";

function RoleSelector({ value, onChange }) {
  return (
    <div style={{ marginBottom: "12px" }}>
      <label style={{ fontWeight: "bold", display: "block", marginBottom: 4 }}>
        Pilih Role
      </label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        style={{ padding: "8px", minWidth: "240px" }}
      >
        <option value="Data_Analyst">Data Analyst</option>
        <option value="Data_Engineer">Data Engineer</option>
        <option value="ML_Engineer">Machine Learning Engineer</option>
      </select>
    </div>
  );
}

export default RoleSelector;
