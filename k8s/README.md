# Kubernetes Deployment for Cat vs Dog Classifier

This directory contains Kubernetes manifests for deploying the Cat vs Dog Classifier application.

## Files

- `backend-deployment.yaml`: Deployment and Service for the backend API
- `frontend-deployment.yaml`: Deployment and Service for the frontend web application

## Manual Deployment

To deploy the application manually:

```bash
# Apply the backend deployment and service
kubectl apply -f backend-deployment.yaml

# Wait for backend to be ready
kubectl rollout status deployment/catvsdog-backend

# Apply the frontend deployment and service
kubectl apply -f frontend-deployment.yaml

# Wait for frontend to be ready
kubectl rollout status deployment/catvsdog-frontend

# Get the frontend service NodePort
kubectl get service catvsdog-frontend-service
```

## Using Ansible

You can also deploy using the provided Ansible playbook:

```bash
ansible-playbook -i inventory.ini k8s-ansible-playbook.yml
```

## Architecture

The deployment consists of:

1. **Backend Deployment**: Runs the ML model serving API
   - Image: `mt2024013/catvsdog:latest`
   - Exposed on port 8000 via ClusterIP service

2. **Frontend Deployment**: Serves the React web application
   - Image: `mt2024013/catvsdog-frontend:latest`
   - Exposed on port 80 with NodePort service
   - Configured to communicate with backend service

## Networking

- The frontend communicates with the backend using the Kubernetes service name
- The frontend is exposed externally via NodePort
- The backend is only accessible within the cluster

## Accessing the Application

After deployment, access the application at:

```
http://<node-ip>:<node-port>
```

Where `<node-port>` is the port assigned to the frontend service. 