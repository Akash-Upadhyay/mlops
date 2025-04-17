#!/bin/bash

echo "Starting the Cat vs Dog Classifier application..."
docker-compose up -d

echo ""
echo "Application services started:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000"
echo ""
echo "To view logs, use: docker-compose logs -f"
echo "To stop all services, use: docker-compose down" 