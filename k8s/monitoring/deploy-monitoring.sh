#!/bin/bash

# Script to deploy monitoring components for the Cat vs Dog Classifier

echo "Deploying Prometheus components..."
kubectl apply -f k8s/monitoring/prometheus-config.yaml
kubectl apply -f k8s/monitoring/prometheus-deployment.yaml

echo "Deploying Grafana components..."
kubectl apply -f k8s/monitoring/grafana-config.yaml
kubectl apply -f k8s/monitoring/grafana-dashboards.yaml
kubectl apply -f k8s/monitoring/grafana-deployment.yaml

# Wait for Prometheus to be ready before deploying ServiceMonitors
echo "Waiting for Prometheus to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/prometheus

echo "Deploying ServiceMonitors..."
kubectl apply -f k8s/monitoring/service-monitor.yaml

echo "Monitoring stack deployment complete!"
echo "Access Prometheus UI at: http://$(minikube ip):30900"
echo "Access Grafana UI at: http://$(minikube ip):30900"
echo "Grafana default credentials - username: admin, password: admin" 