import React, { useState, useEffect } from 'react';
import './Performance.css';

interface Prediction {
  id: string;
  timestamp: string;
  filename: string;
  prediction: string;
  confidence: number;
  processing_time: number;
  ground_truth: string | null;
}

interface ModelPerformance {
  total_predictions: number;
  avg_confidence: number;
  avg_processing_time: number;
  class_distribution: Record<string, number>;
  recent_predictions: Prediction[];
  accuracy: number | null;
}

const Performance: React.FC = () => {
  const [performance, setPerformance] = useState<ModelPerformance | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  const fetchPerformanceData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/performance/');
      
      if (!response.ok) {
        if (response.status === 404) {
          setError('No prediction data available yet. Make some predictions first!');
          setLoading(false);
          return;
        }
        throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      setPerformance(data);
    } catch (err) {
      setError(`Error fetching performance data: ${err instanceof Error ? err.message : 'Unknown error occurred'}`);
    } finally {
      setLoading(false);
    }
  };
  
  // Fetch data on first load
  useEffect(() => {
    fetchPerformanceData();
    
    // Set up polling every 10 seconds
    const intervalId = setInterval(fetchPerformanceData, 10000);
    
    // Clean up on unmount
    return () => clearInterval(intervalId);
  }, []);
  
  // Format date
  const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = {
      year: 'numeric', month: 'short', day: 'numeric',
      hour: '2-digit', minute: '2-digit', second: '2-digit'
    };
    return new Date(dateString).toLocaleString(undefined, options);
  };
  
  return (
    <div className="performance-container">
      <h2>Model Performance Dashboard</h2>
      
      <button onClick={fetchPerformanceData} className="refresh-button">
        Refresh Data
      </button>
      
      {loading && <div className="loading">Loading performance data...</div>}
      {error && <div className="error-message">{error}</div>}
      
      {performance && (
        <div className="dashboard">
          <div className="metrics-grid">
            <div className="metric-card">
              <h3>Total Predictions</h3>
              <div className="metric-value">{performance.total_predictions}</div>
            </div>
            
            <div className="metric-card">
              <h3>Average Confidence</h3>
              <div className="metric-value">{(performance.avg_confidence * 100).toFixed(2)}%</div>
            </div>
            
            <div className="metric-card">
              <h3>Average Processing Time</h3>
              <div className="metric-value">{performance.avg_processing_time.toFixed(3)}s</div>
            </div>
            
            {performance.accuracy !== null && (
              <div className="metric-card">
                <h3>Model Accuracy</h3>
                <div className="metric-value">{(performance.accuracy * 100).toFixed(2)}%</div>
              </div>
            )}
          </div>
          
          <div className="distribution-section">
            <h3>Class Distribution</h3>
            <div className="distribution-bars">
              {Object.entries(performance.class_distribution).map(([className, count]) => {
                const percentage = (count / performance.total_predictions) * 100;
                return (
                  <div key={className} className="distribution-item">
                    <div className="class-label">{className}</div>
                    <div className="bar-container">
                      <div 
                        className={`bar ${className === 'cat' ? 'cat-bar' : 'dog-bar'}`} 
                        style={{ width: `${percentage}%` }}
                      ></div>
                      <span className="percentage">{percentage.toFixed(1)}%</span>
                    </div>
                    <div className="count">{count} images</div>
                  </div>
                );
              })}
            </div>
          </div>
          
          <div className="recent-predictions">
            <h3>Recent Predictions</h3>
            <table className="predictions-table">
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Filename</th>
                  <th>Prediction</th>
                  <th>Confidence</th>
                  <th>Ground Truth</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {performance.recent_predictions.map((pred) => {
                  const isCorrect = pred.ground_truth === null 
                    ? null 
                    : pred.prediction === pred.ground_truth;
                  
                  return (
                    <tr key={pred.id}>
                      <td>{formatDate(pred.timestamp)}</td>
                      <td className="filename">{pred.filename}</td>
                      <td className={pred.prediction}>{pred.prediction}</td>
                      <td>{(pred.confidence * 100).toFixed(2)}%</td>
                      <td>{pred.ground_truth || 'Unknown'}</td>
                      <td>
                        {isCorrect === null ? (
                          <span className="unknown">Unknown</span>
                        ) : isCorrect ? (
                          <span className="correct">Correct</span>
                        ) : (
                          <span className="incorrect">Incorrect</span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default Performance; 