# Quick Start: MCP-Enhanced Framework

## 🚀 Generate Your First AI-Discoverable MCP Server

```bash
# Activate the framework
source venv/bin/activate

# Create a payments processing MCP server
python3 module_scaffolding_system.py create-mcp-server payment-processor --type=CORE --domain=payments

# Create an integration MCP server
python3 module_scaffolding_system.py create-mcp-server stripe-integration --type=INTEGRATION --domain=payments

# Create with containerization
python3 module_scaffolding_system.py create-mcp-server user-service --type=CORE --domain=users --with-docker
```

## 🔍 What Gets Generated

Each MCP server includes:

### **Core MCP Files**
- `core.py` - MCP server implementation with JSON-RPC 2.0
- `interface.py` - MCP interface contract
- `types.py` - Data types with serialization support
- `{name}_server.py` - Runnable MCP server script

### **AI Discovery Features**
- **Tools**: Executable business functions
- **Resources**: API schemas, config, metrics
- **Prompts**: AI implementation guidance

### **Documentation & Testing**
- `AI_COMPLETION.md` - AI implementation guide
- `docs/API.md` - Complete API documentation
- `tests/test_mcp_*.py` - MCP protocol compliance tests

### **Configuration**
- `mcp_config.json` - MCP server settings
- `pytest.ini` - Testing configuration

## 🤖 AI Integration Example

```python
import asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client

async def ai_discovers_and_uses_module():
    """Example of AI agent discovering and using MCP server"""
    
    # 1. Connect to MCP server
    async with stdio_client(["python", "payment-processor_server.py"]) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 2. AI discovers what the module can do
            tools = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools])
            
            capabilities = await session.call_tool("payment-processor_get_capabilities", {})
            print("Module capabilities:", capabilities)
            
            # 3. AI understands the API
            schema = await session.read_resource("mcp://payment-processor/schema")
            print("API schema available for AI understanding")
            
            # 4. AI uses the module
            result = await session.call_tool("payment-processor_execute_primary_operation", {
                "data": {
                    "amount": 100.00,
                    "currency": "USD",
                    "payment_method": "credit_card"
                }
            })
            print("Payment result:", result)
            
            # 5. AI monitors health
            health = await session.call_tool("payment-processor_health_check", {})
            print("Module health:", health)

# Run the example
asyncio.run(ai_discovers_and_uses_module())
```

## 🔧 Module Types & Use Cases

### **CORE Modules** (Business Logic)
```bash
# User management
python3 module_scaffolding_system.py create-mcp-server user-mgmt --type=CORE --domain=users

# Product catalog  
python3 module_scaffolding_system.py create-mcp-server product-catalog --type=CORE --domain=ecommerce

# Order processing
python3 module_scaffolding_system.py create-mcp-server order-processor --type=CORE --domain=orders
```

### **INTEGRATION Modules** (External Services)
```bash
# Stripe integration
python3 module_scaffolding_system.py create-mcp-server stripe-api --type=INTEGRATION --domain=payments

# Email service
python3 module_scaffolding_system.py create-mcp-server sendgrid-email --type=INTEGRATION --domain=communications

# Database integration
python3 module_scaffolding_system.py create-mcp-server postgres-db --type=INTEGRATION --domain=data
```

### **SUPPORTING Modules** (Workflows)
```bash
# Notification orchestration
python3 module_scaffolding_system.py create-mcp-server notification-hub --type=SUPPORTING --domain=communications

# Workflow engine
python3 module_scaffolding_system.py create-mcp-server workflow-engine --type=SUPPORTING --domain=automation
```

### **TECHNICAL Modules** (Infrastructure)
```bash
# Caching layer
python3 module_scaffolding_system.py create-mcp-server redis-cache --type=TECHNICAL --domain=infrastructure

# Metrics collection
python3 module_scaffolding_system.py create-mcp-server metrics-collector --type=TECHNICAL --domain=monitoring
```

## 🎯 AI Discovery Flow

When an AI agent encounters your MCP servers:

### **1. Automatic Discovery**
```python
# AI scans for MCP servers
tools = await session.list_tools()
# Returns: ["payment-processor_execute_primary_operation", "payment-processor_health_check", ...]
```

### **2. Capability Understanding**
```python
# AI learns what the module does
capabilities = await session.call_tool("payment-processor_get_capabilities", {})
# Returns complete business context and API documentation
```

### **3. Schema Introspection**
```python
# AI gets complete API schema
schema = await session.read_resource("mcp://payment-processor/schema") 
# Returns OpenAPI 3.0 specification
```

### **4. Automatic Integration**
```python
# AI can now use the module without manual configuration
result = await session.call_tool("payment-processor_execute_primary_operation", {
    "data": {"amount": 50.00, "currency": "USD"}
})
```

## 🛠️ Development Workflow

### **1. Generate MCP Server**
```bash
python3 module_scaffolding_system.py create-mcp-server my-service --type=CORE --domain=business
```

### **2. Implement Business Logic**
```bash
cd my-service
# Open AI_COMPLETION.md for guided implementation
# Implement _process_business_logic() and _validate_input()
```

### **3. Test MCP Server**
```bash
# Run the server
python3 my-service_server.py

# Test with MCP client (in another terminal)
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | python3 my-service_server.py
```

### **4. Deploy & Scale**
```bash
# With Docker support
python3 module_scaffolding_system.py create-mcp-server production-service --type=CORE --domain=business --with-docker

cd production-service
docker-compose up  # Local deployment
./scripts/deploy.sh staging  # Cloud deployment
```

## 🌟 Key Benefits

### **For AI Agents**
- **Zero Configuration**: Automatic discovery and integration
- **Self-Documenting**: Complete API schemas and examples
- **Standardized**: Same JSON-RPC 2.0 protocol everywhere
- **Reliable**: Built-in error handling and health monitoring

### **For Developers**  
- **Rapid Development**: Generate complete MCP servers in seconds
- **AI-Guided**: Comprehensive implementation guides
- **Production-Ready**: Full testing, monitoring, and deployment
- **Consistent**: Same patterns across all module types

### **For Teams**
- **Microservices-Ready**: Each module runs independently
- **Scalable**: Kubernetes and cloud deployment built-in
- **Maintainable**: Standard structure and documentation
- **Discoverable**: AI agents can find and use modules automatically

---

**🎉 Your modules are now AI-discoverable building blocks for the next generation of AI systems!**
