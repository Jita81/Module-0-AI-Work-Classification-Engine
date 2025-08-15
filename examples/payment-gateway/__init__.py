"""
payment-gateway - 

This module provides .
"""

from .core import PaymentGatewayModule
from .interface import PaymentGatewayInterface
from .types import (
    PaymentGatewayConfig,
    
    PaymentGatewayInput,
    PaymentGatewayOutput,
    DomainEntity,
    BusinessRule,
    
    PaymentGatewayRequest,
    PaymentGatewayResponse,
    
    PaymentGatewayRequest,
    PaymentGatewayResponse,
    
    TechnicalRequest,
    TechnicalResponse,
    
    OperationResult,
    ModuleStatus
)

# Public API
__all__ = [
    "PaymentGatewayModule",
    "PaymentGatewayInterface",
    "PaymentGatewayConfig",
    
    "PaymentGatewayInput",
    "PaymentGatewayOutput",
    "DomainEntity",
    "BusinessRule",
    
    "PaymentGatewayRequest",
    "PaymentGatewayResponse",
    
    "PaymentGatewayRequest",
    "PaymentGatewayResponse",
    
    "TechnicalRequest",
    "TechnicalResponse",
    
    "OperationResult",
    "ModuleStatus"
]

# Version information
__version__ = "1.0.0"
__author__ = ""
