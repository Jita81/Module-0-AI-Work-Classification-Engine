#!/usr/bin/env python3
"""
Comprehensive Test Suite for Standardized Modules Framework

This test suite validates:
1. All module types generate correctly
2. Generated modules are syntactically valid
3. Generated files are complete and properly structured
4. AI completion guides are comprehensive
5. Template rendering works correctly
6. Edge cases and error conditions
"""

import os
import sys
import tempfile
import shutil
import ast
import pytest
from pathlib import Path
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Mock dependencies for testing
class MockTemplate:
    def __init__(self, template_str):
        self.template = template_str
    
    def render(self, **kwargs):
        result = self.template
        for key, value in kwargs.items():
            result = result.replace('{{ ' + key + ' }}', str(value))
            # Handle conditional blocks
            if '{% if ' + key + ' %}' in result:
                if value:
                    result = result.replace('{% if ' + key + ' %}', '').replace('{% endif %}', '')
                else:
                    # Remove conditional content
                    import re
                    pattern = r'{% if ' + key + ' %}.*?{% endif %}'
                    result = re.sub(pattern, '', result, flags=re.DOTALL)
        # Clean up remaining template syntax
        import re
        result = re.sub(r'{%.*?%}', '', result)
        result = re.sub(r'{{.*?}}', '', result)
        return result

# Patch the Template class
import module_scaffolding_system
module_scaffolding_system.Template = MockTemplate

from module_scaffolding_system import ModuleGenerator, ModuleTemplates, GenerationResult

class TestModuleGeneration:
    """Test module generation for all types"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test output"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def generator(self):
        """Create module generator instance"""
        return ModuleGenerator()
    
    @pytest.mark.parametrize("module_type", ["CORE", "INTEGRATION", "SUPPORTING", "TECHNICAL"])
    def test_module_generation_success(self, generator, temp_dir, module_type):
        """Test that all module types generate successfully"""
        module_name = f"test-{module_type.lower()}"
        
        result = generator.generate_module(
            name=module_name,
            module_type=module_type,
            domain="testing",
            output_dir=temp_dir,
            ai_ready=True
        )
        
        assert result.success, f"Failed to generate {module_type} module: {result.error}"
        assert result.module_path is not None
        assert result.ai_completion_file is not None
        
        # Verify module directory exists
        module_path = Path(result.module_path)
        assert module_path.exists(), f"Module directory not created: {module_path}"
    
    @pytest.mark.parametrize("module_type", ["CORE", "INTEGRATION", "SUPPORTING", "TECHNICAL"])
    def test_required_files_generated(self, generator, temp_dir, module_type):
        """Test that all required files are generated"""
        module_name = f"test-{module_type.lower()}"
        
        result = generator.generate_module(
            name=module_name,
            module_type=module_type,
            domain="testing",
            output_dir=temp_dir,
            ai_ready=True
        )
        
        assert result.success
        
        module_path = Path(result.module_path)
        expected_files = [
            'core.py',
            'types.py',
            'interface.py',
            '__init__.py',
            'tests/test_core.py',
            'tests/test_contracts.py',
            'AI_COMPLETION.md',
            'requirements.txt',
            'pytest.ini',
            '.gitignore'
        ]
        
        for file_name in expected_files:
            file_path = module_path / file_name
            assert file_path.exists(), f"Missing required file: {file_name}"
            
            # Check file is not empty
            assert file_path.stat().st_size > 0, f"Empty file: {file_name}"
    
    @pytest.mark.parametrize("module_type", ["CORE", "INTEGRATION", "SUPPORTING", "TECHNICAL"])
    def test_python_syntax_validity(self, generator, temp_dir, module_type):
        """Test that generated Python files have valid syntax"""
        module_name = f"test-{module_type.lower()}"
        
        result = generator.generate_module(
            name=module_name,
            module_type=module_type,
            domain="testing",
            output_dir=temp_dir,
            ai_ready=True
        )
        
        assert result.success
        
        module_path = Path(result.module_path)
        python_files = [
            'core.py',
            'types.py',
            'interface.py',
            '__init__.py',
            'tests/test_core.py',
            'tests/test_contracts.py'
        ]
        
        for file_name in python_files:
            file_path = module_path / file_name
            if file_path.exists():
                with open(file_path, 'r') as f:
                    content = f.read()
                
                try:
                    ast.parse(content)
                except SyntaxError as e:
                    pytest.fail(f"Syntax error in {file_name}: {e}")
    
    def test_class_name_conversion(self, generator):
        """Test module name to class name conversion"""
        test_cases = [
            ("user-management", "UserManagement"),
            ("payment-gateway", "PaymentGateway"),
            ("simple", "Simple"),
            ("multi-word-module", "MultiWordModule"),
            ("api-v2-client", "ApiV2Client")
        ]
        
        for module_name, expected_class_name in test_cases:
            actual_class_name = generator._to_class_name(module_name)
            assert actual_class_name == expected_class_name, \
                f"Expected {expected_class_name}, got {actual_class_name}"
    
    def test_ai_ready_flag(self, generator, temp_dir):
        """Test AI-ready flag affects generated content"""
        module_name = "test-ai-flag"
        
        # Generate with AI ready
        result_ai = generator.generate_module(
            name=f"{module_name}-ai",
            module_type="CORE",
            domain="testing",
            output_dir=temp_dir,
            ai_ready=True
        )
        
        # Generate without AI ready
        result_no_ai = generator.generate_module(
            name=f"{module_name}-no-ai",
            module_type="CORE",
            domain="testing",
            output_dir=temp_dir,
            ai_ready=False
        )
        
        assert result_ai.success
        assert result_no_ai.success
        
        # Check AI completion file differences
        ai_completion_ai = Path(result_ai.module_path) / "AI_COMPLETION.md"
        ai_completion_no_ai = Path(result_no_ai.module_path) / "AI_COMPLETION.md"
        
        with open(ai_completion_ai, 'r') as f:
            content_ai = f.read()
        
        with open(ai_completion_no_ai, 'r') as f:
            content_no_ai = f.read()
        
        # AI version should have more AI-specific content
        assert len(content_ai) >= len(content_no_ai), \
            "AI-ready version should have more comprehensive completion guide"

class TestTemplateEngine:
    """Test template generation functionality"""
    
    @pytest.fixture
    def templates(self):
        """Create template engine instance"""
        return ModuleTemplates()
    
    @pytest.fixture
    def context(self):
        """Sample template context"""
        return {
            'module_name': 'test-module',
            'class_name': 'TestModule',
            'module_type': 'CORE',
            'domain': 'testing',
            'ai_ready': True
        }
    
    def test_core_module_template(self, templates, context):
        """Test CORE module template generation"""
        content = templates.generate_core_module('CORE', context)
        
        assert content is not None
        assert len(content) > 0
        assert 'TestModule' in content
        assert 'test-module' in content
        assert 'CORE' in content
    
    def test_integration_module_template(self, templates, context):
        """Test INTEGRATION module template generation"""
        content = templates.generate_core_module('INTEGRATION', context)
        
        assert content is not None
        assert len(content) > 0
        assert 'aiohttp' in content
        assert 'circuit_breaker' in content
        assert 'INTEGRATION' in content
    
    def test_supporting_module_template(self, templates, context):
        """Test SUPPORTING module template generation"""
        content = templates.generate_core_module('SUPPORTING', context)
        
        assert content is not None
        assert len(content) > 0
        assert 'workflow' in content
        assert 'SUPPORTING' in content
    
    def test_technical_module_template(self, templates, context):
        """Test TECHNICAL module template generation"""
        content = templates.generate_core_module('TECHNICAL', context)
        
        assert content is not None
        assert len(content) > 0
        assert 'performance' in content
        assert 'TECHNICAL' in content
    
    def test_types_file_generation(self, templates, context):
        """Test types file template generation"""
        for module_type in ['CORE', 'INTEGRATION', 'SUPPORTING', 'TECHNICAL']:
            content = templates.generate_types_file(module_type, context)
            
            assert content is not None
            assert len(content) > 0
            assert 'OperationResult' in content
            assert 'TestModuleConfig' in content
    
    def test_interface_file_generation(self, templates, context):
        """Test interface file template generation"""
        for module_type in ['CORE', 'INTEGRATION', 'SUPPORTING', 'TECHNICAL']:
            content = templates.generate_interface_file(module_type, context)
            
            assert content is not None
            assert len(content) > 0
            assert 'TestModuleInterface' in content
            assert 'abstractmethod' in content
    
    def test_ai_completion_generation(self, templates, context):
        """Test AI completion guide generation"""
        for module_type in ['CORE', 'INTEGRATION', 'SUPPORTING', 'TECHNICAL']:
            content = templates.generate_ai_completion_file(module_type, context)
            
            assert content is not None
            assert len(content) > 0
            assert 'AI Completion Guide' in content
            assert 'Your Task' in content

class TestErrorHandling:
    """Test error conditions and edge cases"""
    
    @pytest.fixture
    def generator(self):
        """Create module generator instance"""
        return ModuleGenerator()
    
    def test_invalid_module_type(self, generator):
        """Test handling of invalid module type"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = generator.generate_module(
                name="test-invalid",
                module_type="INVALID_TYPE",
                domain="testing",
                output_dir=temp_dir,
                ai_ready=True
            )
            
            # Should handle gracefully
            assert isinstance(result, GenerationResult)
    
    def test_invalid_output_directory(self, generator):
        """Test handling of invalid output directory"""
        # Try to write to a non-existent parent directory
        invalid_path = "/this/path/does/not/exist"
        
        result = generator.generate_module(
            name="test-invalid-path",
            module_type="CORE",
            domain="testing",
            output_dir=invalid_path,
            ai_ready=True
        )
        
        # Should fail gracefully
        assert not result.success
        assert result.error is not None
    
    def test_empty_module_name(self, generator):
        """Test handling of empty module name"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = generator.generate_module(
                name="",
                module_type="CORE",
                domain="testing",
                output_dir=temp_dir,
                ai_ready=True
            )
            
            # Should handle gracefully
            assert isinstance(result, GenerationResult)
    
    def test_special_characters_in_name(self, generator):
        """Test handling of special characters in module name"""
        with tempfile.TemporaryDirectory() as temp_dir:
            special_names = [
                "test@module",
                "test module",
                "test.module",
                "test/module",
                "test\\module"
            ]
            
            for name in special_names:
                result = generator.generate_module(
                    name=name,
                    module_type="CORE",
                    domain="testing",
                    output_dir=temp_dir,
                    ai_ready=True
                )
                
                # Should handle gracefully (either succeed or fail gracefully)
                assert isinstance(result, GenerationResult)

class TestFileContent:
    """Test generated file content quality"""
    
    @pytest.fixture
    def generator(self):
        return ModuleGenerator()
    
    def test_ai_completion_guide_completeness(self, generator):
        """Test that AI completion guides are comprehensive"""
        with tempfile.TemporaryDirectory() as temp_dir:
            for module_type in ['CORE', 'INTEGRATION', 'SUPPORTING', 'TECHNICAL']:
                result = generator.generate_module(
                    name=f"test-{module_type.lower()}",
                    module_type=module_type,
                    domain="testing",
                    output_dir=temp_dir,
                    ai_ready=True
                )
                
                assert result.success
                
                ai_completion_path = Path(result.ai_completion_file)
                with open(ai_completion_path, 'r') as f:
                    content = f.read()
                
                # Check for essential AI completion elements
                required_sections = [
                    "Your Task",
                    "What You Need to Complete",
                    "Getting Started",
                    "Framework Features Already Available",
                    "Quality Checklist"
                ]
                
                for section in required_sections:
                    assert section in content, \
                        f"Missing section '{section}' in {module_type} AI completion guide"
    
    def test_import_statements_validity(self, generator):
        """Test that generated import statements are valid"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = generator.generate_module(
                name="test-imports",
                module_type="CORE",
                domain="testing",
                output_dir=temp_dir,
                ai_ready=True
            )
            
            assert result.success
            
            # Check core.py imports
            core_path = Path(result.module_path) / "core.py"
            with open(core_path, 'r') as f:
                content = f.read()
            
            # Should have proper relative imports
            assert "from .interface import" in content
            assert "from .types import" in content
    
    def test_class_inheritance(self, generator):
        """Test that generated classes properly inherit from interfaces"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = generator.generate_module(
                name="test-inheritance",
                module_type="CORE",
                domain="testing",
                output_dir=temp_dir,
                ai_ready=True
            )
            
            assert result.success
            
            # Check that core module inherits from interface
            core_path = Path(result.module_path) / "core.py"
            with open(core_path, 'r') as f:
                content = f.read()
            
            assert "TestInheritanceInterface" in content
            assert "class TestInheritanceModule(TestInheritanceInterface)" in content

class TestPerformance:
    """Test framework performance"""
    
    def test_generation_speed(self):
        """Test that module generation is reasonably fast"""
        import time
        
        generator = ModuleGenerator()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            start_time = time.time()
            
            result = generator.generate_module(
                name="performance-test",
                module_type="CORE",
                domain="testing",
                output_dir=temp_dir,
                ai_ready=True
            )
            
            end_time = time.time()
            generation_time = end_time - start_time
            
            assert result.success
            # Should generate in under 5 seconds (very generous)
            assert generation_time < 5.0, f"Generation took {generation_time:.2f} seconds"
    
    def test_memory_usage(self):
        """Test that module generation doesn't use excessive memory"""
        import tracemalloc
        
        tracemalloc.start()
        
        generator = ModuleGenerator()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate multiple modules to test memory accumulation
            for i in range(5):
                result = generator.generate_module(
                    name=f"memory-test-{i}",
                    module_type="CORE",
                    domain="testing",
                    output_dir=temp_dir,
                    ai_ready=True
                )
                assert result.success
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Peak memory should be reasonable (less than 100MB)
        peak_mb = peak / 1024 / 1024
        assert peak_mb < 100, f"Peak memory usage: {peak_mb:.2f} MB"

class TestIntegration:
    """Test integration scenarios"""
    
    def test_multiple_modules_same_directory(self):
        """Test generating multiple modules in same directory"""
        generator = ModuleGenerator()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            module_types = ['CORE', 'INTEGRATION', 'SUPPORTING', 'TECHNICAL']
            
            for module_type in module_types:
                result = generator.generate_module(
                    name=f"multi-{module_type.lower()}",
                    module_type=module_type,
                    domain="testing",
                    output_dir=temp_dir,
                    ai_ready=True
                )
                
                assert result.success, f"Failed to generate {module_type} module"
            
            # Verify all modules exist
            for module_type in module_types:
                module_path = Path(temp_dir) / f"multi-{module_type.lower()}"
                assert module_path.exists(), f"Module directory missing: {module_path}"
    
    def test_nested_directory_creation(self):
        """Test creating modules in nested directories"""
        generator = ModuleGenerator()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_path = Path(temp_dir) / "level1" / "level2" / "level3"
            
            result = generator.generate_module(
                name="nested-test",
                module_type="CORE",
                domain="testing",
                output_dir=str(nested_path),
                ai_ready=True
            )
            
            assert result.success
            
            # Verify nested structure was created
            module_path = nested_path / "nested-test"
            assert module_path.exists()
            assert (module_path / "core.py").exists()

if __name__ == "__main__":
    # Run tests if executed directly
    import subprocess
    import sys
    
    # Install pytest if not available
    try:
        import pytest
    except ImportError:
        print("Installing pytest...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest"])
        import pytest
    
    # Run the tests
    pytest.main([__file__, "-v", "--tb=short"])
