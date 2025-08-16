"""
Microservice Factory

Core engine that generates production-ready microservices from JSON specifications,
integrating with existing framework patterns and automated agile methodology.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from .spec_parser import ParsedSpec, SpecParser
from ..core.generators.module_generator import ModuleGenerator
from ..core.generators.templates import ModuleTemplates
from ..core.models.generation_result import GenerationResult


@dataclass
class MicroserviceResult:
    """Result of microservice generation."""
    success: bool
    microservice_name: str
    output_dir: Path
    files_generated: List[str]
    sprint_artifacts: Dict[str, str]
    errors: List[str]
    metadata: Dict[str, Any]


class MicroserviceFactory:
    """
    Factory for generating microservices from JSON specifications.
    
    Integrates with existing framework patterns while adding JSON-driven automation
    and automated agile sprint artifact generation.
    """
    
    def __init__(self, output_base_dir: str = "microservices"):
        """Initialize factory with output directory."""
        self.output_base_dir = Path(output_base_dir)
        self.output_base_dir.mkdir(exist_ok=True)
        
        # Initialize existing framework components
        self.module_generator = ModuleGenerator()
        self.module_templates = ModuleTemplates()
        self.spec_parser = SpecParser()
    
    def generate_from_file(self, spec_file: str, **kwargs) -> MicroserviceResult:
        """Generate microservice from JSON specification file."""
        try:
            parsed_spec = self.spec_parser.parse_file(spec_file)
            return self.generate_from_spec(parsed_spec, **kwargs)
        except Exception as e:
            return MicroserviceResult(
                success=False,
                microservice_name="unknown",
                output_dir=self.output_base_dir,
                files_generated=[],
                sprint_artifacts={},
                errors=[f"Failed to parse specification file: {e}"],
                metadata={}
            )
    
    def generate_from_json(self, json_string: str, **kwargs) -> MicroserviceResult:
        """Generate microservice from JSON string."""
        try:
            import json
            spec_data = json.loads(json_string)
            parsed_spec = self.spec_parser.parse_dict(spec_data)
            return self.generate_from_spec(parsed_spec, **kwargs)
        except Exception as e:
            return MicroserviceResult(
                success=False,
                microservice_name="unknown",
                output_dir=self.output_base_dir,
                files_generated=[],
                sprint_artifacts={},
                errors=[f"Failed to parse JSON specification: {e}"],
                metadata={}
            )
    
    def generate_from_spec(self, spec: ParsedSpec, **kwargs) -> MicroserviceResult:
        """Generate microservice from parsed specification."""
        microservice_dir = self.output_base_dir / spec.microservice_type
        files_generated = []
        sprint_artifacts = {}
        errors = []
        
        try:
            # Create microservice directory structure
            self._create_microservice_structure(microservice_dir, spec)
            
            # Generate core microservice using existing framework
            core_result = self._generate_core_microservice(microservice_dir, spec, **kwargs)
            files_generated.extend(core_result.files_created)
            if core_result.errors:
                errors.extend(core_result.errors)
            
            # Generate TDD tests from JSON specification
            test_files = self._generate_tdd_tests(microservice_dir, spec)
            files_generated.extend(test_files)
            
            # Generate sprint artifacts for automated agile
            sprint_artifacts = self._generate_sprint_artifacts(microservice_dir, spec)
            
            # Generate microservice-specific automation
            automation_files = self._generate_microservice_automation(microservice_dir, spec)
            files_generated.extend(automation_files)
            
            # Generate documentation
            doc_files = self._generate_documentation(microservice_dir, spec)
            files_generated.extend(doc_files)
            
            # Create metadata
            metadata = self._generate_metadata(spec, files_generated, sprint_artifacts)
            
            return MicroserviceResult(
                success=len(errors) == 0,
                microservice_name=spec.microservice_type,
                output_dir=microservice_dir,
                files_generated=files_generated,
                sprint_artifacts=sprint_artifacts,
                errors=errors,
                metadata=metadata
            )
            
        except Exception as e:
            errors.append(f"Generation failed: {e}")
            return MicroserviceResult(
                success=False,
                microservice_name=spec.microservice_type,
                output_dir=microservice_dir,
                files_generated=files_generated,
                sprint_artifacts=sprint_artifacts,
                errors=errors,
                metadata={}
            )
    
    def _create_microservice_structure(self, microservice_dir: Path, spec: ParsedSpec):
        """Create the standard microservice directory structure."""
        # Core directories
        directories = [
            "src",
            "tests",
            "tests/unit",
            "tests/integration",
            "tests/contract",
            "docs",
            "scripts",
            "sprint-artifacts/planning",
            "sprint-artifacts/execution",
            "sprint-artifacts/review",
            "sprint-artifacts/retrospective",
            ".github/workflows"
        ]
        
        # Add containerization directories if deployment is configured
        if spec.deployment and spec.deployment.get('target') == 'kubernetes':
            directories.extend([
                "k8s",
                "terraform/aws",
                "terraform/azure",
                "docker"
            ])
        
        for directory in directories:
            (microservice_dir / directory).mkdir(parents=True, exist_ok=True)
    
    def _generate_core_microservice(self, microservice_dir: Path, spec: ParsedSpec, **kwargs) -> GenerationResult:
        """Generate core microservice using existing framework patterns."""
        # Use existing module generator with JSON specification data
        return self.module_generator.generate_module(
            module_name=spec.module_name,
            module_type=spec.module_type,
            output_dir=str(microservice_dir / "src"),
            with_docker=spec.deployment.get('target') == 'kubernetes' if spec.deployment else True,
            deployment_target=spec.deployment.get('cloud_provider', 'aws') if spec.deployment else 'aws',
            description=spec.metadata.get('description', f"Generated microservice: {spec.microservice_type}") if spec.metadata else None,
            **kwargs
        )
    
    def _generate_tdd_tests(self, microservice_dir: Path, spec: ParsedSpec) -> List[str]:
        """Generate TDD tests from JSON specification."""
        test_files = []
        
        # Generate test files for each TDD test specification
        for i, test_spec in enumerate(spec.tdd_tests):
            test_file_path = microservice_dir / "tests" / "unit" / f"test_{test_spec['test_name']}.py"
            
            test_content = self._generate_test_content(test_spec, spec)
            
            with open(test_file_path, 'w') as f:
                f.write(test_content)
            
            test_files.append(str(test_file_path.relative_to(microservice_dir)))
        
        # Generate integration tests
        integration_test_path = microservice_dir / "tests" / "integration" / f"test_{spec.module_name}_integration.py"
        integration_content = self._generate_integration_test_content(spec)
        
        with open(integration_test_path, 'w') as f:
            f.write(integration_content)
        
        test_files.append(str(integration_test_path.relative_to(microservice_dir)))
        
        return test_files
    
    def _generate_test_content(self, test_spec: Dict[str, Any], spec: ParsedSpec) -> str:
        """Generate individual test content from test specification."""
        return f'''"""
Test: {test_spec['test_name']}

{test_spec['description']}
Expected: {test_spec['expected_behavior']}

Generated from JSON specification for automated TDD development.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch

from src.{spec.module_name} import {spec.class_name}


class Test{spec.class_name}:
    """Test class for {spec.class_name} microservice."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.service = {spec.class_name}()
    
    def test_{test_spec['test_name']}(self):
        """
        Test: {test_spec['description']}
        
        Expected Behavior: {test_spec['expected_behavior']}
        
        Priority: {test_spec.get('priority', 'medium')}
        """
        # AI_TODO: Implement test logic based on specification
        # This test was generated from JSON TDD specification
        # Expected behavior: {test_spec['expected_behavior']}
        
        # Arrange
        # AI_IMPLEMENTATION_REQUIRED: Setup test data and mocks
        
        # Act
        # AI_IMPLEMENTATION_REQUIRED: Execute the functionality being tested
        
        # Assert
        # AI_IMPLEMENTATION_REQUIRED: Verify expected behavior
        assert True, "AI_TODO: Implement actual test logic"
    
    @pytest.mark.asyncio
    async def test_{test_spec['test_name']}_async(self):
        """Async version of {test_spec['test_name']} test."""
        # AI_TODO: Implement async test if needed
        # Some microservices may require async testing
        pass
'''
    
    def _generate_integration_test_content(self, spec: ParsedSpec) -> str:
        """Generate integration test content."""
        return f'''"""
Integration Tests for {spec.class_name} Microservice

Tests the complete microservice functionality including:
- API endpoints
- Database integration
- External service communication
- Performance requirements

Generated from JSON specification: {spec.microservice_type}
Domain: {spec.domain}
Performance requirement: {spec.requirements.get('performance', 'Not specified')}
"""

import pytest
import asyncio
import time
from unittest.mock import Mock, patch

from src.{spec.module_name} import {spec.class_name}


class Test{spec.class_name}Integration:
    """Integration tests for {spec.class_name} microservice."""
    
    def setup_method(self):
        """Setup integration test environment."""
        self.service = {spec.class_name}()
    
    def test_performance_requirement(self):
        """
        Test performance requirement: {spec.requirements.get('performance', 'Not specified')}
        """
        # AI_TODO: Implement performance test
        start_time = time.time()
        
        # AI_IMPLEMENTATION_REQUIRED: Execute performance-critical operation
        
        end_time = time.time()
        response_time_ms = (end_time - start_time) * 1000
        
        # Extract performance requirement from specification
        perf_req = "{spec.requirements.get('performance', '< 1000ms response time')}"
        if "ms" in perf_req:
            max_time = int(perf_req.split('<')[1].strip().split('ms')[0])
            assert response_time_ms < max_time, f"Response time {{response_time_ms}}ms exceeds requirement {{max_time}}ms"
    
    def test_security_requirements(self):
        """
        Test security requirements: {spec.requirements.get('security', 'Standard security practices')}
        """
        # AI_TODO: Implement security tests based on requirements
        # Security requirement: {spec.requirements.get('security', 'Not specified')}
        pass
    
    def test_integration_requirements(self):
        """
        Test integration with external services: {spec.requirements.get('integration', [])}
        """
        # AI_TODO: Test integration with external services
        external_services = {spec.requirements.get('integration', [])}
        for service in external_services:
            # AI_IMPLEMENTATION_REQUIRED: Test integration with {{service}}
            pass
'''
    
    def _generate_sprint_artifacts(self, microservice_dir: Path, spec: ParsedSpec) -> Dict[str, str]:
        """Generate automated agile sprint artifacts."""
        artifacts = {}
        
        # Sprint planning artifacts
        planning_dir = microservice_dir / "sprint-artifacts" / "planning"
        
        # Sprint goal
        sprint_goal = f"""# Microservice Sprint Goal: {spec.microservice_type}

**Microservice**: {spec.microservice_type}  
**Domain**: {spec.domain}  
**Type**: {spec.module_type}  

## Sprint Objective
Implement and deliver a production-ready {spec.microservice_type} microservice that meets all specified TDD requirements and performance criteria.

## Success Criteria
- [ ] All {len(spec.tdd_tests)} TDD tests pass
- [ ] Performance requirement met: {spec.requirements.get('performance', 'Not specified')}
- [ ] Security requirements implemented: {spec.requirements.get('security', 'Standard practices')}
- [ ] Integration with external services: {', '.join(spec.requirements.get('integration', ['None']))}
- [ ] Containerization and deployment ready
- [ ] Documentation complete
- [ ] AI code review passes with >75 score

## Generated from JSON Specification
This sprint was automatically generated from JSON specification using automated agile methodology.
"""
        
        sprint_goal_path = planning_dir / "sprint-goal.md"
        with open(sprint_goal_path, 'w') as f:
            f.write(sprint_goal)
        artifacts['sprint_goal'] = str(sprint_goal_path.relative_to(microservice_dir))
        
        # Definition of Done
        dod_content = f"""# Definition of Done: {spec.microservice_type}

## Functional Requirements
- [ ] All TDD tests pass ({len(spec.tdd_tests)} tests implemented)
- [ ] Performance requirement validated: {spec.requirements.get('performance')}
- [ ] Security requirements implemented and tested
- [ ] Integration tests pass for: {', '.join(spec.requirements.get('integration', ['N/A']))}

## Quality Requirements  
- [ ] AI code review score >75
- [ ] Test coverage >90%
- [ ] Documentation complete
- [ ] Containerization functional

## Deployment Requirements
- [ ] {spec.deployment.get('target', 'kubernetes') if spec.deployment else 'kubernetes'} deployment ready
- [ ] {spec.deployment.get('cloud_provider', 'aws') if spec.deployment else 'aws'} infrastructure configured
- [ ] Monitoring and health checks active
- [ ] Auto-scaling configured: {spec.deployment.get('auto_scaling', True) if spec.deployment else True}

## Business Value
- [ ] Meets domain requirements for {spec.domain}
- [ ] Ready for production deployment
- [ ] Supports automated agile self-improvement
"""
        
        dod_path = planning_dir / "definition-of-done.md"
        with open(dod_path, 'w') as f:
            f.write(dod_content)
        artifacts['definition_of_done'] = str(dod_path.relative_to(microservice_dir))
        
        return artifacts
    
    def _generate_microservice_automation(self, microservice_dir: Path, spec: ParsedSpec) -> List[str]:
        """Generate microservice-specific GitHub Actions and automation."""
        automation_files = []
        
        # Microservice CI/CD pipeline
        workflow_content = f"""name: {spec.class_name} CI/CD

on:
  push:
    paths:
      - 'microservices/{spec.microservice_type}/**'
  pull_request:
    paths:
      - 'microservices/{spec.microservice_type}/**'

jobs:
  test:
    name: Test {spec.class_name}
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install Dependencies
        working-directory: microservices/{spec.microservice_type}
        run: |
          pip install -r requirements.txt || echo "No requirements.txt found"
          pip install pytest pytest-asyncio pytest-cov
          
      - name: Run TDD Tests
        working-directory: microservices/{spec.microservice_type}
        run: |
          pytest tests/ -v --cov=src --cov-report=term-missing
          
      - name: Performance Test
        working-directory: microservices/{spec.microservice_type}
        run: |
          # Test performance requirement: {spec.requirements.get('performance', 'Not specified')}
          pytest tests/integration/ -v -k performance
          
  deploy:
    name: Deploy {spec.class_name}
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to {spec.deployment.get('cloud_provider', 'AWS') if spec.deployment else 'AWS'}
        run: |
          echo "Deploying {spec.microservice_type} to {spec.deployment.get('target', 'kubernetes') if spec.deployment else 'kubernetes'}"
          # AI_TODO: Implement actual deployment logic
"""
        
        workflow_path = microservice_dir / ".github" / "workflows" / f"{spec.module_name}-cicd.yml"
        with open(workflow_path, 'w') as f:
            f.write(workflow_content)
        automation_files.append(str(workflow_path.relative_to(microservice_dir)))
        
        return automation_files
    
    def _generate_documentation(self, microservice_dir: Path, spec: ParsedSpec) -> List[str]:
        """Generate microservice documentation."""
        doc_files = []
        
        # README
        readme_content = f"""# {spec.class_name} Microservice

**Domain**: {spec.domain}  
**Type**: {spec.module_type}  
**Generated**: Automatically from JSON specification

## Overview
{spec.metadata.get('description', f'Microservice for {spec.domain} domain') if spec.metadata else f'Microservice for {spec.domain} domain'}

## API Configuration
- **Type**: {spec.api.get('type', 'REST') if spec.api else 'REST'}
- **Version**: {spec.api.get('version', 'v1') if spec.api else 'v1'}
- **Authentication**: {spec.api.get('authentication', 'JWT') if spec.api else 'JWT'}

## Performance Requirements
- **Response Time**: {spec.requirements.get('performance', 'Not specified')}
- **Security**: {spec.requirements.get('security', 'Standard practices')}

## TDD Tests
This microservice includes {len(spec.tdd_tests)} TDD tests:

{chr(10).join(f"- **{test['test_name']}**: {test['description']}" for test in spec.tdd_tests)}

## Integration
External services: {', '.join(spec.requirements.get('integration', ['None']))}

## Deployment
- **Target**: {spec.deployment.get('target', 'kubernetes') if spec.deployment else 'kubernetes'}
- **Cloud**: {spec.deployment.get('cloud_provider', 'aws') if spec.deployment else 'aws'}
- **Auto-scaling**: {spec.deployment.get('auto_scaling', True) if spec.deployment else True}

## Development
This microservice was generated using the Standardized Modules Framework with automated agile methodology.

### Running Tests
```bash
pytest tests/ -v
```

### Running the Service
```bash
python src/{spec.module_name}/main.py
```

Generated by: JSON-to-Microservice Pipeline
"""
        
        readme_path = microservice_dir / "README.md"
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        doc_files.append(str(readme_path.relative_to(microservice_dir)))
        
        return doc_files
    
    def _generate_metadata(self, spec: ParsedSpec, files_generated: List[str], sprint_artifacts: Dict[str, str]) -> Dict[str, Any]:
        """Generate metadata about the microservice generation."""
        from datetime import datetime
        
        return {
            'generation_timestamp': datetime.now().isoformat(),
            'specification': {
                'microservice_type': spec.microservice_type,
                'domain': spec.domain,
                'module_type': spec.module_type,
                'tdd_tests_count': len(spec.tdd_tests),
                'performance_requirement': spec.requirements.get('performance'),
                'security_requirement': spec.requirements.get('security'),
                'integrations': spec.requirements.get('integration', [])
            },
            'generation_results': {
                'files_generated': len(files_generated),
                'sprint_artifacts': len(sprint_artifacts),
                'automated_agile_ready': True,
                'ai_completion_markers': True
            },
            'framework_version': '1.1.0',
            'generation_method': 'JSON-to-microservice pipeline'
        }


# Example usage
if __name__ == "__main__":
    # Example: Generate microservice from JSON
    example_spec = {
        "microservice_type": "payment-processor",
        "domain": "fintech",
        "module_type": "INTEGRATION",
        "tdd_tests": [
            {
                "test_name": "process_valid_payment",
                "description": "Should successfully process a valid payment request",
                "expected_behavior": "Returns success response with transaction ID"
            }
        ],
        "requirements": {
            "performance": "< 200ms response time",
            "security": "PCI DSS compliant payment processing",
            "integration": ["stripe", "paypal"]
        }
    }
    
    factory = MicroserviceFactory()
    result = factory.generate_from_json(json.dumps(example_spec))
    
    if result.success:
        print(f"✅ Generated microservice: {result.microservice_name}")
        print(f"   Files: {len(result.files_generated)}")
        print(f"   Sprint artifacts: {len(result.sprint_artifacts)}")
    else:
        print(f"❌ Generation failed: {result.errors}")
