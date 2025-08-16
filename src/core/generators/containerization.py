"""
Containerization module for generating Docker, Kubernetes, and CI/CD files.

This module handles the generation of all infrastructure files needed for
containerized deployment of modules.
"""

import os
from pathlib import Path
from typing import Dict, Any


class ContainerizationGenerator:
    """Generates containerization and deployment infrastructure files"""
    
    def generate_all_files(self, module_path: Path, context: Dict[str, Any]):
        """Generate all containerization files"""
        
        # Generate Dockerfile
        dockerfile_content = self._generate_dockerfile(context)
        self._write_file(module_path / 'Dockerfile', dockerfile_content)
        
        # Generate docker-compose for local development
        docker_compose_content = self._generate_docker_compose(context)
        self._write_file(module_path / 'docker-compose.yml', docker_compose_content)
        
        # Generate Kubernetes manifests
        self._generate_kubernetes_manifests(module_path, context)
        
        # Generate CI/CD pipeline
        self._generate_cicd_pipeline(module_path, context)
        
        # Generate Terraform infrastructure
        self._generate_terraform_files(module_path, context)
        
        # Generate deployment scripts
        self._generate_deployment_scripts(module_path, context)
    
    def _write_file(self, file_path: Path, content: str):
        """Write content to file"""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
    
    def _generate_dockerfile(self, context: Dict[str, Any]) -> str:
        """Generate production-ready Dockerfile"""
        return f'''# Multi-stage Dockerfile for {context['module_name']}
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \\
    PYTHONDONTWRITEBYTECODE=1 \\
    PIP_NO_CACHE_DIR=1 \\
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim as production

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set environment variables
ENV PYTHONUNBUFFERED=1 \\
    PYTHONDONTWRITEBYTECODE=1 \\
    PATH="/home/appuser/.local/bin:$PATH"

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Create working directory and set ownership
WORKDIR /app
RUN chown appuser:appuser /app

# Copy dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["python", "-m", "uvicorn", "core:app", "--host", "0.0.0.0", "--port", "8000"]
'''
    
    def _generate_docker_compose(self, context: Dict[str, Any]) -> str:
        """Generate docker-compose.yml for local development"""
        module_name = context['module_name']
        module_type = context['module_type']
        
        # Base services for all modules
        services = f'''version: '3.8'

services:
  {module_name}:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
    volumes:
      - .:/app
      - /app/__pycache__
    depends_on:'''
        
        # Add dependencies based on module type
        dependencies = []
        if module_type in ['CORE', 'SUPPORTING']:
            dependencies.extend(['postgres', 'redis'])
        elif module_type == 'INTEGRATION':
            dependencies.extend(['redis'])  # For caching and rate limiting
        elif module_type == 'TECHNICAL':
            dependencies.extend(['postgres', 'redis'])
        
        for dep in dependencies:
            services += f'\\n      - {dep}'
        
        # Add database services if needed
        if 'postgres' in dependencies:
            services += f'''

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB={module_name}_dev
      - POSTGRES_USER=dev
      - POSTGRES_PASSWORD=dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:'''
        
        # Add Redis if needed
        if 'redis' in dependencies:
            services += '''

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

volumes:
  redis_data:'''
        
        return services
    
    def _generate_kubernetes_manifests(self, module_path: Path, context: Dict[str, Any]):
        """Generate Kubernetes deployment manifests"""
        module_name = context['module_name']
        
        # Deployment manifest
        deployment = f'''apiVersion: apps/v1
kind: Deployment
metadata:
  name: {module_name}
  labels:
    app: {module_name}
    version: "1.0.0"
    tier: {context['module_type'].lower()}
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: {module_name}
  template:
    metadata:
      labels:
        app: {module_name}
        version: "1.0.0"
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: {module_name}
        image: {module_name}:latest
        ports:
        - containerPort: 8000
          name: http
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: LOG_LEVEL
          value: "INFO"
        envFrom:
        - configMapRef:
            name: {module_name}-config
        - secretRef:
            name: {module_name}-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
'''
        self._write_file(module_path / 'k8s' / 'deployment.yaml', deployment)
        
        # Service manifest
        service = f'''apiVersion: v1
kind: Service
metadata:
  name: {module_name}
  labels:
    app: {module_name}
spec:
  selector:
    app: {module_name}
  ports:
  - port: 80
    targetPort: 8000
    name: http
  type: ClusterIP
'''
        self._write_file(module_path / 'k8s' / 'service.yaml', service)
        
        # ConfigMap
        configmap = f'''apiVersion: v1
kind: ConfigMap
metadata:
  name: {module_name}-config
data:
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "production"
  # Add module-specific configuration here
'''
        self._write_file(module_path / 'k8s' / 'configmap.yaml', configmap)
        
        # HorizontalPodAutoscaler
        hpa = f'''apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {module_name}-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {module_name}
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
'''
        self._write_file(module_path / 'k8s' / 'hpa.yaml', hpa)
        
        # Ingress
        ingress = f'''apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {module_name}-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  tls:
  - hosts:
    - {module_name}.yourdomain.com
    secretName: {module_name}-tls
  rules:
  - host: {module_name}.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {module_name}
            port:
              number: 80
'''
        self._write_file(module_path / 'k8s' / 'ingress.yaml', ingress)
    
    def _generate_cicd_pipeline(self, module_path: Path, context: Dict[str, Any]):
        """Generate GitHub Actions CI/CD pipeline"""
        module_name = context['module_name']
        
        # CI Pipeline
        ci_pipeline = f'''name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{{{ github.repository }}}}/{module_name}

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: {module_name}_test
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{{{ runner.os }}}}-pip-${{{{ hashFiles('**/requirements.txt') }}}}
        restore-keys: |
          ${{{{ runner.os }}}}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-asyncio
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov={module_name} --cov-report=xml --cov-report=html
        
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        
    - name: Security scan
      run: |
        pip install bandit safety
        bandit -r {module_name}/
        safety check

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
      
    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{{{ env.REGISTRY }}}}
        username: ${{{{ github.actor }}}}
        password: ${{{{ secrets.GITHUB_TOKEN }}}}
        
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{{{ env.REGISTRY }}}}/${{{{ env.IMAGE_NAME }}}}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=sha,prefix={{{{branch}}}}-
          
    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{{{ steps.meta.outputs.tags }}}}
        labels: ${{{{ steps.meta.outputs.labels }}}}
        cache-from: type=gha
        cache-to: type=gha,mode=max
'''
        self._write_file(module_path / '.github' / 'workflows' / 'ci.yml', ci_pipeline)
        
        # CD Pipeline
        cd_pipeline = f'''name: CD Pipeline

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{{{ github.repository }}}}/{module_name}

jobs:
  deploy-staging:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{{{ secrets.AWS_ACCESS_KEY_ID }}}}
        aws-secret-access-key: ${{{{ secrets.AWS_SECRET_ACCESS_KEY }}}}
        aws-region: us-east-1
        
    - name: Deploy to EKS staging
      run: |
        aws eks update-kubeconfig --region us-east-1 --name staging-cluster
        kubectl apply -f k8s/
        kubectl set image deployment/{module_name} {module_name}=${{{{ env.REGISTRY }}}}/${{{{ env.IMAGE_NAME }}}}:main-${{{{ github.sha }}}}
        kubectl rollout status deployment/{module_name} --timeout=300s

  deploy-production:
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    environment: production
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{{{ secrets.AWS_ACCESS_KEY_ID }}}}
        aws-secret-access-key: ${{{{ secrets.AWS_SECRET_ACCESS_KEY }}}}
        aws-region: us-east-1
        
    - name: Deploy to EKS production
      run: |
        aws eks update-kubeconfig --region us-east-1 --name production-cluster
        kubectl apply -f k8s/
        kubectl set image deployment/{module_name} {module_name}=${{{{ env.REGISTRY }}}}/${{{{ env.IMAGE_NAME }}}}:${{{{ github.ref_name }}}}
        kubectl rollout status deployment/{module_name} --timeout=300s
        
    - name: Run smoke tests
      run: |
        # Add smoke tests here
        curl -f https://{module_name}.yourdomain.com/health
'''
        self._write_file(module_path / '.github' / 'workflows' / 'cd.yml', cd_pipeline)
    
    def _generate_terraform_files(self, module_path: Path, context: Dict[str, Any]):
        """Generate Terraform infrastructure code"""
        module_name = context['module_name']
        
        # AWS Terraform main file (simplified)
        aws_main = f'''terraform {{
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
  required_version = ">= 1.0"
}}

provider "aws" {{
  region = var.aws_region
}}

# EKS Cluster
resource "aws_eks_cluster" "{module_name}_cluster" {{
  name     = "${{var.environment}}-{module_name}-cluster"
  role_arn = aws_iam_role.cluster_role.arn
  version  = "1.28"

  vpc_config {{
    subnet_ids = aws_subnet.private[*].id
    endpoint_private_access = true
    endpoint_public_access  = true
  }}

  depends_on = [
    aws_iam_role_policy_attachment.cluster_AmazonEKSClusterPolicy,
  ]
}}

# RDS Database
resource "aws_db_instance" "{module_name}_db" {{
  identifier     = "${{var.environment}}-{module_name}-db"
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.micro"
  
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_encrypted     = true
  
  db_name  = "{module_name.replace('-', '_')}"
  username = "dbadmin"
  password = var.db_password
  
  skip_final_snapshot = var.environment != "production"
  
  tags = {{
    Name        = "${{var.environment}}-{module_name}-db"
    Environment = var.environment
  }}
}}
'''
        self._write_file(module_path / 'terraform' / 'aws' / 'main.tf', aws_main)
        
        # Variables file
        variables = f'''variable "aws_region" {{
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}}

variable "environment" {{
  description = "Environment name"
  type        = string
  default     = "staging"
}}

variable "db_password" {{
  description = "Database password"
  type        = string
  sensitive   = true
}}
'''
        self._write_file(module_path / 'terraform' / 'aws' / 'variables.tf', variables)
        
        # Outputs file
        outputs = f'''output "cluster_name" {{
  description = "EKS cluster name"
  value       = aws_eks_cluster.{module_name}_cluster.name
}}

output "database_endpoint" {{
  description = "RDS database endpoint" 
  value       = aws_db_instance.{module_name}_db.endpoint
  sensitive   = true
}}
'''
        self._write_file(module_path / 'terraform' / 'aws' / 'outputs.tf', outputs)
        
        # Placeholder files
        self._write_file(module_path / 'terraform' / 'aws' / 'networking.tf', '# VPC and networking configuration')
        self._write_file(module_path / 'terraform' / 'aws' / 'iam.tf', '# IAM roles and policies')
        self._write_file(module_path / 'terraform' / 'aws' / 'security.tf', '# Security groups')
    
    def _generate_deployment_scripts(self, module_path: Path, context: Dict[str, Any]):
        """Generate deployment automation scripts"""
        module_name = context['module_name']
        
        # Build script
        build_script = f'''#!/bin/bash
set -e

echo "🏗️  Building {module_name}..."

# Build Docker image
docker build -t {module_name}:latest .

# Run security scan
echo "🔒 Running security scan..."
docker run --rm -v "$(pwd):/app" aquasec/trivy fs --security-checks vuln /app

# Run tests in container
echo "🧪 Running tests..."
docker run --rm {module_name}:latest python -m pytest tests/ -v

echo "✅ Built {module_name}:latest"
'''
        self._write_file(module_path / 'scripts' / 'build.sh', build_script)
        
        # Deploy script
        deploy_script = f'''#!/bin/bash
set -e

ENVIRONMENT=${{1:-staging}}
REGION=${{2:-us-east-1}}

echo "🚀 Deploying {module_name} to ${{ENVIRONMENT}}..."

# Update kubeconfig
aws eks update-kubeconfig --region ${{REGION}} --name ${{ENVIRONMENT}}-{module_name}-cluster

# Apply Kubernetes manifests
kubectl apply -f k8s/

# Update deployment image
kubectl set image deployment/{module_name} {module_name}={module_name}:latest

# Wait for rollout
kubectl rollout status deployment/{module_name} --timeout=300s

echo "✅ Deployment complete!"
'''
        self._write_file(module_path / 'scripts' / 'deploy.sh', deploy_script)
        
        # Test script
        test_script = f'''#!/bin/bash
set -e

echo "🧪 Running comprehensive tests for {module_name}..."

# Start test environment
echo "🐳 Starting test environment..."
docker-compose up -d

# Wait for services
echo "⏳ Waiting for services to be ready..."
sleep 15

# Run tests
echo "🔬 Running unit tests..."
docker-compose exec -T {module_name} python -m pytest tests/unit/ -v

echo "🔗 Running integration tests..."
docker-compose exec -T {module_name} python -m pytest tests/integration/ -v

# Cleanup
echo "🧹 Cleaning up..."
docker-compose down

echo "✅ All tests passed!"
'''
        self._write_file(module_path / 'scripts' / 'test.sh', test_script)
        
        # Make scripts executable
        import os
        for script in ['build.sh', 'deploy.sh', 'test.sh']:
            script_path = module_path / 'scripts' / script
            os.chmod(script_path, 0o755)
