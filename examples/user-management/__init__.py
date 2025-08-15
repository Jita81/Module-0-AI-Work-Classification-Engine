"""
user-management - 

This module provides .
"""

from .core import UserManagementModule
from .interface import UserManagementInterface
from .types import (
    UserManagementConfig,
    
    UserManagementInput,
    UserManagementOutput,
    DomainEntity,
    BusinessRule,
    
    UserManagementRequest,
    UserManagementResponse,
    
    UserManagementRequest,
    UserManagementResponse,
    
    TechnicalRequest,
    TechnicalResponse,
    
    OperationResult,
    ModuleStatus
)

# Public API
__all__ = [
    "UserManagementModule",
    "UserManagementInterface",
    "UserManagementConfig",
    
    "UserManagementInput",
    "UserManagementOutput",
    "DomainEntity",
    "BusinessRule",
    
    "UserManagementRequest",
    "UserManagementResponse",
    
    "UserManagementRequest",
    "UserManagementResponse",
    
    "TechnicalRequest",
    "TechnicalResponse",
    
    "OperationResult",
    "ModuleStatus"
]

# Version information
__version__ = "1.0.0"
__author__ = ""
