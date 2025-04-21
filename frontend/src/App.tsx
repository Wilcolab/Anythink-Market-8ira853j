import React from 'react';
import './App.css';
import { RouterList } from './components/RouterList/RouterList';

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
          <RouterList />
        </div>
      </main>
    </div>
  );
}

export default App;
