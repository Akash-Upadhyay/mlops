# Frontend

This repository contains the frontend application of the MLOps project for cat vs dog classification.

## Features

- Upload images for classification
- Real-time image preview
- Display classification results with confidence scores
- Responsive design

## Setup and Running

1. Install the required dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

3. The application will be available at http://localhost:3000

## Usage

1. Make sure the backend API is running at http://localhost:8000
2. Click on "Choose an image to classify" to select an image file
3. View the image preview
4. Click "Classify Image" to send the image to the API
5. View the classification result and confidence score

## Environment Configuration

The application can be configured to connect to different backend API endpoints using environment variables:

1. Create a `.env` file in the frontend root directory
2. Set the backend API URL:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

For production deployments, you can set this to your production API URL.

## Docker Deployment

This application can be containerized using Docker:

1. Build the Docker image:
   ```bash
   docker build -t catvsdog-frontend .
   ```

2. Run the container with environment variables:
   ```bash
   docker run -p 3000:80 -e REACT_APP_API_URL=http://your-backend-api catvsdog-frontend
   ```

3. Alternatively, use docker-compose:
   ```bash
   docker-compose up -d
   ```

   This will start the frontend container and expose it on port 3000.

## Building for Production

To create a production build:

```bash
npm run build
```

The build files will be located in the `build` directory and can be served by any static file server.
