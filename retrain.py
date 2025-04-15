#!/usr/bin/env python3
"""
Standalone script to retrain the model using the DVC pipeline.
Run this directly with: python retrain.py [--force]
"""

import os
import sys
import time
import argparse
import subprocess
from datetime import datetime

def run_dvc_training(force=False):
    """
    Run DVC pipeline to retrain the model.
    
    Args:
        force (bool): Whether to force retraining even if no changes detected
    
    Returns:
        dict: Training job status
    """
    try:
        # Ensure we're in the project root directory
        project_root = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_root)
        
        print(f"Starting model training at {datetime.now().isoformat()}")
        print(f"Working directory: {project_root}")
        print(f"Force mode: {'Enabled' if force else 'Disabled'}")
        
        job_status = {
            "status": "running",
            "started_at": datetime.now().isoformat()
        }
        
        # Pull data from DVC remote
        print("\n==== Pulling data from DVC remote ====")
        pull_process = subprocess.run(
            ["dvc", "pull"], 
            capture_output=True, 
            text=True, 
            check=False
        )
        
        if pull_process.returncode != 0:
            print(f"Warning: DVC pull failed, but continuing anyway")
            print(f"Error: {pull_process.stderr}")
        else:
            print("DVC pull successful")
        
        # Run DVC reproduce with or without force flag
        print("\n==== Running DVC pipeline ====")
        if force:
            print("Running with --force flag (will rerun all stages)")
            repro_process = subprocess.run(
                ["dvc", "repro", "--force"], 
                capture_output=True, 
                text=True, 
                check=False
            )
        else:
            print("Running without force flag (will only rerun changed stages)")
            repro_process = subprocess.run(
                ["dvc", "repro"], 
                capture_output=True, 
                text=True, 
                check=False
            )
        
        if repro_process.returncode != 0:
            print(f"Error: DVC reproduction failed")
            print(f"Error details: {repro_process.stderr}")
            job_status["status"] = "failed"
            job_status["error"] = repro_process.stderr
            return job_status
        else:
            print(repro_process.stdout)
            print("DVC reproduction successful")
        
        # Push changes back to DVC remote
        print("\n==== Pushing changes to DVC remote ====")
        push_process = subprocess.run(
            ["dvc", "push"], 
            capture_output=True, 
            text=True, 
            check=False
        )
        
        if push_process.returncode != 0:
            print(f"Warning: DVC push failed, but training was successful")
            print(f"Error: {push_process.stderr}")
        else:
            print("DVC push successful")
        
        # Update job status
        job_status["status"] = "completed"
        job_status["completed_at"] = datetime.now().isoformat()
        
        # Check if model file exists
        model_path = os.path.join(project_root, "ml_part", "checkpoints", "model.h5")
        if os.path.exists(model_path):
            print(f"\nModel saved successfully at: {model_path}")
        else:
            print(f"\nWarning: Model file not found at expected location: {model_path}")
        
        print(f"\nTraining completed at {datetime.now().isoformat()}")
        return job_status
        
    except Exception as e:
        error_msg = f"Error during training: {str(e)}"
        print(error_msg)
        return {
            "status": "failed",
            "error": error_msg
        }

def main():
    parser = argparse.ArgumentParser(description='Retrain the model using DVC pipeline')
    parser.add_argument('--force', action='store_true', help='Force rerun all pipeline stages')
    args = parser.parse_args()
    
    start_time = time.time()
    result = run_dvc_training(force=args.force)
    duration = time.time() - start_time
    
    print(f"\n{'=' * 50}")
    print(f" {'completed successfully' if result['status'] == 'completed' else 'failed'}")
    print(f"Total duration: {duration:.2f} seconds")
    print(f"Status: {result['status']}")
    if result['status'] == 'failed' and 'error' in result:
        print(f"Error: {result['error']}")
    print(f"{'=' * 50}")
    
    # Return exit code based on success/failure
    return 0 if result['status'] == 'completed' else 1

if __name__ == "__main__":
    sys.exit(main()) 