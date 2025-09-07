"""
Interface definition for ai-work-classification-engine
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


from classification_types import AiWorkClassificationEngineConfig, AiWorkClassificationEngineInput, AiWorkClassificationEngineOutput, OperationResult, DomainEntity


class AiWorkClassificationEngineInterface(ABC):
    """
    Interface for ai-work-classification-engine module
    Type: CORE
    
    Defines the contract that all ai-work-classification-engine implementations must follow.
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
    def execute_primary_operation(self, input_data: AiWorkClassificationEngineInput) -> OperationResult[AiWorkClassificationEngineOutput]:
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