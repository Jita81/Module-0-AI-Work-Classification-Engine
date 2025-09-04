"""
MCP Server Generator for Standardized Modules Framework

This module extends the existing ModuleGenerator to create MCP (Model Context Protocol)
servers instead of traditional modules, enabling AI-discoverable, API-first services.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any

from ..models.generation_result import GenerationResult
from .mcp_templates import MCPServerTemplates


class MCPServerGenerator:
    """Generates MCP servers with AI completion markers and discovery capabilities"""
    
    def __init__(self):
        self.templates = MCPServerTemplates()
    
    def generate_mcp_server(self, name: str, module_type: str, domain: str, 
                           output_dir: str, ai_ready: bool = True, 
                           with_docker: bool = False, deployment_target: str = "kubernetes") -> GenerationResult:
        """Generate complete MCP server structure with discovery endpoints"""
        
        module_path = Path(output_dir) / name
        
        try:
            # Create directory structure for MCP server
            self._create_mcp_directory_structure(module_path, with_docker)
            
            # Generate MCP server files
            template_context = {
                'module_name': name,
                'module_type': module_type,
                'domain': domain,
                'class_name': self._to_class_name(name),
                'ai_ready': ai_ready,
                'with_docker': with_docker,
                'deployment_target': deployment_target
            }
            
            # Generate core MCP server file
            mcp_server_content = self.templates.generate_mcp_server(module_type, template_context)
            self._write_file(module_path / 'core.py', mcp_server_content)
            
            # Generate MCP interface file
            interface_content = self.templates.generate_mcp_interface(template_context)
            self._write_file(module_path / 'interface.py', interface_content)
            
            # Generate MCP types file
            types_content = self.templates.generate_mcp_types(template_context)
            self._write_file(module_path / 'types.py', types_content)
            
            # Generate MCP server runner
            runner_content = self.templates.generate_mcp_server_runner(template_context)
            self._write_file(module_path / f'{name}_server.py', runner_content)
            
            # Generate package init file
            init_content = self._generate_mcp_init_file(template_context)
            self._write_file(module_path / '__init__.py', init_content)
            
            # Generate MCP server configuration
            config_content = self._generate_mcp_config_file(template_context)
            self._write_file(module_path / 'mcp_config.json', config_content)
            
            # Generate AI completion guide for MCP
            ai_completion_content = self.templates.generate_mcp_ai_completion_guide(template_context)
            ai_completion_file = module_path / 'AI_COMPLETION.md'
            self._write_file(ai_completion_file, ai_completion_content)
            
            # Generate MCP-specific tests
            self._generate_mcp_tests(module_path, template_context)
            
            # Generate documentation
            self._generate_mcp_documentation(module_path, template_context)
            
            # Generate Docker and Kubernetes files if requested
            if with_docker:
                self._generate_mcp_containerization(module_path, template_context)
            
            return GenerationResult(
                success=True,
                module_path=str(module_path),
                ai_completion_file=str(ai_completion_file),
                containerized=with_docker,
                deployment_target=deployment_target if with_docker else None
            )
            
        except Exception as e:
            return GenerationResult(
                success=False,
                error=str(e)
            )
    
    def _create_mcp_directory_structure(self, module_path: Path, with_docker: bool):
        """Create directory structure for MCP server"""
        
        # Core directories
        module_path.mkdir(parents=True, exist_ok=True)
        (module_path / 'tests').mkdir(exist_ok=True)
        (module_path / 'docs').mkdir(exist_ok=True)
        (module_path / 'examples').mkdir(exist_ok=True)
        (module_path / 'config').mkdir(exist_ok=True)
        (module_path / 'logs').mkdir(exist_ok=True)
        
        # MCP-specific directories
        (module_path / 'schemas').mkdir(exist_ok=True)
        (module_path / 'tools').mkdir(exist_ok=True)
        (module_path / 'resources').mkdir(exist_ok=True)
        (module_path / 'prompts').mkdir(exist_ok=True)
        
        if with_docker:
            (module_path / 'k8s').mkdir(exist_ok=True)
            (module_path / 'terraform').mkdir(exist_ok=True)
            (module_path / 'scripts').mkdir(exist_ok=True)
            (module_path / '.github' / 'workflows').mkdir(parents=True, exist_ok=True)
    
    def _generate_mcp_init_file(self, context: Dict[str, Any]) -> str:
        """Generate __init__.py for MCP server package"""
        
        class_name = context['class_name']
        module_name = context['module_name']
        
        return f'''"""
{class_name} MCP Server Package

This package provides a Model Context Protocol (MCP) server for {context['domain']} domain operations.
The server is AI-discoverable and provides standardized API endpoints.
"""

from .core import {class_name}MCPServer, create_{module_name.replace('-', '_')}_mcp_server
from .interface import {class_name}Interface
from .types import {class_name}Config, {class_name}Result, HealthStatus

__version__ = "1.0.0"
__mcp_server__ = True

# MCP Server metadata for discovery
MCP_SERVER_INFO = {{
    "name": "{module_name}",
    "version": __version__,
    "type": "{context['module_type']}",
    "domain": "{context['domain']}",
    "protocol_version": "2024-11-05",
    "transport": ["stdio", "http"],
    "capabilities": {{
        "tools": True,
        "resources": True, 
        "prompts": True,
        "sampling": False
    }}
}}

# Export main classes and functions
__all__ = [
    "{class_name}MCPServer",
    "{class_name}Interface", 
    "{class_name}Config",
    "{class_name}Result",
    "HealthStatus",
    "create_{module_name.replace('-', '_')}_mcp_server",
    "MCP_SERVER_INFO"
]


def get_mcp_server_info() -> Dict[str, Any]:
    """Get MCP server information for discovery"""
    return MCP_SERVER_INFO


def create_mcp_server(config: {class_name}Config = None) -> {class_name}MCPServer:
    """Factory function to create MCP server instance"""
    if config is None:
        config = {class_name}Config()
    return {class_name}MCPServer(config)
'''
    
    def _generate_mcp_config_file(self, context: Dict[str, Any]) -> str:
        """Generate MCP server configuration file"""
        
        config = {
            "mcp_server": {
                "name": context['module_name'],
                "version": "1.0.0",
                "type": context['module_type'],
                "domain": context['domain'],
                "protocol_version": "2024-11-05"
            },
            "transport": {
                "type": "stdio",
                "options": {
                    "buffer_size": 8192,
                    "timeout": 30
                }
            },
            "capabilities": {
                "tools": {
                    "enabled": True,
                    "max_concurrent": 10
                },
                "resources": {
                    "enabled": True,
                    "cache_ttl": 300
                },
                "prompts": {
                    "enabled": True,
                    "template_cache": True
                }
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": f"{context['module_name']}_mcp.log"
            },
            "performance": {
                "max_request_size": "10MB",
                "request_timeout": 30,
                "rate_limit": {
                    "enabled": True,
                    "requests_per_minute": 100
                }
            },
            "ai_integration": {
                "auto_discovery": True,
                "schema_validation": True,
                "completion_hints": True
            }
        }
        
        return json.dumps(config, indent=2)
    
    def _generate_mcp_ai_completion_guide(self, context: Dict[str, Any]) -> str:
        """Generate AI completion guide for MCP server development"""
        
        module_name = context['module_name']
        class_name = context['class_name']
        domain = context['domain']
        module_type = context['module_type']
        
        return f'''# AI Completion Guide: {module_name} MCP Server ({module_type})

## 🎯 Your Mission
Transform this {module_type} module into a fully functional MCP (Model Context Protocol) server for the {domain} domain. This server will be **AI-discoverable** and provide **standardized API endpoints** for seamless integration.

## 🚀 MCP Server Benefits
- **AI-Discoverable**: Other AI agents can automatically find and integrate this module
- **Self-Describing**: Exposes its own API schema and capabilities
- **Standardized**: Uses JSON-RPC 2.0 protocol for consistent communication
- **Production-Ready**: Built-in error handling, logging, and monitoring

## 📋 Implementation Checklist

### 🔧 Core Implementation (HIGH PRIORITY)

#### 1. Business Logic Implementation
**File: `core.py`**

```python
async def _process_business_logic(self, data: Dict[str, Any]) -> Dict[str, Any]:
    # AI_TODO: Implement {domain}-specific business logic
    # This is the core value-add of your module
    
    # Example patterns for {module_type} modules:
    {"# - Data validation and transformation" if module_type == "CORE" else ""}
    {"# - External service integration with retry logic" if module_type == "INTEGRATION" else ""}
    {"# - Workflow orchestration and step management" if module_type == "SUPPORTING" else ""}
    {"# - Resource pool management and scaling" if module_type == "TECHNICAL" else ""}
    
    pass
```

#### 2. Input Validation
```python
def _validate_input(self, data: Dict[str, Any]) -> bool:
    # AI_TODO: Implement {domain}-specific validation
    # - Required field checking
    # - Business rule validation
    # - Data type verification
    # - Authorization checks
    
    pass
```

#### 3. Configuration Setup
**File: `types.py`**

```python
@dataclass
class {class_name}Config:
    # AI_TODO: Define configuration specific to {domain}
    # Examples:
    # - database_url: str
    # - api_key: str  
    # - rate_limit: int
    # - external_service_endpoints: Dict[str, str]
    
    pass
```

### 🔌 MCP Integration (MEDIUM PRIORITY)

#### 4. Enhance Tool Definitions
**File: `core.py` - Update `list_tools()`**

Add domain-specific tools that AI agents can discover and use:

```python
Tool(
    name=f"{{module_name}}_your_custom_operation",
    description="Describe what this operation does in business terms",
    inputSchema={{
        # AI_TODO: Define input schema for your operation
        "type": "object",
        "properties": {{
            "field_name": {{"type": "string", "description": "Field description"}}
        }},
        "required": ["field_name"]
    }}
)
```

#### 5. Define Resources for AI Access
**File: `core.py` - Update `list_resources()`**

Expose data that AI agents might need:

```python
Resource(
    uri=f"mcp://{module_name}/your-resource",
    name=f"{module_name} Your Resource",
    description="Describe what data this resource provides",
    mimeType="application/json"
)
```

#### 6. Create AI-Helpful Prompts
**File: `core.py` - Update `list_prompts()`**

Provide templates that help AI agents use your module effectively:

```python
Prompt(
    name=f"{module_name}_usage_guide",
    description="Guide for using this module effectively",
    arguments=[
        {{
            "name": "use_case",
            "description": "Specific use case for guidance",
            "required": False
        }}
    ]
)
```

### 📊 Discovery & Documentation (HIGH PRIORITY)

#### 7. Update Capabilities Response
**File: `core.py` - `get_capabilities()` method**

```python
async def get_capabilities(self) -> Dict[str, Any]:
    return {{
        "module_info": {{
            "name": "{module_name}",
            "type": "{module_type}",
            "domain": "{domain}",
            "version": "1.0.0",
            "description": "Your module description here"
        }},
        "business_capabilities": {{
            # AI_TODO: Define what business operations this module provides
            "primary_operations": ["operation1", "operation2"],
            "data_entities": ["Entity1", "Entity2"],
            "business_rules": ["rule1", "rule2"],
            "integration_points": ["external_service1", "external_service2"]
        }},
        "api_endpoints": {{
            # This will be auto-generated from your MCP tools
        }},
        "integration_patterns": {{
            "api_style": "MCP JSON-RPC 2.0",
            "transport": ["stdio", "http"],
            "authentication": "configurable",
            "rate_limiting": "built-in"
        }}
    }}
```

#### 8. API Schema Definition
**File: `core.py` - `get_api_schema()` method**

Define complete OpenAPI schema so AI agents understand your endpoints:

```python
async def get_api_schema(self) -> Dict[str, Any]:
    return {{
        "openapi": "3.0.0",
        "info": {{
            "title": f"{class_name} MCP Server API",
            "version": "1.0.0",
            "description": "Your API description here"
        }},
        "paths": {{
            # AI_TODO: Define your API endpoints here
            # Each MCP tool becomes a path in the schema
        }}
    }}
```

## 🧪 Testing Your MCP Server

### Quick Test
```bash
# Test MCP server locally
python3 {module_name}_server.py

# Test with MCP client
echo '{{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {{}}}}' | python3 {module_name}_server.py
```

### Integration Test
```python
# Test AI integration
from mcp import ClientSession
from mcp.client.stdio import stdio_client

async with stdio_client(["python", "{module_name}_server.py"]) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        
        # Test tool discovery
        tools = await session.list_tools()
        print(f"Available tools: {{[t.name for t in tools]}}")
        
        # Test capability discovery
        capabilities = await session.call_tool("{module_name}_get_capabilities", {{}})
        print(f"Module capabilities: {{capabilities}}")
```

## 🔄 Integration Patterns

### AI Agent Discovery Flow
1. **Connect**: AI agent connects to your MCP server
2. **Discover**: Agent calls `list_tools()`, `list_resources()`, `list_prompts()`
3. **Understand**: Agent calls `get_capabilities()` and `get_api_schema()`
4. **Integrate**: Agent can now use your module's functionality automatically

### Module-to-Module Communication
```python
# MCP servers can communicate with each other
from mcp.client.stdio import stdio_client

async def integrate_with_other_module():
    async with stdio_client(["python", "other-module_server.py"]) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("other_module_operation", {{"data": "value"}})
            return result
```

## 📈 Success Metrics

Your MCP server implementation is complete when:

- ✅ All MCP tools execute without errors
- ✅ Resources return valid JSON data
- ✅ Prompts provide helpful guidance
- ✅ `get_capabilities()` accurately describes functionality
- ✅ `get_api_schema()` provides complete OpenAPI spec
- ✅ AI agents can discover and use the module automatically
- ✅ Health checks pass consistently
- ✅ Error handling is comprehensive

## 🤖 AI Integration Tips

1. **Be Descriptive**: Use clear, business-focused descriptions in tool definitions
2. **Provide Examples**: Include example inputs/outputs in your documentation
3. **Schema Validation**: Ensure your input schemas are comprehensive
4. **Error Messages**: Make error messages helpful for AI debugging
5. **Resource Exposure**: Expose configuration and metrics for AI monitoring

## 🎯 Next Steps After Completion

1. **Test Locally**: Run the MCP server and verify all endpoints work
2. **AI Integration**: Test with an AI agent to ensure discoverability
3. **Documentation**: Update the README with usage examples
4. **Deployment**: Use Docker/Kubernetes files if generated with `--with-docker`
5. **Monitoring**: Set up logging and metrics collection

---

**🚀 You're building the future of AI-module integration! Each MCP server you create becomes part of an AI-discoverable ecosystem.**
'''
    
    def _generate_mcp_tests(self, module_path: Path, context: Dict[str, Any]):
        """Generate MCP-specific test files"""
        
        # Test core MCP functionality
        test_core_content = self._generate_mcp_core_tests(context)
        self._write_file(module_path / 'tests' / 'test_mcp_core.py', test_core_content)
        
        # Test MCP protocol compliance
        test_protocol_content = self._generate_mcp_protocol_tests(context)
        self._write_file(module_path / 'tests' / 'test_mcp_protocol.py', test_protocol_content)
        
        # Test AI integration
        test_ai_content = self._generate_mcp_ai_integration_tests(context)
        self._write_file(module_path / 'tests' / 'test_ai_integration.py', test_ai_content)
        
        # Pytest configuration
        pytest_content = self._generate_mcp_pytest_config(context)
        self._write_file(module_path / 'pytest.ini', pytest_content)
    
    def _generate_mcp_core_tests(self, context: Dict[str, Any]) -> str:
        """Generate core MCP server tests"""
        
        class_name = context['class_name']
        module_name = context['module_name']
        
        return f'''"""
Core MCP server tests for {class_name}

Tests the basic MCP server functionality, tool execution,
and business logic implementation.
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch

from ..core import {class_name}MCPServer
from ..types import {class_name}Config, {class_name}Result


@pytest.fixture
async def mcp_server():
    """Create MCP server instance for testing"""
    config = {class_name}Config()
    server = {class_name}MCPServer(config)
    await server.initialize()
    yield server
    await server.cleanup()


@pytest.mark.asyncio
async def test_mcp_server_initialization(mcp_server):
    """Test MCP server initializes correctly"""
    assert mcp_server._initialized == True
    assert mcp_server.server.name == "{module_name}-mcp-server"


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
    assert module_info["name"] == "{module_name}"
    assert module_info["type"] == "{context['module_type']}"
    assert module_info["domain"] == "{context['domain']}"


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
    assert schema["info"]["title"] == f"{class_name} MCP Server API"


@pytest.mark.asyncio 
async def test_mcp_tool_list():
    """Test that MCP tools are properly defined"""
    config = {class_name}Config()
    server = {class_name}MCPServer(config)
    
    # Get tools via MCP list_tools handler
    tools = await server.server.call_handler("tools/list", {{}})
    
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
    config = {class_name}Config()
    server = {class_name}MCPServer(config)
    
    resources = await server.server.call_handler("resources/list", {{}})
    
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
'''
    
    def _generate_mcp_protocol_tests(self, context: Dict[str, Any]) -> str:
        """Generate MCP protocol compliance tests"""
        
        class_name = context['class_name']
        module_name = context['module_name']
        
        return f'''"""
MCP Protocol compliance tests for {class_name}

Tests that the MCP server properly implements the Model Context Protocol
specification and can communicate with MCP clients.
"""

import pytest
import asyncio
import json
from mcp import types
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

from ..core import {class_name}MCPServer
from ..types import {class_name}Config


@pytest.mark.asyncio
async def test_mcp_initialization():
    """Test MCP server initialization handshake"""
    
    # AI_TODO: Implement full MCP initialization test
    # - Test protocol version negotiation
    # - Test capability exchange
    # - Test client/server handshake
    
    config = {class_name}Config()
    server = {class_name}MCPServer(config)
    
    # Test server info
    server_info = {{
        "name": server.server.name,
        "version": "1.0.0"
    }}
    
    assert server_info["name"] == "{module_name}-mcp-server"


@pytest.mark.asyncio
async def test_json_rpc_compliance():
    """Test JSON-RPC 2.0 compliance"""
    
    # AI_TODO: Implement JSON-RPC 2.0 compliance tests
    # - Test request/response format
    # - Test error handling format
    # - Test batch request support
    # - Test notification handling
    
    # Example test structure
    request = {{
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {{}}
    }}
    
    # Verify request format is valid JSON-RPC 2.0
    assert request["jsonrpc"] == "2.0"
    assert "id" in request
    assert "method" in request


@pytest.mark.asyncio
async def test_tool_execution_protocol():
    """Test tool execution follows MCP protocol"""
    
    config = {class_name}Config()
    server = {class_name}MCPServer(config)
    await server.initialize()
    
    # Test tool execution returns proper MCP response
    tools = await server.server.call_handler("tools/list", {{}})
    assert isinstance(tools, list)
    
    if tools:
        # Test executing first tool
        tool_name = tools[0].name
        result = await server.server.call_handler("tools/call", {{
            "name": tool_name,
            "arguments": {{}}
        }})
        
        # Verify result is proper MCP format
        assert isinstance(result, list)
        assert all(hasattr(item, 'type') for item in result)


@pytest.mark.asyncio
async def test_resource_access_protocol():
    """Test resource access follows MCP protocol"""
    
    config = {class_name}Config()
    server = {class_name}MCPServer(config)
    await server.initialize()
    
    # Test resource listing
    resources = await server.server.call_handler("resources/list", {{}})
    assert isinstance(resources, list)
    
    if resources:
        # Test reading first resource
        resource_uri = resources[0].uri
        content = await server.server.call_handler("resources/read", {{
            "uri": resource_uri
        }})
        
        # Verify content is valid
        assert isinstance(content, str)
        # Should be valid JSON for application/json resources
        if resources[0].mimeType == "application/json":
            json.loads(content)  # Should not raise exception


@pytest.mark.asyncio
async def test_error_handling_protocol():
    """Test error handling follows MCP protocol"""
    
    config = {class_name}Config()
    server = {class_name}MCPServer(config)
    await server.initialize()
    
    # Test invalid tool call
    with pytest.raises(ValueError):
        await server.server.call_handler("tools/call", {{
            "name": "nonexistent_tool",
            "arguments": {{}}
        }})
    
    # Test invalid resource access
    with pytest.raises(ValueError):
        await server.server.call_handler("resources/read", {{
            "uri": "mcp://invalid/resource"
        }})


# AI_TODO: Add more protocol compliance tests
# - Test prompt handling protocol
# - Test streaming response protocol (if supported)
# - Test authentication protocol (if implemented)
# - Test rate limiting behavior
'''
    
    def _generate_mcp_ai_integration_tests(self, context: Dict[str, Any]) -> str:
        """Generate AI integration tests"""
        
        class_name = context['class_name']
        module_name = context['module_name']
        
        return f'''"""
AI integration tests for {class_name} MCP Server

Tests that AI agents can discover, understand, and integrate
with this MCP server automatically.
"""

import pytest
import asyncio
import json

from ..core import {class_name}MCPServer
from ..types import {class_name}Config


@pytest.mark.asyncio
async def test_ai_discoverability():
    """Test that AI agents can discover this module's capabilities"""
    
    config = {class_name}Config()
    server = {class_name}MCPServer(config)
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
    
    config = {class_name}Config()
    server = {class_name}MCPServer(config)
    await server.initialize()
    
    # Step 1: AI discovers available tools
    tools = await server.server.call_handler("tools/list", {{}})
    assert len(tools) > 0
    
    # Step 2: AI gets module capabilities
    capabilities = await server.get_capabilities()
    assert "api_endpoints" in capabilities
    
    # Step 3: AI gets API schema
    schema = await server.get_api_schema()
    assert "paths" in schema
    
    # Step 4: AI can execute operations
    health_result = await server.server.call_handler("tools/call", {{
        "name": f"{module_name}_health_check",
        "arguments": {{}}
    }})
    assert len(health_result) > 0


@pytest.mark.asyncio
async def test_schema_validation_for_ai():
    """Test that schemas are AI-friendly and complete"""
    
    config = {class_name}Config()
    server = {class_name}MCPServer(config)
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
    
    config = {class_name}Config()
    server = {class_name}MCPServer(config)
    await server.initialize()
    
    # Get available prompts
    prompts = await server.server.call_handler("prompts/list", {{}})
    
    for prompt in prompts:
        # Test prompt retrieval
        prompt_result = await server.server.call_handler("prompts/get", {{
            "name": prompt.name,
            "arguments": {{}}
        }})
        
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
'''
    
    def _generate_mcp_documentation(self, module_path: Path, context: Dict[str, Any]):
        """Generate MCP server documentation"""
        
        readme_content = self._generate_mcp_readme(context)
        self._write_file(module_path / 'docs' / 'README.md', readme_content)
        
        api_docs_content = self._generate_mcp_api_docs(context)
        self._write_file(module_path / 'docs' / 'API.md', api_docs_content)
        
        integration_guide_content = self._generate_mcp_integration_guide(context)
        self._write_file(module_path / 'docs' / 'INTEGRATION.md', integration_guide_content)
    
    def _generate_mcp_readme(self, context: Dict[str, Any]) -> str:
        """Generate README for MCP server"""
        
        module_name = context['module_name']
        class_name = context['class_name']
        domain = context['domain']
        module_type = context['module_type']
        
        return f'''# {class_name} MCP Server

**Type**: {module_type} | **Domain**: {domain} | **Protocol**: MCP 2024-11-05

AI-discoverable MCP server providing standardized API endpoints for {domain} domain operations.

## 🚀 Quick Start

### Running the MCP Server

```bash
# Direct execution
python3 {module_name}_server.py

# With configuration
python3 {module_name}_server.py --config config/production.json
```

### AI Integration

```python
from mcp import ClientSession
from mcp.client.stdio import stdio_client

# Connect to MCP server
async with stdio_client(["python", "{module_name}_server.py"]) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        
        # Discover capabilities
        tools = await session.list_tools()
        capabilities = await session.call_tool("{module_name}_get_capabilities", {{}})
        
        # Execute operations
        result = await session.call_tool("{module_name}_execute_operation", {{
            "data": {{"key": "value"}}
        }})
```

## 🔧 MCP Tools

| Tool Name | Description | Input Schema |
|-----------|-------------|--------------|
| `{module_name}_health_check` | Check server health | No parameters |
| `{module_name}_get_capabilities` | Get module capabilities | No parameters |

## 📊 MCP Resources

| Resource URI | Description | Content Type |
|--------------|-------------|--------------|
| `mcp://{module_name}/schema` | Complete API schema | application/json |
| `mcp://{module_name}/config` | Current configuration | application/json |

## 💬 MCP Prompts

| Prompt Name | Description | Arguments |
|-------------|-------------|-----------|
| `{module_name}_completion_guide` | AI implementation guidance | business_context (optional) |
| `{module_name}_integration_guide` | Integration instructions | integration_type (required) |

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run MCP-specific tests
pytest tests/test_mcp_*.py -v
```

---

Built with the Standardized Modules Framework v1.1.0 - MCP Edition
'''
    
    def _generate_mcp_api_docs(self, context: Dict[str, Any]) -> str:
        """Generate API documentation for MCP server"""
        
        module_name = context['module_name']
        class_name = context['class_name']
        domain = context['domain']
        
        return f'''# {class_name} MCP Server API Documentation

## Overview

This document describes the API endpoints provided by the {class_name} MCP Server for {domain} domain operations.

## MCP Protocol

This server implements the Model Context Protocol (MCP) 2024-11-05 specification using JSON-RPC 2.0.

### Transport

- **Primary**: stdio (standard input/output)
- **Alternative**: HTTP (when configured)

### Authentication

- **Type**: Configurable (API key, OAuth, custom)
- **Default**: None (suitable for trusted environments)

## API Endpoints

### Tools (Executable Functions)

#### {module_name}_execute_primary_operation

Execute the primary business operation for {domain} domain.

**Input Schema:**
```json
{{
  "type": "object",
  "properties": {{
    "data": {{
      "type": "object",
      "description": "Input data for business operation"
    }},
    "options": {{
      "type": "object",
      "description": "Optional processing parameters"
    }}
  }},
  "required": ["data"]
}}
```

**Output:**
```json
{{
  "success": true,
  "data": {{}},
  "timestamp": "2024-01-01T00:00:00Z",
  "operation_id": "uuid"
}}
```

#### {module_name}_health_check

Check the health status of the MCP server.

**Input Schema:**
```json
{{
  "type": "object",
  "properties": {{}},
  "additionalProperties": false
}}
```

**Output:**
```json
{{
  "status": "healthy",
  "module": "{class_name}",
  "domain": "{domain}",
  "mcp_server": true,
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00Z",
  "capabilities": {{
    "tools": 3,
    "resources": 3,
    "prompts": 2
  }}
}}
```

### Resources (Data Sources)

#### mcp://{module_name}/schema

Complete OpenAPI 3.0 schema for all endpoints.

**Content-Type:** application/json

#### mcp://{module_name}/config

Current module configuration and settings.

**Content-Type:** application/json

#### mcp://{module_name}/metrics

Performance and usage metrics.

**Content-Type:** application/json

### Prompts (Templates)

#### {module_name}_completion_guide

AI completion guide for implementing {domain} business logic.

**Arguments:**
- `business_context` (optional): Specific business context for implementation

#### {module_name}_integration_guide

Guide for integrating with {domain} module.

**Arguments:**
- `integration_type` (required): Type of integration (api, event, data)

## Error Handling

All endpoints return standardized error responses:

```json
{{
  "success": false,
  "error": "Error description",
  "timestamp": "2024-01-01T00:00:00Z",
  "operation_id": "uuid"
}}
```

## Rate Limiting

- **Default**: 100 requests per minute
- **Configurable**: Yes, via configuration
- **Headers**: Standard rate limit headers included

## Examples

### Basic Usage

```bash
# List available tools
echo '{{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {{}}}}' | python3 {module_name}_server.py

# Execute primary operation
echo '{{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {{"name": "{module_name}_execute_primary_operation", "arguments": {{"data": {{"test": "value"}}}}}}}}' | python3 {module_name}_server.py
```

### Python Client

```python
import asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client

async def main():
    async with stdio_client(["python", "{module_name}_server.py"]) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Get capabilities
            result = await session.call_tool("{module_name}_get_capabilities", {{}})
            print("Capabilities:", result)
            
            # Execute operation
            result = await session.call_tool("{module_name}_execute_primary_operation", {{
                "data": {{"test": "value"}}
            }})
            print("Result:", result)

if __name__ == "__main__":
    asyncio.run(main())
```
'''
    
    def _generate_mcp_integration_guide(self, context: Dict[str, Any]) -> str:
        """Generate integration guide for MCP server"""
        
        module_name = context['module_name']
        class_name = context['class_name']
        domain = context['domain']
        
        return f'''# Integration Guide: {class_name} MCP Server

## Overview

This guide explains how to integrate with the {class_name} MCP Server for {domain} domain operations.

## Integration Patterns

### 1. Direct MCP Client Integration

```python
from mcp import ClientSession
from mcp.client.stdio import stdio_client

async def integrate_with_{module_name.replace('-', '_')}():
    async with stdio_client(["python", "{module_name}_server.py"]) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Discover capabilities
            capabilities = await session.call_tool("{module_name}_get_capabilities", {{}})
            
            # Use the module
            result = await session.call_tool("{module_name}_execute_primary_operation", {{
                "data": {{"your": "data"}}
            }})
            
            return result
```

### 2. AI Agent Integration

AI agents can automatically discover and integrate this module:

```python
# AI Discovery Flow
1. Connect to MCP server
2. Call list_tools() to discover available operations
3. Call get_capabilities() to understand business context
4. Call tools based on discovered capabilities
5. Use resources for additional context
6. Use prompts for guidance on complex operations
```

### 3. Service Mesh Integration

For microservices environments:

```yaml
# Kubernetes Service
apiVersion: v1
kind: Service
metadata:
  name: {module_name}-mcp-service
  annotations:
    mcp.protocol/version: "2024-11-05"
    mcp.discovery/enabled: "true"
spec:
  selector:
    app: {module_name}-mcp-server
  ports:
  - port: 8000
    targetPort: 8000
```

## Discovery Mechanisms

### Automatic Discovery

The MCP server exposes discovery endpoints:

```bash
# Get server info
curl -X POST http://localhost:8000/mcp \\
  -H "Content-Type: application/json" \\
  -d '{{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {{}}}}'

# List capabilities
curl -X POST http://localhost:8000/mcp \\
  -H "Content-Type: application/json" \\
  -d '{{"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {{}}}}'
```

### Service Registry Integration

```python
# Register with service discovery
import consul

def register_mcp_server():
    consul_client = consul.Consul()
    consul_client.agent.service.register(
        name="{module_name}-mcp-server",
        service_id="{module_name}-instance-1",
        port=8000,
        tags=["mcp", "ai-discoverable", "{domain}"],
        meta={{
            "protocol": "mcp-2024-11-05",
            "domain": "{domain}",
            "type": "core-business-logic"
        }},
        check=consul.Check.http("http://localhost:8000/health", interval="10s")
    )
```

## Error Handling

### Standard Error Response

```json
{{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {{
    "code": -32000,
    "message": "Business validation failed",
    "data": {{
      "operation": "execute_primary_operation",
      "module": "{class_name}",
      "timestamp": "2024-01-01T00:00:00Z",
      "details": {{}}
    }}
  }}
}}
```

### Error Codes

- `-32000`: Application error (business logic failure)
- `-32001`: Authentication error
- `-32002`: Authorization error
- `-32003`: Rate limit exceeded
- `-32004`: Resource unavailable

## Performance Considerations

### Optimization Tips

1. **Connection Pooling**: Reuse MCP client connections
2. **Batch Operations**: Group multiple tool calls when possible
3. **Resource Caching**: Cache resource responses when appropriate
4. **Async Operations**: Use async/await for non-blocking operations

### Monitoring

```python
# Get performance metrics
metrics = await session.read_resource("mcp://{module_name}/metrics")
print("Performance:", json.loads(metrics))
```

## Security

### Best Practices

1. **Input Validation**: Always validate input data
2. **Rate Limiting**: Configure appropriate rate limits
3. **Authentication**: Use proper authentication in production
4. **Logging**: Log all operations for audit trails
5. **Error Handling**: Don't expose sensitive information in errors

### Production Configuration

```json
{{
  "security": {{
    "authentication": {{
      "type": "api_key",
      "header": "X-API-Key"
    }},
    "rate_limiting": {{
      "requests_per_minute": 100,
      "burst_size": 10
    }},
    "cors": {{
      "enabled": true,
      "allowed_origins": ["https://yourdomain.com"]
    }}
  }}
}}
```

## Troubleshooting

### Common Issues

1. **Connection Refused**: Check if server is running on correct port
2. **Tool Not Found**: Verify tool name matches exactly
3. **Schema Validation**: Check input matches required schema
4. **Resource Not Found**: Verify resource URI is correct

### Debug Mode

```bash
# Run with debug logging
LOG_LEVEL=DEBUG python3 {module_name}_server.py
```
'''
    
    def _generate_mcp_readme(self, context: Dict[str, Any]) -> str:
        """Generate README for MCP server"""
        
        module_name = context['module_name']
        class_name = context['class_name']
        domain = context['domain']
        module_type = context['module_type']
        
        return f'''# {class_name} MCP Server

**Type**: {module_type} | **Domain**: {domain} | **Protocol**: MCP 2024-11-05

AI-discoverable MCP server providing standardized API endpoints for {domain} domain operations.

## 🚀 Quick Start

### Running the MCP Server

```bash
# Direct execution
python3 {module_name}_server.py

# With configuration
python3 {module_name}_server.py --config config/production.json
```

### AI Integration

```python
from mcp import ClientSession
from mcp.client.stdio import stdio_client

# Connect to MCP server
async with stdio_client(["python", "{module_name}_server.py"]) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        
        # Discover capabilities
        tools = await session.list_tools()
        capabilities = await session.call_tool("{module_name}_get_capabilities", {{}})
        
        # Execute operations
        result = await session.call_tool("{module_name}_execute_operation", {{
            "data": {{"key": "value"}}
        }})
```

## 🔧 MCP Tools

| Tool Name | Description | Input Schema |
|-----------|-------------|--------------|
| `{module_name}_health_check` | Check server health | No parameters |
| `{module_name}_get_capabilities` | Get module capabilities | No parameters |
| AI_TODO | Add your domain-specific tools | Define schemas |

## 📊 MCP Resources

| Resource URI | Description | Content Type |
|--------------|-------------|--------------|
| `mcp://{module_name}/schema` | Complete API schema | application/json |
| `mcp://{module_name}/config` | Current configuration | application/json |
| AI_TODO | Add your domain-specific resources | Define types |

## 💬 MCP Prompts

| Prompt Name | Description | Arguments |
|-------------|-------------|-----------|
| `{module_name}_completion_guide` | AI implementation guidance | business_context (optional) |
| `{module_name}_integration_guide` | Integration instructions | integration_type (required) |

## 🎯 Business Capabilities

### Primary Operations
- AI_TODO: List main business operations

### Data Entities  
- AI_TODO: List domain entities managed

### Business Rules
- AI_TODO: List key business constraints

### Integration Points
- AI_TODO: List external dependencies

## 🔍 Discovery Information

This MCP server exposes the following for AI discovery:

```json
{{
  "name": "{module_name}",
  "type": "{module_type}",
  "domain": "{domain}",
  "protocol": "MCP 2024-11-05",
  "transport": ["stdio", "http"],
  "capabilities": {{
    "tools": true,
    "resources": true,
    "prompts": true
  }}
}}
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run MCP-specific tests
pytest tests/test_mcp_*.py -v

# Run AI integration tests
pytest tests/test_ai_integration.py -v
```

## 📈 Monitoring

The MCP server provides built-in monitoring through:

- Health check endpoints
- Performance metrics resources
- Operation logging
- Error tracking

## 🤖 AI Agent Integration

This MCP server is designed for seamless AI agent integration:

1. **Auto-Discovery**: AI agents can discover capabilities automatically
2. **Self-Documentation**: Complete API schemas and examples provided
3. **Error Recovery**: Detailed error messages help AI agents debug
4. **Context Awareness**: Prompts provide domain-specific guidance

---

Built with the Standardized Modules Framework v1.1.0 - MCP Edition
'''
    
    def _generate_mcp_containerization(self, module_path: Path, context: Dict[str, Any]):
        """Generate Docker and Kubernetes files for MCP server"""
        
        # Generate Dockerfile
        dockerfile_content = self.templates.generate_mcp_dockerfile(context)
        self._write_file(module_path / 'Dockerfile', dockerfile_content)
        
        # Generate Docker Compose
        compose_content = self.templates.generate_mcp_docker_compose(context)
        self._write_file(module_path / 'docker-compose.yml', compose_content)
        
        # Generate Kubernetes manifests
        self._generate_mcp_k8s_manifests(module_path, context)
        
        # Generate deployment scripts
        self._generate_mcp_deployment_scripts(module_path, context)
    
    def _generate_mcp_k8s_manifests(self, module_path: Path, context: Dict[str, Any]):
        """Generate Kubernetes manifests for MCP server"""
        
        module_name = context['module_name']
        
        # Deployment manifest
        deployment_content = f'''apiVersion: apps/v1
kind: Deployment
metadata:
  name: {module_name}-mcp-server
  labels:
    app: {module_name}-mcp-server
    type: mcp-server
    domain: {context['domain']}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {module_name}-mcp-server
  template:
    metadata:
      labels:
        app: {module_name}-mcp-server
    spec:
      containers:
      - name: mcp-server
        image: {module_name}-mcp-server:latest
        ports:
        - containerPort: 8000
        env:
        - name: LOG_LEVEL
          value: "INFO"
        - name: MCP_TRANSPORT
          value: "http"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
'''
        
        self._write_file(module_path / 'k8s' / 'deployment.yaml', deployment_content)
        
        # Service manifest
        service_content = f'''apiVersion: v1
kind: Service
metadata:
  name: {module_name}-mcp-service
  labels:
    app: {module_name}-mcp-server
spec:
  selector:
    app: {module_name}-mcp-server
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
  type: ClusterIP
'''
        
        self._write_file(module_path / 'k8s' / 'service.yaml', service_content)
    
    def _to_class_name(self, module_name: str) -> str:
        """Convert module name to class name"""
        return ''.join(word.capitalize() for word in module_name.replace('-', '_').split('_'))
    
    def _write_file(self, file_path: Path, content: str):
        """Write content to file"""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_mcp_pytest_config(self, context: Dict[str, Any]) -> str:
        """Generate pytest configuration for MCP tests"""
        
        return '''[tool:pytest]
minversion = 7.0
addopts = -ra -q --tb=short
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto

# MCP-specific test markers
markers =
    mcp: MCP protocol tests
    ai_integration: AI integration tests
    performance: Performance tests
    unit: Unit tests
    integration: Integration tests

# Test discovery patterns
collect_ignore = [
    "setup.py",
    "conftest.py"
]

# Async test configuration
asyncio_mode = auto
asyncio_default_fixture_loop_scope = function

# Coverage configuration for MCP tests
addopts = --cov=core --cov=interface --cov=types --cov-report=term-missing
'''
