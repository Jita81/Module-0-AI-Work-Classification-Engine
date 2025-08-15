"""
Type definitions for payment-gateway
"""

from typing import Dict, Any, List, Optional, Generic, TypeVar
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

T = TypeVar('T')

@dataclass
class PaymentGatewayConfig:
    """Configuration for payment-gateway module"""
    
    # 
    domain: str = "payments"
    persist_audit_trail: bool = True
    max_audit_events: int = 1000
    # AI_TODO: Add domain-specific configuration
    
    # 
    base_url: str
    api_key: str
    timeout_seconds: int = 30
    circuit_breaker_config: Dict[str, Any] = None
    retry_config: Dict[str, Any] = None
    rate_limit_config: Dict[str, Any] = None
    # AI_TODO: Add service-specific configuration
    
    # 
    workflow_timeout: int = 300
    max_concurrent_workflows: int = 10
    # AI_TODO: Add workflow-specific configuration
    
    # 
    resource_pool_size: int = 10
    performance_monitoring: bool = True
    # AI_TODO: Add infrastructure-specific configuration
    


@dataclass
class PaymentGatewayInput:
    """Input data for payment-gateway operations"""
    # 
    operation_type: str = "default"
    # AI_TODO: Add business-specific input fields

@dataclass
class PaymentGatewayOutput:
    """Output data from payment-gateway operations"""
    # 
    result: str
    audit_trail: List[Dict[str, Any]] = None
    # AI_TODO: Add business-specific output fields

@dataclass
class DomainEntity:
    """Core domain entity for payment-gateway"""
    # 
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


@dataclass
class PaymentGatewayRequest:
    """Request data for external service calls"""
    # 
    request_id: str
    operation: str
    # AI_TODO: Add service-specific request fields

@dataclass
class PaymentGatewayResponse:
    """Response data from external service"""
    # 
    response_id: str
    status: str
    data: Dict[str, Any] = None
    # AI_TODO: Add service-specific response fields


@dataclass
class PaymentGatewayRequest:
    """Request data for supporting operations"""
    # 
    workflow_id: str
    operation_type: str
    # AI_TODO: Add workflow-specific request fields

@dataclass
class PaymentGatewayResponse:
    """Response data from supporting operations"""
    # 
    workflow_id: str
    status: str
    data: Dict[str, Any] = None
    # AI_TODO: Add workflow-specific response fields


@dataclass
class TechnicalRequest:
    """Request data for technical operations"""
    # 
    operation: str
    parameters: Dict[str, Any]
    # AI_TODO: Add infrastructure-specific request fields

@dataclass
class TechnicalResponse:
    """Response data from technical operations"""
    # 
    operation: str
    result: Dict[str, Any]
    performance_metrics: Dict[str, Any] = None
    # AI_TODO: Add infrastructure-specific response fields


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
