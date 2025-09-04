"""
AI integration tests for PaymentGateway MCP Server

Tests that AI agents can discover, understand, and integrate
with this MCP server automatically.
"""

import pytest
import asyncio
import json

from ..core import PaymentGatewayMCPServer
from ..types import PaymentGatewayConfig


@pytest.mark.asyncio
async def test_ai_discoverability():
    """Test that AI agents can discover this module's capabilities"""
    
    config = PaymentGatewayConfig()
    server = PaymentGatewayMCPServer(config)
    await server.initialize()
    
    # Test capability discovery
    capabilities = await server.get_capabilities()
    
    # Verify AI can understand module purpose
    assert "module_info" in capabilities
    assert "description" in capabilities["module_info"]
    assert len(capabilities["module_info"]["description"]) > 0
    
    # Verify AI can find business operations
    assert "business_capabilities" in capabilities
    business_caps = capabilities["business_capabilities"]
    assert "primary_operations" in business_caps
    assert isinstance(business_caps["primary_operations"], list)


@pytest.mark.asyncio 
async def test_ai_integration_workflow():
    """Test complete AI integration workflow"""
    
    config = PaymentGatewayConfig()
    server = PaymentGatewayMCPServer(config)
    await server.initialize()
    
    # Step 1: AI discovers available tools
    tools = await server.server.call_handler("tools/list", {})
    assert len(tools) > 0
    
    # Step 2: AI gets module capabilities
    capabilities = await server.get_capabilities()
    assert "api_endpoints" in capabilities
    
    # Step 3: AI gets API schema
    schema = await server.get_api_schema()
    assert "paths" in schema
    
    # Step 4: AI can execute operations
    health_result = await server.server.call_handler("tools/call", {
        "name": f"payment-gateway_health_check",
        "arguments": {}
    })
    assert len(health_result) > 0


@pytest.mark.asyncio
async def test_schema_validation_for_ai():
    """Test that schemas are AI-friendly and complete"""
    
    config = PaymentGatewayConfig()
    server = PaymentGatewayMCPServer(config)
    await server.initialize()
    
    # Get API schema
    schema = await server.get_api_schema()
    
    # Verify schema completeness for AI understanding
    assert "openapi" in schema
    assert schema["openapi"] == "3.0.0"
    
    # Verify info section
    info = schema["info"]
    assert "title" in info
    assert "version" in info
    assert "description" in info
    
    # Verify paths are defined
    if "paths" in schema and schema["paths"]:
        for path, methods in schema["paths"].items():
            for method, spec in methods.items():
                # Each endpoint should have description for AI
                assert "summary" in spec or "description" in spec
                
                # Should have proper request/response schemas
                if "requestBody" in spec:
                    assert "content" in spec["requestBody"]
                
                if "responses" in spec:
                    assert "200" in spec["responses"]


@pytest.mark.asyncio
async def test_prompt_quality_for_ai():
    """Test that prompts provide quality AI guidance"""
    
    config = PaymentGatewayConfig()
    server = PaymentGatewayMCPServer(config)
    await server.initialize()
    
    # Get available prompts
    prompts = await server.server.call_handler("prompts/list", {})
    
    for prompt in prompts:
        # Test prompt retrieval
        prompt_result = await server.server.call_handler("prompts/get", {
            "name": prompt.name,
            "arguments": {}
        })
        
        # Verify prompt provides useful AI guidance
        assert hasattr(prompt_result, 'description')
        assert hasattr(prompt_result, 'messages')
        assert len(prompt_result.messages) > 0
        
        # Verify message content is substantial
        message_content = prompt_result.messages[0].content.text
        assert len(message_content) > 100  # Should be substantial guidance


# AI_TODO: Add domain-specific AI integration tests
# Examples:

# Test AI can understand business context:
# @pytest.mark.asyncio
# async def test_business_context_understanding():
#     """Test AI can understand business context from capabilities"""
#     pass

# Test AI can generate proper requests:
# @pytest.mark.asyncio  
# async def test_ai_request_generation():
#     """Test AI can generate valid requests based on schema"""
#     pass

# Test AI error recovery:
# @pytest.mark.asyncio
# async def test_ai_error_recovery():
#     """Test AI can understand and recover from errors"""
#     pass
