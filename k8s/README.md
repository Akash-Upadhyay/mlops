# Kubernetes Deployment for Cat vs Dog Classifier

This directory contains the Kubernetes manifests for deploying the Cat vs Dog Classifier application.

## Components

- **Deployment**: Manages the application pods and ensures the specified number of replicas are running.
- **Service**: Exposes the application to the network.
- **ConfigMap**: Stores configuration data for the application.

## Deployment Instructions

### Prerequisites

- A working Kubernetes cluster
- `kubectl` configured to connect to your cluster
- Ansible with the `kubernetes.core` collection installed

### Manual Deployment

1. Apply the Kubernetes manifests:

```bash
kubectl create namespace catvsdog
kubectl apply -f configmap.yaml -n catvsdog
kubectl apply -f deployment.yaml -n catvsdog
kubectl apply -f service.yaml -n catvsdog
```

2. Verify the deployment:

```bash
kubectl get pods -n catvsdog
kubectl get services -n catvsdog
```

### Using Ansible

1. Install the required Ansible collection:

```bash
ansible-galaxy collection install kubernetes.core
```

2. Run the Ansible playbook:

```bash
ansible-playbook -i inventory.ini k8s-ansible-playbook.yml
```

### Local Testing with Minikube

1. Start Minikube:

```bash
./setup-minikube.sh
```

2. Deploy the application:

```bash
ansible-playbook -i inventory.ini k8s-ansible-playbook.yml
```

3. Access the application:

```bash
minikube service catvsdog-service -n catvsdog
```

## Scaling the Application

To scale the application to more replicas:

```bash
kubectl scale deployment catvsdog-deployment -n catvsdog --replicas=3
```

## Monitoring

You can monitor the application using:

```bash
kubectl get pods -n catvsdog -w
kubectl logs -f deployment/catvsdog-deployment -n catvsdog
``` 