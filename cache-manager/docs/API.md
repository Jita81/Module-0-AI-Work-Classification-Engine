# CacheManager MCP Server API Documentation

## Overview

This document describes the API endpoints provided by the CacheManager MCP Server for infrastructure domain operations.

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

#### cache-manager_execute_primary_operation

Execute the primary business operation for infrastructure domain.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "data": {
      "type": "object",
      "description": "Input data for business operation"
    },
    "options": {
      "type": "object",
      "description": "Optional processing parameters"
    }
  },
  "required": ["data"]
}
```

**Output:**
```json
{
  "success": true,
  "data": {},
  "timestamp": "2024-01-01T00:00:00Z",
  "operation_id": "uuid"
}
```

#### cache-manager_health_check

Check the health status of the MCP server.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {},
  "additionalProperties": false
}
```

**Output:**
```json
{
  "status": "healthy",
  "module": "CacheManager",
  "domain": "infrastructure",
  "mcp_server": true,
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00Z",
  "capabilities": {
    "tools": 3,
    "resources": 3,
    "prompts": 2
  }
}
```

### Resources (Data Sources)

#### mcp://cache-manager/schema

Complete OpenAPI 3.0 schema for all endpoints.

**Content-Type:** application/json

#### mcp://cache-manager/config

Current module configuration and settings.

**Content-Type:** application/json

#### mcp://cache-manager/metrics

Performance and usage metrics.

**Content-Type:** application/json

### Prompts (Templates)

#### cache-manager_completion_guide

AI completion guide for implementing infrastructure business logic.

**Arguments:**
- `business_context` (optional): Specific business context for implementation

#### cache-manager_integration_guide

Guide for integrating with infrastructure module.

**Arguments:**
- `integration_type` (required): Type of integration (api, event, data)

## Error Handling

All endpoints return standardized error responses:

```json
{
  "success": false,
  "error": "Error description",
  "timestamp": "2024-01-01T00:00:00Z",
  "operation_id": "uuid"
}
```

## Rate Limiting

- **Default**: 100 requests per minute
- **Configurable**: Yes, via configuration
- **Headers**: Standard rate limit headers included

## Examples

### Basic Usage

```bash
# List available tools
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | python3 cache-manager_server.py

# Execute primary operation
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "cache-manager_execute_primary_operation", "arguments": {"data": {"test": "value"}}}}' | python3 cache-manager_server.py
```

### Python Client

```python
import asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client

async def main():
    async with stdio_client(["python", "cache-manager_server.py"]) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Get capabilities
            result = await session.call_tool("cache-manager_get_capabilities", {})
            print("Capabilities:", result)
            
            # Execute operation
            result = await session.call_tool("cache-manager_execute_primary_operation", {
                "data": {"test": "value"}
            })
            print("Result:", result)

if __name__ == "__main__":
    asyncio.run(main())
```
