# Monitoring Stack for Cat vs Dog Classifier

This directory contains configurations for deploying a basic monitoring stack with Prometheus and Grafana to monitor the Cat vs Dog Classifier application.

## Components

- **Prometheus**: Collects and stores metrics from the application
- **Grafana**: Visualizes metrics with interactive dashboards
- **ServiceMonitors**: Configure Prometheus to scrape metrics from your services

## Manual Deployment

To deploy the monitoring stack manually:

```bash
# From the project root directory
./k8s/monitoring/deploy-monitoring.sh
```

Or apply each component individually:

```bash
kubectl apply -f k8s/monitoring/prometheus-config.yaml
kubectl apply -f k8s/monitoring/prometheus-deployment.yaml
kubectl apply -f k8s/monitoring/grafana-config.yaml
kubectl apply -f k8s/monitoring/grafana-dashboards.yaml
kubectl apply -f k8s/monitoring/grafana-deployment.yaml
kubectl apply -f k8s/monitoring/service-monitor.yaml
```

## Automated Deployment

The monitoring stack is integrated into the main Ansible playbook. To deploy everything including monitoring:

```bash
ansible-playbook -i inventory.ini ansible-playbook.yml
```

## Accessing the Dashboards

After deployment:

- **Prometheus**: http://$(minikube ip):30900
- **Grafana**: http://$(minikube ip):30900
  - Username: admin
  - Password: admin

## Adding Custom Metrics

To expose custom metrics from your application:

1. For Python backend: Add Prometheus client library and expose metrics endpoints
2. For Frontend: Add Prometheus JavaScript client
3. Create new ServiceMonitor configurations as needed
4. Create custom Grafana dashboards for visualization 