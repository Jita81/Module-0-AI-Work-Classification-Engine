"""
Type definitions for TestPaymentProcessor MCP Server

This module contains all type definitions, data classes, and schemas
used by the test-payment-processor MCP server for payments domain.
"""

from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


@dataclass
class TestPaymentProcessorConfig:
    """Configuration for TestPaymentProcessor MCP Server"""
    
    # AI_TODO: Define configuration parameters specific to payments
    # Examples:
    # - Database connection strings
    # - External service endpoints
    # - Authentication credentials
    # - Performance thresholds
    
    server_name: str = "test-payment-processor-mcp-server"
    domain: str = "payments"
    log_level: str = "INFO"
    max_concurrent_operations: int = 100
    
    # MCP-specific configuration
    mcp_transport: str = "stdio"  # stdio, http
    mcp_version: str = "2024-11-05"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "server_name": self.server_name,
            "domain": self.domain,
            "log_level": self.log_level,
            "max_concurrent_operations": self.max_concurrent_operations,
            "mcp_transport": self.mcp_transport,
            "mcp_version": self.mcp_version
        }


@dataclass
class TestPaymentProcessorResult:
    """Standard result format for all MCP operations"""
    
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: Optional[datetime] = field(default_factory=datetime.utcnow)
    operation_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for JSON serialization"""
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "operation_id": self.operation_id
        }


@dataclass
class HealthStatus:
    """Health check result format"""
    
    status: str  # healthy, degraded, unhealthy
    module_name: str
    domain: str
    timestamp: datetime
    details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "module_name": self.module_name,
            "domain": self.domain,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details
        }


# AI_TODO: Add domain-specific type definitions
# Examples for different domains:

# E-commerce domain types:
# @dataclass
# class User:
#     id: str
#     email: str
#     created_at: datetime

# Finance domain types:
# @dataclass
# class Transaction:
#     id: str
#     amount: float
#     currency: str
#     timestamp: datetime
