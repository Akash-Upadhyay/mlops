# Nginx Ingress Controller Setup for Cat vs Dog Classifier

This document explains how to use the Nginx Ingress Controller to manage HTTP traffic between the frontend and backend services in our Kubernetes cluster.

## What is Ingress?

Ingress is a Kubernetes resource that manages external access to services in a cluster, typically HTTP. Ingress can provide load balancing, SSL termination, and name-based virtual hosting.

## Our Ingress Configuration

We've set up an Ingress resource that:

1. Routes all `/api/*` requests to the backend service
2. Routes all other requests to the frontend service
3. Uses URL rewriting to strip the `/api` prefix before sending requests to the backend

## Prerequisites

1. A Kubernetes cluster (e.g., minikube, K3s)
2. The Nginx Ingress Controller installed

## Setup Instructions

### 1. Enable the Ingress Controller in Minikube

```bash
minikube addons enable ingress
```

### 2. Apply the Ingress Resource

```bash
kubectl apply -f k8s/ingress.yaml
```

### 3. Set up Local DNS (for local development)

Add an entry to your `/etc/hosts` file:

```
<minikube-ip> catvsdog.local
```

You can use our helper script to do this automatically:

```bash
./setup-ingress-hosts.sh
```

### 4. Access the Application

Once everything is set up, you can access the application at:

```
http://catvsdog.local
```

## Troubleshooting

1. **Backend API not accessible**: Check if the Ingress rewrite rules are working properly:
   ```bash
   kubectl get ing catvsdog-ingress -o yaml
   ```

2. **DNS not resolving**: Make sure your `/etc/hosts` file is correctly configured:
   ```bash
   cat /etc/hosts | grep catvsdog
   ```

3. **Ingress controller not working**: Check if the Ingress controller pods are running:
   ```bash
   kubectl get pods -n ingress-nginx
   ```

4. **Test the backend directly**:
   ```bash
   curl http://catvsdog.local/api/metrics/
   ```

## How It Works

1. When a request comes to `http://catvsdog.local/api/metrics/`:
   - The Ingress controller routes it to the backend service
   - The rewrite rule transforms `/api/metrics/` to `/metrics/`
   - The backend service receives the request at `/metrics/`

2. When a request comes to `http://catvsdog.local/`:
   - The Ingress controller routes it to the frontend service
   - The frontend service serves the React application

This setup eliminates the need for the frontend to know the internal service name of the backend, as all communication happens through the Ingress controller. 