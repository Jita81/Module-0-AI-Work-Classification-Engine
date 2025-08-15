"""
cache-manager - 

This module provides .
"""

from .core import CacheManagerModule
from .interface import CacheManagerInterface
from .types import (
    CacheManagerConfig,
    
    CacheManagerInput,
    CacheManagerOutput,
    DomainEntity,
    BusinessRule,
    
    CacheManagerRequest,
    CacheManagerResponse,
    
    CacheManagerRequest,
    CacheManagerResponse,
    
    TechnicalRequest,
    TechnicalResponse,
    
    OperationResult,
    ModuleStatus
)

# Public API
__all__ = [
    "CacheManagerModule",
    "CacheManagerInterface",
    "CacheManagerConfig",
    
    "CacheManagerInput",
    "CacheManagerOutput",
    "DomainEntity",
    "BusinessRule",
    
    "CacheManagerRequest",
    "CacheManagerResponse",
    
    "CacheManagerRequest",
    "CacheManagerResponse",
    
    "TechnicalRequest",
    "TechnicalResponse",
    
    "OperationResult",
    "ModuleStatus"
]

# Version information
__version__ = "1.0.0"
__author__ = ""
