"""
notification-service - 

This module provides .
"""

from .core import NotificationServiceModule
from .interface import NotificationServiceInterface
from .types import (
    NotificationServiceConfig,
    
    NotificationServiceInput,
    NotificationServiceOutput,
    DomainEntity,
    BusinessRule,
    
    NotificationServiceRequest,
    NotificationServiceResponse,
    
    NotificationServiceRequest,
    NotificationServiceResponse,
    
    TechnicalRequest,
    TechnicalResponse,
    
    OperationResult,
    ModuleStatus
)

# Public API
__all__ = [
    "NotificationServiceModule",
    "NotificationServiceInterface",
    "NotificationServiceConfig",
    
    "NotificationServiceInput",
    "NotificationServiceOutput",
    "DomainEntity",
    "BusinessRule",
    
    "NotificationServiceRequest",
    "NotificationServiceResponse",
    
    "NotificationServiceRequest",
    "NotificationServiceResponse",
    
    "TechnicalRequest",
    "TechnicalResponse",
    
    "OperationResult",
    "ModuleStatus"
]

# Version information
__version__ = "1.0.0"
__author__ = ""
