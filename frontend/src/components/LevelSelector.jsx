import React from "react";

function LevelSelector({ value, onChange }) {
  return (
    <div className="field-group">
      <label className="field-label">Pilih level</label>
      <p className="field-hint">
        Junior cenderung fokus ke fundamental, Senior lebih banyak ke desain
        sistem dan ownership.
      </p>
      <div className="level-chips">
        {["Junior", "Senior"].map((lvl) => {
          const active = value === lvl;
          return (
            <label
              key={lvl}
              className={`level-chip ${active ? "active" : ""}`}
            >
              <input
                type="radio"
                name="level"
                value={lvl}
                checked={active}
                onChange={() => onChange(lvl)}
              />
              <span className="level-chip-indicator" />
              <span>{lvl}</span>
            </label>
          );
        })}
      </div>
    </div>
  );
}

export default LevelSelector;
