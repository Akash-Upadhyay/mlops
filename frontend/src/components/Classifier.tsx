import React, { useState } from 'react';

const Classifier: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [prediction, setPrediction] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [feedbackSent, setFeedbackSent] = useState<boolean>(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files ? event.target.files[0] : null;
    setError(null);
    setPrediction(null);
    setFeedbackSent(false);
    
    if (file) {
      if (!file.type.startsWith('image/')) {
        setError('Please select an image file');
        setSelectedFile(null);
        setPreviewUrl(null);
        return;
      }
      
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result as string);
      };
      reader.readAsDataURL(file);
    } else {
      setSelectedFile(null);
      setPreviewUrl(null);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);
    setFeedbackSent(false);
    
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('/predict/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      setPrediction(result);
    } catch (err) {
      setError(`Error: ${err instanceof Error ? err.message : 'Unknown error occurred'}`);
    } finally {
      setLoading(false);
    }
  };

  const submitFeedback = async (isCat: boolean) => {
    if (!prediction || !prediction.id) {
      setError('No prediction data available to provide feedback for');
      return;
    }
    
    try {
      const response = await fetch('/feedback/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          prediction_id: prediction.id,
          ground_truth: isCat ? 'cat' : 'dog'
        })
      });
      
      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
      }
      
      setFeedbackSent(true);
    } catch (err) {
      setError(`Error sending feedback: ${err instanceof Error ? err.message : 'Unknown error occurred'}`);
    }
  };

  return (
    <div className="container">
      <form onSubmit={handleSubmit}>
        <div className="file-upload">
          <label htmlFor="file-input">
            Choose an image to classify
            <input
              id="file-input"
              type="file"
              accept="image/*"
              onChange={handleFileChange}
            />
          </label>
        </div>

        {previewUrl && (
          <div className="preview-container">
            <h3>Selected Image:</h3>
            <img src={previewUrl} alt="Preview" className="image-preview" />
          </div>
        )}

        <button 
          type="submit" 
          disabled={!selectedFile || loading} 
          className="submit-button"
        >
          {loading ? 'Classifying...' : 'Classify Image'}
        </button>
      </form>

      {error && <div className="error-message">{error}</div>}

      {prediction && (
        <div className="result-container">
          <h2>Result:</h2>
          <div className="prediction">
            <p className="prediction-text">
              This is a <span className="animal-type">{prediction.prediction}</span>
            </p>
            <p className="confidence">
              Confidence: {(prediction.confidence * 100).toFixed(2)}%
            </p>
            <p className="processing-time">
              Processing time: {prediction.processing_time.toFixed(3)}s
            </p>
          </div>
          
          {!feedbackSent && (
            <div className="feedback-container">
              <h4>Is this correct?</h4>
              <div className="feedback-buttons">
                <button 
                  onClick={() => submitFeedback(true)}
                  className="feedback-button"
                >
                  It's a cat
                </button>
                <button 
                  onClick={() => submitFeedback(false)}
                  className="feedback-button"
                >
                  It's a dog
                </button>
              </div>
            </div>
          )}
          
          {feedbackSent && (
            <div className="feedback-sent">
              Thank you for your feedback!
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Classifier; 