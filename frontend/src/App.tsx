import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import './App.css';
import RouterList from './components/RouterList';


const App: React.FC = () => {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <div className="container">
            <h1 className="App-title">DriveNets Dashboard</h1>
          </div>
        </header>
        <main className="App-main">
          <div className="container">
            <Switch>
              <Route exact path="/">
                <div className="home-container">
                  <h2>Network Routers</h2>
                  <RouterList />
                </div>
              </Route>
            </Switch>
          </div>
        </main>
      </div>
    </Router>
  );
};

export default App;
