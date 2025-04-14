import requests
import json
import time

BASE_URL = "http://localhost:8000"  # Change if your API is running on a different URL

def test_retrain():
    """
    Test the model retraining endpoint.
    """
    print("Testing model retraining...")
    
    # Make the retrain request
    response = requests.post(
        f"{BASE_URL}/retrain/",
        json={"force": True}  # Force retraining regardless of data changes
    )
    
    if response.status_code == 200:
        result = response.json()
        job_id = result.get("job_id")
        print(f"Retraining started. Job ID: {job_id}")
        print(f"Status: {result.get('status')}")
        print(f"Message: {result.get('message')}")
        
        # Poll for job status a few times
        for i in range(5):
            time.sleep(5)  # Wait 5 seconds between polls
            status_response = requests.get(f"{BASE_URL}/training-status/{job_id}")
            
            if status_response.status_code == 200:
                status = status_response.json()
                print(f"Current status: {status.get('status')}")
                
                if status.get("status") == "completed":
                    print("Training completed successfully!")
                    break
                elif status.get("status") == "failed":
                    print(f"Training failed: {status.get('error')}")
                    break
            else:
                print(f"Failed to get status: {status_response.text}")
    else:
        print(f"Failed to start retraining: {response.text}")

if __name__ == "__main__":
    test_retrain() 