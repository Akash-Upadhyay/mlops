FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    ssh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first for better caching
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip wheel setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application
COPY . /app/

# Set up DVC
RUN mkdir -p /root/.config/dvc
RUN mkdir -p /root/.dvc/tmp
RUN mkdir -p /root/.config/gcloud

# Move Google Drive credentials to the correct location
# Assumes gdrive-credentials.json exists in the project root
RUN if [ -f /app/gdrive-credentials.json ]; then \
    mkdir -p /root/.dvc/tmp/gdrive-user-creds && \
    cp /app/gdrive-credentials.json /root/.dvc/tmp/gdrive-user-creds/ && \
    echo "Copied Google Drive credentials"; \
    fi

# Set environment variables for authentication
ENV PYTHONUNBUFFERED=1
# If you have a service account JSON, set this
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/google-credentials.json

# Expose port for backend
EXPOSE 8000

# Script to handle authentication and startup
# RUN echo '#!/bin/bash \n\
# # Check if DVC remote is configured \n\
# if ! dvc remote list | grep -q "gdrive"; then \n\
#     echo "Setting up DVC remote with Google Drive..." \n\
#     dvc remote add -d gdrive gdrive://YOUR_FOLDER_ID \n\
# fi \n\
# \n\
# if [ "$1" = "backend" ]; then \n\
#     echo "Starting backend server..." \n\
#     cd /app/backend && python main.py \n\
# elif [ "$1" = "train" ]; then \n\
#     echo "Running DVC pipeline..." \n\
#     # Use existing credentials from the mounted JSON file \n\
#     dvc pull || echo "DVC pull failed, continuing anyway" \n\
#     dvc repro \n\
#     dvc push || echo "DVC push failed" \n\
# elif [ "$1" = "shell" ]; then \n\
#     echo "Starting shell..." \n\
#     /bin/bash \n\
# else \n\
#     echo "Usage: ./docker-entrypoint.sh [backend|train|shell]" \n\
#     echo "  backend: Start the FastAPI backend server" \n\
#     echo "  train: Run the DVC pipeline (pull, repro, push)" \n\
#     echo "  shell: Start a bash shell" \n\
#     exit 1 \n\
# fi' > /app/docker-entrypoint.sh

RUN sed -i 's|gdrive_service_account_json_file_path = .*|gdrive_service_account_json_file_path = /app/gdrive-credentials.json|' .dvc/config

RUN chmod +x /app/docker-entrypoint.sh

# Default command
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["backend"]

# Instructions for simplified setup:
# 1. Place your Google Drive credentials JSON file in the project root as "gdrive-credentials.json"
# 2. If using a service account, place it in project root as "google-credentials.json"
# 3. Replace YOUR_FOLDER_ID in the entrypoint script with your actual Google Drive folder ID
# 4. Build and run the container without needing interactive authentication
