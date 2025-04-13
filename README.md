# MLOps Project: Cat vs Dog Classifier

This project demonstrates an end-to-end MLOps implementation with three main components: machine learning model development, backend API service, and frontend web application.

## Directory Structure

```
mlops_project/
├── ml_part/                          # Machine learning model development
│   ├── config.py                     # Configuration parameters
│   ├── data_preprocessing.py         # Data download and preprocessing
│   ├── model.py                      # Model definition and training
│   ├── checkpoints/                  # Saved model files
│   │   └── model.h5                  # Trained model weights
│   ├── data/                         # Dataset directory
│   │   ├── train/                    # Training images
│   │   │   ├── cats/                 # Cat training images
│   │   │   └── dogs/                 # Dog training images
│   │   └── test/                     # Test images
│   │       ├── cats/                 # Cat test images
│   │       └── dogs/                 # Dog test images
│   ├── plots/                        # Training visualization plots
│   └── README.md                     # ML documentation
│
├── backend/                          # API services for model serving
│   ├── main.py                       # FastAPI application with endpoints
│   ├── requirements.txt              # Backend dependencies
│   └── README.md                     # Backend documentation
│
├── frontend/                         # User interface
│   ├── src/                          # React source code
│   │   ├── components/               # React components
│   │   │   ├── Classifier.tsx        # Image classification component
│   │   │   ├── Performance.tsx       # Model performance dashboard
│   │   │   └── Performance.css       # Dashboard styles
│   │   ├── App.tsx                   # Main application component
│   │   ├── App.css                   # Application styles
│   │   ├── index.tsx                 # React entry point
│   │   └── index.css                 # Global styles
│   ├── public/                       # Static public assets
│   ├── package.json                  # Frontend dependencies
│   ├── tsconfig.json                 # TypeScript configuration
│   └── README.md                     # Frontend documentation
│
├── activate_env.sh                   # Script to activate virtual environment
├── requirements.txt                  # Core Python dependencies
└── README.md                         # Main project documentation
```

## Environment Setup

This project uses a Python virtual environment located at `~/mlops_env` to manage dependencies for both the ML and backend components.

### Activating the Environment

To activate the virtual environment, run:

```bash
source activate_env.sh
```

### Dependencies

The main dependencies installed in the environment are:
- tensorflow
- numpy
- matplotlib
- requests
- scikit-learn
- pillow
- pillow-avif-plugin
- fastapi
- uvicorn

## Running the Project

### Step 1: Train the ML Model

```bash
cd ml_part
python data_preprocessing.py  # Download and prepare dataset
python model.py               # Train and evaluate model
```

### Step 2: Start the Backend API

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at http://localhost:8000 with Swagger documentation at http://localhost:8000/docs

### Step 3: Start the Frontend

```bash
cd frontend
npm start
```

The React application will be available at http://localhost:3000

## Key Features

1. **Machine Learning**
   - CNN-based cat vs dog image classifier
   - Data preprocessing and augmentation
   - Model training and evaluation

2. **Backend API**
   - Image upload and classification endpoint
   - Model performance tracking
   - User feedback collection

3. **Frontend Application**
   - Image upload and preview
   - Classification results display
   - Performance dashboard with metrics
   - User feedback submission

## API Endpoints

- `POST /predict/` - Upload and classify an image
- `GET /performance/` - Get model performance metrics
- `POST /feedback/` - Provide feedback on predictions 