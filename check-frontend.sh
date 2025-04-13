#!/bin/bash

echo "🧹 Șterg vechiul deployment și service..."
kubectl delete deployment frontend-service --ignore-not-found
kubectl delete service frontend-service --ignore-not-found

echo "🔧 Construiesc imaginea Docker corect din folderul ~/Desktop/licenta/app..."
cd ~/Desktop/licenta/app/frontend-services || exit 1
docker build -t adapirjol/frontend-service:latest .

echo "🚀 Reaplic frontend-deployment.yml..."
cd ~/Desktop/licenta/app/k8s || exit 1
kubectl apply -f frontend-deployment.yml

echo "⏳ Aștept 5 secunde pentru ca podul să pornească..."
sleep 5
kubectl get pods

echo "🔍 Loguri pentru deployment/frontend-service:"
kubectl logs deployment/frontend-service
