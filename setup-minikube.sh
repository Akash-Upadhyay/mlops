#!/bin/bash

# Check if minikube is installed
if ! command -v minikube &> /dev/null; then
    echo "Minikube is not installed. Please install it first."
    echo "Visit: https://minikube.sigs.k8s.io/docs/start/"
    exit 1
fi

# Start minikube
echo "Starting Minikube..."
minikube start --driver=docker

# Enable ingress addon
echo "Enabling ingress addon..."
minikube addons enable ingress

# Configure kubectl to use minikube
echo "Configuring kubectl..."
kubectl config use-context minikube

# Verify connection
echo "Verifying connection to Kubernetes cluster..."
kubectl get nodes

echo "Minikube is ready for deployment!"
echo "To deploy the application, run: ansible-playbook -i inventory.ini k8s-ansible-playbook.yml"
echo "To access the Minikube dashboard, run: minikube dashboard" 