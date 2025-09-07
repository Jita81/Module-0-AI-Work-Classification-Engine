"""
Contract compliance tests for ai-work-classification-engine
These tests verify that the module correctly implements its interface contract.
"""

import pytest
from abc import ABC

from ..core import AiWorkClassificationEngineModule
from ..interface import AiWorkClassificationEngineInterface

from ..types import AiWorkClassificationEngineConfig, AiWorkClassificationEngineInput, AiWorkClassificationEngineOutput, OperationResult


class TestContractCompliance:
    """Test that AiWorkClassificationEngineModule complies with its interface contract"""
    
    @pytest.fixture
    def config(self):
        """Create test configuration"""
        
        return AiWorkClassificationEngineConfig(domain="ai-analysis")
        
    
    @pytest.fixture
    def module(self, config):
        """Create module instance for testing"""
        return AiWorkClassificationEngineModule(config)
    
    def test_implements_interface(self, module):
        """Test that module implements the required interface"""
        assert isinstance(module, AiWorkClassificationEngineInterface)
        assert not isinstance(module, ABC)  # Should not be abstract
    
    def test_interface_methods_exist(self, module):
        """Test that all interface methods are implemented"""
        required_methods = [
            'initialize',
            
            'execute_primary_operation',
            'get_domain_entity',
            'apply_business_rule',
            
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
    
    
    def test_execute_primary_operation_signature(self, module):
        """Test primary operation method signature"""
        module.initialize()
        input_data = AiWorkClassificationEngineInput()
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
        
        input_data = AiWorkClassificationEngineInput()
        result = module.execute_primary_operation(input_data)
        assert not result.success
        assert result.error is not None
        