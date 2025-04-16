import React from 'react';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Cat vs Dog Classifier</h1>
        <p>
          Upload an image to classify whether it contains a cat or a dog.
        </p>
      </header>
      <main>
        <div className="upload-container">
          <h2>Upload Image</h2>
          <div className="upload-box">
            <p>Drag and drop an image here, or click to select a file</p>
          </div>
        </div>
        <div className="results-container">
          <h2>Results</h2>
          <div className="results-box">
            <p>Results will appear here after classification</p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App; 