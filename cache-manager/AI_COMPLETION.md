# AI Completion Guide: cache-manager MCP Server (TECHNICAL)

## 🎯 Your Mission
Transform this TECHNICAL module into a fully functional MCP (Model Context Protocol) server for the infrastructure domain. This server will be **AI-discoverable** and provide **standardized API endpoints** for seamless integration.

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
    # AI_TODO: Implement infrastructure-specific business logic
    # This is the core value-add of your module
    
    # Example patterns for TECHNICAL modules:
    
    
    
    # - Resource pool management and scaling
    
    pass
```

#### 2. Input Validation
```python
def _validate_input(self, data: Dict[str, Any]) -> bool:
    # AI_TODO: Implement infrastructure-specific validation
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
class CacheManagerConfig:
    # AI_TODO: Define configuration specific to infrastructure
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
    name=f"cache-manager_your_custom_operation",
    description="Describe what this operation does in business terms",
    inputSchema={
        # AI_TODO: Define input schema for your operation
        "type": "object",
        "properties": {
            "field_name": {"type": "string", "description": "Field description"}
        },
        "required": ["field_name"]
    }
)
```

#### 5. Define Resources for AI Access
**File: `core.py` - Update `list_resources()`**

Expose data that AI agents might need:

```python
Resource(
    uri=f"mcp://cache-manager/your-resource",
    name=f"cache-manager Your Resource",
    description="Describe what data this resource provides",
    mimeType="application/json"
)
```

### 📊 Discovery & Documentation (HIGH PRIORITY)

#### 6. Update Capabilities Response
**File: `core.py` - `get_capabilities()` method**

```python
async def get_capabilities(self) -> Dict[str, Any]:
    return {
        "module_info": {
            "name": "cache-manager",
            "type": "TECHNICAL",
            "domain": "infrastructure",
            "version": "1.0.0",
            "description": "Your module description here"
        },
        "business_capabilities": {
            # AI_TODO: Define what business operations this module provides
            "primary_operations": ["operation1", "operation2"],
            "data_entities": ["Entity1", "Entity2"],
            "business_rules": ["rule1", "rule2"],
            "integration_points": ["external_service1", "external_service2"]
        }
    }
```

## 🧪 Testing Your MCP Server

### Quick Test
```bash
# Test MCP server locally
python3 cache-manager_server.py

# Test with MCP client
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | python3 cache-manager_server.py
```

## 🔄 Integration Patterns

### AI Agent Discovery Flow
1. **Connect**: AI agent connects to your MCP server
2. **Discover**: Agent calls `list_tools()`, `list_resources()`, `list_prompts()`
3. **Understand**: Agent calls `get_capabilities()` and `get_api_schema()`
4. **Integrate**: Agent can now use your module's functionality automatically

## 📈 Success Metrics

Your MCP server implementation is complete when:

- ✅ All MCP tools execute without errors
- ✅ Resources return valid JSON data
- ✅ `get_capabilities()` accurately describes functionality
- ✅ AI agents can discover and use the module automatically
- ✅ Health checks pass consistently

---

**🚀 You're building the future of AI-module integration! Each MCP server you create becomes part of an AI-discoverable ecosystem.**
