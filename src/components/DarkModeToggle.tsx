import React, { useState, useEffect } from 'react';
import './DarkModeToggle.css';

const DarkModeToggle: React.FC = () => {
  const [isDarkMode, setIsDarkMode] = useState<boolean>(() => {
    const saved = localStorage.getItem('darkMode');
    console.log('Initial load - saved value:', saved);
    return saved ? JSON.parse(saved) : false;
  });

  console.log('Component mounted, isDarkMode:', isDarkMode);

  useEffect(() => {
    localStorage.setItem('darkMode', JSON.stringify(isDarkMode));
    
    if (isDarkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
    
    console.log('State changed to:', isDarkMode);
  }, [isDarkMode]); // Fixed: Added isDarkMode to dependency array

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <button
      className="dark-mode-toggle"
      onClick={toggleDarkMode}
      aria-label={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
      data-testid="dark-mode-toggle"
    >
      {isDarkMode ? '☀️' : '🌙'}
    </button>
  );
};

export default DarkModeToggle;