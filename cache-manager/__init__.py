"""
CacheManager MCP Server Package

This package provides a Model Context Protocol (MCP) server for infrastructure domain operations.
The server is AI-discoverable and provides standardized API endpoints.
"""

from .core import CacheManagerMCPServer, create_cache_manager_mcp_server
from .interface import CacheManagerInterface
from .types import CacheManagerConfig, CacheManagerResult, HealthStatus

__version__ = "1.0.0"
__mcp_server__ = True

# MCP Server metadata for discovery
MCP_SERVER_INFO = {
    "name": "cache-manager",
    "version": __version__,
    "type": "TECHNICAL",
    "domain": "infrastructure",
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
    "CacheManagerMCPServer",
    "CacheManagerInterface", 
    "CacheManagerConfig",
    "CacheManagerResult",
    "HealthStatus",
    "create_cache_manager_mcp_server",
    "MCP_SERVER_INFO"
]


def get_mcp_server_info() -> Dict[str, Any]:
    """Get MCP server information for discovery"""
    return MCP_SERVER_INFO


def create_mcp_server(config: CacheManagerConfig = None) -> CacheManagerMCPServer:
    """Factory function to create MCP server instance"""
    if config is None:
        config = CacheManagerConfig()
    return CacheManagerMCPServer(config)
