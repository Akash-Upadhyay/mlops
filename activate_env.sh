#!/bin/bash

# This script activates the MLOps virtual environment
# Usage: source activate_env.sh

if [ -f ~/mlops_env/bin/activate ]; then
    source ~/mlops_env/bin/activate
    echo "MLOps virtual environment activated successfully!"
    echo "Python version: $(python --version)"
    echo "Pip version: $(pip --version)"
    echo ""
    echo "Available packages:"
    pip list | grep -E "tensorflow|numpy|matplotlib|requests|scikit-learn|pillow"
else
    echo "Error: Virtual environment not found at ~/mlops_env"
    echo "Please run the setup script first to create the environment."
fi 