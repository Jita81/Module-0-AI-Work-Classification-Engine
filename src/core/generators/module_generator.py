"""
Core module generator for the Standardized Modules Framework.

This module contains the main ModuleGenerator class responsible for creating
complete module structures with containerization support.
"""

import os
from pathlib import Path
from typing import Dict, Any

from ..models.generation_result import GenerationResult
from .templates import ModuleTemplates


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
            
            # Generate interface file
            interface_content = self.templates.generate_interface_file(module_type, template_context)
            self._write_file(module_path / 'interface.py', interface_content)
            
            # Generate types file
            types_content = self.templates.generate_types_file(template_context)
            self._write_file(module_path / 'types.py', types_content)
            
            # Generate test files
            test_content = self.templates.generate_test_file(module_type, template_context)
            self._write_file(module_path / 'tests' / 'test_core.py', test_content)
            
            contract_test_content = self.templates.generate_contract_tests(template_context)
            self._write_file(module_path / 'tests' / 'test_contracts.py', contract_test_content)
            
            # Generate init file
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
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
    
    def _generate_config_files(self, module_path: Path, context: Dict[str, Any]):
        """Generate configuration files (requirements.txt, README, etc.)"""
        
        # Generate requirements.txt
        requirements = '''# Core dependencies
fastapi>=0.68.0
uvicorn>=0.15.0
pydantic>=1.8.0
python-dotenv>=0.19.0

# Development dependencies  
pytest>=6.2.0
pytest-asyncio>=0.15.0
pytest-cov>=2.12.0
black>=21.0.0
mypy>=0.910
'''
        self._write_file(module_path / 'requirements.txt', requirements)
        
        # Generate pytest.ini
        pytest_config = f'''[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --tb=short
    --cov={context['module_name'].replace('-', '_')}
    --cov-report=html
    --cov-report=term-missing
'''
        self._write_file(module_path / 'pytest.ini', pytest_config)
        
        # Generate module README
        readme = f'''# {context['module_name'].title()} Module

**Type**: {context['module_type']}  
**Domain**: {context['domain']}

## Overview

{context['module_type']} module for {context['domain']} domain functionality.

## Usage

```python
from {context['module_name'].replace('-', '_')} import {context['class_name']}

# Initialize the module
{context['module_name'].replace('-', '_')} = {context['class_name']}()
```

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run with coverage
pytest --cov={context['module_name'].replace('-', '_')}
```

## AI Completion

See `AI_COMPLETION.md` for detailed prompts and completion guidance.
'''
        self._write_file(module_path / 'docs' / 'README.md', readme)
        
        # Generate gitignore
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
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/

# Virtual environments
.env
.venv
env/
venv/
'''
        self._write_file(module_path / '.gitignore', gitignore)
    
    def _generate_containerization_files(self, module_path: Path, context: Dict[str, Any]):
        """Generate Docker, Kubernetes, and CI/CD files"""
        
        # Import containerization module when needed
        from .containerization import ContainerizationGenerator
        
        containerization = ContainerizationGenerator()
        containerization.generate_all_files(module_path, context)
