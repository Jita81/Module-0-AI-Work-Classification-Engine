"""
Interface definition for CacheManager MCP Server

This module defines the interface contract that all TECHNICAL MCP servers
must implement for infrastructure domain operations.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from types import CacheManagerConfig, CacheManagerResult, HealthStatus


class CacheManagerInterface(ABC):
    """
    Interface contract for CacheManager MCP Server
    
    All TECHNICAL modules in the infrastructure domain must implement
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
    async def execute_primary_operation(self, data: Dict[str, Any]) -> CacheManagerResult:
        """Execute the primary business operation"""
        pass
