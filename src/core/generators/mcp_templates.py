"""
MCP Server Templates for Standardized Modules Framework

This module contains templates for generating MCP (Model Context Protocol) servers
that are API-first, self-describing, and AI-discoverable.
"""

from typing import Dict, Any


class MCPServerTemplates:
    """Templates for generating MCP servers from standardized modules"""
    
    def generate_mcp_server(self, module_type: str, context: Dict[str, Any]) -> str:
        """Generate MCP server based on module type"""
        
        if module_type == 'CORE':
            return self._generate_core_mcp_server(context)
        elif module_type == 'INTEGRATION':
            return self._generate_integration_mcp_server(context)
        elif module_type == 'SUPPORTING':
            return self._generate_supporting_mcp_server(context)
        elif module_type == 'TECHNICAL':
            return self._generate_technical_mcp_server(context)
        else:
            raise ValueError(f"Unknown module type: {module_type}")
    
    def _generate_core_mcp_server(self, context: Dict[str, Any]) -> str:
        """Generate CORE business logic MCP server"""
        
        module_name = context['module_name']
        class_name = context['class_name']
        domain = context['domain']
        
        return f'''"""
{class_name} MCP Server - Core Business Module

This MCP server handles core business logic for {domain} domain.
Provides standardized API endpoints for AI integration and discovery.
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

# MCP Server dependencies
from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, Prompt

from types import {class_name}Config, {class_name}Result
from interface import {class_name}Interface


logger = logging.getLogger(__name__)


class {class_name}MCPServer({class_name}Interface):
    """
    MCP Server implementation for {domain} domain core business logic.
    
    Provides standardized API endpoints for:
    - Business operation execution
    - Module discovery and introspection  
    - Health monitoring
    - Configuration management
    """
    
    def __init__(self, config: {class_name}Config):
        self.config = config
        self.server = Server(name="{module_name}-mcp-server")
        self._initialized = False
        self._setup_mcp_handlers()
        logger.info(f"Initializing {class_name} MCP Server for {domain} domain")
    
    def _setup_mcp_handlers(self):
        """Setup MCP protocol handlers"""
        
        # Register tools (executable functions)
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List all available tools for this module"""
            return [
                Tool(
                    name=f"{module_name}_execute_primary_operation",
                    description=f"Execute primary business operation for {domain} domain",
                    inputSchema={{
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
                ),
                Tool(
                    name=f"{module_name}_health_check",
                    description=f"Check health status of {module_name} module",
                    inputSchema={{
                        "type": "object",
                        "properties": {{}},
                        "additionalProperties": False
                    }}
                ),
                Tool(
                    name=f"{module_name}_get_capabilities",
                    description=f"Get detailed capabilities and API documentation",
                    inputSchema={{
                        "type": "object", 
                        "properties": {{}},
                        "additionalProperties": False
                    }}
                )
            ]
        
        # Register resources (data sources)
        @self.server.list_resources()
        async def list_resources() -> List[Resource]:
            """List all available resources for this module"""
            return [
                Resource(
                    uri=f"mcp://{module_name}/schema",
                    name=f"{module_name} API Schema",
                    description=f"Complete API schema for {domain} operations",
                    mimeType="application/json"
                ),
                Resource(
                    uri=f"mcp://{module_name}/config",
                    name=f"{module_name} Configuration",
                    description=f"Current module configuration and settings",
                    mimeType="application/json"
                ),
                Resource(
                    uri=f"mcp://{module_name}/metrics",
                    name=f"{module_name} Metrics",
                    description=f"Performance and usage metrics",
                    mimeType="application/json"
                )
            ]
        
        # Register prompts (reusable templates)
        @self.server.list_prompts()
        async def list_prompts() -> List[Prompt]:
            """List all available prompts for this module"""
            return [
                Prompt(
                    name=f"{module_name}_completion_guide",
                    description=f"AI completion guide for implementing {domain} business logic",
                    arguments=[
                        {{
                            "name": "business_context",
                            "description": "Specific business context for implementation",
                            "required": False
                        }}
                    ]
                ),
                Prompt(
                    name=f"{module_name}_integration_guide", 
                    description=f"Guide for integrating with {domain} module",
                    arguments=[
                        {{
                            "name": "integration_type",
                            "description": "Type of integration (api, event, data)",
                            "required": True
                        }}
                    ]
                )
            ]
        
        # Tool execution handlers
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
            """Execute tool based on name and arguments"""
            
            if name == f"{module_name}_execute_primary_operation":
                result = await self.execute_primary_operation(arguments.get("data", {{}}))
                return [types.TextContent(
                    type="text",
                    text=json.dumps(result.to_dict() if hasattr(result, 'to_dict') else result, indent=2)
                )]
            
            elif name == f"{module_name}_health_check":
                health = await self.health_check()
                return [types.TextContent(
                    type="text", 
                    text=json.dumps(health, indent=2)
                )]
                
            elif name == f"{module_name}_get_capabilities":
                capabilities = await self.get_capabilities()
                return [types.TextContent(
                    type="text",
                    text=json.dumps(capabilities, indent=2)
                )]
            
            else:
                raise ValueError(f"Unknown tool: {{name}}")
        
        # Resource reading handlers
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read resource content based on URI"""
            
            if uri == f"mcp://{module_name}/schema":
                return json.dumps(await self.get_api_schema(), indent=2)
            elif uri == f"mcp://{module_name}/config":
                return json.dumps(self.config.to_dict() if hasattr(self.config, 'to_dict') else {{}}, indent=2)
            elif uri == f"mcp://{module_name}/metrics":
                return json.dumps(await self.get_metrics(), indent=2)
            else:
                raise ValueError(f"Unknown resource: {{uri}}")
        
        # Prompt handling
        @self.server.get_prompt()
        async def get_prompt(name: str, arguments: Dict[str, str]) -> types.GetPromptResult:
            """Get prompt content based on name and arguments"""
            
            if name == f"{module_name}_completion_guide":
                content = f"AI completion guide for {domain} business logic implementation. See AI_COMPLETION.md for detailed instructions."
                return types.GetPromptResult(
                    description=f"AI completion guide for {domain} business logic",
                    messages=[
                        types.PromptMessage(
                            role="user",
                            content=types.TextContent(type="text", text=content)
                        )
                    ]
                )
            
            elif name == f"{module_name}_integration_guide":
                integration_type = arguments.get("integration_type", "api")
                content = f"Integration guide for {module_name} using {{integration_type}} pattern. This MCP server provides standardized JSON-RPC 2.0 endpoints for AI integration."
                return types.GetPromptResult(
                    description=f"Integration guide for {module_name} ({{integration_type}})",
                    messages=[
                        types.PromptMessage(
                            role="user", 
                            content=types.TextContent(type="text", text=content)
                        )
                    ]
                )
            
            else:
                raise ValueError(f"Unknown prompt: {{name}}")
    
    async def initialize(self) -> bool:
        """Initialize the MCP server and business module"""
        try:
            # AI_TODO: Implement initialization logic
            # - Set up database connections
            # - Initialize external service clients
            # - Load configuration and validate settings
            # - Register with service discovery
            
            self._initialized = True
            logger.info(f"{class_name} MCP Server initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize {class_name} MCP Server: {{e}}")
            return False
    
    async def execute_primary_operation(self, data: Dict[str, Any]) -> {class_name}Result:
        """Execute primary business operation (MCP Tool)"""
        
        if not self._initialized:
            return {class_name}Result(
                success=False,
                error="Module not initialized",
                data=None
            )
        
        try:
            logger.info(f"Executing primary operation in {class_name}")
            
            # AI_TODO: Implement core business logic
            # 1. Validate business input according to domain rules
            # 2. Apply business transformations and calculations
            # 3. Enforce business constraints and policies
            # 4. Generate audit trail for compliance
            # 5. Return structured result
            
            # Example validation
            if not self._validate_input(data):
                return {class_name}Result(
                    success=False,
                    error="Input validation failed",
                    data=None
                )
            
            # AI_IMPLEMENTATION_REQUIRED: Core business processing
            processed_data = await self._process_business_logic(data)
            
            # Generate audit trail
            await self._create_audit_entry(data, processed_data)
            
            return {class_name}Result(
                success=True,
                data=processed_data,
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Processing failed in {class_name}: {{e}}")
            return {class_name}Result(
                success=False,
                error=str(e),
                data=None
            )
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get module capabilities for AI discovery (MCP Tool)"""
        return {{
            "module_info": {{
                "name": "{module_name}",
                "type": "CORE",
                "domain": "{domain}",
                "version": "1.0.0",
                "description": "Core business logic module for {domain} domain"
            }},
            "api_endpoints": {{
                "tools": [
                    {{
                        "name": f"{module_name}_execute_primary_operation",
                        "description": "Execute primary business operation",
                        "input_schema": "See MCP tool definition",
                        "output_schema": "{class_name}Result"
                    }},
                    {{
                        "name": f"{module_name}_health_check",
                        "description": "Check module health status",
                        "input_schema": "No parameters",
                        "output_schema": "HealthStatus"
                    }}
                ],
                "resources": [
                    {{
                        "uri": f"mcp://{module_name}/schema",
                        "description": "Complete API schema"
                    }},
                    {{
                        "uri": f"mcp://{module_name}/config", 
                        "description": "Module configuration"
                    }}
                ]
            }},
            "integration_patterns": {{
                "api_style": "MCP JSON-RPC 2.0",
                "transport": ["stdio", "http"],
                "authentication": "configurable",
                "rate_limiting": "built-in"
            }},
            "business_capabilities": {{
                # AI_TODO: Define specific business capabilities
                "primary_operations": ["process", "validate", "audit"],
                "data_entities": [],  # Define domain entities
                "business_rules": [],  # Define business constraints
                "integration_points": []  # Define external dependencies
            }}
        }}
    
    async def get_api_schema(self) -> Dict[str, Any]:
        """Get complete API schema for AI integration (MCP Resource)"""
        return {{
            "openapi": "3.0.0",
            "info": {{
                "title": f"{class_name} MCP Server API",
                "version": "1.0.0",
                "description": f"MCP server for {domain} domain business logic"
            }},
            "paths": {{
                "/tools/{module_name}_execute_primary_operation": {{
                    "post": {{
                        "summary": "Execute primary business operation",
                        "requestBody": {{
                            "content": {{
                                "application/json": {{
                                    "schema": {{
                                        "type": "object",
                                        "properties": {{
                                            "data": {{"type": "object"}},
                                            "options": {{"type": "object"}}
                                        }}
                                    }}
                                }}
                            }}
                        }},
                        "responses": {{
                            "200": {{
                                "description": "Operation result",
                                "content": {{
                                    "application/json": {{
                                        "schema": {{
                                            "type": "object",
                                            "properties": {{
                                                "success": {{"type": "boolean"}},
                                                "data": {{"type": "object"}},
                                                "error": {{"type": "string"}},
                                                "timestamp": {{"type": "string"}}
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }},
            "components": {{
                "schemas": {{
                    "{class_name}Result": {{
                        "type": "object",
                        "properties": {{
                            "success": {{"type": "boolean"}},
                            "data": {{"type": "object"}},
                            "error": {{"type": "string"}}, 
                            "timestamp": {{"type": "string"}}
                        }}
                    }}
                }}
            }}
        }}
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get performance and usage metrics (MCP Resource)"""
        return {{
            "module": "{module_name}",
            "type": "CORE",
            "domain": "{domain}",
            "status": "healthy" if self._initialized else "not_initialized",
            "performance": {{
                "total_operations": 0,  # AI_TODO: Implement metrics tracking
                "average_response_time": 0.0,
                "error_rate": 0.0,
                "last_operation": None
            }},
            "resources": {{
                "memory_usage": "0MB",  # AI_TODO: Implement resource monitoring
                "cpu_usage": "0%",
                "connections": 0
            }},
            "timestamp": datetime.utcnow().isoformat()
        }}
    
    def _validate_input(self, data: Dict[str, Any]) -> bool:
        """Validate input data against business rules"""
        # AI_TODO: Implement validation logic specific to {domain}
        # - Check required fields
        # - Validate data types and formats
        # - Apply business rule constraints
        # - Check authorization and permissions
        
        return True  # Placeholder
    
    async def _process_business_logic(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Core business logic processing"""
        # AI_IMPLEMENTATION_REQUIRED: Implement domain-specific business logic
        # This is where the main business value is created
        
        processed = {{
            "input": data,
            "processed_at": datetime.utcnow().isoformat(),
            "processor": "{class_name}",
            "domain": "{domain}",
            "mcp_server": True
        }}
        
        return processed
    
    async def _create_audit_entry(self, input_data: Dict[str, Any], 
                                 output_data: Dict[str, Any]) -> None:
        """Create audit trail entry for compliance"""
        # AI_TODO: Implement audit logging
        # - Record all business operations
        # - Include user context and timestamps
        # - Ensure immutable audit trail
        # - Support compliance reporting
        
        audit_entry = {{
            "operation": "process",
            "module": "{class_name}",
            "mcp_server": True,
            "input_hash": hash(str(input_data)),
            "output_hash": hash(str(output_data)),
            "timestamp": datetime.utcnow().isoformat()
        }}
        
        logger.info(f"Audit entry created: {{audit_entry}}")
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for monitoring and alerting (MCP Tool)"""
        return {{
            "status": "healthy" if self._initialized else "not_initialized",
            "module": "{class_name}",
            "domain": "{domain}",
            "mcp_server": True,
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat(),
            "capabilities": {{
                "tools": 3,
                "resources": 3,
                "prompts": 2
            }}
        }}
    
    async def cleanup(self) -> None:
        """Cleanup resources on shutdown"""
        # AI_TODO: Implement cleanup logic
        # - Close database connections
        # - Release external resources
        # - Flush any pending operations
        # - Deregister from service discovery
        
        self._initialized = False
        logger.info(f"{class_name} MCP Server cleaned up successfully")


async def main():
    """Main entry point for MCP server"""
    
    # AI_TODO: Load configuration from environment or config file
    config = {class_name}Config()
    
    # Create MCP server instance
    server_instance = {class_name}MCPServer(config)
    
    # Initialize the server
    if not await server_instance.initialize():
        logger.error("Failed to initialize MCP server")
        return
    
    # Run MCP server with stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server_instance.server.run(
            read_stream,
            write_stream,
            server_instance.server.create_initialization_options()
        )


if __name__ == "__main__":
    # Run the MCP server
    asyncio.run(main())


# Factory function for programmatic use
def create_{module_name.replace('-', '_')}_mcp_server(config: {class_name}Config) -> {class_name}MCPServer:
    """Factory function to create {class_name} MCP Server instance"""
    return {class_name}MCPServer(config)
'''
    
    def _generate_integration_mcp_server(self, context: Dict[str, Any]) -> str:
        """Generate INTEGRATION MCP server template"""
        
        module_name = context['module_name']
        class_name = context['class_name']
        domain = context['domain']
        
        return f'''"""
{class_name} MCP Server - Integration Module

This MCP server handles external service integration for {domain} domain.
Provides fault-tolerant API endpoints with circuit breaker protection.
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import aiohttp

# MCP Server dependencies
from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, Prompt

from types import {class_name}Config, {class_name}Result
from interface import {class_name}Interface


logger = logging.getLogger(__name__)


class {class_name}MCPServer({class_name}Interface):
    """
    MCP Server implementation for {domain} domain external integration.
    
    Provides standardized API endpoints for:
    - External service communication
    - Circuit breaker management
    - Retry policy execution
    - Integration health monitoring
    """
    
    def __init__(self, config: {class_name}Config):
        self.config = config
        self.server = Server(name="{module_name}-mcp-server")
        self._initialized = False
        self._circuit_breaker_state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self._failure_count = 0
        self._last_failure_time = None
        self._setup_mcp_handlers()
        logger.info(f"Initializing {class_name} MCP Server for {domain} integration")


async def main():
    """Main entry point for Integration MCP server"""
    
    config = {class_name}Config()
    server_instance = {class_name}MCPServer(config)
    
    if not await server_instance.initialize():
        logger.error("Failed to initialize Integration MCP server")
        return
    
    async with stdio_server() as (read_stream, write_stream):
        await server_instance.server.run(
            read_stream,
            write_stream,
            server_instance.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
'''
    
    def _generate_supporting_mcp_server(self, context: Dict[str, Any]) -> str:
        """Generate SUPPORTING workflow MCP server template"""
        
        module_name = context['module_name']
        class_name = context['class_name']
        domain = context['domain']
        
        return f'''"""
{class_name} MCP Server - Supporting Module

This MCP server handles supporting workflows for {domain} domain.
Provides orchestration and workflow management API endpoints.
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

# MCP Server dependencies
from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, Prompt

from types import {class_name}Config, {class_name}Result
from interface import {class_name}Interface


logger = logging.getLogger(__name__)


class {class_name}MCPServer({class_name}Interface):
    """
    MCP Server implementation for {domain} domain workflow management.
    
    Provides standardized API endpoints for:
    - Workflow orchestration
    - Process monitoring
    - Step execution tracking
    - Workflow state management
    """
    
    def __init__(self, config: {class_name}Config):
        self.config = config
        self.server = Server(name="{module_name}-mcp-server")
        self._initialized = False
        self._active_workflows = {{}}  # workflow_id -> workflow_data
        self._setup_mcp_handlers()
        logger.info(f"Initializing {class_name} MCP Server for {domain} workflows")


async def main():
    """Main entry point for Supporting MCP server"""
    
    config = {class_name}Config()
    server_instance = {class_name}MCPServer(config)
    
    if not await server_instance.initialize():
        logger.error("Failed to initialize Supporting MCP server")
        return
    
    async with stdio_server() as (read_stream, write_stream):
        await server_instance.server.run(
            read_stream,
            write_stream,
            server_instance.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
'''
    
    def _generate_technical_mcp_server(self, context: Dict[str, Any]) -> str:
        """Generate TECHNICAL infrastructure MCP server template"""
        
        module_name = context['module_name']
        class_name = context['class_name']
        domain = context['domain']
        
        return f'''"""
{class_name} MCP Server - Technical Module

This MCP server handles technical infrastructure for {domain} domain.
Provides resource management and performance monitoring API endpoints.
"""

import asyncio
import json
import logging
import psutil
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

# MCP Server dependencies
from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, Prompt

from types import {class_name}Config, {class_name}Result
from interface import {class_name}Interface


logger = logging.getLogger(__name__)


class {class_name}MCPServer({class_name}Interface):
    """
    MCP Server implementation for {domain} domain technical infrastructure.
    
    Provides standardized API endpoints for:
    - Resource pool management
    - Performance monitoring
    - Scaling operations
    - Infrastructure health checks
    """
    
    def __init__(self, config: {class_name}Config):
        self.config = config
        self.server = Server(name="{module_name}-mcp-server")
        self._initialized = False
        self._resource_pools = {{}}
        self._metrics_history = []
        self._setup_mcp_handlers()
        logger.info(f"Initializing {class_name} MCP Server for {domain} infrastructure")


async def main():
    """Main entry point for Technical MCP server"""
    
    config = {class_name}Config()
    server_instance = {class_name}MCPServer(config)
    
    if not await server_instance.initialize():
        logger.error("Failed to initialize Technical MCP server")
        return
    
    async with stdio_server() as (read_stream, write_stream):
        await server_instance.server.run(
            read_stream,
            write_stream,
            server_instance.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
'''
    
    def generate_mcp_ai_completion_guide(self, context: Dict[str, Any]) -> str:
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
    name=f"{module_name}_your_custom_operation",
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

### 📊 Discovery & Documentation (HIGH PRIORITY)

#### 6. Update Capabilities Response
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
'''
    
    def generate_mcp_types(self, context: Dict[str, Any]) -> str:
        """Generate MCP-specific type definitions"""
        
        class_name = context['class_name']
        module_name = context['module_name']
        domain = context['domain']
        
        return f'''"""
Type definitions for {class_name} MCP Server

This module contains all type definitions, data classes, and schemas
used by the {module_name} MCP server for {domain} domain.
"""

from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


@dataclass
class {class_name}Config:
    """Configuration for {class_name} MCP Server"""
    
    # AI_TODO: Define configuration parameters specific to {domain}
    # Examples:
    # - Database connection strings
    # - External service endpoints
    # - Authentication credentials
    # - Performance thresholds
    
    server_name: str = "{module_name}-mcp-server"
    domain: str = "{domain}"
    log_level: str = "INFO"
    max_concurrent_operations: int = 100
    
    # MCP-specific configuration
    mcp_transport: str = "stdio"  # stdio, http
    mcp_version: str = "2024-11-05"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {{
            "server_name": self.server_name,
            "domain": self.domain,
            "log_level": self.log_level,
            "max_concurrent_operations": self.max_concurrent_operations,
            "mcp_transport": self.mcp_transport,
            "mcp_version": self.mcp_version
        }}


@dataclass
class {class_name}Result:
    """Standard result format for all MCP operations"""
    
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: Optional[datetime] = field(default_factory=datetime.utcnow)
    operation_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for JSON serialization"""
        return {{
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "operation_id": self.operation_id
        }}


@dataclass
class HealthStatus:
    """Health check result format"""
    
    status: str  # healthy, degraded, unhealthy
    module_name: str
    domain: str
    timestamp: datetime
    details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {{
            "status": self.status,
            "module_name": self.module_name,
            "domain": self.domain,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details
        }}


# AI_TODO: Add domain-specific type definitions
# Examples for different domains:

# E-commerce domain types:
# @dataclass
# class User:
#     id: str
#     email: str
#     created_at: datetime

# Finance domain types:
# @dataclass
# class Transaction:
#     id: str
#     amount: float
#     currency: str
#     timestamp: datetime
'''
    
    def generate_mcp_interface(self, context: Dict[str, Any]) -> str:
        """Generate MCP server interface definition"""
        
        class_name = context['class_name']
        module_name = context['module_name']
        domain = context['domain']
        module_type = context['module_type']
        
        return f'''"""
Interface definition for {class_name} MCP Server

This module defines the interface contract that all {module_type} MCP servers
must implement for {domain} domain operations.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from types import {class_name}Config, {class_name}Result, HealthStatus


class {class_name}Interface(ABC):
    """
    Interface contract for {class_name} MCP Server
    
    All {module_type} modules in the {domain} domain must implement
    this interface to ensure consistent API behavior and AI discoverability.
    """
    
    @abstractmethod
    async def initialize(self) -> bool:
        """
        Initialize the MCP server and all required resources
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check and return current status
        
        Returns:
            Dict: Current health status with details
        """
        pass
    
    @abstractmethod
    async def get_capabilities(self) -> Dict[str, Any]:
        """
        Get module capabilities for AI discovery
        
        Returns:
            Dict: Complete capabilities description including:
            - Available API endpoints
            - Integration patterns
            - Business capabilities
            - Technical specifications
        """
        pass
    
    @abstractmethod
    async def get_api_schema(self) -> Dict[str, Any]:
        """
        Get complete API schema in OpenAPI format
        
        Returns:
            Dict: OpenAPI 3.0 schema for all endpoints
        """
        pass
    
    @abstractmethod
    async def cleanup(self) -> None:
        """
        Cleanup all resources and prepare for shutdown
        """
        pass
    
    # AI_TODO: Add domain-specific interface methods
    # Each module type should define its core operations here
    
    @abstractmethod
    async def execute_primary_operation(self, data: Dict[str, Any]) -> {class_name}Result:
        """Execute the primary business operation"""
        pass
'''
    
    def generate_mcp_server_runner(self, context: Dict[str, Any]) -> str:
        """Generate MCP server runner script"""
        
        module_name = context['module_name']
        class_name = context['class_name']
        
        return f'''#!/usr/bin/env python3
"""
MCP Server Runner for {module_name}

This script starts the {class_name} MCP server with proper configuration
and error handling. It can be used directly or imported as a module.
"""

import asyncio
import sys
import logging
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core import {class_name}MCPServer
from types import {class_name}Config


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stderr),  # MCP uses stderr for logging
            logging.FileHandler(f'{module_name}_mcp.log')
        ]
    )


async def run_mcp_server():
    """Run the MCP server with proper error handling"""
    
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        
        # AI_TODO: Load configuration from environment or config file
        config = {class_name}Config()
        
        # Create and initialize MCP server
        server = {class_name}MCPServer(config)
        
        if not await server.initialize():
            logger.error("Failed to initialize MCP server")
            sys.exit(1)
        
        logger.info(f"Starting {class_name} MCP Server...")
        
        # Run the server
        await server.server.run_stdio()
        
    except KeyboardInterrupt:
        logger.info("MCP server stopped by user")
    except Exception as e:
        logger.error(f"MCP server error: {{e}}")
        sys.exit(1)
    finally:
        # Cleanup
        if 'server' in locals():
            await server.cleanup()


def main():
    """Main entry point"""
    asyncio.run(run_mcp_server())


if __name__ == "__main__":
    main()
'''
    
    def generate_mcp_dockerfile(self, context: Dict[str, Any]) -> str:
        """Generate Dockerfile for MCP server deployment"""
        
        module_name = context['module_name']
        
        return f'''# Multi-stage Dockerfile for {module_name} MCP Server

# Build stage
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN pip install --no-cache-dir build wheel

# Copy source code
COPY . .

# Build the package
RUN python -m build --wheel

# Production stage  
FROM python:3.11-slim

# Create non-root user for security
RUN groupadd -r mcp && useradd -r -g mcp mcp

# Set working directory
WORKDIR /app

# Install runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy MCP server files
COPY core.py interface.py types.py ./
COPY {module_name}_server.py ./

# Set proper permissions
RUN chown -R mcp:mcp /app
USER mcp

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD python3 -c "import asyncio; from core import {context['class_name']}MCPServer; from types import {context['class_name']}Config; asyncio.run({context['class_name']}MCPServer({context['class_name']}Config()).health_check())" || exit 1

# Expose MCP server (stdio transport doesn't need ports, but useful for HTTP transport)
EXPOSE 8000

# Run MCP server
CMD ["python3", "{module_name}_server.py"]
'''
    
    def generate_mcp_docker_compose(self, context: Dict[str, Any]) -> str:
        """Generate Docker Compose for MCP server development"""
        
        module_name = context['module_name']
        
        return f'''# Docker Compose for {module_name} MCP Server Development

version: '3.8'

services:
  {module_name.replace('-', '_')}_mcp_server:
    build: .
    container_name: {module_name}-mcp-server
    restart: unless-stopped
    
    # Environment configuration
    environment:
      - LOG_LEVEL=INFO
      - MCP_TRANSPORT=stdio
      # AI_TODO: Add domain-specific environment variables
    
    # Volume mounts for development
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config
    
    # Health check
    healthcheck:
      test: ["CMD", "python3", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    
    # Resource limits
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
    
    # Logging configuration
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

networks:
  {module_name.replace('-', '_')}_network:
    driver: bridge

volumes:
  {module_name.replace('-', '_')}_data:
    driver: local
'''
