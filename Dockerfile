# # Build stage
# FROM python:3.12-slim AS builder
# WORKDIR /app
# COPY requirements-serve.txt .
# RUN pip install --no-cache-dir --target=/app/deps -r requirements-serve.txt

# # Final stage
# FROM python:3.12-slim
# WORKDIR /app
# COPY --from=builder /app/deps /usr/local/lib/python3.12/site-packages/

# # Set working directory
# WORKDIR /app

# # Install system dependencies (minimized)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     curl \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # Create required directories
# RUN mkdir -p /app/ml_part/checkpoints

# # Copy only the requirements for serving
# COPY requirements-serve.txt /app/requirements-serve.txt

# # Install Python dependencies
# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir -r /app/requirements-serve.txt && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/* && \
#     find /usr/local -name '*.pyc' -delete

# # Copy only the necessary files
# COPY backend/main.py /app/backend/
# COPY backend/test_retrain.py /app/backend/
# COPY ml_part/config.py /app/ml_part/
# COPY ml_part/checkpoints/model.h5 /app/ml_part/checkpoints/
# COPY ml_part/metrics.json /app/ml_part/

# # Expose the port the app will run on
# EXPOSE 8000

# # Set environment variables
# ENV PYTHONUNBUFFERED=1
# ENV MODEL_PATH=/app/ml_part/checkpoints/model.h5

# # Command to run the application
# CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]



# Use official Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies including those required for Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements-serve.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-serve.txt && \
    # Make sure Pillow is installed with all features
    pip install --no-cache-dir --force-reinstall pillow==11.2.1

# Create necessary directories
RUN mkdir -p /app/ml_part/checkpoints

# Copy application code
COPY backend/main.py /app/backend/
COPY backend/test_retrain.py /app/backend/
COPY ml_part/config.py /app/ml_part/
COPY ml_part/checkpoints/model.h5 /app/ml_part/checkpoints/
COPY ml_part/metrics.json /app/ml_part/

# Expose the port the FastAPI app will run on
EXPOSE 8000

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=/app/ml_part/checkpoints/model.h5

# Start the application using uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

