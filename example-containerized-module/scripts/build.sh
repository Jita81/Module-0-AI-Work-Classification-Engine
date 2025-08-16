#!/bin/bash
set -e

echo "🏗️  Building payment-processor..."

# Build Docker image
docker build -t payment-processor:latest .

# Run security scan
echo "🔒 Running security scan..."
docker run --rm -v "$(pwd):/app" aquasec/trivy fs --security-checks vuln /app

# Run tests in container
echo "🧪 Running tests..."
docker run --rm payment-processor:latest python -m pytest tests/ -v

# Tag for registry
if [ ! -z "${GITHUB_SHA}" ]; then
    docker tag payment-processor:latest ghcr.io/${GITHUB_REPOSITORY}/payment-processor:${GITHUB_SHA}
    echo "✅ Built and tagged payment-processor:${GITHUB_SHA}"
else
    echo "✅ Built payment-processor:latest"
fi
