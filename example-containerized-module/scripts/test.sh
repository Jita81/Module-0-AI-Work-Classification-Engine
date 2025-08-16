#!/bin/bash
set -e

echo "🧪 Running comprehensive tests for payment-processor..."

# Start test environment
echo "🐳 Starting test environment..."
docker-compose -f docker-compose.yml up -d

# Wait for services
echo "⏳ Waiting for services to be ready..."
sleep 15

# Run tests
echo "🔬 Running unit tests..."
docker-compose exec -T payment-processor python -m pytest tests/unit/ -v

echo "🔗 Running integration tests..."
docker-compose exec -T payment-processor python -m pytest tests/integration/ -v

echo "📋 Running contract tests..."
docker-compose exec -T payment-processor python -m pytest tests/contract/ -v

# Generate coverage report
echo "📊 Generating coverage report..."
docker-compose exec -T payment-processor python -m pytest tests/ --cov=payment-processor --cov-report=html

# Cleanup
echo "🧹 Cleaning up..."
docker-compose down

echo "✅ All tests passed!"
