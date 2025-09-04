"""
UserAuth MCP Server Package

This package provides a Model Context Protocol (MCP) server for authentication domain operations.
The server is AI-discoverable and provides standardized API endpoints.
"""

from .core import UserAuthMCPServer, create_user_auth_mcp_server
from .interface import UserAuthInterface
from .types import UserAuthConfig, UserAuthResult, HealthStatus

__version__ = "1.0.0"
__mcp_server__ = True

# MCP Server metadata for discovery
MCP_SERVER_INFO = {
    "name": "user-auth",
    "version": __version__,
    "type": "CORE",
    "domain": "authentication",
    "protocol_version": "2024-11-05",
    "transport": ["stdio", "http"],
    "capabilities": {
        "tools": True,
        "resources": True, 
        "prompts": True,
        "sampling": False
    }
}

# Export main classes and functions
__all__ = [
    "UserAuthMCPServer",
    "UserAuthInterface", 
    "UserAuthConfig",
    "UserAuthResult",
    "HealthStatus",
    "create_user_auth_mcp_server",
    "MCP_SERVER_INFO"
]


def get_mcp_server_info() -> Dict[str, Any]:
    """Get MCP server information for discovery"""
    return MCP_SERVER_INFO


def create_mcp_server(config: UserAuthConfig = None) -> UserAuthMCPServer:
    """Factory function to create MCP server instance"""
    if config is None:
        config = UserAuthConfig()
    return UserAuthMCPServer(config)
