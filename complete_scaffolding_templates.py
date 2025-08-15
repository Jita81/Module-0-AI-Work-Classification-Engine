# === INTEGRATION MODULE TEMPLATE ===

def _generate_integration_module(self, context: Dict[str, Any]) -> str:
    """Generate INTEGRATION module template with fault tolerance"""
    
    template = Template('''"""
{{ module_name }}: {{ "AI_TODO: External service integration purpose" if ai_ready else "External integration module" }}
Type: INTEGRATION
Intent: {{ "AI_TODO: What external service this integrates with and why" if ai_ready else "External service integration" }}
External Service: {{ "AI_TODO: Name and purpose of external service" if ai_ready else "TBD" }}
Fault Tolerance: {{ "AI_TODO: List fault tolerance requirements" if ai_ready else "Circuit breaker, retry, timeout" }}
"""

import asyncio
import aiohttp
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

from .interface import {{ class_name }}Interface
from .types import {{ class_name }}Config, {{ class_name }}Request, {{ class_name }}Response, OperationResult

logger = logging.getLogger(__name__)

class {{ class_name }}Module({{ class_name }}Interface):
    """
    {{ module_name }} external integration
    Type: INTEGRATION
    
    {{ "AI_TODO: Document external service details:" if ai_ready else "" }}
    {{ "- Service name and API documentation URL" if ai_ready else "" }}
    {{ "- Authentication method" if ai_ready else "" }}
    {{ "- Rate limits and SLA" if ai_ready else "" }}
    {{ "- Error codes and recovery strategies" if ai_ready else "" }}
    """
    
    def __init__(self, config: {{ class_name }}Config):
        self.config = config
        self._client_session = None
        self._circuit_breaker = CircuitBreaker(config.circuit_breaker_config)
        self._retry_policy = RetryPolicy(config.retry_config)
        self._rate_limiter = RateLimiter(config.rate_limit_config)
        self._health_status = "unknown"
        self._initialized = False
        
        # {{ "AI_TODO: Add external service specific initialization" if ai_ready else "" }}
        
    async def initialize(self) -> OperationResult:
        """Initialize external service connection with health check"""
        try:
            # Create HTTP client session
            timeout = aiohttp.ClientTimeout(total=self.config.timeout_seconds)
            self._client_session = aiohttp.ClientSession(timeout=timeout)
            
            # {{ "AI_TODO: Add authentication setup" if ai_ready else "" }}
            # {{ "AI_IMPLEMENTATION_REQUIRED: Set up API keys, tokens, etc." if ai_ready else "" }}
            
            # Perform health check
            health_check = await self._perform_health_check()
            if not health_check.success:
                return health_check
                
            self._health_status = "healthy"
            self._initialized = True
            logger.info(f"{{ class_name }} integration initialized successfully")
            return OperationResult.success("Integration initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize {{ module_name }}: {e}")
            return OperationResult.error(f"Initialization failed: {e}")
    
    @circuit_breaker_protected
    @retry_on_failure
    @rate_limited
    async def call_external_service(self, request: {{ class_name }}Request) -> OperationResult[{{ class_name }}Response]:
        """
        {{ "AI_TODO: Main external service operation" if ai_ready else "Call external service with fault tolerance" }}
        
        {{ "AI_TODO: Document:" if ai_ready else "" }}
        {{ "- What this call accomplishes" if ai_ready else "" }}
        {{ "- Expected response format" if ai_ready else "" }}
        {{ "- Error conditions and handling" if ai_ready else "" }}
        """
        if not self._initialized:
            return OperationResult.error("Integration not initialized")
            
        try:
            # {{ "AI_IMPLEMENTATION_REQUIRED" if ai_ready else "External service call implementation" }}
            {% if ai_ready %}
            # AI_TODO: Implement the external service call:
            # 1. Build request URL and headers
            # 2. Make HTTP request
            # 3. Handle response and errors
            # 4. Transform response to internal format
            {% endif %}
            
            # Placeholder - AI will implement actual call
            url = self._build_request_url(request)
            headers = self._build_request_headers(request)
            payload = self._build_request_payload(request)
            
            async with self._client_session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    response_data = await response.json()
                    result = self._transform_response(response_data)
                    return OperationResult.success(result)
                elif response.status == 429:
                    # Rate limited
                    raise RateLimitExceeded("Service rate limit exceeded")
                elif response.status >= 500:
                    # Server error - will trigger retry
                    raise ExternalServiceError(f"Server error: {response.status}")
                else:
                    # Client error - don't retry
                    error_text = await response.text()
                    return OperationResult.error(f"Client error {response.status}: {error_text}")
                    
        except asyncio.TimeoutError:
            logger.warning(f"Timeout calling {{ module_name }}")
            raise ExternalServiceTimeout("Request timed out")
        except aiohttp.ClientError as e:
            logger.error(f"Client error calling {{ module_name }}: {e}")
            raise ExternalServiceError(f"Client error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error calling {{ module_name }}: {e}")
            return OperationResult.error(f"Unexpected error: {e}")
    
    async def get_health_status(self) -> Dict[str, Any]:
        """Get integration health with external service status"""
        service_health = await self._check_external_service_health()
        
        return {
            "module_name": "{{ module_name }}",
            "type": "INTEGRATION", 
            "status": self._health_status,
            "circuit_breaker_state": self._circuit_breaker.state,
            "external_service_health": service_health,
            "rate_limit_remaining": self._rate_limiter.remaining_calls,
            "last_successful_call": self._circuit_breaker.last_success_time,
            "error_rate": self._circuit_breaker.error_rate
        }
    
    async def shutdown(self) -> OperationResult:
        """Gracefully shutdown external connections"""
        try:
            if self._client_session:
                await self._client_session.close()
            
            self._initialized = False
            logger.info("{{ class_name }} integration shutdown completed")
            return OperationResult.success("Shutdown completed")
            
        except Exception as e:
            return OperationResult.error(f"Shutdown error: {e}")
    
    # Private helper methods - FRAMEWORK PROVIDED
    def _build_request_url(self, request: {{ class_name }}Request) -> str:
        """Build external service URL - AI_IMPLEMENTATION_REQUIRED"""
        # {{ "AI_TODO: Implement URL building logic" if ai_ready else "URL building logic" }}
        return f"{self.config.base_url}/api/endpoint"
    
    def _build_request_headers(self, request: {{ class_name }}Request) -> Dict[str, str]:
        """Build request headers with authentication - AI_IMPLEMENTATION_REQUIRED"""
        # {{ "AI_TODO: Implement header building with auth" if ai_ready else "Header building logic" }}
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }
    
    def _build_request_payload(self, request: {{ class_name }}Request) -> Dict[str, Any]:
        """Build request payload - AI_IMPLEMENTATION_REQUIRED"""
        # {{ "AI_TODO: Transform internal request to external format" if ai_ready else "Payload building logic" }}
        return request.__dict__
    
    def _transform_response(self, response_data: Dict[str, Any]) -> {{ class_name }}Response:
        """Transform external response to internal format - AI_IMPLEMENTATION_REQUIRED"""
        # {{ "AI_TODO: Transform external response to internal format" if ai_ready else "Response transformation logic" }}
        return {{ class_name }}Response(**response_data)
    
    async def _perform_health_check(self) -> OperationResult:
        """Check external service health - FRAMEWORK PROVIDED"""
        try:
            async with self._client_session.get(f"{self.config.base_url}/health") as response:
                if response.status == 200:
                    return OperationResult.success("Service healthy")
                else:
                    return OperationResult.error(f"Service unhealthy: {response.status}")
        except Exception as e:
            return OperationResult.error(f"Health check failed: {e}")
    
    async def _check_external_service_health(self) -> str:
        """Check current external service health - FRAMEWORK PROVIDED"""
        try:
            health_result = await self._perform_health_check()
            return "healthy" if health_result.success else "unhealthy"
        except:
            return "unknown"

# Fault tolerance decorators - FRAMEWORK PROVIDED
def circuit_breaker_protected(func):
    """Circuit breaker decorator"""
    async def wrapper(self, *args, **kwargs):
        if not self._circuit_breaker.can_execute():
            raise CircuitBreakerOpenError("Circuit breaker is open")
        
        try:
            result = await func(self, *args, **kwargs)
            self._circuit_breaker.record_success()
            return result
        except Exception as e:
            self._circuit_breaker.record_failure()
            raise
    return wrapper

def retry_on_failure(func):
    """Retry decorator with exponential backoff"""
    async def wrapper(self, *args, **kwargs):
        return await self._retry_policy.execute(func, self, *args, **kwargs)
    return wrapper

def rate_limited(func):
    """Rate limiting decorator"""
    async def wrapper(self, *args, **kwargs):
        await self._rate_limiter.acquire()
        return await func(self, *args, **kwargs)
    return wrapper

# Exception classes - FRAMEWORK PROVIDED
class ExternalServiceError(Exception):
    pass

class ExternalServiceTimeout(ExternalServiceError):
    pass

class RateLimitExceeded(ExternalServiceError):
    pass

class CircuitBreakerOpenError(ExternalServiceError):
    pass
''')
    
    return template.render(**context)

# === SUPPORTING MODULE TEMPLATE ===

def _generate_supporting_module(self, context: Dict[str, Any]) -> str:
    """Generate SUPPORTING module template"""
    
    template = Template('''"""
{{ module_name }}: {{ "AI_TODO: Supporting business function purpose" if ai_ready else "Supporting business module" }}
Type: SUPPORTING
Intent: {{ "AI_TODO: What supporting business capability this provides" if ai_ready else "Supporting business functionality" }}
Business Function: {{ "AI_TODO: Name the business function this supports" if ai_ready else "TBD" }}
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import logging
from datetime import datetime

from .interface import {{ class_name }}Interface
from .types import {{ class_name }}Config, {{ class_name }}Request, {{ class_name }}Response, OperationResult

logger = logging.getLogger(__name__)

class {{ class_name }}Module({{ class_name }}Interface):
    """
    {{ module_name }} supporting business function
    Type: SUPPORTING
    
    {{ "AI_TODO: Document supporting business function:" if ai_ready else "" }}
    {{ "- What business capability this provides" if ai_ready else "" }}
    {{ "- How it integrates with core business modules" if ai_ready else "" }}
    {{ "- Standard patterns and workflows it implements" if ai_ready else "" }}
    """
    
    def __init__(self, config: {{ class_name }}Config):
        self.config = config
        self._business_patterns = {}
        self._workflow_state = {}
        self._performance_metrics = {}
        self._initialized = False
        
    def initialize(self) -> OperationResult:
        """Initialize supporting business module"""
        try:
            # Load business patterns and workflows
            self._load_business_patterns()
            self._initialize_workflows()
            
            self._initialized = True
            logger.info("{{ class_name }} supporting module initialized")
            return OperationResult.success("Module initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize {{ module_name }}: {e}")
            return OperationResult.error(f"Initialization failed: {e}")
    
    def execute_supporting_operation(self, request: {{ class_name }}Request) -> OperationResult[{{ class_name }}Response]:
        """
        {{ "AI_TODO: Main supporting business operation" if ai_ready else "Execute supporting business operation" }}
        
        {{ "AI_TODO: Document:" if ai_ready else "" }}
        {{ "- What business workflow this supports" if ai_ready else "" }}
        {{ "- Integration points with other modules" if ai_ready else "" }}
        {{ "- Standard patterns applied" if ai_ready else "" }}
        """
        if not self._initialized:
            return OperationResult.error("Module not initialized")
            
        try:
            # {{ "AI_IMPLEMENTATION_REQUIRED" if ai_ready else "Supporting business logic" }}
            {% if ai_ready %}
            # AI_TODO: Implement supporting business logic:
            # 1. Validate request against business patterns
            # 2. Execute standard workflow
            # 3. Update business state
            # 4. Return standardized response
            {% endif %}
            
            # Placeholder implementation
            result = {{ class_name }}Response(
                status="success",
                data="AI_TODO: Implement actual business result"
            )
            
            return OperationResult.success(result)
            
        except Exception as e:
            logger.error(f"Error in {{ module_name }} operation: {e}")
            return OperationResult.error(f"Operation failed: {e}")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get supporting module health"""
        return {
            "module_name": "{{ module_name }}",
            "type": "SUPPORTING",
            "status": "healthy" if self._initialized else "unhealthy",
            "active_workflows": len(self._workflow_state),
            "performance_metrics": self._performance_metrics
        }
    
    def shutdown(self) -> OperationResult:
        """Shutdown supporting module"""
        try:
            # Complete active workflows
            self._complete_active_workflows()
            
            self._initialized = False
            return OperationResult.success("Shutdown completed")
        except Exception as e:
            return OperationResult.error(f"Shutdown error: {e}")
    
    # Private helper methods
    def _load_business_patterns(self):
        """Load business patterns - AI_IMPLEMENTATION_REQUIRED"""
        # {{ "AI_TODO: Load standard business patterns for this domain" if ai_ready else "" }}
        pass
    
    def _initialize_workflows(self):
        """Initialize workflows - AI_IMPLEMENTATION_REQUIRED"""
        # {{ "AI_TODO: Set up standard workflows" if ai_ready else "" }}
        pass
    
    def _complete_active_workflows(self):
        """Complete active workflows - FRAMEWORK PROVIDED"""
        for workflow_id in list(self._workflow_state.keys()):
            try:
                # Complete workflow gracefully
                self._workflow_state.pop(workflow_id)
            except Exception as e:
                logger.warning(f"Error completing workflow {workflow_id}: {e}")
''')
    
    return template.render(**context)

# === TECHNICAL MODULE TEMPLATE ===

def _generate_technical_module(self, context: Dict[str, Any]) -> str:
    """Generate TECHNICAL module template"""
    
    template = Template('''"""
{{ module_name }}: {{ "AI_TODO: Technical capability purpose" if ai_ready else "Technical infrastructure module" }}
Type: TECHNICAL
Intent: {{ "AI_TODO: What technical capability this provides" if ai_ready else "Technical infrastructure" }}
Performance: {{ "AI_TODO: Performance requirements and characteristics" if ai_ready else "TBD" }}
"""

from typing import Dict, Any, Optional
import logging
import asyncio
from datetime import datetime

from .interface import {{ class_name }}Interface
from .types import {{ class_name }}Config, OperationResult

logger = logging.getLogger(__name__)

class {{ class_name }}Module({{ class_name }}Interface):
    """
    {{ module_name }} technical infrastructure
    Type: TECHNICAL
    
    {{ "AI_TODO: Document technical capability:" if ai_ready else "" }}
    {{ "- What infrastructure need this addresses" if ai_ready else "" }}
    {{ "- Performance characteristics and requirements" if ai_ready else "" }}
    {{ "- Resource usage and scaling behavior" if ai_ready else "" }}
    """
    
    def __init__(self, config: {{ class_name }}Config):
        self.config = config
        self._resource_pool = None
        self._performance_monitor = PerformanceMonitor()
        self._initialized = False
        
    async def initialize(self) -> OperationResult:
        """Initialize technical infrastructure"""
        try:
            # {{ "AI_IMPLEMENTATION_REQUIRED" if ai_ready else "Initialize infrastructure" }}
            # {{ "AI_TODO: Set up resource pools, connections, caches, etc." if ai_ready else "" }}
            
            self._resource_pool = await self._create_resource_pool()
            self._performance_monitor.start()
            
            self._initialized = True
            logger.info("{{ class_name }} technical module initialized")
            return OperationResult.success("Module initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize {{ module_name }}: {e}")
            return OperationResult.error(f"Initialization failed: {e}")
    
    async def execute_technical_operation(self, operation: str, params: Dict[str, Any]) -> OperationResult:
        """
        {{ "AI_TODO: Main technical operation" if ai_ready else "Execute technical operation" }}
        
        {{ "AI_TODO: Document:" if ai_ready else "" }}
        {{ "- What technical operations are supported" if ai_ready else "" }}
        {{ "- Performance characteristics" if ai_ready else "" }}
        {{ "- Resource management" if ai_ready else "" }}
        """
        if not self._initialized:
            return OperationResult.error("Module not initialized")
            
        start_time = datetime.utcnow()
        
        try:
            # {{ "AI_IMPLEMENTATION_REQUIRED" if ai_ready else "Technical operation implementation" }}
            {% if ai_ready %}
            # AI_TODO: Implement technical operations:
            # - Route to appropriate handler based on operation
            # - Manage resources efficiently 
            # - Monitor performance
            # - Handle errors gracefully
            {% endif %}
            
            result = await self._execute_operation_handler(operation, params)
            
            # Record performance metrics
            duration = (datetime.utcnow() - start_time).total_seconds()
            self._performance_monitor.record_operation(operation, duration, True)
            
            return OperationResult.success(result)
            
        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds()
            self._performance_monitor.record_operation(operation, duration, False)
            
            logger.error(f"Technical operation failed: {e}")
            return OperationResult.error(f"Operation failed: {e}")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get technical module health with performance metrics"""
        return {
            "module_name": "{{ module_name }}",
            "type": "TECHNICAL",
            "status": "healthy" if self._initialized else "unhealthy",
            "resource_pool_status": self._get_resource_pool_status(),
            "performance_metrics": self._performance_monitor.get_metrics(),
            "resource_utilization": self._get_resource_utilization()
        }
    
    async def shutdown(self) -> OperationResult:
        """Shutdown technical infrastructure"""
        try:
            # Clean shutdown of resources
            if self._resource_pool:
                await self._resource_pool.close()
            
            self._performance_monitor.stop()
            self._initialized = False
            
            return OperationResult.success("Shutdown completed")
        except Exception as e:
            return OperationResult.error(f"Shutdown error: {e}")
    
    # Private helper methods
    async def _create_resource_pool(self):
        """Create resource pool - AI_IMPLEMENTATION_REQUIRED"""
        # {{ "AI_TODO: Create and configure resource pool" if ai_ready else "" }}
        pass
    
    async def _execute_operation_handler(self, operation: str, params: Dict[str, Any]):
        """Execute operation handler - AI_IMPLEMENTATION_REQUIRED"""
        # {{ "AI_TODO: Route to appropriate operation handler" if ai_ready else "" }}
        pass
    
    def _get_resource_pool_status(self) -> Dict[str, Any]:
        """Get resource pool status - FRAMEWORK PROVIDED"""
        if not self._resource_pool:
            return {"status": "not_initialized"}
        
        return {
            "status": "active",
            "active_connections": getattr(self._resource_pool, 'active_count', 0),
            "available_connections": getattr(self._resource_pool, 'available_count', 0)
        }
    
    def _get_resource_utilization(self) -> Dict[str, Any]:
        """Get resource utilization - FRAMEWORK PROVIDED"""
        return {
            "cpu_usage": "N/A",  # Would implement actual monitoring
            "memory_usage": "N/A",
            "disk_usage": "N/A"
        }

class PerformanceMonitor:
    """Performance monitoring - FRAMEWORK PROVIDED"""
    
    def __init__(self):
        self._metrics = {}
        self._running = False
    
    def start(self):
        self._running = True
    
    def stop(self):
        self._running = False
    
    def record_operation(self, operation: str, duration: float, success: bool):
        if operation not in self._metrics:
            self._metrics[operation] = {
                "total_calls": 0,
                "successful_calls": 0,
                "total_duration": 0.0,
                "avg_duration": 0.0
            }
        
        metrics = self._metrics[operation]
        metrics["total_calls"] += 1
        if success:
            metrics["successful_calls"] += 1
        metrics["total_duration"] += duration
        metrics["avg_duration"] = metrics["total_duration"] / metrics["total_calls"]
    
    def get_metrics(self) -> Dict[str, Any]:
        return self._metrics.copy()
''')
    
    return template.render(**context)

# === COMPLETE SETUP SCRIPT ===

# setup.py for the scaffolding package
setup_script = '''
from setuptools import setup, find_packages

setup(
    name="standardized-modules-framework",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "jinja2>=3.0.0",
        "pyyaml>=6.0.0",
        "aiohttp>=3.8.0"
    ],
    entry_points={
        "console_scripts": [
            "sm=standardized_modules.cli:cli",
        ],
    },
    python_requires=">=3.8",
)
'''

# pyproject.toml alternative
pyproject_toml = '''
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "standardized-modules-framework"
version = "1.0.0"
description = "Standardized module framework for AI-assisted development"
dependencies = [
    "click>=8.0.0",
    "jinja2>=3.0.0", 
    "pyyaml>=6.0.0",
    "aiohttp>=3.8.0"
]

[project.scripts]
sm = "standardized_modules.cli:cli"
'''