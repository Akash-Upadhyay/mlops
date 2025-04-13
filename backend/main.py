from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import uvicorn
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel

# Add the project root to path so we can import from ml_part
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ml_part import config

app = FastAPI(title="Cat vs Dog Classifier API")

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow React dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Load the model on startup
model = None

# Store prediction data for performance tracking
class Prediction(BaseModel):
    id: str
    timestamp: str
    filename: str
    prediction: str
    confidence: float
    processing_time: float
    ground_truth: Optional[str] = None

# In-memory storage for predictions (in a production app, this would be a database)
predictions: List[Prediction] = []

# Performance metrics
class ModelPerformance(BaseModel):
    total_predictions: int
    avg_confidence: float
    avg_processing_time: float
    class_distribution: Dict[str, int]
    recent_predictions: List[Prediction]
    accuracy: Optional[float] = None

class FeedbackRequest(BaseModel):
    prediction_id: str
    ground_truth: str

@app.on_event("startup")
async def startup_event():
    global model
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                             "ml_part", "checkpoints", "model.h5")
    if not os.path.exists(model_path):
        raise RuntimeError(f"Model file not found at {model_path}")
    
    print(f"Loading model from {model_path}")
    model = tf.keras.models.load_model(model_path)
    print("Model loaded successfully")

def preprocess_image(image):
    """
    Preprocess the image to be compatible with the model.
    """
    # Resize image
    image = image.resize((config.IMG_WIDTH, config.IMG_HEIGHT))
    
    # Convert image to array and normalize
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = img_array / 255.0  # Normalize to [0,1]
    
    # Add batch dimension
    img_array = tf.expand_dims(img_array, 0)
    
    return img_array

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """
    Predict whether an uploaded image is a cat or a dog.
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Validate file
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        start_time = time.time()
        
        # Read and preprocess the image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        processed_image = preprocess_image(image)
        
        # Make prediction
        prediction = model.predict(processed_image)[0][0]
        
        # Interpret results (sigmoid output: 0 = cat, 1 = dog)
        is_dog = prediction > 0.5
        animal_class = "dog" if is_dog else "cat"
        confidence = float(prediction) if is_dog else float(1 - prediction)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Store prediction data
        prediction_data = Prediction(
            id=f"pred_{len(predictions) + 1}",
            timestamp=datetime.now().isoformat(),
            filename=file.filename or "unknown",
            prediction=animal_class,
            confidence=confidence,
            processing_time=processing_time
        )
        predictions.append(prediction_data)
        
        # Keep only the most recent 100 predictions
        if len(predictions) > 100:
            predictions.pop(0)
        
        return {
            "id": prediction_data.id,
            "prediction": animal_class,
            "confidence": confidence,
            "raw_prediction": float(prediction),
            "processing_time": processing_time
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/performance/", response_model=ModelPerformance)
async def get_performance():
    """
    Get model performance metrics.
    """
    if not predictions:
        raise HTTPException(status_code=404, detail="No prediction data available yet")
    
    # Calculate metrics
    total_predictions = len(predictions)
    avg_confidence = sum(p.confidence for p in predictions) / total_predictions
    avg_processing_time = sum(p.processing_time for p in predictions) / total_predictions
    
    # Calculate class distribution
    class_distribution = {}
    for p in predictions:
        if p.prediction in class_distribution:
            class_distribution[p.prediction] += 1
        else:
            class_distribution[p.prediction] = 1
    
    # Calculate accuracy if ground truth is available
    accuracy = None
    predictions_with_ground_truth = [p for p in predictions if p.ground_truth is not None]
    if predictions_with_ground_truth:
        correct = sum(1 for p in predictions_with_ground_truth if p.prediction == p.ground_truth)
        accuracy = correct / len(predictions_with_ground_truth)
    
    # Get the 10 most recent predictions
    recent_predictions = predictions[-10:] if len(predictions) > 10 else predictions
    
    return ModelPerformance(
        total_predictions=total_predictions,
        avg_confidence=avg_confidence,
        avg_processing_time=avg_processing_time,
        class_distribution=class_distribution,
        recent_predictions=recent_predictions,
        accuracy=accuracy
    )

@app.post("/feedback/")
async def provide_feedback(feedback: FeedbackRequest):
    """
    Provide ground truth feedback for a prediction to calculate accuracy.
    """
    if feedback.ground_truth not in ["cat", "dog"]:
        raise HTTPException(status_code=400, detail="Ground truth must be 'cat' or 'dog'")
    
    # Find the prediction by ID
    for p in predictions:
        if p.id == feedback.prediction_id:
            p.ground_truth = feedback.ground_truth
            return {"message": "Feedback recorded successfully"}
    
    raise HTTPException(status_code=404, detail=f"Prediction with ID {feedback.prediction_id} not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 