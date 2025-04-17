#!/bin/bash

# Build the Docker image
echo "Building the frontend Docker image..."
docker build -t catvsdog-frontend:latest .

# Run the container
echo "Running the frontend container..."
docker run -d -p 3000:3000 --name catvsdog-frontend catvsdog-frontend:latest

# Instructions to use
echo ""
echo "The frontend is now available at http://localhost:3000"
echo "To connect with the backend, ensure both containers are running and on the same Docker network." 