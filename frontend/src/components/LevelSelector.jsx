import React from "react";

function LevelSelector({ value, onChange }) {
  return (
    <div style={{ marginBottom: "12px" }}>
      <label style={{ fontWeight: "bold", display: "block", marginBottom: 4 }}>
        Pilih Level
      </label>
      <label style={{ marginRight: "12px" }}>
        <input
          type="radio"
          value="Junior"
          checked={value === "Junior"}
          onChange={(e) => onChange(e.target.value)}
        />{" "}
        Junior
      </label>
      <label>
        <input
          type="radio"
          value="Senior"
          checked={value === "Senior"}
          onChange={(e) => onChange(e.target.value)}
        />{" "}
        Senior
      </label>
    </div>
  );
}

export default LevelSelector;
