import React, { useState, useEffect } from "react";
import "./DarkModeToggle.css";

const DarkModeToggle: React.FC = () => {
  const [isDarkMode, setIsDarkMode] = useState(() => {
    const saved = localStorage.getItem("darkMode");
    console.log("Initial load - saved value:", saved);
    return saved ? JSON.parse(saved) : false;
  });

  useEffect(() => {
    console.log("Component mounted, isDarkMode:", isDarkMode);
    if (isDarkMode) {
      document.body.classList.add("dark-mode");
    } else {
      document.body.classList.remove("dark-mode");
    }
  }, []);

  useEffect(() => {
    console.log("State changed to:", isDarkMode);
    localStorage.setItem("darkMode", JSON.stringify(isDarkMode));
    if (isDarkMode) {
      document.body.classList.add("dark-mode");
    } else {
      document.body.classList.remove("dark-mode");
    }
  }, [isDarkMode]);

  const toggleDarkMode = () => {
    console.log("Toggle clicked, current state:", isDarkMode);
    setIsDarkMode(!isDarkMode);
  };

  return (
    <button 
      className="dark-mode-toggle"
      onClick={toggleDarkMode}
      aria-label={`Switch to ${isDarkMode ? "light" : "dark"} mode`}
      data-testid="dark-mode-toggle"
    >
      {isDarkMode ? "" : ""}
    </button>
  );
};

export default DarkModeToggle;
