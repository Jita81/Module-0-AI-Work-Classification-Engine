"""
Type definitions for ClaudeApiGateway MCP Server

This module contains all type definitions, data classes, and schemas
used by the claude-api-gateway MCP server for ai-services domain.
"""

from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


@dataclass
class ClaudeApiGatewayConfig:
    """Configuration for ClaudeApiGateway MCP Server"""
    
    # Core server configuration
    server_name: str = "claude-api-gateway-mcp-server"
    domain: str = "ai-services"
    log_level: str = "INFO"
    max_concurrent_operations: int = 100
    
    # MCP-specific configuration
    mcp_transport: str = "stdio"  # stdio, http
    mcp_version: str = "2024-11-05"
    
    # Claude API configuration
    anthropic_api_url: str = "https://api.anthropic.com"
    claude_model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 4096
    temperature: float = 0.7
    
    # Security configuration
    encryption_key: Optional[str] = None
    database_url: str = "sqlite:///claude_api_gateway.db"
    session_timeout: int = 3600  # 1 hour
    
    # Rate limiting
    requests_per_minute: int = 60
    max_conversation_length: int = 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "server_name": self.server_name,
            "domain": self.domain,
            "log_level": self.log_level,
            "max_concurrent_operations": self.max_concurrent_operations,
            "mcp_transport": self.mcp_transport,
            "mcp_version": self.mcp_version,
            "anthropic_api_url": self.anthropic_api_url,
            "claude_model": self.claude_model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "database_url": self.database_url,
            "session_timeout": self.session_timeout,
            "requests_per_minute": self.requests_per_minute,
            "max_conversation_length": self.max_conversation_length
        }


@dataclass
class ClaudeApiGatewayResult:
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


# Claude API Gateway specific types

@dataclass
class User:
    """User registration data"""
    id: str
    username: str
    email: str
    api_key_hash: str
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "is_active": self.is_active
        }


@dataclass
class Conversation:
    """Conversation tracking data"""
    id: str
    user_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "message_count": self.message_count,
            "is_active": self.is_active
        }


@dataclass
class Message:
    """Individual message in conversation"""
    id: str
    conversation_id: str
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    token_count: Optional[int] = None
    model_used: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "token_count": self.token_count,
            "model_used": self.model_used
        }


@dataclass
class AuthCredentials:
    """Authentication credentials for API access"""
    user_id: str
    access_token: str
    expires_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "access_token": self.access_token,
            "expires_at": self.expires_at.isoformat()
        }


@dataclass
class ClaudeRequest:
    """Request to Claude API"""
    conversation_id: Optional[str] = None
    message: str = ""
    model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 4096
    temperature: float = 0.7
    system_prompt: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "conversation_id": self.conversation_id,
            "message": self.message,
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "system_prompt": self.system_prompt
        }


@dataclass
class ClaudeResponse:
    """Response from Claude API"""
    message_id: str
    conversation_id: str
    content: str
    model: str
    usage: Dict[str, int]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "conversation_id": self.conversation_id,
            "content": self.content,
            "model": self.model,
            "usage": self.usage,
            "timestamp": self.timestamp.isoformat()
        }
