import React, { useState } from 'react';
import './App.css';
import Classifier from './components/Classifier';
import Performance from './components/Performance';

function App() {
  const [currentPage, setCurrentPage] = useState<'classifier' | 'performance'>('classifier');

  return (
    <div className="App">
      <header className="App-header">
        <h1>Cat vs Dog Classifier</h1>
        <nav className="navigation">
          <button 
            className={currentPage === 'classifier' ? 'active' : ''} 
            onClick={() => setCurrentPage('classifier')}
          >
            Classifier
          </button>
          <button 
            className={currentPage === 'performance' ? 'active' : ''} 
            onClick={() => setCurrentPage('performance')}
          >
            Performance
          </button>
        </nav>

        {currentPage === 'classifier' ? (
          <Classifier />
        ) : (
          <Performance />
        )}
      </header>
    </div>
  );
}

export default App;
