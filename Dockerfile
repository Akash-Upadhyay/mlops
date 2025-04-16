FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (minimized)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create required directories
RUN mkdir -p /app/ml_part/checkpoints

# Copy only the requirements for serving
COPY requirements-serve.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy only the necessary files
COPY backend/main.py /app/backend/
COPY backend/test_retrain.py /app/backend/
COPY ml_part/config.py /app/ml_part/
COPY ml_part/checkpoints/model.h5 /app/ml_part/checkpoints/
COPY ml_part/metrics.json /app/ml_part/

# Expose the port the app will run on
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=/app/ml_part/checkpoints/model.h5

# Command to run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
