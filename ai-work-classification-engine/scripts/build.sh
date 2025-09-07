#!/bin/bash
set -e

echo "🏗️  Building ai-work-classification-engine..."

# Build Docker image
docker build -t ai-work-classification-engine:latest .

# Run security scan
echo "🔒 Running security scan..."
docker run --rm -v "$(pwd):/app" aquasec/trivy fs --security-checks vuln /app

# Run tests in container
echo "🧪 Running tests..."
docker run --rm ai-work-classification-engine:latest python -m pytest tests/ -v

# Tag for registry
if [ ! -z "${GITHUB_SHA}" ]; then
    docker tag ai-work-classification-engine:latest ghcr.io/${GITHUB_REPOSITORY}/ai-work-classification-engine:${GITHUB_SHA}
    echo "✅ Built and tagged ai-work-classification-engine:${GITHUB_SHA}"
else
    echo "✅ Built ai-work-classification-engine:latest"
fi
