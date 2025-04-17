#!/bin/bash

# Build the Docker image
echo "Building the Docker image..."
docker build -t cat-dog-classifier:latest .

# Run the container
echo "Running the container..."
docker run -p 8000:8000 cat-dog-classifier:latest

# Instructions to use
echo ""
echo "The API is now available at http://localhost:8000"
echo "API documentation is available at http://localhost:8000/docs" 