"""
Core MCP server tests for NotificationHub

Tests the basic MCP server functionality, tool execution,
and business logic implementation.
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch

from ..core import NotificationHubMCPServer
from ..types import NotificationHubConfig, NotificationHubResult


@pytest.fixture
async def mcp_server():
    """Create MCP server instance for testing"""
    config = NotificationHubConfig()
    server = NotificationHubMCPServer(config)
    await server.initialize()
    yield server
    await server.cleanup()


@pytest.mark.asyncio
async def test_mcp_server_initialization(mcp_server):
    """Test MCP server initializes correctly"""
    assert mcp_server._initialized == True
    assert mcp_server.server.name == "notification-hub-mcp-server"


@pytest.mark.asyncio
async def test_health_check_tool(mcp_server):
    """Test health check MCP tool"""
    health = await mcp_server.health_check()
    
    assert isinstance(health, dict)
    assert "status" in health
    assert "module" in health
    assert "mcp_server" in health
    assert health["mcp_server"] == True


@pytest.mark.asyncio
async def test_capabilities_tool(mcp_server):
    """Test capabilities discovery MCP tool"""
    capabilities = await mcp_server.get_capabilities()
    
    assert isinstance(capabilities, dict)
    assert "module_info" in capabilities
    assert "api_endpoints" in capabilities
    assert "integration_patterns" in capabilities
    
    # Verify module info
    module_info = capabilities["module_info"]
    assert module_info["name"] == "notification-hub"
    assert module_info["type"] == "SUPPORTING"
    assert module_info["domain"] == "communications"


@pytest.mark.asyncio
async def test_api_schema_resource(mcp_server):
    """Test API schema resource"""
    schema = await mcp_server.get_api_schema()
    
    assert isinstance(schema, dict)
    assert "openapi" in schema
    assert "info" in schema
    assert "paths" in schema
    
    # Verify OpenAPI structure
    assert schema["openapi"] == "3.0.0"
    assert schema["info"]["title"] == f"NotificationHub MCP Server API"


@pytest.mark.asyncio 
async def test_mcp_tool_list():
    """Test that MCP tools are properly defined"""
    config = NotificationHubConfig()
    server = NotificationHubMCPServer(config)
    
    # Get tools via MCP list_tools handler
    tools = await server.server.call_handler("tools/list", {})
    
    assert isinstance(tools, list)
    assert len(tools) > 0
    
    # Verify each tool has required properties
    for tool in tools:
        assert hasattr(tool, 'name')
        assert hasattr(tool, 'description') 
        assert hasattr(tool, 'inputSchema')


@pytest.mark.asyncio
async def test_mcp_resource_list():
    """Test that MCP resources are properly defined"""
    config = NotificationHubConfig()
    server = NotificationHubMCPServer(config)
    
    resources = await server.server.call_handler("resources/list", {})
    
    assert isinstance(resources, list)
    assert len(resources) > 0
    
    # Verify each resource has required properties
    for resource in resources:
        assert hasattr(resource, 'uri')
        assert hasattr(resource, 'name')
        assert hasattr(resource, 'description')


# AI_TODO: Add domain-specific tests
# Examples for different module types:

# CORE module tests:
# - Test business rule enforcement
# - Test data validation
# - Test audit trail creation

# INTEGRATION module tests:
# - Test external service calls
# - Test circuit breaker functionality
# - Test retry policies

# SUPPORTING module tests:
# - Test workflow orchestration
# - Test step execution
# - Test state management

# TECHNICAL module tests:
# - Test resource management
# - Test performance monitoring
# - Test scaling operations
