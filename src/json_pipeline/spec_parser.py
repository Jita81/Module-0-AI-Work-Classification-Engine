"""
JSON Specification Parser

Parses and validates JSON microservice specifications against the schema,
providing structured data for the microservice factory.
"""

import json
import jsonschema
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class ParsedSpec:
    """Parsed and validated microservice specification."""
    microservice_type: str
    domain: str
    module_type: str
    tdd_tests: List[Dict[str, Any]]
    requirements: Dict[str, Any]
    deployment: Optional[Dict[str, Any]] = None
    api: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
    monitoring: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    
    @property
    def class_name(self) -> str:
        """Generate class name from microservice type."""
        return ''.join(word.capitalize() for word in self.microservice_type.split('-'))
    
    @property
    def module_name(self) -> str:
        """Generate module name from microservice type."""
        return self.microservice_type.replace('-', '_')


class SpecParser:
    """JSON specification parser and validator."""
    
    def __init__(self, schema_path: Optional[str] = None):
        """Initialize parser with JSON schema."""
        if schema_path is None:
            # Default to the framework's schema
            schema_path = Path(__file__).parent.parent.parent / '.github' / 'templates' / 'microservice-json-schema.json'
        
        self.schema_path = Path(schema_path)
        self.schema = self._load_schema()
    
    def _load_schema(self) -> Dict[str, Any]:
        """Load and return the JSON schema."""
        try:
            with open(self.schema_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise ValueError(f"Failed to load JSON schema from {self.schema_path}: {e}")
    
    def parse_file(self, spec_file: str) -> ParsedSpec:
        """Parse microservice specification from JSON file."""
        try:
            with open(spec_file, 'r') as f:
                spec_data = json.load(f)
            return self.parse_dict(spec_data)
        except Exception as e:
            raise ValueError(f"Failed to parse specification file {spec_file}: {e}")
    
    def parse_dict(self, spec_data: Dict[str, Any]) -> ParsedSpec:
        """Parse microservice specification from dictionary."""
        # Validate against schema
        try:
            jsonschema.validate(spec_data, self.schema)
        except jsonschema.ValidationError as e:
            raise ValueError(f"Specification validation failed: {e.message}")
        except Exception as e:
            raise ValueError(f"Schema validation error: {e}")
        
        # Apply defaults for optional fields
        spec_data = self._apply_defaults(spec_data)
        
        # Create parsed specification object
        return ParsedSpec(
            microservice_type=spec_data['microservice_type'],
            domain=spec_data['domain'],
            module_type=spec_data.get('module_type', 'CORE'),
            tdd_tests=spec_data['tdd_tests'],
            requirements=spec_data['requirements'],
            deployment=spec_data.get('deployment'),
            api=spec_data.get('api'),
            data=spec_data.get('data'),
            monitoring=spec_data.get('monitoring'),
            metadata=spec_data.get('metadata')
        )
    
    def _apply_defaults(self, spec_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply default values based on schema."""
        # Set default module_type
        if 'module_type' not in spec_data:
            spec_data['module_type'] = 'CORE'
        
        # Set default deployment configuration
        if 'deployment' not in spec_data:
            spec_data['deployment'] = {
                'target': 'kubernetes',
                'cloud_provider': 'aws',
                'auto_scaling': True,
                'high_availability': True
            }
        
        # Set default API configuration
        if 'api' not in spec_data:
            spec_data['api'] = {
                'type': 'REST',
                'version': 'v1',
                'authentication': 'JWT',
                'rate_limiting': {
                    'requests_per_minute': 1000,
                    'burst_size': 10
                }
            }
        
        # Set default data configuration
        if 'data' not in spec_data:
            spec_data['data'] = {
                'storage': 'postgresql',
                'caching': True,
                'backup': True,
                'encryption': True
            }
        
        # Set default monitoring configuration
        if 'monitoring' not in spec_data:
            spec_data['monitoring'] = {
                'metrics': True,
                'logging': 'structured',
                'tracing': True,
                'health_checks': True
            }
        
        # Set default metadata
        if 'metadata' not in spec_data:
            spec_data['metadata'] = {
                'version': '1.0.0',
                'description': f"Generated microservice: {spec_data['microservice_type']}"
            }
        
        return spec_data
    
    def validate_spec(self, spec_data: Dict[str, Any]) -> List[str]:
        """Validate specification and return list of issues."""
        issues = []
        
        try:
            jsonschema.validate(spec_data, self.schema)
        except jsonschema.ValidationError as e:
            issues.append(f"Schema validation: {e.message}")
        except Exception as e:
            issues.append(f"Validation error: {e}")
        
        # Additional business logic validation
        if 'tdd_tests' in spec_data:
            test_names = [test.get('test_name', '') for test in spec_data['tdd_tests']]
            if len(test_names) != len(set(test_names)):
                issues.append("TDD tests must have unique test_name values")
        
        if 'requirements' in spec_data and 'performance' in spec_data['requirements']:
            perf_req = spec_data['requirements']['performance']
            if not perf_req.endswith('response time'):
                issues.append("Performance requirement must specify 'response time'")
        
        return issues


def parse_specification(spec_input: str) -> ParsedSpec:
    """
    Convenience function to parse specification from file or JSON string.
    
    Args:
        spec_input: Path to JSON file or JSON string
        
    Returns:
        ParsedSpec: Validated and parsed specification
    """
    parser = SpecParser()
    
    # Try to parse as file first
    try:
        if Path(spec_input).exists():
            return parser.parse_file(spec_input)
    except (OSError, IOError):
        pass
    
    # Try to parse as JSON string
    try:
        spec_data = json.loads(spec_input)
        return parser.parse_dict(spec_data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON specification: {e}")


# Example usage
if __name__ == "__main__":
    # Example JSON specification
    example_spec = {
        "microservice_type": "user-auth-api",
        "domain": "authentication",
        "tdd_tests": [
            {
                "test_name": "authenticate_valid_user",
                "description": "Should authenticate user with valid credentials",
                "expected_behavior": "Returns JWT token and user profile"
            }
        ],
        "requirements": {
            "performance": "< 100ms response time",
            "security": "OAuth2 and JWT token validation"
        }
    }
    
    # Parse the specification
    parser = SpecParser()
    try:
        parsed = parser.parse_dict(example_spec)
        print(f"✅ Parsed specification for: {parsed.microservice_type}")
        print(f"   Class name: {parsed.class_name}")
        print(f"   Module name: {parsed.module_name}")
        print(f"   TDD tests: {len(parsed.tdd_tests)}")
    except Exception as e:
        print(f"❌ Parsing failed: {e}")
