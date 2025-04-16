# Cat vs Dog Frontend

This is the frontend for the Cat vs Dog classifier application.

## Docker Setup

### Building the Docker Image

To build the Docker image for the frontend:

```bash
cd frontend
docker build -t mt2024013/catvsdog-frontend:latest .
```

### Running the Docker Container Locally

To run the Docker container locally:

```bash
docker run -p 3000:3000 -e BACKEND_SERVICE=http://localhost:8000 mt2024013/catvsdog-frontend:latest
```

### Push to Docker Hub

To push the Docker image to Docker Hub:

```bash
docker login
docker push mt2024013/catvsdog-frontend:latest
```

## Kubernetes Deployment

The frontend is deployed to Kubernetes using the manifests in the `k8s` directory.

```bash
kubectl apply -f k8s/frontend-deployment.yaml
```

## Local Development

To run the frontend locally for development:

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. To build the app:
```bash
npm run build
```

4. To run the API proxy server:
```bash
npm run serve
```

## Environment Variables

- `PORT`: The port on which the server runs (default: 3000)
- `BACKEND_SERVICE`: The URL of the backend service (default: http://catvsdog-service.catvsdog.svc.cluster.local:8000)

## Features

- Upload images for classification
- Real-time image preview
- Display classification results with confidence scores
- Responsive design

## Usage

1. Make sure the backend API is running at http://localhost:8000
2. Click on "Choose an image to classify" to select an image file
3. View the image preview
4. Click "Classify Image" to send the image to the API
5. View the classification result and confidence score

## Building for Production

To create a production build:

```bash
npm run build
```

The build files will be located in the `build` directory and can be served by any static file server.
