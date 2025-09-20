import React from "react";
import DarkModeToggle from "./components/DarkModeToggle";
import logo from "./logo.svg";
import "./App.css";

function App() {
  return (
    <div className="App">
      <DarkModeToggle />
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h1>Enhanced Web Application</h1>
        <p>Automated enhancement pipeline demo</p>
        <p><strong>New Feature:</strong> Dark Mode Toggle (top-right corner)</p>
      </header>
    </div>
  );
}

export default App;
