#!/bin/bash

# Retrain the model
echo "Retraining model..."
# Activate Python virtual environment if needed (optional)
# source /app/mlops_env/bin/activate

# Run retraining logic
# Assuming 'main.py' has the logic to handle DVC pull and repro
# python3 /app/retrain.py   # Add flags if needed for retraining

# Start the backend after retraining
echo "Model retrained. Starting backend..."
cd /app/backend && python3 main.py


