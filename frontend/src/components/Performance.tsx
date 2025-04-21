import React, { useState, useEffect, useCallback } from 'react';
import './Performance.css';
import { getApiUrl } from '../apiConfig';

interface Metrics {
  training: {
    epochs_completed: number;
    final_accuracy: number;
    final_loss: number;
  };
  validation: {
    final_accuracy: number;
    final_loss: number;
  };
  testing: {
    accuracy: number;
    loss: number;
  };
  parameters: {
    img_height: number;
    img_width: number;
    batch_size: number;
    learning_rate: number;
    max_epochs: number;
  };
}

interface TrainingJob {
  status: string;
  started_at: string;
  completed_at?: string;
  error?: string;
  progress?: number;
}

const Performance: React.FC = () => {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [retraining, setRetraining] = useState<boolean>(false);
  const [trainingJob, setTrainingJob] = useState<TrainingJob | null>(null);
  const [trainingJobId, setTrainingJobId] = useState<string | null>(null);
  
  const fetchMetricsData = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(getApiUrl('metrics'));
      
      if (!response.ok) {
        if (response.status === 404) {
          setError('No metrics data available yet. Train the model first!');
          setLoading(false);
          return;
        }
        throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      setMetrics(data);
    } catch (err) {
      setError(`Error fetching metrics data: ${err instanceof Error ? err.message : 'Unknown error occurred'}`);
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchTrainingStatus = useCallback(async () => {
    if (!trainingJobId) return;

    try {
      const response = await fetch(getApiUrl(`training-status/${trainingJobId}`));
      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      // Simulate progress for demonstration
      const simulatedProgress = data.status === 'running' 
        ? Math.min((Date.now() - new Date(data.started_at).getTime()) / (60 * 1000) * 20, 95)
        : data.status === 'completed' ? 100 : 0;
        
      setTrainingJob({
        ...data,
        progress: simulatedProgress
      });
      
      // If training is complete or failed, stop polling
      if (data.status === 'completed' || data.status === 'failed') {
        setRetraining(false);
        setTrainingJobId(null);
        // Refresh metrics data if training completed successfully
        if (data.status === 'completed') {
          fetchMetricsData();
        }
      }
    } catch (err) {
      console.error('Error fetching training status:', err);
      setRetraining(false);
    }
  }, [trainingJobId, fetchMetricsData]);
  
  const handleRetrainModel = async () => {
    setRetraining(true);
    setTrainingJob({
      status: 'starting',
      started_at: new Date().toISOString(),
      progress: 0
    });
    setError(null);
    
    try {
      const response = await fetch(getApiUrl('retrain'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ force: true }),
      });
      
      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      setTrainingJobId(data.job_id);
      setTrainingJob({
        status: 'running',
        started_at: new Date().toISOString(),
        progress: 5 // Start with a small progress value
      });
    } catch (err) {
      setError(`Error starting model retraining: ${err instanceof Error ? err.message : 'Unknown error occurred'}`);
      setRetraining(false);
    }
  };
  
  // Fetch data on first load
  useEffect(() => {
    fetchMetricsData();
    
    // Set up polling every 30 seconds
    const intervalId = setInterval(fetchMetricsData, 30000);
    
    // Clean up on unmount
    return () => clearInterval(intervalId);
  }, []);
  
  // Poll for training status when a job is running
  useEffect(() => {
    if (retraining && trainingJobId) {
      const intervalId = setInterval(fetchTrainingStatus, 2000);
      
      // Clean up interval on unmount or when retraining is done
      return () => clearInterval(intervalId);
    }
  }, [retraining, trainingJobId, fetchTrainingStatus]);
  
  // Format date
  const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = {
      year: 'numeric', month: 'short', day: 'numeric',
      hour: '2-digit', minute: '2-digit', second: '2-digit'
    };
    return new Date(dateString).toLocaleString(undefined, options);
  };
  
  // Format percentage
  const formatPercentage = (value: number) => {
    return `${(value * 100).toFixed(2)}%`;
  };
  
  return (
    <div className="performance-container">
      <h2>Model Performance Dashboard</h2>
      
      <div className="action-buttons">
        <button onClick={fetchMetricsData} className="refresh-button">
          Refresh Metrics
        </button>
        
        <button 
          onClick={handleRetrainModel} 
          className="retrain-button"
          disabled={retraining}
        >
          {retraining ? 'Retraining in progress...' : 'Retrain Model'}
        </button>
      </div>
      
      {trainingJob && (
        <div className={`training-status ${trainingJob.status}`}>
          <h3>Training Status: <span className={trainingJob.status}>{trainingJob.status}</span></h3>
          
          <div className="progress-container">
            <div 
              className="progress-bar" 
              style={{ width: `${trainingJob.progress || 0}%` }}
            >
              <span className="progress-text">{Math.round(trainingJob.progress || 0)}%</span>
            </div>
          </div>
          
          {trainingJob.started_at && <p>Started: {formatDate(trainingJob.started_at)}</p>}
          {trainingJob.completed_at && <p>Completed: {formatDate(trainingJob.completed_at)}</p>}
          {trainingJob.error && <p className="error">Error: {trainingJob.error}</p>}
        </div>
      )}
      
      {loading && <div className="loading">Loading metrics data...</div>}
      {error && <div className="error-message">{error}</div>}
      
      {metrics && (
        <div className="dashboard">
          <div className="metrics-grid">
            <div className="metric-card">
              <h3>Training Accuracy</h3>
              <div className="metric-value">{formatPercentage(metrics.training.final_accuracy)}</div>
            </div>
            
            <div className="metric-card">
              <h3>Validation Accuracy</h3>
              <div className="metric-value">{formatPercentage(metrics.validation.final_accuracy)}</div>
            </div>
            
            <div className="metric-card">
              <h3>Test Accuracy</h3>
              <div className="metric-value">{formatPercentage(metrics.testing.accuracy)}</div>
            </div>
            
            <div className="metric-card">
              <h3>Epochs Completed</h3>
              <div className="metric-value">{metrics.training.epochs_completed} / {metrics.parameters.max_epochs}</div>
            </div>
          </div>
          
          <div className="metrics-grid">
            <div className="metric-card">
              <h3>Training Loss</h3>
              <div className="metric-value">{metrics.training.final_loss.toFixed(4)}</div>
            </div>
            
            <div className="metric-card">
              <h3>Validation Loss</h3>
              <div className="metric-value">{metrics.validation.final_loss.toFixed(4)}</div>
            </div>
            
            <div className="metric-card">
              <h3>Test Loss</h3>
              <div className="metric-value">{metrics.testing.loss.toFixed(4)}</div>
            </div>
            
            <div className="metric-card">
              <h3>Batch Size</h3>
              <div className="metric-value">{metrics.parameters.batch_size}</div>
            </div>
          </div>
          
          <div className="parameters-section">
            <h3>Model Parameters</h3>
            <div className="parameters-grid">
              <div className="parameter-item">
                <span className="parameter-label">Image Size:</span>
                <span className="parameter-value">{metrics.parameters.img_width} x {metrics.parameters.img_height}</span>
              </div>
              <div className="parameter-item">
                <span className="parameter-label">Learning Rate:</span>
                <span className="parameter-value">{metrics.parameters.learning_rate}</span>
              </div>
              <div className="parameter-item">
                <span className="parameter-label">Max Epochs:</span>
                <span className="parameter-value">{metrics.parameters.max_epochs}</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Performance; 