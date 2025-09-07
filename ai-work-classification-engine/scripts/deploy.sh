#!/bin/bash
set -e

ENVIRONMENT=${1:-staging}
REGION=${2:-us-east-1}

echo "🚀 Deploying ai-work-classification-engine to ${ENVIRONMENT}..."

# Update kubeconfig
aws eks update-kubeconfig --region ${REGION} --name ${ENVIRONMENT}-ai-work-classification-engine-cluster

# Apply Kubernetes manifests
kubectl apply -f k8s/

# Update deployment image
if [ ! -z "${GITHUB_SHA}" ]; then
    kubectl set image deployment/ai-work-classification-engine ai-work-classification-engine=ghcr.io/${GITHUB_REPOSITORY}/ai-work-classification-engine:${GITHUB_SHA}
else
    kubectl set image deployment/ai-work-classification-engine ai-work-classification-engine=ai-work-classification-engine:latest
fi

# Wait for rollout
kubectl rollout status deployment/ai-work-classification-engine --timeout=300s

# Get service URL
SERVICE_URL=$(kubectl get ingress ai-work-classification-engine-ingress -o jsonpath='{.spec.rules[0].host}')
echo "✅ Deployment complete! Service available at: https://${SERVICE_URL}"

# Run health check
echo "🏥 Running health check..."
sleep 10
curl -f https://${SERVICE_URL}/health || echo "⚠️  Health check failed"
