# AI Completion Guide: payment-gateway (INTEGRATION Module)

## 🎯 Your Task
Complete the external service integration for this payments integration module.
The framework provides fault tolerance, circuit breakers, retries, and rate limiting - you only need to fill in the service-specific parts.

## 📋 What You Need to Complete

### 1. External Service Configuration (HIGH PRIORITY)
**File: `core.py` - Update module docstring**
```python
"""
payment-gateway: [YOUR INTEGRATION PURPOSE HERE]
Type: INTEGRATION
Intent: [WHAT EXTERNAL SERVICE AND WHY]
External Service: [SERVICE NAME AND PURPOSE]
Fault Tolerance: [YOUR REQUIREMENTS]
"""
```

**Document:**
- What external service this integrates with
- API documentation URL and version
- Authentication method required
- Rate limits and SLA information
- Expected error codes and recovery strategies

### 2. Service Integration Implementation (HIGH PRIORITY)
**File: `core.py` - Complete these methods:**

#### `_build_request_url()` method:
```python
def _build_request_url(self, request: PaymentGatewayRequest) -> str:
    # Build the complete URL for the external service
    endpoint = "your_endpoint_here"  # Based on request type
    return f"{self.config.base_url}/api/{endpoint}"
```

#### `_build_request_headers()` method:
```python
def _build_request_headers(self, request: PaymentGatewayRequest) -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {self.config.api_key}",
        # Add other required headers
    }
```

#### `_build_request_payload()` method:
```python
def _build_request_payload(self, request: PaymentGatewayRequest) -> Dict[str, Any]:
    # Transform internal request to external service format
    return {
        "external_field": request.internal_field,
        # Map all required fields
    }
```

#### `_transform_response()` method:
```python
def _transform_response(self, response_data: Dict[str, Any]) -> PaymentGatewayResponse:
    # Transform external response to internal format
    return PaymentGatewayResponse(
        internal_field=response_data.get("external_field"),
        # Map all response fields
    )
```

### 3. Data Types (MEDIUM PRIORITY)
**File: `types.py` - Define your service-specific types:**

```python
@dataclass
class PaymentGatewayRequest:
    # Define request fields for your external service
    pass

@dataclass  
class PaymentGatewayResponse:
    # Define response fields from external service
    pass

@dataclass
class PaymentGatewayConfig:
    base_url: str
    api_key: str
    timeout_seconds: int = 30
    circuit_breaker_config: Dict = None
    retry_config: Dict = None
    rate_limit_config: Dict = None
```

### 4. Error Handling (MEDIUM PRIORITY)
**Review and customize error handling in `call_external_service()` for your service's specific error codes**

## 🚀 Getting Started

1. **Document the external service**: Update module docstring with service details
2. **Define request/response types**: What data does the service expect/return?
3. **Implement URL building**: How to construct the service endpoints?
4. **Add authentication**: How does the service authenticate requests?
5. **Transform data**: Map between internal and external formats
6. **Test error scenarios**: Verify fault tolerance works correctly

## 💡 Framework Features Already Available

✅ **Complete fault tolerance** - Circuit breaker, retry, rate limiting
✅ **HTTP client management** - aiohttp session with proper timeouts
✅ **Health monitoring** - Built-in health checks and status reporting
✅ **Error categorization** - Proper error types for different scenarios
✅ **Async support** - Full async/await integration
✅ **Logging integration** - Structured logging throughout
✅ **Configuration management** - Handles service configuration

## 🎯 Quality Checklist

Before completing, ensure:
- [ ] External service details clearly documented
- [ ] All request/response mappings implemented
- [ ] Authentication properly configured
- [ ] Error scenarios tested and handled appropriately
- [ ] Rate limiting configured for service requirements
- [ ] Health checks verify service availability

This scaffolding handles all the complex fault tolerance - focus on the service integration!
