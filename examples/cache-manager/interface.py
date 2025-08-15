"""
Interface definition for cache-manager
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


from .types import CacheManagerConfig, CacheManagerInput, CacheManagerOutput, OperationResult, DomainEntity

from .types import CacheManagerConfig, CacheManagerRequest, CacheManagerResponse, OperationResult

from .types import CacheManagerConfig, CacheManagerRequest, CacheManagerResponse, OperationResult

from .types import CacheManagerConfig, TechnicalRequest, TechnicalResponse, OperationResult


class CacheManagerInterface(ABC):
    """
    Interface for cache-manager module
    Type: TECHNICAL
    
    Defines the contract that all cache-manager implementations must follow.
    """
    
    @abstractmethod
    def initialize(self) -> OperationResult:
        """
        Initialize the module
        
        Returns:
            OperationResult indicating success or failure
        """
        pass
    
    
    @abstractmethod
    def execute_primary_operation(self, input_data: CacheManagerInput) -> OperationResult[CacheManagerOutput]:
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
    
    
    @abstractmethod
    async def call_external_service(self, request: CacheManagerRequest) -> OperationResult[CacheManagerResponse]:
        """
        Make a call to the external service
        
        Args:
            request: Request data for the external service
            
        Returns:
            OperationResult containing the service response or error
        """
        pass
    
    
    @abstractmethod
    def execute_supporting_operation(self, request: CacheManagerRequest) -> OperationResult[CacheManagerResponse]:
        """
        Execute a supporting business operation
        
        Args:
            request: Request data for the supporting operation
            
        Returns:
            OperationResult containing the operation response or error
        """
        pass
    
    
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
