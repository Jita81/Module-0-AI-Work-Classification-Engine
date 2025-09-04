"""
NotificationHub MCP Server Package

This package provides a Model Context Protocol (MCP) server for communications domain operations.
The server is AI-discoverable and provides standardized API endpoints.
"""

from .core import NotificationHubMCPServer, create_notification_hub_mcp_server
from .interface import NotificationHubInterface
from .types import NotificationHubConfig, NotificationHubResult, HealthStatus

__version__ = "1.0.0"
__mcp_server__ = True

# MCP Server metadata for discovery
MCP_SERVER_INFO = {
    "name": "notification-hub",
    "version": __version__,
    "type": "SUPPORTING",
    "domain": "communications",
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
    "NotificationHubMCPServer",
    "NotificationHubInterface", 
    "NotificationHubConfig",
    "NotificationHubResult",
    "HealthStatus",
    "create_notification_hub_mcp_server",
    "MCP_SERVER_INFO"
]


def get_mcp_server_info() -> Dict[str, Any]:
    """Get MCP server information for discovery"""
    return MCP_SERVER_INFO


def create_mcp_server(config: NotificationHubConfig = None) -> NotificationHubMCPServer:
    """Factory function to create MCP server instance"""
    if config is None:
        config = NotificationHubConfig()
    return NotificationHubMCPServer(config)
