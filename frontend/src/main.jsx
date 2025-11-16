import React from "react";
import ReactDOM from "react-dom/client";
import LandingPage from "./pages/LandingPage.jsx";
import "./styles.css";

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <div className="app-root">
      <div className="app-shell">
        <LandingPage />
      </div>
    </div>
  </React.StrictMode>
);