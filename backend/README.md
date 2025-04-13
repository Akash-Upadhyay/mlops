# Backend

This repository contains the backend service of the MLOps project.

## API Endpoints

- **POST /predict/** - Upload an image for cat/dog classification
- **GET /performance/** - Get model performance metrics and statistics
- **POST /feedback/** - Provide feedback about prediction correctness

## Setup and Running

1. Ensure the ML model has been trained and saved in the `ml_part/checkpoints` directory.

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI application:
   ```bash
   python main.py
   ```

4. The API will be available at http://localhost:8000

5. You can access the Swagger documentation at http://localhost:8000/docs

## Using the API

### Classify an Image

To classify an image, send a POST request to `/predict/` with a form field named `file` containing the image:

```bash
curl -X POST "http://localhost:8000/predict/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@your_image.jpg"
```

The response will be a JSON object with the following fields:
- `id`: Unique identifier for the prediction
- `prediction`: "cat" or "dog"
- `confidence`: Confidence score between 0 and 1
- `raw_prediction`: Raw model output
- `processing_time`: Time taken to process the image in seconds

### Get Performance Metrics

To get model performance metrics, send a GET request to `/performance/`:

```bash
curl -X GET "http://localhost:8000/performance/" -H "accept: application/json"
```

### Provide Feedback

To provide feedback about a prediction, send a POST request to `/feedback/`:

```bash
curl -X POST "http://localhost:8000/feedback/" -H "accept: application/json" -H "Content-Type: application/json" -d '{"prediction_id": "pred_1", "ground_truth": "cat"}'
```

## Structure

This repository will include:
- API endpoints
- Database connections
- Model serving infrastructure
- Authentication and authorization 