# UserAuth MCP Server

**Type**: CORE | **Domain**: authentication | **Protocol**: MCP 2024-11-05

AI-discoverable MCP server providing standardized API endpoints for authentication domain operations.

## 🚀 Quick Start

### Running the MCP Server

```bash
# Direct execution
python3 user-auth_server.py

# With configuration
python3 user-auth_server.py --config config/production.json
```

### AI Integration

```python
from mcp import ClientSession
from mcp.client.stdio import stdio_client

# Connect to MCP server
async with stdio_client(["python", "user-auth_server.py"]) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        
        # Discover capabilities
        tools = await session.list_tools()
        capabilities = await session.call_tool("user-auth_get_capabilities", {})
        
        # Execute operations
        result = await session.call_tool("user-auth_execute_operation", {
            "data": {"key": "value"}
        })
```

## 🔧 MCP Tools

| Tool Name | Description | Input Schema |
|-----------|-------------|--------------|
| `user-auth_health_check` | Check server health | No parameters |
| `user-auth_get_capabilities` | Get module capabilities | No parameters |
| AI_TODO | Add your domain-specific tools | Define schemas |

## 📊 MCP Resources

| Resource URI | Description | Content Type |
|--------------|-------------|--------------|
| `mcp://user-auth/schema` | Complete API schema | application/json |
| `mcp://user-auth/config` | Current configuration | application/json |
| AI_TODO | Add your domain-specific resources | Define types |

## 💬 MCP Prompts

| Prompt Name | Description | Arguments |
|-------------|-------------|-----------|
| `user-auth_completion_guide` | AI implementation guidance | business_context (optional) |
| `user-auth_integration_guide` | Integration instructions | integration_type (required) |

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
{
  "name": "user-auth",
  "type": "CORE",
  "domain": "authentication",
  "protocol": "MCP 2024-11-05",
  "transport": ["stdio", "http"],
  "capabilities": {
    "tools": true,
    "resources": true,
    "prompts": true
  }
}
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
