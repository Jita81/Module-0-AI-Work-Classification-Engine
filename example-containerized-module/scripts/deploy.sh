#!/bin/bash
set -e

ENVIRONMENT=${1:-staging}
REGION=${2:-us-east-1}

echo "🚀 Deploying payment-processor to ${ENVIRONMENT}..."

# Update kubeconfig
aws eks update-kubeconfig --region ${REGION} --name ${ENVIRONMENT}-payment-processor-cluster

# Apply Kubernetes manifests
kubectl apply -f k8s/

# Update deployment image
if [ ! -z "${GITHUB_SHA}" ]; then
    kubectl set image deployment/payment-processor payment-processor=ghcr.io/${GITHUB_REPOSITORY}/payment-processor:${GITHUB_SHA}
else
    kubectl set image deployment/payment-processor payment-processor=payment-processor:latest
fi

# Wait for rollout
kubectl rollout status deployment/payment-processor --timeout=300s

# Get service URL
SERVICE_URL=$(kubectl get ingress payment-processor-ingress -o jsonpath='{.spec.rules[0].host}')
echo "✅ Deployment complete! Service available at: https://${SERVICE_URL}"

# Run health check
echo "🏥 Running health check..."
sleep 10
curl -f https://${SERVICE_URL}/health || echo "⚠️  Health check failed"
