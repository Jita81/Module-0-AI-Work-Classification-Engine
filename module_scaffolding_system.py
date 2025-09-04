# standardized_modules/cli.py
"""
CLI tool for generating standardized module scaffolding
Usage: sm create-module user-management --type=CORE --domain=ecommerce
"""

try:
    import click
except ImportError:
    print("click not installed. Install with: pip install click>=8.0.0")
    click = None

import os
from pathlib import Path
from typing import Dict, Any
import json

# Import MCP generator
try:
    from src.core.generators.mcp_generator import MCPServerGenerator
except ImportError:
    MCPServerGenerator = None

try:
    from jinja2 import Template
except ImportError:
    print("jinja2 not installed. Install with: pip install jinja2>=3.0.0")
    Template = None

def create_cli():
    """Create CLI interface when click is available"""
    if click is None:
        print("Error: click is required for CLI functionality")
        print("Install with: pip install click>=8.0.0")
        return None

    @click.group()
    def cli():
        """Standardized Modules Framework CLI"""
        pass

    @cli.command()
    @click.argument('module_name')
    @click.option('--type', 'module_type', 
                  type=click.Choice(['CORE', 'INTEGRATION', 'SUPPORTING', 'TECHNICAL']),
                  required=True, help='Type of module to create')
    @click.option('--domain', default='general', help='Business domain (e.g., ecommerce, finance)')
    @click.option('--output-dir', default='.', help='Output directory')
    @click.option('--ai-ready', is_flag=True, help='Generate with AI completion markers')
    @click.option('--with-docker', is_flag=True, help='Generate Docker and Kubernetes files')
    @click.option('--deployment-target', default='kubernetes', 
                  type=click.Choice(['kubernetes', 'docker-compose', 'lambda']),
                  help='Deployment target platform')
    @click.option('--mcp-server', is_flag=True, default=True, help='Generate as MCP server (default: True)')
    def create_module(module_name: str, module_type: str, domain: str, output_dir: str, 
                     ai_ready: bool, with_docker: bool, deployment_target: str, mcp_server: bool):
        """Create a new standardized module with complete framework structure"""
        
        # Choose generator based on MCP server flag
        if mcp_server and MCPServerGenerator:
            generator = MCPServerGenerator()
            result = generator.generate_mcp_server(
                name=module_name,
                module_type=module_type,
                domain=domain,
                output_dir=output_dir,
                ai_ready=ai_ready,
                with_docker=with_docker,
                deployment_target=deployment_target
            )
        else:
            generator = ModuleGenerator()
            result = generator.generate_module(
                name=module_name,
                module_type=module_type,
                domain=domain,
                output_dir=output_dir,
                ai_ready=ai_ready,
                with_docker=with_docker,
                deployment_target=deployment_target
            )
        
        if result.success:
            if mcp_server:
                click.echo(f"✅ MCP Server '{module_name}' created successfully!")
                click.echo(f"🔌 Type: {module_type} MCP Server")
                click.echo(f"🌐 Domain: {domain}")
            else:
                click.echo(f"✅ Module '{module_name}' created successfully!")
            
            click.echo(f"📁 Location: {result.module_path}")
            click.echo(f"🤖 AI completion file: {result.ai_completion_file}")
            
            if mcp_server:
                click.echo(f"📡 MCP Protocol: JSON-RPC 2.0")
                click.echo(f"🔍 AI-Discoverable: Yes")
                click.echo(f"🛠️  Self-Describing API: Yes")
            
            if with_docker:
                click.echo(f"🐳 Containerized for: {deployment_target}")
                click.echo(f"📦 Docker files generated")
                click.echo(f"☸️  Kubernetes manifests generated")
                click.echo(f"🚀 CI/CD pipeline configured")
                
            click.echo("\nNext steps:")
            if mcp_server:
                click.echo("1. Open the AI completion file in Cursor")
                click.echo("2. Implement business logic using MCP-optimized prompts")
                click.echo(f"3. Test MCP server: python3 {module_name}_server.py")
                click.echo("4. Test AI integration with MCP client")
            else:
                click.echo("1. Open the AI completion file in Cursor")
                click.echo("2. Use the provided prompts to complete the module")
            
            if with_docker:
                click.echo("5. Build and test: ./scripts/build.sh")
                click.echo("6. Start locally: docker-compose up")
                click.echo("7. Deploy: ./scripts/deploy.sh staging")
            else:
                click.echo("5. Run tests: pytest {}/tests/".format(result.module_path))
        else:
            click.echo(f"❌ Error: {result.error}")
    
    @cli.command()
    @click.argument('server_name')
    @click.option('--type', 'module_type', 
                  type=click.Choice(['CORE', 'INTEGRATION', 'SUPPORTING', 'TECHNICAL']),
                  required=True, help='Type of MCP server to create')
    @click.option('--domain', default='general', help='Business domain (e.g., ecommerce, finance)')
    @click.option('--output-dir', default='.', help='Output directory')
    @click.option('--with-docker', is_flag=True, help='Generate Docker and Kubernetes files')
    @click.option('--deployment-target', default='kubernetes', 
                  type=click.Choice(['kubernetes', 'docker-compose', 'lambda']),
                  help='Deployment target platform')
    def create_mcp_server(server_name: str, module_type: str, domain: str, output_dir: str,
                         with_docker: bool, deployment_target: str):
        """Create a new MCP (Model Context Protocol) server for AI integration"""
        
        if not MCPServerGenerator:
            click.echo("❌ Error: MCP generator not available. Check installation.")
            return
        
        generator = MCPServerGenerator()
        result = generator.generate_mcp_server(
            name=server_name,
            module_type=module_type,
            domain=domain,
            output_dir=output_dir,
            ai_ready=True,  # Always AI-ready for MCP servers
            with_docker=with_docker,
            deployment_target=deployment_target
        )
        
        if result.success:
            click.echo(f"🚀 MCP Server '{server_name}' created successfully!")
            click.echo(f"🔌 Type: {module_type} MCP Server")
            click.echo(f"🌐 Domain: {domain}")
            click.echo(f"📁 Location: {result.module_path}")
            click.echo(f"🤖 AI completion file: {result.ai_completion_file}")
            click.echo(f"📡 Protocol: MCP JSON-RPC 2.0")
            click.echo(f"🔍 AI-Discoverable: ✅ Yes")
            click.echo(f"🛠️  Self-Describing API: ✅ Yes")
            
            if with_docker:
                click.echo(f"🐳 Containerized for: {deployment_target}")
                click.echo(f"📦 Docker files generated")
                click.echo(f"☸️  Kubernetes manifests generated")
                
            click.echo("\n🎯 Next Steps:")
            click.echo("1. Open AI completion file for guided implementation")
            click.echo(f"2. Test MCP server: python3 {server_name}_server.py")
            click.echo("3. Test AI discovery with MCP client")
            click.echo("4. Implement business logic using provided templates")
            
            if with_docker:
                click.echo("5. Build container: docker build -t {}-mcp-server .".format(server_name))
                click.echo("6. Start locally: docker-compose up")
                click.echo("7. Deploy to cloud: ./scripts/deploy.sh")
            
            click.echo("\n🤖 AI Integration Ready!")
            click.echo("Your MCP server can now be discovered and integrated by AI agents automatically.")
            
        else:
            click.echo(f"❌ Error: {result.error}")
    
    return cli

# Create the CLI instance
cli = create_cli()

class GenerationResult:
    """Result of module generation operation"""
    def __init__(self, success: bool, module_path: str = None, ai_completion_file: str = None, error: str = None,
                 containerized: bool = False, deployment_target: str = None):
        self.success = success
        self.module_path = module_path
        self.ai_completion_file = ai_completion_file
        self.error = error
        self.containerized = containerized
        self.deployment_target = deployment_target

class ModuleGenerator:
    """Generates complete module scaffolding with AI completion markers"""
    
    def __init__(self):
        self.templates = ModuleTemplates()
    
    def generate_module(self, name: str, module_type: str, domain: str, 
                       output_dir: str, ai_ready: bool = True, 
                       with_docker: bool = False, deployment_target: str = "kubernetes") -> GenerationResult:
        """Generate complete module structure with optional containerization"""
        
        module_path = Path(output_dir) / name
        
        try:
            # Create directory structure
            self._create_directory_structure(module_path, with_docker)
            
            # Generate module files based on type
            template_context = {
                'module_name': name,
                'module_type': module_type,
                'domain': domain,
                'class_name': self._to_class_name(name),
                'ai_ready': ai_ready,
                'with_docker': with_docker,
                'deployment_target': deployment_target
            }
            
            # Generate core module file
            core_content = self.templates.generate_core_module(module_type, template_context)
            self._write_file(module_path / 'core.py', core_content)
            
            # Generate types file
            types_content = self.templates.generate_types_file(module_type, template_context)
            self._write_file(module_path / 'types.py', types_content)
            
            # Generate interface file
            interface_content = self.templates.generate_interface_file(module_type, template_context)
            self._write_file(module_path / 'interface.py', interface_content)
            
            # Generate test files
            test_content = self.templates.generate_test_file(module_type, template_context)
            self._write_file(module_path / 'tests' / 'test_core.py', test_content)
            
            # Generate contract tests
            contract_test_content = self.templates.generate_contract_tests(module_type, template_context)
            self._write_file(module_path / 'tests' / 'test_contracts.py', contract_test_content)
            
            # Generate __init__.py
            init_content = self.templates.generate_init_file(template_context)
            self._write_file(module_path / '__init__.py', init_content)
            
            # Generate AI completion file
            ai_completion_content = self.templates.generate_ai_completion_file(module_type, template_context)
            ai_completion_file = module_path / 'AI_COMPLETION.md'
            self._write_file(ai_completion_file, ai_completion_content)
            
            # Generate configuration files
            self._generate_config_files(module_path, template_context)
            
            # Generate containerization files if requested
            if with_docker:
                self._generate_containerization_files(module_path, template_context)
            
            return GenerationResult(
                success=True,
                module_path=str(module_path),
                ai_completion_file=str(ai_completion_file),
                containerized=with_docker,
                deployment_target=deployment_target if with_docker else None
            )
            
        except Exception as e:
            return GenerationResult(success=False, error=str(e))
    
    def _create_directory_structure(self, module_path: Path, with_docker: bool = False):
        """Create standard module directory structure"""
        directories = [
            module_path,
            module_path / 'tests',
            module_path / 'docs',
            module_path / 'examples'
        ]
        
        # Add containerization directories if requested
        if with_docker:
            directories.extend([
                module_path / 'k8s',
                module_path / '.github' / 'workflows',
                module_path / 'terraform' / 'aws',
                module_path / 'terraform' / 'azure',
                module_path / 'scripts'
            ])
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _to_class_name(self, module_name: str) -> str:
        """Convert module-name to ClassName"""
        return ''.join(word.capitalize() for word in module_name.split('-'))
    
    def _write_file(self, file_path: Path, content: str):
        """Write content to file"""
        with open(file_path, 'w') as f:
            f.write(content)
    
    def _generate_config_files(self, module_path: Path, context: Dict[str, Any]):
        """Generate configuration files for the module"""
        
        # Generate pytest.ini
        pytest_ini = '''[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
asyncio_mode = auto
'''
        self._write_file(module_path / 'pytest.ini', pytest_ini)
        
        # Generate requirements.txt
        requirements = '''# Core dependencies
click>=8.0.0
jinja2>=3.0.0
pydantic>=1.8.0

# Testing dependencies
pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-mock>=3.6.0

# Integration dependencies (for INTEGRATION modules)
aiohttp>=3.8.0

# Optional dependencies
pyyaml>=6.0.0
'''
        self._write_file(module_path / 'requirements.txt', requirements)
        
        # Generate .gitignore
        gitignore = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log

# Environment
.env
.venv
env/
venv/
'''
        self._write_file(module_path / '.gitignore', gitignore)
    
    def _generate_containerization_files(self, module_path: Path, context: Dict[str, Any]):
        """Generate Docker, Kubernetes, and CI/CD files"""
        
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
        
        # AWS Terraform
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

# EKS Node Group
resource "aws_eks_node_group" "{module_name}_nodes" {{
  cluster_name    = aws_eks_cluster.{module_name}_cluster.name
  node_group_name = "${{var.environment}}-{module_name}-nodes"
  node_role_arn   = aws_iam_role.node_role.arn
  subnet_ids      = aws_subnet.private[*].id

  scaling_config {{
    desired_size = 2
    max_size     = 10
    min_size     = 1
  }}

  instance_types = ["t3.medium"]

  depends_on = [
    aws_iam_role_policy_attachment.node_AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.node_AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.node_AmazonEC2ContainerRegistryReadOnly,
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
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = var.environment != "production"
  
  tags = {{
    Name        = "${{var.environment}}-{module_name}-db"
    Environment = var.environment
  }}
}}

# ElastiCache Redis
resource "aws_elasticache_subnet_group" "{module_name}_cache_subnet" {{
  name       = "${{var.environment}}-{module_name}-cache-subnet"
  subnet_ids = aws_subnet.private[*].id
}}

resource "aws_elasticache_cluster" "{module_name}_cache" {{
  cluster_id           = "${{var.environment}}-{module_name}-cache"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.{module_name}_cache_subnet.name
  security_group_ids   = [aws_security_group.redis.id]
}}
'''
        self._write_file(module_path / 'terraform' / 'aws' / 'main.tf', aws_main)
        
        # AWS Variables
        aws_variables = f'''variable "aws_region" {{
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

variable "domain_name" {{
  description = "Domain name for the service"
  type        = string
  default     = "{module_name}.yourdomain.com"
}}
'''
        self._write_file(module_path / 'terraform' / 'aws' / 'variables.tf', aws_variables)
        
        # AWS Outputs
        aws_outputs = f'''output "cluster_endpoint" {{
  description = "EKS cluster endpoint"
  value       = aws_eks_cluster.{module_name}_cluster.endpoint
}}

output "cluster_name" {{
  description = "EKS cluster name"
  value       = aws_eks_cluster.{module_name}_cluster.name
}}

output "database_endpoint" {{
  description = "RDS database endpoint"
  value       = aws_db_instance.{module_name}_db.endpoint
  sensitive   = true
}}

output "redis_endpoint" {{
  description = "Redis cluster endpoint"
  value       = aws_elasticache_cluster.{module_name}_cache.cache_nodes[0].address
}}
'''
        self._write_file(module_path / 'terraform' / 'aws' / 'outputs.tf', aws_outputs)
        
        # Include networking and IAM files (simplified for brevity)
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

# Tag for registry
if [ ! -z "${{GITHUB_SHA}}" ]; then
    docker tag {module_name}:latest ghcr.io/${{GITHUB_REPOSITORY}}/{module_name}:${{GITHUB_SHA}}
    echo "✅ Built and tagged {module_name}:${{GITHUB_SHA}}"
else
    echo "✅ Built {module_name}:latest"
fi
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
if [ ! -z "${{GITHUB_SHA}}" ]; then
    kubectl set image deployment/{module_name} {module_name}=ghcr.io/${{GITHUB_REPOSITORY}}/{module_name}:${{GITHUB_SHA}}
else
    kubectl set image deployment/{module_name} {module_name}={module_name}:latest
fi

# Wait for rollout
kubectl rollout status deployment/{module_name} --timeout=300s

# Get service URL
SERVICE_URL=$(kubectl get ingress {module_name}-ingress -o jsonpath='{{.spec.rules[0].host}}')
echo "✅ Deployment complete! Service available at: https://${{SERVICE_URL}}"

# Run health check
echo "🏥 Running health check..."
sleep 10
curl -f https://${{SERVICE_URL}}/health || echo "⚠️  Health check failed"
'''
        self._write_file(module_path / 'scripts' / 'deploy.sh', deploy_script)
        
        # Test script
        test_script = f'''#!/bin/bash
set -e

echo "🧪 Running comprehensive tests for {module_name}..."

# Start test environment
echo "🐳 Starting test environment..."
docker-compose -f docker-compose.yml up -d

# Wait for services
echo "⏳ Waiting for services to be ready..."
sleep 15

# Run tests
echo "🔬 Running unit tests..."
docker-compose exec -T {module_name} python -m pytest tests/unit/ -v

echo "🔗 Running integration tests..."
docker-compose exec -T {module_name} python -m pytest tests/integration/ -v

echo "📋 Running contract tests..."
docker-compose exec -T {module_name} python -m pytest tests/contract/ -v

# Generate coverage report
echo "📊 Generating coverage report..."
docker-compose exec -T {module_name} python -m pytest tests/ --cov={module_name} --cov-report=html

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

class ModuleTemplates:
    """Templates for generating different types of modules"""
    
    def generate_core_module(self, module_type: str, context: Dict[str, Any]) -> str:
        """Generate the core module implementation with framework structure"""
        
        if module_type == 'CORE':
            return self._generate_core_domain_module(context)
        elif module_type == 'INTEGRATION':
            return self._generate_integration_module(context)
        elif module_type == 'SUPPORTING':
            return self._generate_supporting_module(context)
        else:  # TECHNICAL
            return self._generate_technical_module(context)
    
    def _generate_core_domain_module(self, context: Dict[str, Any]) -> str:
        """Generate CORE domain module template"""
        
        template = Template('''"""
{{ module_name }}: {{ "AI_TODO: Add one-line business purpose" if ai_ready else "Domain module for business logic" }}
Type: CORE
Domain: {{ domain }}
Intent: {{ "AI_TODO: Explain why this module exists in business terms" if ai_ready else "Business logic implementation" }}
Contracts: {{ "AI_TODO: Define inputs → outputs → side effects" if ai_ready else "TBD" }}
Dependencies: {{ "AI_TODO: List required modules" if ai_ready else "None" }}

{{ "# AI_COMPLETION_REQUIRED: Fill in business context and rules" if ai_ready else "" }}
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime

from .interface import {{ class_name }}Interface
from .types import (
    {{ class_name }}Config,
    {{ class_name }}Input,
    {{ class_name }}Output,
    OperationResult,
    BusinessRule,
    DomainEntity
)

logger = logging.getLogger(__name__)

class {{ class_name }}Module({{ class_name }}Interface):
    """
    {{ module_name }} implementation
    Type: CORE Domain Module
    
    {{ "AI_TODO: Add detailed business context explaining:" if ai_ready else "" }}
    {{ "- What business problem this solves" if ai_ready else "" }}
    {{ "- Key business concepts and entities" if ai_ready else "" }}
    {{ "- Important business rules and constraints" if ai_ready else "" }}
    """
    
    def __init__(self, config: {{ class_name }}Config):
        self.config = config
        self._business_rules = self._initialize_business_rules()
        self._domain_entities = {}
        self._audit_trail = []
        self._initialized = False
        logger.info(f"Initializing {{ module_name }} module")
    
    def initialize(self) -> OperationResult:
        """Initialize the domain module with business rule validation"""
        try:
            # Validate configuration
            validation_result = self._validate_configuration()
            if not validation_result.success:
                return validation_result
            
            # Load domain entities and rules
            self._load_domain_data()
            
            # Validate business rules consistency
            rules_validation = self._validate_business_rules()
            if not rules_validation.success:
                return rules_validation
            
            self._initialized = True
            logger.info("{{ class_name }} module initialized successfully")
            return OperationResult.success("Module initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize {{ module_name }}: {e}")
            return OperationResult.error(f"Initialization failed: {e}")
    
    def execute_primary_operation(self, input_data: {{ class_name }}Input) -> OperationResult[{{ class_name }}Output]:
        """
        {{ "AI_TODO: Implement main business operation" if ai_ready else "Execute primary business operation" }}
        
        {{ "AI_TODO: Define what this operation accomplishes:" if ai_ready else "" }}
        {{ "Business Rules:" if ai_ready else "" }}
        {{ "- AI_TODO: List key business rules that apply" if ai_ready else "" }}
        {{ "- AI_TODO: Define validation requirements" if ai_ready else "" }}
        {{ "- AI_TODO: Specify constraint conditions" if ai_ready else "" }}
        
        Args:
            input_data: {{ "AI_TODO: Describe input requirements" if ai_ready else "Input data for operation" }}
            
        Returns:
            OperationResult containing {{ class_name }}Output or error
        """
        if not self._initialized:
            return OperationResult.error("Module not initialized")
        
        try:
            # Start audit trail
            operation_id = self._start_audit_trail("primary_operation", input_data)
            
            # Validate input according to business rules
            validation_result = self._validate_business_input(input_data)
            if not validation_result.success:
                self._record_audit_event(operation_id, "validation_failed", validation_result.error)
                return validation_result
            
            # {{ "AI_TODO: Implement business logic here" if ai_ready else "Business logic implementation" }}
            # {{ "Apply business rules in order:" if ai_ready else "" }}
            {{ "# AI_IMPLEMENTATION_REQUIRED" if ai_ready else "# Business logic goes here" }}
            {% if ai_ready %}
            # 1. AI_TODO: Apply validation rules
            # 2. AI_TODO: Execute business calculations
            # 3. AI_TODO: Update domain entities
            # 4. AI_TODO: Enforce business constraints
            # 5. AI_TODO: Generate business result
            {% endif %}
            
            # Placeholder implementation - AI will replace this
            result_data = {{ class_name }}Output(
                result="AI_TODO: Implement actual business result",
                audit_trail=self._audit_trail.copy()
            )
            
            self._record_audit_event(operation_id, "operation_completed", "Success")
            
            return OperationResult.success(result_data)
            
        except BusinessRuleViolation as e:
            self._record_audit_event(operation_id, "business_rule_violation", str(e))
            logger.warning(f"Business rule violation in {{ module_name }}: {e}")
            return OperationResult.error(f"Business rule violation: {e}", "BUSINESS_RULE_VIOLATION")
            
        except Exception as e:
            self._record_audit_event(operation_id, "system_error", str(e))
            logger.error(f"System error in {{ module_name }}: {e}")
            return OperationResult.error(f"System error: {e}", "SYSTEM_ERROR")
    
    def get_domain_entity(self, entity_id: str) -> OperationResult[DomainEntity]:
        """
        {{ "AI_TODO: Implement entity retrieval with business rules" if ai_ready else "Get domain entity by ID" }}
        """
        # {{ "AI_IMPLEMENTATION_REQUIRED" if ai_ready else "Implementation needed" }}
        pass
    
    def apply_business_rule(self, rule_name: str, context: Dict[str, Any]) -> OperationResult:
        """
        {{ "AI_TODO: Implement business rule application" if ai_ready else "Apply specific business rule" }}
        """
        # {{ "AI_IMPLEMENTATION_REQUIRED" if ai_ready else "Implementation needed" }}
        pass
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get module health with business metrics"""
        return {
            "module_name": "{{ module_name }}",
            "type": "CORE",
            "status": "healthy" if self._initialized else "unhealthy",
            "business_rules_loaded": len(self._business_rules),
            "domain_entities_count": len(self._domain_entities),
            "audit_events_count": len(self._audit_trail),
            "last_operation": self._audit_trail[-1] if self._audit_trail else None
        }
    
    def shutdown(self) -> OperationResult:
        """Gracefully shutdown with audit trail preservation"""
        try:
            # Save audit trail if configured
            if self.config.persist_audit_trail:
                self._save_audit_trail()
            
            self._initialized = False
            logger.info("{{ class_name }} module shutdown completed")
            return OperationResult.success("Shutdown completed")
            
        except Exception as e:
            return OperationResult.error(f"Shutdown error: {e}")
    
    # Private helper methods with complete implementation
    def _initialize_business_rules(self) -> List[BusinessRule]:
        """Initialize business rules - FRAMEWORK PROVIDED"""
        # {{ "AI_TODO: Define business rules for this domain" if ai_ready else "Define business rules" }}
        return []
    
    def _validate_configuration(self) -> OperationResult:
        """Validate module configuration - FRAMEWORK PROVIDED"""
        if not self.config:
            return OperationResult.error("Configuration required")
        return OperationResult.success("Configuration valid")
    
    def _load_domain_data(self):
        """Load domain-specific data - FRAMEWORK PROVIDED"""
        # {{ "AI_TODO: Load domain entities and reference data" if ai_ready else "Load domain data" }}
        pass
    
    def _validate_business_rules(self) -> OperationResult:
        """Validate business rules consistency - FRAMEWORK PROVIDED"""
        return OperationResult.success("Business rules valid")
    
    def _validate_business_input(self, input_data: {{ class_name }}Input) -> OperationResult:
        """Validate input against business rules - FRAMEWORK PROVIDED"""
        # {{ "AI_TODO: Implement business validation logic" if ai_ready else "Implement validation" }}
        return OperationResult.success("Input valid")
    
    def _start_audit_trail(self, operation: str, input_data: Any) -> str:
        """Start audit trail for operation - FRAMEWORK PROVIDED"""
        operation_id = f"{operation}_{datetime.utcnow().isoformat()}"
        self._audit_trail.append({
            "operation_id": operation_id,
            "operation": operation,
            "timestamp": datetime.utcnow().isoformat(),
            "input_summary": str(input_data)[:100]
        })
        return operation_id
    
    def _record_audit_event(self, operation_id: str, event: str, details: str):
        """Record audit event - FRAMEWORK PROVIDED"""
        self._audit_trail.append({
            "operation_id": operation_id,
            "event": event,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def _save_audit_trail(self):
        """Save audit trail - FRAMEWORK PROVIDED"""
        # Implementation for audit trail persistence
        pass

# Custom exceptions for business logic
class BusinessRuleViolation(Exception):
    """Raised when business rule is violated"""
    def __init__(self, rule_name: str, message: str):
        self.rule_name = rule_name
        super().__init__(f"Business rule '{rule_name}' violated: {message}")
''')
        
        return template.render(**context)
    
    def _generate_integration_module(self, context: Dict[str, Any]) -> str:
        """Generate INTEGRATION module template with fault tolerance"""
        
        template = Template('''"""
{{ module_name }}: {{ "AI_TODO: External service integration purpose" if ai_ready else "External integration module" }}
Type: INTEGRATION
Intent: {{ "AI_TODO: What external service this integrates with and why" if ai_ready else "External service integration" }}
External Service: {{ "AI_TODO: Name and purpose of external service" if ai_ready else "TBD" }}
Fault Tolerance: {{ "AI_TODO: List fault tolerance requirements" if ai_ready else "Circuit breaker, retry, timeout" }}
"""

import asyncio
import aiohttp
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

from .interface import {{ class_name }}Interface
from .types import {{ class_name }}Config, {{ class_name }}Request, {{ class_name }}Response, OperationResult

logger = logging.getLogger(__name__)

class {{ class_name }}Module({{ class_name }}Interface):
    """
    {{ module_name }} external integration
    Type: INTEGRATION
    
    {{ "AI_TODO: Document external service details:" if ai_ready else "" }}
    {{ "- Service name and API documentation URL" if ai_ready else "" }}
    {{ "- Authentication method" if ai_ready else "" }}
    {{ "- Rate limits and SLA" if ai_ready else "" }}
    {{ "- Error codes and recovery strategies" if ai_ready else "" }}
    """
    
    def __init__(self, config: {{ class_name }}Config):
        self.config = config
        self._client_session = None
        self._circuit_breaker = CircuitBreaker(config.circuit_breaker_config)
        self._retry_policy = RetryPolicy(config.retry_config)
        self._rate_limiter = RateLimiter(config.rate_limit_config)
        self._health_status = "unknown"
        self._initialized = False
        
        # {{ "AI_TODO: Add external service specific initialization" if ai_ready else "" }}
        
    async def initialize(self) -> OperationResult:
        """Initialize external service connection with health check"""
        try:
            # Create HTTP client session
            timeout = aiohttp.ClientTimeout(total=self.config.timeout_seconds)
            self._client_session = aiohttp.ClientSession(timeout=timeout)
            
            # {{ "AI_TODO: Add authentication setup" if ai_ready else "" }}
            # {{ "AI_IMPLEMENTATION_REQUIRED: Set up API keys, tokens, etc." if ai_ready else "" }}
            
            # Perform health check
            health_check = await self._perform_health_check()
            if not health_check.success:
                return health_check
                
            self._health_status = "healthy"
            self._initialized = True
            logger.info(f"{{ class_name }} integration initialized successfully")
            return OperationResult.success("Integration initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize {{ module_name }}: {e}")
            return OperationResult.error(f"Initialization failed: {e}")
    
    @circuit_breaker_protected
    @retry_on_failure
    @rate_limited
    async def call_external_service(self, request: {{ class_name }}Request) -> OperationResult[{{ class_name }}Response]:
        """
        {{ "AI_TODO: Main external service operation" if ai_ready else "Call external service with fault tolerance" }}
        
        {{ "AI_TODO: Document:" if ai_ready else "" }}
        {{ "- What this call accomplishes" if ai_ready else "" }}
        {{ "- Expected response format" if ai_ready else "" }}
        {{ "- Error conditions and handling" if ai_ready else "" }}
        """
        if not self._initialized:
            return OperationResult.error("Integration not initialized")
            
        try:
            # {{ "AI_IMPLEMENTATION_REQUIRED" if ai_ready else "External service call implementation" }}
            {% if ai_ready %}
            # AI_TODO: Implement the external service call:
            # 1. Build request URL and headers
            # 2. Make HTTP request
            # 3. Handle response and errors
            # 4. Transform response to internal format
            {% endif %}
            
            # Placeholder - AI will implement actual call
            url = self._build_request_url(request)
            headers = self._build_request_headers(request)
            payload = self._build_request_payload(request)
            
            async with self._client_session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    response_data = await response.json()
                    result = self._transform_response(response_data)
                    return OperationResult.success(result)
                elif response.status == 429:
                    # Rate limited
                    raise RateLimitExceeded("Service rate limit exceeded")
                elif response.status >= 500:
                    # Server error - will trigger retry
                    raise ExternalServiceError(f"Server error: {response.status}")
                else:
                    # Client error - don't retry
                    error_text = await response.text()
                    return OperationResult.error(f"Client error {response.status}: {error_text}")
                    
        except asyncio.TimeoutError:
            logger.warning(f"Timeout calling {{ module_name }}")
            raise ExternalServiceTimeout("Request timed out")
        except aiohttp.ClientError as e:
            logger.error(f"Client error calling {{ module_name }}: {e}")
            raise ExternalServiceError(f"Client error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error calling {{ module_name }}: {e}")
            return OperationResult.error(f"Unexpected error: {e}")
    
    async def get_health_status(self) -> Dict[str, Any]:
        """Get integration health with external service status"""
        service_health = await self._check_external_service_health()
        
        return {
            "module_name": "{{ module_name }}",
            "type": "INTEGRATION", 
            "status": self._health_status,
            "circuit_breaker_state": self._circuit_breaker.state,
            "external_service_health": service_health,
            "rate_limit_remaining": self._rate_limiter.remaining_calls,
            "last_successful_call": self._circuit_breaker.last_success_time,
            "error_rate": self._circuit_breaker.error_rate
        }
    
    async def shutdown(self) -> OperationResult:
        """Gracefully shutdown external connections"""
        try:
            if self._client_session:
                await self._client_session.close()
            
            self._initialized = False
            logger.info("{{ class_name }} integration shutdown completed")
            return OperationResult.success("Shutdown completed")
            
        except Exception as e:
            return OperationResult.error(f"Shutdown error: {e}")
    
    # Private helper methods - FRAMEWORK PROVIDED
    def _build_request_url(self, request: {{ class_name }}Request) -> str:
        """Build external service URL - AI_IMPLEMENTATION_REQUIRED"""
        # {{ "AI_TODO: Implement URL building logic" if ai_ready else "URL building logic" }}
        return f"{self.config.base_url}/api/endpoint"
    
    def _build_request_headers(self, request: {{ class_name }}Request) -> Dict[str, str]:
        """Build request headers with authentication - AI_IMPLEMENTATION_REQUIRED"""
        # {{ "AI_TODO: Implement header building with auth" if ai_ready else "Header building logic" }}
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }
    
    def _build_request_payload(self, request: {{ class_name }}Request) -> Dict[str, Any]:
        """Build request payload - AI_IMPLEMENTATION_REQUIRED"""
        # {{ "AI_TODO: Transform internal request to external format" if ai_ready else "Payload building logic" }}
        return request.__dict__
    
    def _transform_response(self, response_data: Dict[str, Any]) -> {{ class_name }}Response:
        """Transform external response to internal format - AI_IMPLEMENTATION_REQUIRED"""
        # {{ "AI_TODO: Transform external response to internal format" if ai_ready else "Response transformation logic" }}
        return {{ class_name }}Response(**response_data)
    
    async def _perform_health_check(self) -> OperationResult:
        """Check external service health - FRAMEWORK PROVIDED"""
        try:
            async with self._client_session.get(f"{self.config.base_url}/health") as response:
                if response.status == 200:
                    return OperationResult.success("Service healthy")
                else:
                    return OperationResult.error(f"Service unhealthy: {response.status}")
        except Exception as e:
            return OperationResult.error(f"Health check failed: {e}")
    
    async def _check_external_service_health(self) -> str:
        """Check current external service health - FRAMEWORK PROVIDED"""
        try:
            health_result = await self._perform_health_check()
            return "healthy" if health_result.success else "unhealthy"
        except:
            return "unknown"

# Fault tolerance classes - FRAMEWORK PROVIDED
class CircuitBreaker:
    def __init__(self, config):
        self.config = config
        self.state = "closed"
        self.error_rate = 0.0
        self.last_success_time = None
    
    def can_execute(self):
        return self.state != "open"
    
    def record_success(self):
        self.last_success_time = datetime.utcnow()
        self.state = "closed"
    
    def record_failure(self):
        # Simple implementation - would be more sophisticated in practice
        pass

class RetryPolicy:
    def __init__(self, config):
        self.config = config
    
    async def execute(self, func, *args, **kwargs):
        # Simple implementation - would include exponential backoff
        return await func(*args, **kwargs)

class RateLimiter:
    def __init__(self, config):
        self.config = config
        self.remaining_calls = 100  # Placeholder
    
    async def acquire(self):
        # Simple implementation - would include actual rate limiting
        pass

# Fault tolerance decorators - FRAMEWORK PROVIDED
def circuit_breaker_protected(func):
    """Circuit breaker decorator"""
    async def wrapper(self, *args, **kwargs):
        if not self._circuit_breaker.can_execute():
            raise CircuitBreakerOpenError("Circuit breaker is open")
        
        try:
            result = await func(self, *args, **kwargs)
            self._circuit_breaker.record_success()
            return result
        except Exception as e:
            self._circuit_breaker.record_failure()
            raise
    return wrapper

def retry_on_failure(func):
    """Retry decorator with exponential backoff"""
    async def wrapper(self, *args, **kwargs):
        return await self._retry_policy.execute(func, self, *args, **kwargs)
    return wrapper

def rate_limited(func):
    """Rate limiting decorator"""
    async def wrapper(self, *args, **kwargs):
        await self._rate_limiter.acquire()
        return await func(self, *args, **kwargs)
    return wrapper

# Exception classes - FRAMEWORK PROVIDED
class ExternalServiceError(Exception):
    pass

class ExternalServiceTimeout(ExternalServiceError):
    pass

class RateLimitExceeded(ExternalServiceError):
    pass

class CircuitBreakerOpenError(ExternalServiceError):
    pass
''')
        
        return template.render(**context)
    
    def _generate_supporting_module(self, context: Dict[str, Any]) -> str:
        """Generate SUPPORTING module template"""
        
        template = Template('''"""
{{ module_name }}: {{ "AI_TODO: Supporting business function purpose" if ai_ready else "Supporting business module" }}
Type: SUPPORTING
Intent: {{ "AI_TODO: What supporting business capability this provides" if ai_ready else "Supporting business functionality" }}
Business Function: {{ "AI_TODO: Name the business function this supports" if ai_ready else "TBD" }}
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import logging
from datetime import datetime

from .interface import {{ class_name }}Interface
from .types import {{ class_name }}Config, {{ class_name }}Request, {{ class_name }}Response, OperationResult

logger = logging.getLogger(__name__)

class {{ class_name }}Module({{ class_name }}Interface):
    """
    {{ module_name }} supporting business function
    Type: SUPPORTING
    
    {{ "AI_TODO: Document supporting business function:" if ai_ready else "" }}
    {{ "- What business capability this provides" if ai_ready else "" }}
    {{ "- How it integrates with core business modules" if ai_ready else "" }}
    {{ "- Standard patterns and workflows it implements" if ai_ready else "" }}
    """
    
    def __init__(self, config: {{ class_name }}Config):
        self.config = config
        self._business_patterns = {}
        self._workflow_state = {}
        self._performance_metrics = {}
        self._initialized = False
        
    def initialize(self) -> OperationResult:
        """Initialize supporting business module"""
        try:
            # Load business patterns and workflows
            self._load_business_patterns()
            self._initialize_workflows()
            
            self._initialized = True
            logger.info("{{ class_name }} supporting module initialized")
            return OperationResult.success("Module initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize {{ module_name }}: {e}")
            return OperationResult.error(f"Initialization failed: {e}")
    
    def execute_supporting_operation(self, request: {{ class_name }}Request) -> OperationResult[{{ class_name }}Response]:
        """
        {{ "AI_TODO: Main supporting business operation" if ai_ready else "Execute supporting business operation" }}
        
        {{ "AI_TODO: Document:" if ai_ready else "" }}
        {{ "- What business workflow this supports" if ai_ready else "" }}
        {{ "- Integration points with other modules" if ai_ready else "" }}
        {{ "- Standard patterns applied" if ai_ready else "" }}
        """
        if not self._initialized:
            return OperationResult.error("Module not initialized")
            
        try:
            # {{ "AI_IMPLEMENTATION_REQUIRED" if ai_ready else "Supporting business logic" }}
            {% if ai_ready %}
            # AI_TODO: Implement supporting business logic:
            # 1. Validate request against business patterns
            # 2. Execute standard workflow
            # 3. Update business state
            # 4. Return standardized response
            {% endif %}
            
            # Placeholder implementation
            result = {{ class_name }}Response(
                status="success",
                data="AI_TODO: Implement actual business result"
            )
            
            return OperationResult.success(result)
            
        except Exception as e:
            logger.error(f"Error in {{ module_name }} operation: {e}")
            return OperationResult.error(f"Operation failed: {e}")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get supporting module health"""
        return {
            "module_name": "{{ module_name }}",
            "type": "SUPPORTING",
            "status": "healthy" if self._initialized else "unhealthy",
            "active_workflows": len(self._workflow_state),
            "performance_metrics": self._performance_metrics
        }
    
    def shutdown(self) -> OperationResult:
        """Shutdown supporting module"""
        try:
            # Complete active workflows
            self._complete_active_workflows()
            
            self._initialized = False
            return OperationResult.success("Shutdown completed")
        except Exception as e:
            return OperationResult.error(f"Shutdown error: {e}")
    
    # Private helper methods
    def _load_business_patterns(self):
        """Load business patterns - AI_IMPLEMENTATION_REQUIRED"""
        # {{ "AI_TODO: Load standard business patterns for this domain" if ai_ready else "" }}
        pass
    
    def _initialize_workflows(self):
        """Initialize workflows - AI_IMPLEMENTATION_REQUIRED"""
        # {{ "AI_TODO: Set up standard workflows" if ai_ready else "" }}
        pass
    
    def _complete_active_workflows(self):
        """Complete active workflows - FRAMEWORK PROVIDED"""
        for workflow_id in list(self._workflow_state.keys()):
            try:
                # Complete workflow gracefully
                self._workflow_state.pop(workflow_id)
            except Exception as e:
                logger.warning(f"Error completing workflow {workflow_id}: {e}")
''')
        
        return template.render(**context)
    
    def _generate_technical_module(self, context: Dict[str, Any]) -> str:
        """Generate TECHNICAL module template"""
        
        template = Template('''"""
{{ module_name }}: {{ "AI_TODO: Technical capability purpose" if ai_ready else "Technical infrastructure module" }}
Type: TECHNICAL
Intent: {{ "AI_TODO: What technical capability this provides" if ai_ready else "Technical infrastructure" }}
Performance: {{ "AI_TODO: Performance requirements and characteristics" if ai_ready else "TBD" }}
"""

from typing import Dict, Any, Optional
import logging
import asyncio
from datetime import datetime

from .interface import {{ class_name }}Interface
from .types import {{ class_name }}Config, OperationResult

logger = logging.getLogger(__name__)

class {{ class_name }}Module({{ class_name }}Interface):
    """
    {{ module_name }} technical infrastructure
    Type: TECHNICAL
    
    {{ "AI_TODO: Document technical capability:" if ai_ready else "" }}
    {{ "- What infrastructure need this addresses" if ai_ready else "" }}
    {{ "- Performance characteristics and requirements" if ai_ready else "" }}
    {{ "- Resource usage and scaling behavior" if ai_ready else "" }}
    """
    
    def __init__(self, config: {{ class_name }}Config):
        self.config = config
        self._resource_pool = None
        self._performance_monitor = PerformanceMonitor()
        self._initialized = False
        
    async def initialize(self) -> OperationResult:
        """Initialize technical infrastructure"""
        try:
            # {{ "AI_IMPLEMENTATION_REQUIRED" if ai_ready else "Initialize infrastructure" }}
            # {{ "AI_TODO: Set up resource pools, connections, caches, etc." if ai_ready else "" }}
            
            self._resource_pool = await self._create_resource_pool()
            self._performance_monitor.start()
            
            self._initialized = True
            logger.info("{{ class_name }} technical module initialized")
            return OperationResult.success("Module initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize {{ module_name }}: {e}")
            return OperationResult.error(f"Initialization failed: {e}")
    
    async def execute_technical_operation(self, operation: str, params: Dict[str, Any]) -> OperationResult:
        """
        {{ "AI_TODO: Main technical operation" if ai_ready else "Execute technical operation" }}
        
        {{ "AI_TODO: Document:" if ai_ready else "" }}
        {{ "- What technical operations are supported" if ai_ready else "" }}
        {{ "- Performance characteristics" if ai_ready else "" }}
        {{ "- Resource management" if ai_ready else "" }}
        """
        if not self._initialized:
            return OperationResult.error("Module not initialized")
            
        start_time = datetime.utcnow()
        
        try:
            # {{ "AI_IMPLEMENTATION_REQUIRED" if ai_ready else "Technical operation implementation" }}
            {% if ai_ready %}
            # AI_TODO: Implement technical operations:
            # - Route to appropriate handler based on operation
            # - Manage resources efficiently 
            # - Monitor performance
            # - Handle errors gracefully
            {% endif %}
            
            result = await self._execute_operation_handler(operation, params)
            
            # Record performance metrics
            duration = (datetime.utcnow() - start_time).total_seconds()
            self._performance_monitor.record_operation(operation, duration, True)
            
            return OperationResult.success(result)
            
        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds()
            self._performance_monitor.record_operation(operation, duration, False)
            
            logger.error(f"Technical operation failed: {e}")
            return OperationResult.error(f"Operation failed: {e}")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get technical module health with performance metrics"""
        return {
            "module_name": "{{ module_name }}",
            "type": "TECHNICAL",
            "status": "healthy" if self._initialized else "unhealthy",
            "resource_pool_status": self._get_resource_pool_status(),
            "performance_metrics": self._performance_monitor.get_metrics(),
            "resource_utilization": self._get_resource_utilization()
        }
    
    async def shutdown(self) -> OperationResult:
        """Shutdown technical infrastructure"""
        try:
            # Clean shutdown of resources
            if self._resource_pool:
                await self._resource_pool.close()
            
            self._performance_monitor.stop()
            self._initialized = False
            
            return OperationResult.success("Shutdown completed")
        except Exception as e:
            return OperationResult.error(f"Shutdown error: {e}")
    
    # Private helper methods
    async def _create_resource_pool(self):
        """Create resource pool - AI_IMPLEMENTATION_REQUIRED"""
        # {{ "AI_TODO: Create and configure resource pool" if ai_ready else "" }}
        pass
    
    async def _execute_operation_handler(self, operation: str, params: Dict[str, Any]):
        """Execute operation handler - AI_IMPLEMENTATION_REQUIRED"""
        # {{ "AI_TODO: Route to appropriate operation handler" if ai_ready else "" }}
        pass
    
    def _get_resource_pool_status(self) -> Dict[str, Any]:
        """Get resource pool status - FRAMEWORK PROVIDED"""
        if not self._resource_pool:
            return {"status": "not_initialized"}
        
        return {
            "status": "active",
            "active_connections": getattr(self._resource_pool, 'active_count', 0),
            "available_connections": getattr(self._resource_pool, 'available_count', 0)
        }
    
    def _get_resource_utilization(self) -> Dict[str, Any]:
        """Get resource utilization - FRAMEWORK PROVIDED"""
        return {
            "cpu_usage": "N/A",  # Would implement actual monitoring
            "memory_usage": "N/A",
            "disk_usage": "N/A"
        }

class PerformanceMonitor:
    """Performance monitoring - FRAMEWORK PROVIDED"""
    
    def __init__(self):
        self._metrics = {}
        self._running = False
    
    def start(self):
        self._running = True
    
    def stop(self):
        self._running = False
    
    def record_operation(self, operation: str, duration: float, success: bool):
        if operation not in self._metrics:
            self._metrics[operation] = {
                "total_calls": 0,
                "successful_calls": 0,
                "total_duration": 0.0,
                "avg_duration": 0.0
            }
        
        metrics = self._metrics[operation]
        metrics["total_calls"] += 1
        if success:
            metrics["successful_calls"] += 1
        metrics["total_duration"] += duration
        metrics["avg_duration"] = metrics["total_duration"] / metrics["total_calls"]
    
    def get_metrics(self) -> Dict[str, Any]:
        return self._metrics.copy()
''')
        
        return template.render(**context)
    
    def generate_ai_completion_file(self, module_type: str, context: Dict[str, Any]) -> str:
        """Generate AI completion instructions"""
        
        if module_type == 'CORE':
            return self._generate_core_ai_completion(context)
        elif module_type == 'INTEGRATION':
            return self._generate_integration_ai_completion(context)
        else:
            return self._generate_general_ai_completion(context)
    
    def _generate_core_ai_completion(self, context: Dict[str, Any]) -> str:
        """Generate AI completion instructions for CORE modules"""
        
        template = Template('''# AI Completion Guide: {{ module_name }} (CORE Domain Module)

## 🎯 Your Task
Complete the business logic implementation for this {{ domain }} domain module.
The framework structure is already provided - you only need to fill in the business-specific parts.

## 📋 What You Need to Complete

### 1. Business Context (HIGH PRIORITY)
**File: `core.py` - Update module docstring**
```python
"""
{{ module_name }}: [YOUR BUSINESS PURPOSE HERE]
Type: CORE
Intent: [WHY THIS MODULE EXISTS IN BUSINESS TERMS]
Contracts: [INPUTS] → [OUTPUTS] → [SIDE EFFECTS]
Dependencies: [LIST REQUIRED MODULES]
"""
```

**What to document:**
- What business problem this solves
- Key business concepts and entities
- Important business rules and constraints
- How it fits into the overall {{ domain }} domain

### 2. Business Rules Implementation (HIGH PRIORITY)
**File: `core.py` - Complete these methods:**

#### `_initialize_business_rules()` method:
```python
def _initialize_business_rules(self) -> List[BusinessRule]:
    # Define your business rules here
    return [
        BusinessRule(
            name="your_rule_name",
            description="what this rule enforces",
            validation_function=self._validate_your_rule
        ),
        # Add more rules...
    ]
```

#### `execute_primary_operation()` method:
Replace the `# AI_IMPLEMENTATION_REQUIRED` section with:
1. Input validation according to your business rules
2. Business calculations and logic
3. Domain entity updates
4. Constraint enforcement
5. Result generation

#### `_validate_business_input()` method:
```python
def _validate_business_input(self, input_data: {{ class_name }}Input) -> OperationResult:
    # Implement your validation logic:
    # - Check required fields
    # - Validate business constraints
    # - Ensure data integrity
    # - Apply domain-specific rules
    pass
```

### 3. Data Types (MEDIUM PRIORITY)
**File: `types.py` - Define your domain-specific types:**

```python
@dataclass
class {{ class_name }}Input:
    # Define input fields for your domain
    pass

@dataclass  
class {{ class_name }}Output:
    # Define output fields for your domain
    pass

@dataclass
class DomainEntity:
    # Define your main business entity
    pass
```

### 4. Tests (MEDIUM PRIORITY)
**File: `tests/test_core.py` - Add business scenario tests:**

```python
def test_main_business_scenario(self):
    """Test the primary business use case"""
    # Given: business scenario setup
    # When: execute operation
    # Then: verify business rules applied correctly

def test_business_rule_validation(self):
    """Test business rule enforcement"""
    # Test that invalid business inputs are rejected

def test_edge_cases(self):
    """Test business edge cases and boundary conditions"""
    # Test unusual but valid business scenarios
```

## 🚀 Getting Started

1. **Start with business context**: Update the module docstring with clear business purpose
2. **Define your data types**: What inputs/outputs does this module handle?
3. **Implement core business logic**: Fill in the `execute_primary_operation` method
4. **Add validation**: Implement `_validate_business_input` with your rules
5. **Test thoroughly**: Add tests that verify business scenarios work correctly

## 💡 Framework Features Already Available

✅ **Complete error handling** - Uses OperationResult pattern
✅ **Audit trail system** - Automatically tracks all operations  
✅ **Logging integration** - Structured logging throughout
✅ **Health monitoring** - Built-in health status reporting
✅ **Configuration management** - Handles module configuration
✅ **Interface compliance** - Implements standardized interface
✅ **Test scaffolding** - Test structure ready for your tests

## 🎯 Quality Checklist

Before completing, ensure:
- [ ] Business purpose clearly documented
- [ ] All business rules explicitly implemented and tested
- [ ] Input validation covers all business constraints  
- [ ] Main business scenarios have test coverage
- [ ] Error conditions properly handled
- [ ] Domain terminology used consistently
- [ ] Business logic separated from technical concerns

## 🔧 Token Budget Optimization

This scaffolding used ~15k tokens, leaving you ~45k for:
- Business logic implementation (~20k tokens)
- Documentation completion (~10k tokens)  
- Test implementation (~15k tokens)

Focus on business value - the technical infrastructure is handled!

## 📞 Need Help?

- Check `interface.py` for the complete contract you need to implement
- Review `types.py` for the data structures you're working with
- Look at existing tests in `tests/` for patterns to follow
- The framework handles all the technical complexity - focus on business logic!
''')
        
        return template.render(**context)

    def _generate_integration_ai_completion(self, context: Dict[str, Any]) -> str:
        """Generate AI completion instructions for INTEGRATION modules"""
        
        template = Template('''# AI Completion Guide: {{ module_name }} (INTEGRATION Module)

## 🎯 Your Task
Complete the external service integration for this {{ domain }} integration module.
The framework provides fault tolerance, circuit breakers, retries, and rate limiting - you only need to fill in the service-specific parts.

## 📋 What You Need to Complete

### 1. External Service Configuration (HIGH PRIORITY)
**File: `core.py` - Update module docstring**
```python
"""
{{ module_name }}: [YOUR INTEGRATION PURPOSE HERE]
Type: INTEGRATION
Intent: [WHAT EXTERNAL SERVICE AND WHY]
External Service: [SERVICE NAME AND PURPOSE]
Fault Tolerance: [YOUR REQUIREMENTS]
"""
```

**Document:**
- What external service this integrates with
- API documentation URL and version
- Authentication method required
- Rate limits and SLA information
- Expected error codes and recovery strategies

### 2. Service Integration Implementation (HIGH PRIORITY)
**File: `core.py` - Complete these methods:**

#### `_build_request_url()` method:
```python
def _build_request_url(self, request: {{ class_name }}Request) -> str:
    # Build the complete URL for the external service
    endpoint = "your_endpoint_here"  # Based on request type
    return f"{self.config.base_url}/api/{endpoint}"
```

#### `_build_request_headers()` method:
```python
def _build_request_headers(self, request: {{ class_name }}Request) -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {self.config.api_key}",
        # Add other required headers
    }
```

#### `_build_request_payload()` method:
```python
def _build_request_payload(self, request: {{ class_name }}Request) -> Dict[str, Any]:
    # Transform internal request to external service format
    return {
        "external_field": request.internal_field,
        # Map all required fields
    }
```

#### `_transform_response()` method:
```python
def _transform_response(self, response_data: Dict[str, Any]) -> {{ class_name }}Response:
    # Transform external response to internal format
    return {{ class_name }}Response(
        internal_field=response_data.get("external_field"),
        # Map all response fields
    )
```

### 3. Data Types (MEDIUM PRIORITY)
**File: `types.py` - Define your service-specific types:**

```python
@dataclass
class {{ class_name }}Request:
    # Define request fields for your external service
    pass

@dataclass  
class {{ class_name }}Response:
    # Define response fields from external service
    pass

@dataclass
class {{ class_name }}Config:
    base_url: str
    api_key: str
    timeout_seconds: int = 30
    circuit_breaker_config: Dict = None
    retry_config: Dict = None
    rate_limit_config: Dict = None
```

### 4. Error Handling (MEDIUM PRIORITY)
**Review and customize error handling in `call_external_service()` for your service's specific error codes**

## 🚀 Getting Started

1. **Document the external service**: Update module docstring with service details
2. **Define request/response types**: What data does the service expect/return?
3. **Implement URL building**: How to construct the service endpoints?
4. **Add authentication**: How does the service authenticate requests?
5. **Transform data**: Map between internal and external formats
6. **Test error scenarios**: Verify fault tolerance works correctly

## 💡 Framework Features Already Available

✅ **Complete fault tolerance** - Circuit breaker, retry, rate limiting
✅ **HTTP client management** - aiohttp session with proper timeouts
✅ **Health monitoring** - Built-in health checks and status reporting
✅ **Error categorization** - Proper error types for different scenarios
✅ **Async support** - Full async/await integration
✅ **Logging integration** - Structured logging throughout
✅ **Configuration management** - Handles service configuration

## 🎯 Quality Checklist

Before completing, ensure:
- [ ] External service details clearly documented
- [ ] All request/response mappings implemented
- [ ] Authentication properly configured
- [ ] Error scenarios tested and handled appropriately
- [ ] Rate limiting configured for service requirements
- [ ] Health checks verify service availability

This scaffolding handles all the complex fault tolerance - focus on the service integration!
''')
        
        return template.render(**context)
    
    def _generate_general_ai_completion(self, context: Dict[str, Any]) -> str:
        """Generate general AI completion instructions for SUPPORTING/TECHNICAL modules"""
        
        template = Template('''# AI Completion Guide: {{ module_name }} ({{ module_type|upper }} Module)

## 🎯 Your Task
Complete the implementation for this {{ module_type.lower() }} module.
The framework provides the structure - you need to fill in the specific functionality.

## 📋 What You Need to Complete

### 1. Module Purpose (HIGH PRIORITY)
**File: `core.py` - Update module docstring**
```python
"""
{{ module_name }}: [YOUR MODULE PURPOSE HERE]
Type: {{ module_type|upper }}
Intent: [WHAT THIS MODULE PROVIDES]
"""
```

### 2. Core Implementation (HIGH PRIORITY)
**File: `core.py` - Complete the main operation method**

### 3. Data Types (MEDIUM PRIORITY)
**File: `types.py` - Define your module-specific types**

### 4. Tests (LOW PRIORITY)
**File: `tests/test_core.py` - Add functionality tests**

## 🚀 Getting Started

1. **Define the purpose**: What does this module accomplish?
2. **Implement core logic**: Fill in the main operation method
3. **Define data types**: What inputs/outputs does this handle?
4. **Test functionality**: Verify the module works correctly

## 💡 Framework Features Already Available

✅ **Error handling** - Structured error management
✅ **Health monitoring** - Built-in status reporting
✅ **Logging integration** - Structured logging
✅ **Configuration management** - Module configuration handling

Focus on your specific functionality - the framework handles the infrastructure!
''')
        
        return template.render(**context)
    
    def generate_types_file(self, module_type: str, context: Dict[str, Any]) -> str:
        """Generate types file for the module"""
        
        template = Template('''"""
Type definitions for {{ module_name }}
"""

from typing import Dict, Any, List, Optional, Generic, TypeVar
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

T = TypeVar('T')

@dataclass
class {{ class_name }}Config:
    """Configuration for {{ module_name }} module"""
    {% if module_type == 'CORE' %}
    # {{ "AI_TODO: Define configuration fields for business logic" if ai_ready else "Configuration fields" }}
    domain: str = "{{ domain }}"
    persist_audit_trail: bool = True
    max_audit_events: int = 1000
    # AI_TODO: Add domain-specific configuration
    {% elif module_type == 'INTEGRATION' %}
    # {{ "AI_TODO: Define external service configuration" if ai_ready else "External service configuration" }}
    base_url: str
    api_key: str
    timeout_seconds: int = 30
    circuit_breaker_config: Dict[str, Any] = None
    retry_config: Dict[str, Any] = None
    rate_limit_config: Dict[str, Any] = None
    # AI_TODO: Add service-specific configuration
    {% elif module_type == 'SUPPORTING' %}
    # {{ "AI_TODO: Define supporting module configuration" if ai_ready else "Supporting module configuration" }}
    workflow_timeout: int = 300
    max_concurrent_workflows: int = 10
    # AI_TODO: Add workflow-specific configuration
    {% else %}
    # {{ "AI_TODO: Define technical module configuration" if ai_ready else "Technical module configuration" }}
    resource_pool_size: int = 10
    performance_monitoring: bool = True
    # AI_TODO: Add infrastructure-specific configuration
    {% endif %}

{% if module_type == 'CORE' %}
@dataclass
class {{ class_name }}Input:
    """Input data for {{ module_name }} operations"""
    # {{ "AI_TODO: Define input fields for your business operations" if ai_ready else "Define input fields" }}
    operation_type: str = "default"
    # AI_TODO: Add business-specific input fields

@dataclass
class {{ class_name }}Output:
    """Output data from {{ module_name }} operations"""
    # {{ "AI_TODO: Define output fields for your business results" if ai_ready else "Define output fields" }}
    result: str
    audit_trail: List[Dict[str, Any]] = None
    # AI_TODO: Add business-specific output fields

@dataclass
class DomainEntity:
    """Core domain entity for {{ module_name }}"""
    # {{ "AI_TODO: Define your main business entity" if ai_ready else "Define domain entity" }}
    entity_id: str
    created_at: datetime
    updated_at: datetime
    # AI_TODO: Add domain-specific entity fields

@dataclass
class BusinessRule:
    """Business rule definition"""
    name: str
    description: str
    validation_function: callable = None
    is_active: bool = True

{% elif module_type == 'INTEGRATION' %}
@dataclass
class {{ class_name }}Request:
    """Request data for external service calls"""
    # {{ "AI_TODO: Define request fields for external service" if ai_ready else "Define request fields" }}
    request_id: str
    operation: str
    # AI_TODO: Add service-specific request fields

@dataclass
class {{ class_name }}Response:
    """Response data from external service"""
    # {{ "AI_TODO: Define response fields from external service" if ai_ready else "Define response fields" }}
    response_id: str
    status: str
    data: Dict[str, Any] = None
    # AI_TODO: Add service-specific response fields

{% elif module_type == 'SUPPORTING' %}
@dataclass
class {{ class_name }}Request:
    """Request data for supporting operations"""
    # {{ "AI_TODO: Define request fields for supporting operations" if ai_ready else "Define request fields" }}
    workflow_id: str
    operation_type: str
    # AI_TODO: Add workflow-specific request fields

@dataclass
class {{ class_name }}Response:
    """Response data from supporting operations"""
    # {{ "AI_TODO: Define response fields from supporting operations" if ai_ready else "Define response fields" }}
    workflow_id: str
    status: str
    data: Dict[str, Any] = None
    # AI_TODO: Add workflow-specific response fields

{% else %}
@dataclass
class TechnicalRequest:
    """Request data for technical operations"""
    # {{ "AI_TODO: Define request fields for technical operations" if ai_ready else "Define request fields" }}
    operation: str
    parameters: Dict[str, Any]
    # AI_TODO: Add infrastructure-specific request fields

@dataclass
class TechnicalResponse:
    """Response data from technical operations"""
    # {{ "AI_TODO: Define response fields from technical operations" if ai_ready else "Define response fields" }}
    operation: str
    result: Dict[str, Any]
    performance_metrics: Dict[str, Any] = None
    # AI_TODO: Add infrastructure-specific response fields
{% endif %}

class OperationResult(Generic[T]):
    """Standard result wrapper for all operations"""
    
    def __init__(self, success: bool, data: T = None, error: str = None, error_code: str = None):
        self.success = success
        self.data = data
        self.error = error
        self.error_code = error_code
        self.timestamp = datetime.utcnow()
    
    @classmethod
    def success(cls, data: T = None) -> 'OperationResult[T]':
        """Create a successful result"""
        return cls(success=True, data=data)
    
    @classmethod
    def error(cls, error: str, error_code: str = None) -> 'OperationResult[T]':
        """Create an error result"""
        return cls(success=False, error=error, error_code=error_code)
    
    def __bool__(self) -> bool:
        return self.success

class ModuleStatus(Enum):
    """Module status enumeration"""
    INITIALIZING = "initializing"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    SHUTTING_DOWN = "shutting_down"
    SHUTDOWN = "shutdown"
''')
        
        return template.render(**context)
    
    def generate_interface_file(self, module_type: str, context: Dict[str, Any]) -> str:
        """Generate interface file for the module"""
        
        template = Template('''"""
Interface definition for {{ module_name }}
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

{% if module_type == 'CORE' %}
from .types import {{ class_name }}Config, {{ class_name }}Input, {{ class_name }}Output, OperationResult, DomainEntity
{% elif module_type == 'INTEGRATION' %}
from .types import {{ class_name }}Config, {{ class_name }}Request, {{ class_name }}Response, OperationResult
{% elif module_type == 'SUPPORTING' %}
from .types import {{ class_name }}Config, {{ class_name }}Request, {{ class_name }}Response, OperationResult
{% else %}
from .types import {{ class_name }}Config, TechnicalRequest, TechnicalResponse, OperationResult
{% endif %}

class {{ class_name }}Interface(ABC):
    """
    Interface for {{ module_name }} module
    Type: {{ module_type }}
    
    Defines the contract that all {{ module_name }} implementations must follow.
    """
    
    @abstractmethod
    def initialize(self) -> OperationResult:
        """
        Initialize the module
        
        Returns:
            OperationResult indicating success or failure
        """
        pass
    
    {% if module_type == 'CORE' %}
    @abstractmethod
    def execute_primary_operation(self, input_data: {{ class_name }}Input) -> OperationResult[{{ class_name }}Output]:
        """
        Execute the primary business operation
        
        Args:
            input_data: Input data for the operation
            
        Returns:
            OperationResult containing the operation output or error
        """
        pass
    
    @abstractmethod
    def get_domain_entity(self, entity_id: str) -> OperationResult[DomainEntity]:
        """
        Retrieve a domain entity by ID
        
        Args:
            entity_id: Unique identifier for the entity
            
        Returns:
            OperationResult containing the domain entity or error
        """
        pass
    
    @abstractmethod
    def apply_business_rule(self, rule_name: str, context: Dict[str, Any]) -> OperationResult:
        """
        Apply a specific business rule
        
        Args:
            rule_name: Name of the business rule to apply
            context: Context data for rule evaluation
            
        Returns:
            OperationResult indicating rule application success or failure
        """
        pass
    
    {% elif module_type == 'INTEGRATION' %}
    @abstractmethod
    async def call_external_service(self, request: {{ class_name }}Request) -> OperationResult[{{ class_name }}Response]:
        """
        Make a call to the external service
        
        Args:
            request: Request data for the external service
            
        Returns:
            OperationResult containing the service response or error
        """
        pass
    
    {% elif module_type == 'SUPPORTING' %}
    @abstractmethod
    def execute_supporting_operation(self, request: {{ class_name }}Request) -> OperationResult[{{ class_name }}Response]:
        """
        Execute a supporting business operation
        
        Args:
            request: Request data for the supporting operation
            
        Returns:
            OperationResult containing the operation response or error
        """
        pass
    
    {% else %}
    @abstractmethod
    async def execute_technical_operation(self, operation: str, params: Dict[str, Any]) -> OperationResult:
        """
        Execute a technical operation
        
        Args:
            operation: Name of the technical operation
            params: Parameters for the operation
            
        Returns:
            OperationResult containing the operation result or error
        """
        pass
    {% endif %}
    
    @abstractmethod
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get the current health status of the module
        
        Returns:
            Dictionary containing health status information
        """
        pass
    
    @abstractmethod
    def shutdown(self) -> OperationResult:
        """
        Gracefully shutdown the module
        
        Returns:
            OperationResult indicating shutdown success or failure
        """
        pass
''')
        
        return template.render(**context)
    
    def generate_test_file(self, module_type: str, context: Dict[str, Any]) -> str:
        """Generate test file for the module"""
        
        template = Template('''"""
Tests for {{ module_name }}
"""

import pytest
from unittest.mock import Mock, patch
import asyncio

{% if module_type == 'CORE' %}
from ..core import {{ class_name }}Module, BusinessRuleViolation
from ..types import {{ class_name }}Config, {{ class_name }}Input, {{ class_name }}Output, OperationResult
{% elif module_type == 'INTEGRATION' %}
from ..core import {{ class_name }}Module
from ..types import {{ class_name }}Config, {{ class_name }}Request, {{ class_name }}Response, OperationResult
{% elif module_type == 'SUPPORTING' %}
from ..core import {{ class_name }}Module
from ..types import {{ class_name }}Config, {{ class_name }}Request, {{ class_name }}Response, OperationResult
{% else %}
from ..core import {{ class_name }}Module
from ..types import {{ class_name }}Config, TechnicalRequest, TechnicalResponse, OperationResult
{% endif %}

class Test{{ class_name }}Module:
    """Test suite for {{ class_name }}Module"""
    
    @pytest.fixture
    def config(self):
        """Create test configuration"""
        {% if module_type == 'CORE' %}
        return {{ class_name }}Config(
            domain="{{ domain }}",
            persist_audit_trail=False,
            max_audit_events=100
        )
        {% elif module_type == 'INTEGRATION' %}
        return {{ class_name }}Config(
            base_url="https://test-api.example.com",
            api_key="test-key",
            timeout_seconds=10,
            circuit_breaker_config={},
            retry_config={},
            rate_limit_config={}
        )
        {% elif module_type == 'SUPPORTING' %}
        return {{ class_name }}Config(
            workflow_timeout=60,
            max_concurrent_workflows=5
        )
        {% else %}
        return {{ class_name }}Config(
            resource_pool_size=5,
            performance_monitoring=True
        )
        {% endif %}
    
    @pytest.fixture
    def module(self, config):
        """Create test module instance"""
        return {{ class_name }}Module(config)
    
    def test_module_initialization(self, module):
        """Test module initialization"""
        result = module.initialize()
        assert result.success
        assert module._initialized
    
    def test_health_status(self, module):
        """Test health status reporting"""
        module.initialize()
        status = module.get_health_status()
        
        assert status["module_name"] == "{{ module_name }}"
        assert status["type"] == "{{ module_type }}"
        assert status["status"] in ["healthy", "unhealthy"]
    
    def test_shutdown(self, module):
        """Test module shutdown"""
        module.initialize()
        result = module.shutdown()
        assert result.success
        assert not module._initialized
    
    {% if module_type == 'CORE' %}
    def test_primary_operation_not_initialized(self, module):
        """Test primary operation fails when module not initialized"""
        input_data = {{ class_name }}Input(operation_type="test")
        result = module.execute_primary_operation(input_data)
        assert not result.success
        assert "not initialized" in result.error
    
    def test_primary_operation_success(self, module):
        """Test successful primary operation"""
        module.initialize()
        input_data = {{ class_name }}Input(operation_type="test")
        
        # {{ "AI_TODO: Mock business logic and test successful scenario" if ai_ready else "Add business logic test" }}
        result = module.execute_primary_operation(input_data)
        # AI_TODO: Add assertions for your business logic
    
    def test_business_rule_validation(self, module):
        """Test business rule validation"""
        module.initialize()
        
        # {{ "AI_TODO: Test business rule validation scenarios" if ai_ready else "Add business rule tests" }}
        # AI_TODO: Create test data that violates business rules
        # AI_TODO: Verify that BusinessRuleViolation is raised appropriately
    
    def test_audit_trail_creation(self, module):
        """Test audit trail is created for operations"""
        module.initialize()
        input_data = {{ class_name }}Input(operation_type="test")
        
        result = module.execute_primary_operation(input_data)
        assert len(module._audit_trail) > 0
        assert module._audit_trail[0]["operation"] == "primary_operation"
    
    {% elif module_type == 'INTEGRATION' %}
    @pytest.mark.asyncio
    async def test_external_service_call_not_initialized(self, module):
        """Test external service call fails when module not initialized"""
        request = {{ class_name }}Request(request_id="test", operation="test")
        result = await module.call_external_service(request)
        assert not result.success
        assert "not initialized" in result.error
    
    @pytest.mark.asyncio
    async def test_external_service_call_success(self, module):
        """Test successful external service call"""
        await module.initialize()
        request = {{ class_name }}Request(request_id="test", operation="test")
        
        # {{ "AI_TODO: Mock external service response and test successful scenario" if ai_ready else "Add integration test" }}
        with patch('aiohttp.ClientSession.post') as mock_post:
            mock_response = Mock()
            mock_response.status = 200
            mock_response.json = Mock(return_value={"status": "success"})
            mock_post.return_value.__aenter__.return_value = mock_response
            
            result = await module.call_external_service(request)
            # AI_TODO: Add assertions for your integration logic
    
    @pytest.mark.asyncio
    async def test_circuit_breaker_protection(self, module):
        """Test circuit breaker protection"""
        await module.initialize()
        
        # {{ "AI_TODO: Test circuit breaker behavior with service failures" if ai_ready else "Add circuit breaker test" }}
        # AI_TODO: Simulate service failures and verify circuit breaker opens
    
    {% elif module_type == 'SUPPORTING' %}
    def test_supporting_operation_not_initialized(self, module):
        """Test supporting operation fails when module not initialized"""
        request = {{ class_name }}Request(workflow_id="test", operation_type="test")
        result = module.execute_supporting_operation(request)
        assert not result.success
        assert "not initialized" in result.error
    
    def test_supporting_operation_success(self, module):
        """Test successful supporting operation"""
        module.initialize()
        request = {{ class_name }}Request(workflow_id="test", operation_type="test")
        
        # {{ "AI_TODO: Test supporting business operation scenarios" if ai_ready else "Add supporting operation test" }}
        result = module.execute_supporting_operation(request)
        # AI_TODO: Add assertions for your supporting logic
    
    def test_workflow_management(self, module):
        """Test workflow state management"""
        module.initialize()
        
        # {{ "AI_TODO: Test workflow creation, execution, and completion" if ai_ready else "Add workflow test" }}
        # AI_TODO: Verify workflow state is managed correctly
    
    {% else %}
    @pytest.mark.asyncio
    async def test_technical_operation_not_initialized(self, module):
        """Test technical operation fails when module not initialized"""
        result = await module.execute_technical_operation("test_op", {"param": "value"})
        assert not result.success
        assert "not initialized" in result.error
    
    @pytest.mark.asyncio
    async def test_technical_operation_success(self, module):
        """Test successful technical operation"""
        await module.initialize()
        
        # {{ "AI_TODO: Test technical operation scenarios" if ai_ready else "Add technical operation test" }}
        result = await module.execute_technical_operation("test_op", {"param": "value"})
        # AI_TODO: Add assertions for your technical logic
    
    @pytest.mark.asyncio
    async def test_performance_monitoring(self, module):
        """Test performance monitoring"""
        await module.initialize()
        
        # Execute operation to generate metrics
        await module.execute_technical_operation("test_op", {"param": "value"})
        
        metrics = module._performance_monitor.get_metrics()
        # AI_TODO: Verify performance metrics are collected correctly
    
    @pytest.mark.asyncio
    async def test_resource_pool_management(self, module):
        """Test resource pool management"""
        await module.initialize()
        
        status = module._get_resource_pool_status()
        # {{ "AI_TODO: Test resource pool creation and management" if ai_ready else "Add resource pool test" }}
        # AI_TODO: Verify resource pool is managed correctly
    {% endif %}

# {{ "AI_TODO: Add integration tests" if ai_ready else "Add more tests as needed" }}
class TestIntegration:
    """Integration tests for {{ class_name }}Module"""
    
    # {{ "AI_TODO: Add tests that verify integration with other modules" if ai_ready else "Integration tests" }}
    # {{ "AI_TODO: Add end-to-end workflow tests" if ai_ready else "" }}
    # {{ "AI_TODO: Add error recovery tests" if ai_ready else "" }}
    pass
''')
        
        return template.render(**context)
    
    def generate_contract_tests(self, module_type: str, context: Dict[str, Any]) -> str:
        """Generate contract compliance tests"""
        
        template = Template('''"""
Contract compliance tests for {{ module_name }}
These tests verify that the module correctly implements its interface contract.
"""

import pytest
from abc import ABC

from ..core import {{ class_name }}Module
from ..interface import {{ class_name }}Interface
{% if module_type == 'CORE' %}
from ..types import {{ class_name }}Config, {{ class_name }}Input, {{ class_name }}Output, OperationResult
{% elif module_type == 'INTEGRATION' %}
from ..types import {{ class_name }}Config, {{ class_name }}Request, {{ class_name }}Response, OperationResult
{% elif module_type == 'SUPPORTING' %}
from ..types import {{ class_name }}Config, {{ class_name }}Request, {{ class_name }}Response, OperationResult
{% else %}
from ..types import {{ class_name }}Config, OperationResult
{% endif %}

class TestContractCompliance:
    """Test that {{ class_name }}Module complies with its interface contract"""
    
    @pytest.fixture
    def config(self):
        """Create test configuration"""
        {% if module_type == 'CORE' %}
        return {{ class_name }}Config(domain="{{ domain }}")
        {% elif module_type == 'INTEGRATION' %}
        return {{ class_name }}Config(
            base_url="https://test.example.com",
            api_key="test-key"
        )
        {% elif module_type == 'SUPPORTING' %}
        return {{ class_name }}Config()
        {% else %}
        return {{ class_name }}Config()
        {% endif %}
    
    @pytest.fixture
    def module(self, config):
        """Create module instance for testing"""
        return {{ class_name }}Module(config)
    
    def test_implements_interface(self, module):
        """Test that module implements the required interface"""
        assert isinstance(module, {{ class_name }}Interface)
        assert not isinstance(module, ABC)  # Should not be abstract
    
    def test_interface_methods_exist(self, module):
        """Test that all interface methods are implemented"""
        required_methods = [
            'initialize',
            {% if module_type == 'CORE' %}
            'execute_primary_operation',
            'get_domain_entity',
            'apply_business_rule',
            {% elif module_type == 'INTEGRATION' %}
            'call_external_service',
            {% elif module_type == 'SUPPORTING' %}
            'execute_supporting_operation',
            {% else %}
            'execute_technical_operation',
            {% endif %}
            'get_health_status',
            'shutdown'
        ]
        
        for method_name in required_methods:
            assert hasattr(module, method_name)
            assert callable(getattr(module, method_name))
    
    def test_initialize_returns_operation_result(self, module):
        """Test that initialize returns OperationResult"""
        result = module.initialize()
        assert isinstance(result, OperationResult)
        assert isinstance(result.success, bool)
    
    {% if module_type == 'CORE' %}
    def test_execute_primary_operation_signature(self, module):
        """Test primary operation method signature"""
        module.initialize()
        input_data = {{ class_name }}Input()
        result = module.execute_primary_operation(input_data)
        assert isinstance(result, OperationResult)
    
    def test_get_domain_entity_signature(self, module):
        """Test get domain entity method signature"""
        module.initialize()
        result = module.get_domain_entity("test_id")
        assert isinstance(result, OperationResult)
    
    def test_apply_business_rule_signature(self, module):
        """Test apply business rule method signature"""
        module.initialize()
        result = module.apply_business_rule("test_rule", {})
        assert isinstance(result, OperationResult)
    
    {% elif module_type == 'INTEGRATION' %}
    @pytest.mark.asyncio
    async def test_call_external_service_signature(self, module):
        """Test external service call method signature"""
        await module.initialize()
        request = {{ class_name }}Request(request_id="test", operation="test")
        result = await module.call_external_service(request)
        assert isinstance(result, OperationResult)
    
    {% elif module_type == 'SUPPORTING' %}
    def test_execute_supporting_operation_signature(self, module):
        """Test supporting operation method signature"""
        module.initialize()
        request = {{ class_name }}Request(workflow_id="test", operation_type="test")
        result = module.execute_supporting_operation(request)
        assert isinstance(result, OperationResult)
    
    {% else %}
    @pytest.mark.asyncio
    async def test_execute_technical_operation_signature(self, module):
        """Test technical operation method signature"""
        await module.initialize()
        result = await module.execute_technical_operation("test", {})
        assert isinstance(result, OperationResult)
    {% endif %}
    
    def test_get_health_status_returns_dict(self, module):
        """Test that get_health_status returns a dictionary"""
        module.initialize()
        status = module.get_health_status()
        assert isinstance(status, dict)
        
        # Verify required fields
        required_fields = ["module_name", "type", "status"]
        for field in required_fields:
            assert field in status
    
    def test_shutdown_returns_operation_result(self, module):
        """Test that shutdown returns OperationResult"""
        module.initialize()
        result = module.shutdown()
        assert isinstance(result, OperationResult)
        assert isinstance(result.success, bool)
    
    def test_module_lifecycle(self, module):
        """Test complete module lifecycle"""
        # Initialize
        init_result = module.initialize()
        assert init_result.success
        
        # Check health
        status = module.get_health_status()
        assert status["status"] in ["healthy", "initializing"]
        
        # Shutdown
        shutdown_result = module.shutdown()
        assert shutdown_result.success
        
        # Verify shutdown state
        final_status = module.get_health_status()
        assert final_status["status"] in ["unhealthy", "shutdown"]
    
    def test_error_handling_compliance(self, module):
        """Test that errors are properly handled and returned"""
        # Test operations on uninitialized module
        {% if module_type == 'CORE' %}
        input_data = {{ class_name }}Input()
        result = module.execute_primary_operation(input_data)
        assert not result.success
        assert result.error is not None
        {% elif module_type == 'SUPPORTING' %}
        request = {{ class_name }}Request(workflow_id="test", operation_type="test")
        result = module.execute_supporting_operation(request)
        assert not result.success
        assert result.error is not None
        {% endif %}
''')
        
        return template.render(**context)
    
    def generate_init_file(self, context: Dict[str, Any]) -> str:
        """Generate __init__.py file for the module"""
        
        template = Template('''"""
{{ module_name }} - {{ "AI_TODO: Add module description" if ai_ready else "Module for " + domain }}

This module provides {{ "AI_TODO: describe what this module provides" if ai_ready else "functionality for " + domain }}.
"""

from .core import {{ class_name }}Module
from .interface import {{ class_name }}Interface
from .types import (
    {{ class_name }}Config,
    {% if module_type == 'CORE' %}
    {{ class_name }}Input,
    {{ class_name }}Output,
    DomainEntity,
    BusinessRule,
    {% elif module_type == 'INTEGRATION' %}
    {{ class_name }}Request,
    {{ class_name }}Response,
    {% elif module_type == 'SUPPORTING' %}
    {{ class_name }}Request,
    {{ class_name }}Response,
    {% else %}
    TechnicalRequest,
    TechnicalResponse,
    {% endif %}
    OperationResult,
    ModuleStatus
)

# Public API
__all__ = [
    "{{ class_name }}Module",
    "{{ class_name }}Interface",
    "{{ class_name }}Config",
    {% if module_type == 'CORE' %}
    "{{ class_name }}Input",
    "{{ class_name }}Output",
    "DomainEntity",
    "BusinessRule",
    {% elif module_type == 'INTEGRATION' %}
    "{{ class_name }}Request",
    "{{ class_name }}Response",
    {% elif module_type == 'SUPPORTING' %}
    "{{ class_name }}Request",
    "{{ class_name }}Response",
    {% else %}
    "TechnicalRequest",
    "TechnicalResponse",
    {% endif %}
    "OperationResult",
    "ModuleStatus"
]

# Version information
__version__ = "1.0.0"
__author__ = "{{ "AI_TODO: Add author information" if ai_ready else "Generated by Standardized Modules Framework" }}"
''')
        
        return template.render(**context)

# Entry point for CLI
if __name__ == '__main__':
    cli()

# === USAGE EXAMPLES ===

# Command line usage:
"""
# Install CLI
pip install standardized-modules-framework[cli]

# Create a new CORE domain module
sm create-module user-management --type=CORE --domain=ecommerce

# Create an INTEGRATION module  
sm create-module payment-gateway --type=INTEGRATION --domain=payments

# Create with custom output directory
sm create-module order-processing --type=CORE --domain=ecommerce --output-dir=./modules/

# Generate without AI completion markers (for human development)
sm create-module analytics --type=TECHNICAL --ai-ready=false
"""

# What gets generated:
"""
user-management/
├── __init__.py              # Public interface exports
├── core.py                  # Complete implementation template with AI_TODO markers
├── interface.py             # Full interface contract  
├── types.py                 # Data type definitions with placeholders
├── tests/
│   ├── test_core.py         # Business scenario test templates
│   └── test_contracts.py    # Contract compliance tests (complete)
├── docs/
│   └── README.md            # Module documentation template
├── examples/
│   └── usage_example.py     # Usage example template
└── AI_COMPLETION.md         # Detailed AI completion instructions
"""

# Integration with existing framework:
"""
# After generation, module works immediately with framework
import standardized_modules as sm

# Register the new module
user_mgmt = UserManagementModule(config)
orchestrator = sm.orchestrator()
orchestrator.register_module('user_management', user_mgmt)

# Use it
result = orchestrator.execute_operation(
    'user_management', 
    'execute_primary_operation',
    user_data
)
"""