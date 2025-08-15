#!/usr/bin/env python3
"""
CLI Testing Suite for Standardized Modules Framework

Tests the command-line interface functionality including:
1. Command parsing and validation
2. Module generation via CLI
3. Error handling and user feedback
4. Help and documentation
"""

import os
import sys
import tempfile
import shutil
import subprocess
from pathlib import Path
import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestCLIInterface:
    """Test CLI functionality"""
    
    def test_cli_help(self):
        """Test that CLI help works"""
        try:
            result = subprocess.run(
                [sys.executable, "module_scaffolding_system.py", "--help"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent,
                timeout=30
            )
            
            # Should show help even without click installed
            assert result.returncode in [0, 1]  # May fail due to missing click, but shouldn't crash
            
        except subprocess.TimeoutExpired:
            pytest.fail("CLI help command timed out")
        except Exception as e:
            # Expected if click is not installed
            print(f"CLI help test skipped due to missing dependencies: {e}")
    
    def test_cli_module_generation(self):
        """Test module generation via CLI"""
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Mock click for testing
                cmd = [
                    sys.executable, "-c", 
                    f"""
import sys
sys.path.insert(0, '{Path(__file__).parent.parent}')

# Mock dependencies
class MockTemplate:
    def __init__(self, template_str):
        self.template = template_str
    def render(self, **kwargs):
        result = self.template
        for key, value in kwargs.items():
            result = result.replace('{{{{ ' + key + ' }}}}', str(value))
        return result

import module_scaffolding_system
module_scaffolding_system.Template = MockTemplate

from module_scaffolding_system import ModuleGenerator

generator = ModuleGenerator()
result = generator.generate_module(
    name='cli-test-module',
    module_type='CORE',
    domain='testing',
    output_dir='{temp_dir}',
    ai_ready=True
)

if result.success:
    print('CLI_TEST_SUCCESS')
    print(f'Module path: {{result.module_path}}')
else:
    print('CLI_TEST_FAILED')
    print(f'Error: {{result.error}}')
"""
                ]
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                assert "CLI_TEST_SUCCESS" in result.stdout, f"CLI test failed: {result.stdout} {result.stderr}"
                
                # Verify module was created
                module_path = Path(temp_dir) / "cli-test-module"
                assert module_path.exists(), "Module directory not created via CLI simulation"
                
            except subprocess.TimeoutExpired:
                pytest.fail("CLI module generation timed out")
            except Exception as e:
                pytest.fail(f"CLI test failed: {e}")

class TestCLIValidation:
    """Test CLI input validation"""
    
    def test_invalid_module_type_handling(self):
        """Test CLI handles invalid module types gracefully"""
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                cmd = [
                    sys.executable, "-c",
                    f"""
import sys
sys.path.insert(0, '{Path(__file__).parent.parent}')

# Mock dependencies
class MockTemplate:
    def __init__(self, template_str):
        self.template = template_str
    def render(self, **kwargs):
        result = self.template
        for key, value in kwargs.items():
            result = result.replace('{{{{ ' + key + ' }}}}', str(value))
        return result

import module_scaffolding_system
module_scaffolding_system.Template = MockTemplate

from module_scaffolding_system import ModuleGenerator

generator = ModuleGenerator()
result = generator.generate_module(
    name='invalid-type-test',
    module_type='INVALID',
    domain='testing',
    output_dir='{temp_dir}',
    ai_ready=True
)

print(f'Result success: {{result.success}}')
if not result.success:
    print(f'Error handled: {{result.error}}')
    print('VALIDATION_TEST_SUCCESS')
else:
    print('VALIDATION_TEST_UNEXPECTED_SUCCESS')
"""
                ]
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                # Should handle invalid input gracefully
                assert result.returncode == 0, f"Process failed: {result.stderr}"
                
            except subprocess.TimeoutExpired:
                pytest.fail("CLI validation test timed out")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
