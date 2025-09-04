"""
ClaudeApiGateway MCP Server Package

This package provides a Model Context Protocol (MCP) server for ai-services domain operations.
The server is AI-discoverable and provides standardized API endpoints.
"""

from .core import ClaudeApiGatewayMCPServer, create_claude_api_gateway_mcp_server
from .interface import ClaudeApiGatewayInterface
from .types import ClaudeApiGatewayConfig, ClaudeApiGatewayResult, HealthStatus

__version__ = "1.0.0"
__mcp_server__ = True

# MCP Server metadata for discovery
MCP_SERVER_INFO = {
    "name": "claude-api-gateway",
    "version": __version__,
    "type": "INTEGRATION",
    "domain": "ai-services",
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
    "ClaudeApiGatewayMCPServer",
    "ClaudeApiGatewayInterface", 
    "ClaudeApiGatewayConfig",
    "ClaudeApiGatewayResult",
    "HealthStatus",
    "create_claude_api_gateway_mcp_server",
    "MCP_SERVER_INFO"
]


def get_mcp_server_info() -> Dict[str, Any]:
    """Get MCP server information for discovery"""
    return MCP_SERVER_INFO


def create_mcp_server(config: ClaudeApiGatewayConfig = None) -> ClaudeApiGatewayMCPServer:
    """Factory function to create MCP server instance"""
    if config is None:
        config = ClaudeApiGatewayConfig()
    return ClaudeApiGatewayMCPServer(config)
