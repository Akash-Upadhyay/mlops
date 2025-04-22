#!/bin/bash

# Get minikube IP address
MINIKUBE_IP=$(minikube ip || echo "127.0.0.1")

echo "Setting up ingress host entry for catvsdog.local"
echo "This will add an entry to /etc/hosts to point catvsdog.local to $MINIKUBE_IP"
echo "You'll need sudo privileges to modify /etc/hosts"

# Check if entry already exists
if grep -q "catvsdog.local" /etc/hosts; then
    echo "Updating existing entry for catvsdog.local"
    sudo sed -i "s/.*catvsdog.local/$MINIKUBE_IP catvsdog.local/" /etc/hosts
else
    echo "Adding new entry for catvsdog.local"
    echo "$MINIKUBE_IP catvsdog.local" | sudo tee -a /etc/hosts
fi

echo "Done. You can now access the application at http://catvsdog.local"
echo "Make sure you've enabled the ingress addon in minikube:"
echo "  minikube addons enable ingress"

# Check if ingress is enabled
if minikube addons list | grep -q "ingress.*enabled"; then
    echo "✅ Ingress addon is enabled"
else
    echo "❌ Ingress addon is not enabled. Enable it with:"
    echo "  minikube addons enable ingress"
fi

# Wait for ingress to be ready
echo "Checking for ingress controller readiness..."
kubectl get pods -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx --field-selector=status.phase=Running -o name || {
    echo "Ingress controller not found or not ready."
    echo "It might still be starting up. Check status with:"
    echo "  kubectl get pods -n ingress-nginx"
}

echo ""
echo "Testing connectivity to catvsdog.local:"
curl -I http://catvsdog.local || echo "Could not connect. It might take a minute for DNS changes to propagate." 