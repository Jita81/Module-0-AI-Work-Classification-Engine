"""
Interface definition for TestPaymentProcessor MCP Server

This module defines the interface contract that all CORE MCP servers
must implement for payments domain operations.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from types import TestPaymentProcessorConfig, TestPaymentProcessorResult, HealthStatus


class TestPaymentProcessorInterface(ABC):
    """
    Interface contract for TestPaymentProcessor MCP Server
    
    All CORE modules in the payments domain must implement
    this interface to ensure consistent API behavior and AI discoverability.
    """
    
    @abstractmethod
    async def initialize(self) -> bool:
        """
        Initialize the MCP server and all required resources
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check and return current status
        
        Returns:
            Dict: Current health status with details
        """
        pass
    
    @abstractmethod
    async def get_capabilities(self) -> Dict[str, Any]:
        """
        Get module capabilities for AI discovery
        
        Returns:
            Dict: Complete capabilities description including:
            - Available API endpoints
            - Integration patterns
            - Business capabilities
            - Technical specifications
        """
        pass
    
    @abstractmethod
    async def get_api_schema(self) -> Dict[str, Any]:
        """
        Get complete API schema in OpenAPI format
        
        Returns:
            Dict: OpenAPI 3.0 schema for all endpoints
        """
        pass
    
    @abstractmethod
    async def cleanup(self) -> None:
        """
        Cleanup all resources and prepare for shutdown
        """
        pass
    
    # AI_TODO: Add domain-specific interface methods
    # Each module type should define its core operations here
    
    @abstractmethod
    async def execute_primary_operation(self, data: Dict[str, Any]) -> TestPaymentProcessorResult:
        """Execute the primary business operation"""
        pass
