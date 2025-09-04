# Integration Guide: UserAuth MCP Server

## Overview

This guide explains how to integrate with the UserAuth MCP Server for authentication domain operations.

## Integration Patterns

### 1. Direct MCP Client Integration

```python
from mcp import ClientSession
from mcp.client.stdio import stdio_client

async def integrate_with_user_auth():
    async with stdio_client(["python", "user-auth_server.py"]) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Discover capabilities
            capabilities = await session.call_tool("user-auth_get_capabilities", {})
            
            # Use the module
            result = await session.call_tool("user-auth_execute_primary_operation", {
                "data": {"your": "data"}
            })
            
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
  name: user-auth-mcp-service
  annotations:
    mcp.protocol/version: "2024-11-05"
    mcp.discovery/enabled: "true"
spec:
  selector:
    app: user-auth-mcp-server
  ports:
  - port: 8000
    targetPort: 8000
```

## Discovery Mechanisms

### Automatic Discovery

The MCP server exposes discovery endpoints:

```bash
# Get server info
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}'

# List capabilities
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}'
```

### Service Registry Integration

```python
# Register with service discovery
import consul

def register_mcp_server():
    consul_client = consul.Consul()
    consul_client.agent.service.register(
        name="user-auth-mcp-server",
        service_id="user-auth-instance-1",
        port=8000,
        tags=["mcp", "ai-discoverable", "authentication"],
        meta={
            "protocol": "mcp-2024-11-05",
            "domain": "authentication",
            "type": "core-business-logic"
        },
        check=consul.Check.http("http://localhost:8000/health", interval="10s")
    )
```

## Error Handling

### Standard Error Response

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32000,
    "message": "Business validation failed",
    "data": {
      "operation": "execute_primary_operation",
      "module": "UserAuth",
      "timestamp": "2024-01-01T00:00:00Z",
      "details": {}
    }
  }
}
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
metrics = await session.read_resource("mcp://user-auth/metrics")
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
{
  "security": {
    "authentication": {
      "type": "api_key",
      "header": "X-API-Key"
    },
    "rate_limiting": {
      "requests_per_minute": 100,
      "burst_size": 10
    },
    "cors": {
      "enabled": true,
      "allowed_origins": ["https://yourdomain.com"]
    }
  }
}
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
LOG_LEVEL=DEBUG python3 user-auth_server.py
```
