#!/bin/bash

# Stop and remove existing containers
echo "Stopping and removing existing containers..."
docker stop catvsdog-frontend catvsdog-backend 2>/dev/null || true
docker rm catvsdog-frontend catvsdog-backend 2>/dev/null || true

# Start the backend container
echo "Starting backend container..."
cd $(dirname $0)
docker build -t catvsdog-backend:local . && \
docker run -d --name catvsdog-backend -p 30800:8000 catvsdog-backend:local

# Update CORS configuration to allow all origins
echo "Updating CORS configuration..."
docker exec catvsdog-backend sed -i 's/allow_origins=\["http:\/\/localhost:3000"\]/allow_origins=["*"]/' /app/backend/main.py
docker restart catvsdog-backend

# Build and start the frontend container
echo "Building and starting frontend container..."
cd frontend
npm run build
docker run -d --name catvsdog-frontend -p 3001:80 \
  -v $(pwd)/build:/usr/share/nginx/html \
  -v $(pwd)/nginx.conf:/etc/nginx/conf.d/default.conf \
  --add-host=host.docker.internal:host-gateway \
  nginx:latest

# Print container status
echo
echo "Container status:"
docker ps | grep catvsdog

echo
echo "The application is now running:"
echo "- Frontend: http://localhost:3001"
echo "- Backend API: http://localhost:30800" 