"""
Type definitions for ai-work-classification-engine
"""

from typing import Dict, Any, List, Optional, Generic, TypeVar
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

T = TypeVar('T')

@dataclass
class AiWorkClassificationEngineConfig:
    """Configuration for ai-work-classification-engine module"""
    
    # AI_TODO: Define configuration fields for business logic
    domain: str = "ai-analysis"
    persist_audit_trail: bool = True
    max_audit_events: int = 1000
    # AI_TODO: Add domain-specific configuration
    


@dataclass
class AiWorkClassificationEngineInput:
    """Input data for ai-work-classification-engine operations"""
    # AI_TODO: Define input fields for your business operations
    operation_type: str = "default"
    # AI_TODO: Add business-specific input fields

@dataclass
class AiWorkClassificationEngineOutput:
    """Output data from ai-work-classification-engine operations"""
    # AI_TODO: Define output fields for your business results
    result: str
    audit_trail: List[Dict[str, Any]] = None
    # AI_TODO: Add business-specific output fields

@dataclass
class DomainEntity:
    """Core domain entity for ai-work-classification-engine"""
    # AI_TODO: Define your main business entity
    entity_id: str
    created_at: datetime
    updated_at: datetime
    # AI_TODO: Add domain-specific entity fields

@dataclass
class BusinessRule:
    """Business rule definition"""
    name: str
    description: str
    validation_function: callable = None
    is_active: bool = True



class OperationResult(Generic[T]):
    """Standard result wrapper for all operations"""
    
    def __init__(self, success: bool, data: T = None, error: str = None, error_code: str = None):
        self.success = success
        self.data = data
        self.error = error
        self.error_code = error_code
        self.timestamp = datetime.utcnow()
    
    @classmethod
    def success(cls, data: T = None) -> 'OperationResult[T]':
        """Create a successful result"""
        return cls(success=True, data=data)
    
    @classmethod
    def error(cls, error: str, error_code: str = None) -> 'OperationResult[T]':
        """Create an error result"""
        return cls(success=False, error=error, error_code=error_code)
    
    def __bool__(self) -> bool:
        return self.success

class ModuleStatus(Enum):
    """Module status enumeration"""
    INITIALIZING = "initializing"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    SHUTTING_DOWN = "shutting_down"
    SHUTDOWN = "shutdown"