"""
Template generation module for different types of modules.

This module contains the ModuleTemplates class responsible for generating
code templates for different module types with AI completion markers.
"""

from typing import Dict, Any


class ModuleTemplates:
    """Templates for generating different types of modules"""
    
    def generate_core_module(self, module_type: str, context: Dict[str, Any]) -> str:
        """Generate core module based on type"""
        
        if module_type == 'CORE':
            return self._generate_core_business_module(context)
        elif module_type == 'INTEGRATION':
            return self._generate_integration_module(context)
        elif module_type == 'SUPPORTING':
            return self._generate_supporting_module(context)
        elif module_type == 'TECHNICAL':
            return self._generate_technical_module(context)
        else:
            raise ValueError(f"Unknown module type: {module_type}")
    
    def _generate_core_business_module(self, context: Dict[str, Any]) -> str:
        """Generate CORE business logic module"""
        
        module_name = context['module_name']
        class_name = context['class_name']
        domain = context['domain']
        
        template = f'''"""
{class_name} - Core Business Module

This module handles core business logic for {domain} domain.
Responsibilities include business rule enforcement, data validation,
and domain entity management.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from .types import {class_name}Config, {class_name}Result
from .interface import {class_name}Interface


logger = logging.getLogger(__name__)


class {class_name}({class_name}Interface):
    """
    Core business logic implementation for {domain} domain.
    
    This class encapsulates business rules, validation logic,
    and domain-specific operations.
    """
    
    def __init__(self, config: {class_name}Config):
        self.config = config
        self._initialized = False
        logger.info(f"Initializing {class_name} for {domain} domain")
    
    async def initialize(self) -> bool:
        """Initialize the module with necessary resources"""
        try:
            # AI_TODO: Implement initialization logic
            # - Set up database connections
            # - Initialize external service clients
            # - Load configuration and validate settings
            # - Perform any required startup tasks
            
            self._initialized = True
            logger.info(f"{class_name} initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize {class_name}: {{e}}")
            return False
    
    async def process(self, data: Dict[str, Any]) -> {class_name}Result:
        """
        Main processing method for business operations
        
        Args:
            data: Input data for processing
            
        Returns:
            {class_name}Result: Processing result with status and data
        """
        if not self._initialized:
            raise RuntimeError("{class_name} not initialized. Call initialize() first.")
        
        try:
            # AI_TODO: Implement core business logic
            # 1. Validate input data against business rules
            # 2. Apply domain-specific transformations
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
            "domain": "{domain}"
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
            "input_hash": hash(str(input_data)),
            "output_hash": hash(str(output_data)),
            "timestamp": datetime.utcnow().isoformat()
        }}
        
        logger.info(f"Audit entry created: {{audit_entry}}")
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for monitoring and alerting"""
        return {{
            "status": "healthy" if self._initialized else "not_initialized",
            "module": "{class_name}",
            "domain": "{domain}",
            "timestamp": datetime.utcnow().isoformat()
        }}
    
    async def cleanup(self) -> None:
        """Cleanup resources on shutdown"""
        # AI_TODO: Implement cleanup logic
        # - Close database connections
        # - Release external resources
        # - Flush any pending operations
        
        self._initialized = False
        logger.info(f"{class_name} cleaned up successfully")


# Factory function for easy instantiation
def create_{module_name.replace('-', '_')}(config: {class_name}Config) -> {class_name}:
    """Factory function to create {class_name} instance"""
    return {class_name}(config)
'''
        
        return template
    
    def _generate_integration_module(self, context: Dict[str, Any]) -> str:
        """Generate INTEGRATION module with fault tolerance"""
        
        class_name = context['class_name']
        module_name = context['module_name']
        
        return f'''"""
{class_name} - Integration Module

Handles external service integration with fault tolerance patterns.
Includes circuit breaker, retry policies, and rate limiting.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import aiohttp
from .types import {class_name}Config, {class_name}Result
from .interface import {class_name}Interface


logger = logging.getLogger(__name__)


class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open"""
    pass


class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded"""
    pass


class {class_name}({class_name}Interface):
    """
    Integration module with fault tolerance patterns
    """
    
    def __init__(self, config: {class_name}Config):
        self.config = config
        self._session: Optional[aiohttp.ClientSession] = None
        self._circuit_breaker_state = "closed"
        self._failure_count = 0
        self._last_failure_time: Optional[datetime] = None
        self._rate_limit_tokens = config.rate_limit_per_minute
        self._last_token_refresh = datetime.utcnow()
    
    async def initialize(self) -> bool:
        """Initialize HTTP session and resources"""
        try:
            # AI_TODO: Configure HTTP session with proper settings
            timeout = aiohttp.ClientTimeout(total=self.config.timeout_seconds)
            self._session = aiohttp.ClientSession(timeout=timeout)
            
            logger.info(f"{class_name} initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize {class_name}: {{e}}")
            return False
    
    async def call_external_service(self, endpoint: str, data: Dict[str, Any]) -> {class_name}Result:
        """
        Call external service with fault tolerance
        """
        try:
            # Check circuit breaker
            if not self._is_circuit_closed():
                raise CircuitBreakerOpenError("Circuit breaker is open")
            
            # Check rate limiting
            if not self._check_rate_limit():
                raise RateLimitExceeded("Rate limit exceeded")
            
            # AI_IMPLEMENTATION_REQUIRED: Implement API call with retry logic
            result = await self._make_api_call_with_retry(endpoint, data)
            
            # Reset circuit breaker on success
            self._reset_circuit_breaker()
            
            return {class_name}Result(
                success=True,
                data=result,
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            # Handle circuit breaker
            self._record_failure()
            
            logger.error(f"External service call failed: {{e}}")
            return {class_name}Result(
                success=False,
                error=str(e),
                data=None
            )
    
    async def _make_api_call_with_retry(self, endpoint: str, data: Dict[str, Any], 
                                       max_retries: int = 3) -> Dict[str, Any]:
        """Make API call with exponential backoff retry"""
        
        for attempt in range(max_retries + 1):
            try:
                # AI_TODO: Implement actual API call
                async with self._session.post(
                    f"{{self.config.base_url}}/{{endpoint}}",
                    json=data,
                    headers={{"Authorization": f"Bearer {{self.config.api_key}}"}}
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        response.raise_for_status()
                        
            except Exception as e:
                if attempt == max_retries:
                    raise e
                
                # Exponential backoff
                wait_time = 2 ** attempt
                logger.warning(f"Retry {{attempt + 1}}/{{max_retries}} after {{wait_time}}s: {{e}}")
                await asyncio.sleep(wait_time)
        
        raise Exception("Max retries exceeded")
    
    def _is_circuit_closed(self) -> bool:
        """Check if circuit breaker allows requests"""
        if self._circuit_breaker_state == "closed":
            return True
        
        # Check if we should attempt to close the circuit
        if (self._last_failure_time and 
            datetime.utcnow() - self._last_failure_time > timedelta(minutes=5)):
            self._circuit_breaker_state = "half-open"
            return True
        
        return False
    
    def _check_rate_limit(self) -> bool:
        """Check and update rate limiting tokens"""
        now = datetime.utcnow()
        
        # Refresh tokens every minute
        if now - self._last_token_refresh >= timedelta(minutes=1):
            self._rate_limit_tokens = self.config.rate_limit_per_minute
            self._last_token_refresh = now
        
        if self._rate_limit_tokens > 0:
            self._rate_limit_tokens -= 1
            return True
        
        return False
    
    def _record_failure(self) -> None:
        """Record failure for circuit breaker"""
        self._failure_count += 1
        self._last_failure_time = datetime.utcnow()
        
        # Open circuit breaker after threshold failures
        if self._failure_count >= 5:
            self._circuit_breaker_state = "open"
            logger.warning("Circuit breaker opened due to failures")
    
    def _reset_circuit_breaker(self) -> None:
        """Reset circuit breaker on successful call"""
        self._failure_count = 0
        self._circuit_breaker_state = "closed"
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check including circuit breaker status"""
        return {{
            "status": "healthy",
            "circuit_breaker": self._circuit_breaker_state,
            "failure_count": self._failure_count,
            "rate_limit_tokens": self._rate_limit_tokens,
            "timestamp": datetime.utcnow().isoformat()
        }}
    
    async def cleanup(self) -> None:
        """Cleanup HTTP session and resources"""
        if self._session:
            await self._session.close()
        logger.info(f"{class_name} cleaned up successfully")
'''
    
    def _generate_supporting_module(self, context: Dict[str, Any]) -> str:
        """Generate SUPPORTING workflow module"""
        
        class_name = context['class_name']
        
        return f'''"""
{class_name} - Supporting Workflow Module

Orchestrates workflows and coordinates between different modules.
Handles task scheduling, workflow state management, and coordination.
"""

import asyncio
import logging
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime
from enum import Enum
from .types import {class_name}Config, {class_name}Result, WorkflowState
from .interface import {class_name}Interface


logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running" 
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class {class_name}({class_name}Interface):
    """
    Supporting module for workflow orchestration and coordination
    """
    
    def __init__(self, config: {class_name}Config):
        self.config = config
        self._workflows: Dict[str, WorkflowState] = {{}}
        self._task_handlers: Dict[str, Callable] = {{}}
        self._running_tasks: Dict[str, asyncio.Task] = {{}}
    
    async def initialize(self) -> bool:
        """Initialize workflow engine"""
        try:
            # AI_TODO: Initialize workflow engine components
            # - Set up task queue
            # - Initialize state storage
            # - Register default task handlers
            # - Start background processors
            
            await self._register_default_handlers()
            logger.info(f"{class_name} initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize {class_name}: {{e}}")
            return False
    
    async def start_workflow(self, workflow_id: str, workflow_definition: Dict[str, Any]) -> {class_name}Result:
        """
        Start a new workflow execution
        
        Args:
            workflow_id: Unique identifier for the workflow
            workflow_definition: Definition of tasks and dependencies
            
        Returns:
            {class_name}Result: Workflow start result
        """
        try:
            # AI_IMPLEMENTATION_REQUIRED: Implement workflow startup logic
            
            # Validate workflow definition
            if not self._validate_workflow_definition(workflow_definition):
                return {class_name}Result(
                    success=False,
                    error="Invalid workflow definition",
                    data=None
                )
            
            # Create workflow state
            workflow_state = WorkflowState(
                id=workflow_id,
                definition=workflow_definition,
                status=TaskStatus.PENDING,
                created_at=datetime.utcnow(),
                tasks={{}}
            )
            
            self._workflows[workflow_id] = workflow_state
            
            # Start workflow execution
            task = asyncio.create_task(self._execute_workflow(workflow_id))
            self._running_tasks[workflow_id] = task
            
            return {class_name}Result(
                success=True,
                data={{"workflow_id": workflow_id, "status": "started"}},
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Failed to start workflow {{workflow_id}}: {{e}}")
            return {class_name}Result(
                success=False,
                error=str(e),
                data=None
            )
    
    async def _execute_workflow(self, workflow_id: str) -> None:
        """Execute workflow tasks according to definition"""
        workflow = self._workflows[workflow_id]
        workflow.status = TaskStatus.RUNNING
        
        try:
            # AI_TODO: Implement workflow execution logic
            # 1. Parse task dependencies
            # 2. Execute tasks in correct order
            # 3. Handle task failures and retries
            # 4. Update workflow state
            # 5. Handle completion or failure
            
            tasks_definition = workflow.definition.get("tasks", [])
            
            for task_def in tasks_definition:
                task_id = task_def["id"]
                task_type = task_def["type"]
                task_config = task_def.get("config", {{}})
                
                # Execute task
                result = await self._execute_task(task_id, task_type, task_config)
                workflow.tasks[task_id] = result
                
                if not result.success:
                    workflow.status = TaskStatus.FAILED
                    logger.error(f"Task {{task_id}} failed in workflow {{workflow_id}}")
                    return
            
            workflow.status = TaskStatus.COMPLETED
            workflow.completed_at = datetime.utcnow()
            logger.info(f"Workflow {{workflow_id}} completed successfully")
            
        except Exception as e:
            workflow.status = TaskStatus.FAILED
            workflow.error = str(e)
            logger.error(f"Workflow {{workflow_id}} execution failed: {{e}}")
        
        finally:
            # Cleanup running task reference
            if workflow_id in self._running_tasks:
                del self._running_tasks[workflow_id]
    
    async def _execute_task(self, task_id: str, task_type: str, config: Dict[str, Any]) -> {class_name}Result:
        """Execute individual task"""
        try:
            # AI_TODO: Implement task execution based on type
            handler = self._task_handlers.get(task_type)
            
            if not handler:
                raise ValueError(f"No handler found for task type: {{task_type}}")
            
            result = await handler(task_id, config)
            
            logger.info(f"Task {{task_id}} of type {{task_type}} completed")
            return result
            
        except Exception as e:
            logger.error(f"Task {{task_id}} execution failed: {{e}}")
            return {class_name}Result(
                success=False,
                error=str(e),
                data=None
            )
    
    def register_task_handler(self, task_type: str, handler: Callable) -> None:
        """Register a handler for a specific task type"""
        self._task_handlers[task_type] = handler
        logger.info(f"Registered handler for task type: {{task_type}}")
    
    async def _register_default_handlers(self) -> None:
        """Register default task handlers"""
        # AI_TODO: Register handlers for common task types
        
        async def default_handler(task_id: str, config: Dict[str, Any]) -> {class_name}Result:
            # Default implementation
            await asyncio.sleep(0.1)  # Simulate work
            return {class_name}Result(
                success=True,
                data={{"task_id": task_id, "processed": True}},
                timestamp=datetime.utcnow()
            )
        
        self.register_task_handler("default", default_handler)
    
    def _validate_workflow_definition(self, definition: Dict[str, Any]) -> bool:
        """Validate workflow definition structure"""
        # AI_TODO: Implement comprehensive validation
        required_fields = ["tasks"]
        return all(field in definition for field in required_fields)
    
    async def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a workflow"""
        workflow = self._workflows.get(workflow_id)
        if not workflow:
            return None
        
        return {{
            "id": workflow.id,
            "status": workflow.status.value,
            "created_at": workflow.created_at.isoformat(),
            "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None,
            "tasks": {{task_id: task.success for task_id, task in workflow.tasks.items()}},
            "error": workflow.error
        }}
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check with workflow statistics"""
        active_workflows = len([w for w in self._workflows.values() if w.status == TaskStatus.RUNNING])
        
        return {{
            "status": "healthy",
            "active_workflows": active_workflows,
            "total_workflows": len(self._workflows),
            "registered_handlers": len(self._task_handlers),
            "timestamp": datetime.utcnow().isoformat()
        }}
    
    async def cleanup(self) -> None:
        """Cleanup workflows and cancel running tasks"""
        # Cancel all running tasks
        for task in self._running_tasks.values():
            task.cancel()
        
        await asyncio.gather(*self._running_tasks.values(), return_exceptions=True)
        
        self._running_tasks.clear()
        logger.info(f"{class_name} cleaned up successfully")
'''
    
    def _generate_technical_module(self, context: Dict[str, Any]) -> str:
        """Generate TECHNICAL infrastructure module"""
        
        class_name = context['class_name']
        
        return f'''"""
{class_name} - Technical Infrastructure Module

Provides technical infrastructure services like caching, logging,
monitoring, and other cross-cutting concerns.
"""

import logging
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import json
from .types import {class_name}Config, {class_name}Result
from .interface import {class_name}Interface


logger = logging.getLogger(__name__)


class {class_name}({class_name}Interface):
    """
    Technical infrastructure module for cross-cutting concerns
    """
    
    def __init__(self, config: {class_name}Config):
        self.config = config
        self._cache: Dict[str, Any] = {{}}
        self._metrics: Dict[str, List[float]] = {{}}
        self._health_status = "unknown"
    
    async def initialize(self) -> bool:
        """Initialize technical infrastructure"""
        try:
            # AI_TODO: Initialize infrastructure components
            # - Set up caching backend (Redis, in-memory, etc.)
            # - Initialize monitoring and metrics collection
            # - Configure logging systems
            # - Set up health monitoring
            
            await self._initialize_cache()
            await self._initialize_metrics()
            
            self._health_status = "healthy"
            logger.info(f"{class_name} initialized successfully")
            return True
            
        except Exception as e:
            self._health_status = "unhealthy"
            logger.error(f"Failed to initialize {class_name}: {{e}}")
            return False
    
    async def cache_get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            # AI_IMPLEMENTATION_REQUIRED: Implement caching logic
            cache_entry = self._cache.get(key)
            
            if cache_entry is None:
                logger.debug(f"Cache miss for key: {{key}}")
                return None
            
            # Check expiration
            if "expires_at" in cache_entry:
                if datetime.utcnow() > cache_entry["expires_at"]:
                    del self._cache[key]
                    logger.debug(f"Cache expired for key: {{key}}")
                    return None
            
            logger.debug(f"Cache hit for key: {{key}}")
            return cache_entry["value"]
            
        except Exception as e:
            logger.error(f"Cache get failed for key {{key}}: {{e}}")
            return None
    
    async def cache_set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL"""
        try:
            cache_entry = {{"value": value}}
            
            if ttl_seconds:
                cache_entry["expires_at"] = datetime.utcnow() + timedelta(seconds=ttl_seconds)
            
            self._cache[key] = cache_entry
            logger.debug(f"Cache set for key: {{key}}")
            return True
            
        except Exception as e:
            logger.error(f"Cache set failed for key {{key}}: {{e}}")
            return False
    
    async def cache_delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            if key in self._cache:
                del self._cache[key]
                logger.debug(f"Cache deleted for key: {{key}}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Cache delete failed for key {{key}}: {{e}}")
            return False
    
    async def record_metric(self, metric_name: str, value: float) -> None:
        """Record a metric value"""
        try:
            if metric_name not in self._metrics:
                self._metrics[metric_name] = []
            
            self._metrics[metric_name].append(value)
            
            # Keep only last 1000 values to prevent memory growth
            if len(self._metrics[metric_name]) > 1000:
                self._metrics[metric_name] = self._metrics[metric_name][-1000:]
            
            logger.debug(f"Metric recorded: {{metric_name}} = {{value}}")
            
        except Exception as e:
            logger.error(f"Failed to record metric {{metric_name}}: {{e}}")
    
    async def get_metrics(self, metric_name: Optional[str] = None) -> Dict[str, Any]:
        """Get metric statistics"""
        try:
            if metric_name:
                values = self._metrics.get(metric_name, [])
                if not values:
                    return {{}}
                
                return {{
                    "count": len(values),
                    "average": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "recent": values[-10:]  # Last 10 values
                }}
            else:
                # Return summary for all metrics
                summary = {{}}
                for name, values in self._metrics.items():
                    if values:
                        summary[name] = {{
                            "count": len(values),
                            "average": sum(values) / len(values),
                            "min": min(values),
                            "max": max(values)
                        }}
                return summary
                
        except Exception as e:
            logger.error(f"Failed to get metrics: {{e}}")
            return {{}}
    
    async def log_structured(self, level: str, message: str, **kwargs) -> None:
        """Log structured data for better observability"""
        try:
            # AI_TODO: Implement structured logging
            log_entry = {{
                "timestamp": datetime.utcnow().isoformat(),
                "level": level.upper(),
                "message": message,
                "module": "{class_name}",
                **kwargs
            }}
            
            # For now, just use standard logger
            log_func = getattr(logger, level.lower(), logger.info)
            log_func(json.dumps(log_entry))
            
        except Exception as e:
            logger.error(f"Structured logging failed: {{e}}")
    
    async def _initialize_cache(self) -> None:
        """Initialize caching backend"""
        # AI_TODO: Initialize proper caching backend
        # - Redis for distributed caching
        # - In-memory for single instance
        # - Implement cache eviction policies
        
        logger.info("Cache initialized (in-memory)")
    
    async def _initialize_metrics(self) -> None:
        """Initialize metrics collection"""
        # AI_TODO: Initialize metrics backend
        # - Prometheus integration
        # - Custom metrics storage
        # - Implement metric aggregation
        
        logger.info("Metrics collection initialized")
    
    async def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        cache_health = "healthy" if self._cache is not None else "unhealthy"
        metrics_health = "healthy" if self._metrics is not None else "unhealthy"
        
        return {{
            "status": self._health_status,
            "cache_status": cache_health,
            "metrics_status": metrics_health,
            "cache_size": len(self._cache),
            "metrics_count": len(self._metrics),
            "timestamp": datetime.utcnow().isoformat()
        }}
    
    async def cleanup(self) -> None:
        """Cleanup technical infrastructure"""
        # AI_TODO: Implement proper cleanup
        # - Close cache connections
        # - Flush metrics to storage
        # - Cleanup temporary resources
        
        self._cache.clear()
        self._metrics.clear()
        self._health_status = "stopped"
        logger.info(f"{class_name} cleaned up successfully")
'''
    
    def generate_interface_file(self, module_type: str, context: Dict[str, Any]) -> str:
        """Generate interface/contract file"""
        
        class_name = context['class_name']
        
        return f'''"""
Interface definition for {class_name}

This file defines the contract that the {class_name} implementation must follow.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from .types import {class_name}Config, {class_name}Result


class {class_name}Interface(ABC):
    """
    Abstract interface for {class_name}
    
    This interface defines the contract that all implementations must follow.
    It ensures consistency and enables easy testing and mocking.
    """
    
    @abstractmethod
    async def initialize(self) -> bool:
        """
        Initialize the module with necessary resources
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check and return status information
        
        Returns:
            Dict[str, Any]: Health status information
        """
        pass
    
    @abstractmethod
    async def cleanup(self) -> None:
        """
        Cleanup resources on shutdown
        """
        pass


# AI_TODO: Add module-specific interface methods
# Define additional abstract methods that are specific to this module's functionality
# This should include the main business operations that external consumers will use
'''
    
    def generate_types_file(self, context: Dict[str, Any]) -> str:
        """Generate types and data models file"""
        
        class_name = context['class_name']
        
        return f'''"""
Type definitions for {class_name}

This file contains all data models, configurations, and type definitions
used by the {class_name} module.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


@dataclass
class {class_name}Config:
    """Configuration for {class_name}"""
    
    # AI_TODO: Define configuration parameters specific to this module
    # Common configuration options:
    
    # Basic settings
    enabled: bool = True
    debug_mode: bool = False
    log_level: str = "INFO"
    
    # Timeouts and limits
    timeout_seconds: int = 30
    max_retries: int = 3
    rate_limit_per_minute: int = 100
    
    # External service configuration (if applicable)
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    
    # Module-specific configuration
    # Add fields specific to your module's needs
    
    def validate(self) -> bool:
        """Validate configuration parameters"""
        # AI_TODO: Implement validation logic
        if self.timeout_seconds <= 0:
            return False
        if self.max_retries < 0:
            return False
        if self.rate_limit_per_minute <= 0:
            return False
        
        return True


@dataclass 
class {class_name}Result:
    """Result object for {class_name} operations"""
    
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
    
    @property
    def is_success(self) -> bool:
        """Check if operation was successful"""
        return self.success
    
    @property
    def has_error(self) -> bool:
        """Check if operation has error"""
        return self.error is not None


# AI_TODO: Add module-specific data models
# Define additional data classes, enums, and types that are specific to your module

class OperationStatus(Enum):
    """Status enumeration for operations"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress" 
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class WorkflowState:
    """State object for workflow operations (if applicable)"""
    id: str
    definition: Dict[str, Any]
    status: OperationStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    tasks: Dict[str, Any] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.tasks is None:
            self.tasks = {{}}


# Type aliases for common patterns
ConfigDict = Dict[str, Any]
ResultDict = Dict[str, Any]
MetricsDict = Dict[str, List[float]]
'''
    
    def generate_test_file(self, module_type: str, context: Dict[str, Any]) -> str:
        """Generate test file"""
        
        class_name = context['class_name']
        module_name = context['module_name'].replace('-', '_')
        
        return f'''"""
Unit tests for {class_name}

This file contains comprehensive unit tests for the {class_name} module.
Tests cover both happy paths and error scenarios.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
from {module_name}.core import {class_name}
from {module_name}.types import {class_name}Config, {class_name}Result


class Test{class_name}:
    """Test suite for {class_name}"""
    
    @pytest.fixture
    def config(self) -> {class_name}Config:
        """Create test configuration"""
        return {class_name}Config(
            enabled=True,
            debug_mode=True,
            timeout_seconds=10,
            max_retries=2
        )
    
    @pytest.fixture
    async def module_instance(self, config: {class_name}Config) -> {class_name}:
        """Create and initialize module instance for testing"""
        instance = {class_name}(config)
        await instance.initialize()
        yield instance
        await instance.cleanup()
    
    @pytest.mark.asyncio
    async def test_initialization_success(self, config: {class_name}Config):
        """Test successful module initialization"""
        # Arrange
        module = {class_name}(config)
        
        # Act
        result = await module.initialize()
        
        # Assert
        assert result is True
        
        # Cleanup
        await module.cleanup()
    
    @pytest.mark.asyncio
    async def test_health_check(self, module_instance: {class_name}):
        """Test health check functionality"""
        # Act
        health = await module_instance.health_check()
        
        # Assert
        assert isinstance(health, dict)
        assert "status" in health
        assert "timestamp" in health
    
    @pytest.mark.asyncio
    async def test_config_validation(self):
        """Test configuration validation"""
        # Test valid config
        valid_config = {class_name}Config(timeout_seconds=30)
        assert valid_config.validate() is True
        
        # Test invalid config
        invalid_config = {class_name}Config(timeout_seconds=-1)
        assert invalid_config.validate() is False
    
    # AI_TODO: Add module-specific test methods
    # Test the main business operations of your module
    # Include both success and failure scenarios
    
    @pytest.mark.asyncio
    async def test_main_operation_success(self, module_instance: {class_name}):
        """Test main operation success scenario"""
        # Arrange
        test_data = {{"key": "value", "timestamp": datetime.utcnow().isoformat()}}
        
        # Act
        # Replace 'process' with your module's main method
        # result = await module_instance.process(test_data)
        
        # Assert  
        # assert result.success is True
        # assert result.data is not None
        
        # For now, just test that the module is initialized
        health = await module_instance.health_check()
        assert health["status"] in ["healthy", "initialized"]
    
    @pytest.mark.asyncio
    async def test_error_handling(self, module_instance: {class_name}):
        """Test error handling scenarios"""
        # AI_TODO: Implement error scenario tests
        # Test what happens when:
        # - Invalid input is provided
        # - External dependencies fail
        # - Network timeouts occur
        # - Configuration is invalid
        
        # For now, test that module handles its own health check
        health = await module_instance.health_check()
        assert isinstance(health, dict)
    
    @pytest.mark.asyncio
    async def test_cleanup(self, config: {class_name}Config):
        """Test proper resource cleanup"""
        # Arrange
        module = {class_name}(config)
        await module.initialize()
        
        # Act
        await module.cleanup()
        
        # Assert - verify cleanup was successful
        # This could include checking that connections are closed,
        # resources are freed, etc.
        health = await module.health_check()
        # Some modules might return different status after cleanup
        assert isinstance(health, dict)


# Integration test class
class Test{class_name}Integration:
    """Integration tests for {class_name}"""
    
    @pytest.mark.asyncio
    async def test_full_workflow(self):
        """Test complete workflow from initialization to cleanup"""
        # AI_TODO: Implement integration tests
        # Test realistic scenarios that involve:
        # - Multiple operations in sequence
        # - Interaction with external dependencies
        # - Error recovery scenarios
        # - Performance under load
        
        config = {class_name}Config()
        module = {class_name}(config)
        
        try:
            # Initialize
            init_result = await module.initialize()
            assert init_result is True
            
            # Perform operations
            health = await module.health_check()
            assert health["status"] in ["healthy", "initialized"]
            
            # Test multiple operations
            for i in range(3):
                health = await module.health_check()
                assert isinstance(health, dict)
        
        finally:
            # Always cleanup
            await module.cleanup()


# Performance test class  
class Test{class_name}Performance:
    """Performance tests for {class_name}"""
    
    @pytest.mark.asyncio
    async def test_concurrent_operations(self):
        """Test module performance under concurrent load"""
        # AI_TODO: Implement performance tests
        config = {class_name}Config()
        module = {class_name}(config)
        
        try:
            await module.initialize()
            
            # Test concurrent health checks
            tasks = [module.health_check() for _ in range(10)]
            results = await asyncio.gather(*tasks)
            
            # All should succeed
            assert len(results) == 10
            for result in results:
                assert isinstance(result, dict)
        
        finally:
            await module.cleanup()
    
    @pytest.mark.asyncio  
    async def test_memory_usage(self):
        """Test that module doesn't leak memory"""
        # AI_TODO: Implement memory usage tests
        # This could involve:
        # - Running many operations
        # - Monitoring memory usage
        # - Ensuring cleanup releases resources
        
        config = {class_name}Config()
        module = {class_name}(config)
        
        try:
            await module.initialize()
            
            # Perform multiple operations
            for _ in range(100):
                await module.health_check()
        
        finally:
            await module.cleanup()
'''
    
    def generate_contract_tests(self, context: Dict[str, Any]) -> str:
        """Generate contract/compliance tests"""
        
        class_name = context['class_name']
        module_name = context['module_name'].replace('-', '_')
        
        return f'''"""
Contract tests for {class_name}

These tests verify that the module implementation complies with
the defined interface and follows the framework standards.
"""

import pytest
import asyncio
import inspect
from typing import get_type_hints
from {module_name}.core import {class_name}
from {module_name}.interface import {class_name}Interface
from {module_name}.types import {class_name}Config, {class_name}Result


class Test{class_name}Compliance:
    """Test compliance with framework standards"""
    
    def test_implements_interface(self):
        """Verify that module implements the required interface"""
        # Check that class inherits from interface
        assert issubclass({class_name}, {class_name}Interface)
        
        # Check that all abstract methods are implemented
        interface_methods = {{
            name for name, method in inspect.getmembers({class_name}Interface)
            if inspect.isabstract(method)
        }}
        
        implemented_methods = {{
            name for name, method in inspect.getmembers({class_name})
            if inspect.ismethod(method) or inspect.isfunction(method)
        }}
        
        missing_methods = interface_methods - implemented_methods
        assert not missing_methods, f"Missing interface methods: {{missing_methods}}"
    
    def test_required_methods_exist(self):
        """Verify that required framework methods exist"""
        required_methods = ['initialize', 'health_check', 'cleanup']
        
        for method_name in required_methods:
            assert hasattr({class_name}, method_name), f"Missing required method: {{method_name}}"
            method = getattr({class_name}, method_name)
            assert callable(method), f"{{method_name}} is not callable"
    
    def test_method_signatures(self):
        """Verify method signatures match interface"""
        # Test initialize method
        init_method = getattr({class_name}, 'initialize')
        init_sig = inspect.signature(init_method)
        
        # Should be async and return bool
        assert asyncio.iscoroutinefunction(init_method), "initialize must be async"
        
        # Test health_check method
        health_method = getattr({class_name}, 'health_check')
        assert asyncio.iscoroutinefunction(health_method), "health_check must be async"
        
        # Test cleanup method
        cleanup_method = getattr({class_name}, 'cleanup')
        assert asyncio.iscoroutinefunction(cleanup_method), "cleanup must be async"
    
    def test_config_type_compliance(self):
        """Verify configuration type compliance"""
        # Check that Config class exists and has required attributes
        assert hasattr({class_name}Config, 'validate'), "Config must have validate method"
        
        # Check that config has standard fields
        config = {class_name}Config()
        standard_fields = ['enabled', 'debug_mode', 'log_level', 'timeout_seconds']
        
        for field in standard_fields:
            assert hasattr(config, field), f"Config missing standard field: {{field}}"
    
    def test_result_type_compliance(self):
        """Verify result type compliance"""
        # Check that Result class has required attributes
        result = {class_name}Result(success=True)
        
        required_fields = ['success', 'data', 'error', 'timestamp']
        for field in required_fields:
            assert hasattr(result, field), f"Result missing required field: {{field}}"
        
        # Check properties
        assert hasattr(result, 'is_success'), "Result missing is_success property"
        assert hasattr(result, 'has_error'), "Result missing has_error property"


class Test{class_name}Lifecycle:
    """Test module lifecycle compliance"""
    
    @pytest.mark.asyncio
    async def test_initialization_contract(self):
        """Test that initialization follows the contract"""
        config = {class_name}Config()
        module = {class_name}(config)
        
        # Should not be initialized yet
        # (Module should track its own initialization state)
        
        # Initialize should return bool
        result = await module.initialize()
        assert isinstance(result, bool), "initialize must return bool"
        
        # Cleanup
        await module.cleanup()
    
    @pytest.mark.asyncio
    async def test_health_check_contract(self):
        """Test that health check follows the contract"""
        config = {class_name}Config()
        module = {class_name}(config)
        
        try:
            await module.initialize()
            
            # Health check should return dict
            health = await module.health_check()
            assert isinstance(health, dict), "health_check must return dict"
            
            # Should have required fields
            required_fields = ['status', 'timestamp']
            for field in required_fields:
                assert field in health, f"Health check missing required field: {{field}}"
            
            # Status should be string
            assert isinstance(health['status'], str), "Status must be string"
            
        finally:
            await module.cleanup()
    
    @pytest.mark.asyncio
    async def test_cleanup_contract(self):
        """Test that cleanup follows the contract"""
        config = {class_name}Config()
        module = {class_name}(config)
        
        await module.initialize()
        
        # Cleanup should not raise exceptions
        try:
            await module.cleanup()
        except Exception as e:
            pytest.fail(f"Cleanup should not raise exceptions: {{e}}")
        
        # Should be able to call cleanup multiple times
        await module.cleanup()  # Should not fail
    
    @pytest.mark.asyncio
    async def test_error_handling_contract(self):
        """Test that error handling follows the contract"""
        # Test with invalid config
        invalid_config = {class_name}Config(timeout_seconds=-1)
        
        # Should validate config
        assert not invalid_config.validate(), "Invalid config should fail validation"
        
        # Module should handle invalid config gracefully
        module = {class_name}(invalid_config)
        
        try:
            # May fail initialization, but should not crash
            await module.initialize()
        except Exception:
            # Expected for invalid config
            pass
        finally:
            # Cleanup should always work
            await module.cleanup()


class Test{class_name}Standards:
    """Test compliance with coding standards"""
    
    def test_docstring_compliance(self):
        """Verify that classes and methods have proper docstrings"""
        # Class should have docstring
        assert {class_name}.__doc__ is not None, "Class missing docstring"
        assert len({class_name}.__doc__.strip()) > 10, "Class docstring too short"
        
        # Important methods should have docstrings
        important_methods = ['initialize', 'health_check', 'cleanup']
        
        for method_name in important_methods:
            if hasattr({class_name}, method_name):
                method = getattr({class_name}, method_name)
                assert method.__doc__ is not None, f"Method {{method_name}} missing docstring"
    
    def test_logging_compliance(self):
        """Verify that module uses proper logging"""
        # Module should import logging
        import {module_name}.core as core_module
        
        # Should have logger defined
        assert hasattr(core_module, 'logger'), "Module should define logger"
    
    def test_exception_handling(self):
        """Verify proper exception handling patterns"""
        # This is tested through behavior rather than static analysis
        # The lifecycle tests cover exception handling compliance
        pass


# AI_TODO: Add module-specific contract tests
# Test contracts that are specific to your module's domain
# For example:
# - Data validation contracts
# - Business rule compliance
# - Integration contracts with external services
# - Performance contracts (response times, throughput)
'''
    
    def generate_init_file(self, context: Dict[str, Any]) -> str:
        """Generate __init__.py file"""
        
        class_name = context['class_name']
        module_name = context['module_name'].replace('-', '_')
        
        return f'''"""
{class_name} Module

This module provides {context['module_type'].lower()} functionality for {context['domain']} domain.

Usage:
    from {module_name} import {class_name}, {class_name}Config
    
    config = {class_name}Config()
    module = {class_name}(config)
    await module.initialize()
"""

from .core import {class_name}
from .types import {class_name}Config, {class_name}Result
from .interface import {class_name}Interface

# Version information
__version__ = "1.0.0"
__author__ = "Standardized Modules Framework"

# Public API
__all__ = [
    "{class_name}",
    "{class_name}Config", 
    "{class_name}Result",
    "{class_name}Interface",
    "__version__"
]

# Module metadata
MODULE_TYPE = "{context['module_type']}"
MODULE_DOMAIN = "{context['domain']}"
MODULE_NAME = "{module_name}"
'''
    
    def generate_ai_completion_file(self, module_type: str, context: Dict[str, Any]) -> str:
        """Generate AI completion guidance file"""
        
        class_name = context['class_name']
        module_name = context['module_name']
        
        return f'''# AI Completion Guide for {class_name}

**Module Type**: {module_type}  
**Domain**: {context['domain']}  
**Framework**: Standardized Modules v1.1.0

## 🎯 Module Purpose

This {module_type} module is designed for {context['domain']} domain functionality. Your task is to implement the business logic while the framework provides the structure, testing, and infrastructure.

## 📋 Implementation Checklist

### Core Implementation Tasks

- [ ] **Review the interface** (`interface.py`) - understand the contract
- [ ] **Implement main business logic** in `core.py` (look for `AI_TODO` markers)
- [ ] **Define domain-specific types** in `types.py` (add fields to Config and Result)
- [ ] **Add specific test cases** in `tests/test_core.py`
- [ ] **Update contract tests** in `tests/test_contracts.py` if needed

### Key Areas Requiring Implementation

#### 1. Core Business Logic (Priority: HIGH)

**File**: `core.py`  
**Methods to implement**:

```python
# Main processing method
async def process(self, data: Dict[str, Any]) -> {class_name}Result:
    # Implement the core business functionality
    pass

# Business validation
def _validate_input(self, data: Dict[str, Any]) -> bool:
    # Implement domain-specific validation
    pass

# Main business processing
async def _process_business_logic(self, data: Dict[str, Any]) -> Dict[str, Any]:
    # This is where the main business value is created
    pass
```

#### 2. Configuration Customization (Priority: MEDIUM)

**File**: `types.py`  
**Add module-specific configuration**:

```python
@dataclass
class {class_name}Config:
    # Add your domain-specific configuration fields
    # Examples:
    # database_url: str = "sqlite:///default.db"
    # max_batch_size: int = 100
    # external_api_endpoint: str = ""
    pass
```

#### 3. Domain-Specific Types (Priority: MEDIUM)

**File**: `types.py`  
**Add business entities and value objects**:

```python
# Add data models specific to your domain
# Examples for different domains:

# E-commerce domain:
# @dataclass
# class Product:
#     id: str
#     name: str
#     price: Decimal
#     category: str

# Finance domain:
# @dataclass  
# class Transaction:
#     id: str
#     amount: Decimal
#     currency: str
#     timestamp: datetime
```

#### 4. Test Implementation (Priority: MEDIUM)

**File**: `tests/test_core.py`  
**Add comprehensive test cases**:

```python
# Test the main business operations
@pytest.mark.asyncio
async def test_process_valid_data(self, module_instance):
    # Test successful processing with valid data
    test_data = {{"key": "value"}}  # Use realistic test data
    result = await module_instance.process(test_data)
    assert result.success is True

@pytest.mark.asyncio  
async def test_process_invalid_data(self, module_instance):
    # Test error handling with invalid data
    invalid_data = {{}}  # Use realistic invalid data
    result = await module_instance.process(invalid_data)
    assert result.success is False
```

## 🎨 Module-Specific Implementation Guide

### {module_type} Module Best Practices

{self._get_module_specific_guidance(module_type)}

## 🚀 AI Prompts for Implementation

Use these prompts with Cursor/AI to implement the module:

### Prompt 1: Core Business Logic
```
Implement the core business logic for this {module_type} module in the {context['domain']} domain. 

The module should:
1. Handle {context['domain']}-specific data processing
2. Implement proper validation and error handling  
3. Follow the existing code structure and patterns
4. Add comprehensive logging and monitoring
5. Include proper business rule enforcement

Focus on the methods marked with AI_TODO in core.py. Make the implementation production-ready with proper error handling.
```

### Prompt 2: Domain Types and Configuration
```
Define domain-specific types and configuration for this {context['domain']} module.

Add to types.py:
1. Configuration parameters specific to {context['domain']} operations
2. Business entities and value objects
3. Enums for domain-specific constants
4. Validation methods for business rules

Make sure all types are properly typed with Python type hints and include validation logic.
```

### Prompt 3: Comprehensive Testing  
```
Create comprehensive test cases for this {module_type} module in the {context['domain']} domain.

Add to tests/test_core.py:
1. Happy path tests for all main operations
2. Error scenario tests with invalid data
3. Edge case tests for boundary conditions
4. Integration tests for external dependencies
5. Performance tests for critical operations

Use realistic test data that reflects actual {context['domain']} use cases.
```

### Prompt 4: Error Handling and Resilience
```
Implement robust error handling and resilience patterns for this {module_type} module.

Focus on:
1. Graceful degradation when dependencies fail
2. Proper exception handling with meaningful error messages
3. Retry logic for transient failures
4. Circuit breaker patterns for external services (if applicable)
5. Comprehensive logging for debugging and monitoring

Make the module production-ready with enterprise-grade error handling.
```

## 📝 Implementation Notes

### Framework Integration Points

1. **Health Checks**: The `health_check()` method is automatically called by monitoring systems
2. **Logging**: Use the configured logger for consistent log formatting  
3. **Configuration**: All config should go through the {class_name}Config class
4. **Results**: Always return {class_name}Result objects for consistency
5. **Async/Await**: All I/O operations should be async for better performance

### Testing Strategy

1. **Unit Tests**: Test individual methods with mocked dependencies
2. **Integration Tests**: Test with real dependencies in test environment  
3. **Contract Tests**: Verify compliance with interface (already implemented)
4. **Performance Tests**: Ensure module meets performance requirements

### Deployment Considerations

{self._get_deployment_guidance(context)}

## ✅ Completion Verification

Before considering the module complete:

1. [ ] All `AI_TODO` markers have been addressed
2. [ ] Tests pass with >80% coverage
3. [ ] Module can be imported and initialized successfully
4. [ ] Health check returns valid status
5. [ ] Error scenarios are handled gracefully
6. [ ] Configuration validation works correctly
7. [ ] Documentation is updated with usage examples

## 🔧 Development Commands

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov={module_name} --cov-report=html

# Run specific test file
pytest tests/test_core.py -v

# Run contract/compliance tests
pytest tests/test_contracts.py -v
```

## 📚 Additional Resources

- [Framework Documentation](../docs/guides/SUPPORT_DOCUMENTATION.md)
- [Testing Guide](../docs/guides/TESTING.md)
- [Architecture Overview](../docs/architecture/DEPLOYMENT_GUIDE.md)

---

**Next Steps**: Start with implementing the core business logic, then move to configuration and testing. The framework handles infrastructure, deployment, and monitoring automatically.
'''

    def _get_module_specific_guidance(self, module_type: str) -> str:
        """Get specific guidance based on module type"""
        
        guidance = {
            'CORE': '''
**CORE modules** handle main business logic and should focus on:

1. **Business Rule Enforcement**: Implement domain-specific validation and constraints
2. **Data Processing**: Transform and process business entities
3. **Audit Trails**: Track all business operations for compliance
4. **State Management**: Manage business entity lifecycles
5. **Domain Events**: Publish events for other systems to consume

**Key Patterns**:
- Repository pattern for data access
- Domain services for complex business logic
- Event sourcing for audit trails
- Validation pipelines for data integrity
''',
            'INTEGRATION': '''
**INTEGRATION modules** handle external service communication and should focus on:

1. **Fault Tolerance**: Implement circuit breakers and retry policies
2. **Rate Limiting**: Respect external service limits
3. **Data Transformation**: Convert between internal and external formats  
4. **Authentication**: Handle API keys, OAuth, etc.
5. **Monitoring**: Track external service health and performance

**Key Patterns**:
- Circuit breaker for fault tolerance
- Exponential backoff for retries
- Adapter pattern for service abstraction
- Bulkhead pattern for isolation
''',
            'SUPPORTING': '''
**SUPPORTING modules** orchestrate workflows and should focus on:

1. **Workflow Management**: Coordinate between different services
2. **Task Scheduling**: Handle async and batch operations
3. **State Coordination**: Manage distributed workflow state
4. **Error Recovery**: Handle partial failures and compensation
5. **Process Monitoring**: Track workflow progress and performance

**Key Patterns**:
- Saga pattern for distributed transactions
- State machine for workflow management
- Command pattern for task execution
- Observer pattern for progress tracking
''',
            'TECHNICAL': '''
**TECHNICAL modules** provide infrastructure services and should focus on:

1. **Cross-Cutting Concerns**: Logging, monitoring, caching
2. **Performance Optimization**: Caching, connection pooling
3. **Resource Management**: Memory, connections, file handles
4. **Configuration Management**: Environment-specific settings
5. **Observability**: Metrics, traces, health monitoring

**Key Patterns**:
- Singleton pattern for shared resources
- Factory pattern for resource creation
- Decorator pattern for cross-cutting concerns
- Strategy pattern for different implementations
'''
        }
        
        return guidance.get(module_type, "General module implementation guidance.")
    
    def _get_deployment_guidance(self, context: Dict[str, Any]) -> str:
        """Get deployment guidance based on context"""
        
        if context.get('with_docker'):
            return '''
This module includes containerization support:

1. **Docker**: Multi-stage Dockerfile for production deployment
2. **Kubernetes**: Complete manifests for cluster deployment  
3. **CI/CD**: GitHub Actions for automated testing and deployment
4. **Infrastructure**: Terraform for cloud resource provisioning
5. **Monitoring**: Built-in health checks and metrics endpoints

Deploy with:
```bash
# Local development
docker-compose up

# Production deployment  
./scripts/deploy.sh staging
```
'''
        else:
            return '''
This module uses standard Python deployment:

1. **Virtual Environment**: Use venv or conda for isolation
2. **Dependencies**: Install via requirements.txt
3. **Configuration**: Use environment variables or config files
4. **Process Management**: Use systemd, supervisor, or process managers
5. **Monitoring**: Implement custom health check endpoints

Deploy with:
```bash
pip install -r requirements.txt
python -m {module_name}
```
'''
