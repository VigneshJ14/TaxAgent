import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// Import pages (we'll create these next)
import HomePage from './pages/HomePage';
import UploadPage from './pages/UploadPage';
import ProcessingPage from './pages/ProcessingPage';
import ResultsPage from './pages/ResultsPage';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>AI Tax Return Agent</h1>
          <p>Automated Tax Document Processing & Form 1040 Generation</p>
        </header>
        
        <main className="App-main">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/upload" element={<UploadPage />} />
            <Route path="/processing" element={<ProcessingPage />} />
            <Route path="/results" element={<ResultsPage />} />
          </Routes>
        </main>
        
        <footer className="App-footer">
          <p>&copy; 2024 AI Tax Agent Prototype - For Educational Purposes Only</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
