import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <div className="container">
          <h1 className="App-title">DriveNets Dashboard</h1>
        </div>
      </header>
      <main className="App-main">
        <div className="container">
          <div className="placeholder-container">
            <div className="placeholder-icon">🚀</div>
            <h2 className="placeholder-title">Coming Soon</h2>
            <div className="construction-line"></div>
            <p className="placeholder-text">
              We're working on something exciting! The DriveNets Dashboard is currently under development.
              Stay tuned for a powerful network management interface.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
