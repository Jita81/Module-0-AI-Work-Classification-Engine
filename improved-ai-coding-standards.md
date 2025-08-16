# AI-Collaborative Coding Standards: Context-Optimized Module Development

## Token Budget Management

**TARGET: Complete module under 60k tokens (code + docs + tests)**
- Code: ~30k tokens max
- Documentation: ~15k tokens max  
- Tests: ~15k tokens max

**This Standards Document: ~8k tokens - designed for inclusion in every agent context**

---

## 1. Context-Aware Decision Framework

### Component Classification (Choose One)
```
TECHNICAL: [auth, cache, logging, db, api_client, monitoring]
→ Apply strict patterns, focus on reliability
→ Document: Interface contracts, error handling
→ Test: Contract adherence, performance

DOMAIN: [business_rules, workflows, calculations, models]
→ Apply domain-appropriate patterns
→ Document: Business intent, rules, constraints  
→ Test: Business scenarios, edge cases

INTEGRATION: [external_apis, events, gateways, adapters]
→ Apply fault-tolerant patterns
→ Document: External contracts, failure modes
→ Test: Fault tolerance, contract compliance
```

### Granularity Guidelines
```
TECHNICAL: Small, single-purpose functions (10-25 lines)
DOMAIN: Business-operation-sized functions (group related rules)
INTEGRATION: Resilience-focused structure (separate concerns)
```

---

## 2. Essential Documentation Pattern

### Required Header (All Modules)
```python
"""
{ModuleName}: {one_line_purpose}
Type: TECHNICAL|DOMAIN|INTEGRATION
Intent: {why_this_exists}
Contracts: {inputs} → {outputs} → {side_effects}
Dependencies: {what_this_needs}
"""
```

### Context-Specific Documentation

**TECHNICAL Components:**
```python
def cache_get(key: str) -> Optional[Any]:
    """Get cached value. Returns None if missing/expired."""
```

**DOMAIN Components:**  
```python
def calculate_dynamic_price(product: Product, context: MarketContext) -> Price:
    """
    Apply pricing rules: margin protection → competitor matching → demand adjustment
    Business Rule: Price never below cost + 20% margin (PRICING-001)
    """
```

**INTEGRATION Components:**
```python
def call_payment_api(request: PaymentRequest) -> PaymentResult:
    """
    Process payment via external gateway
    Failures: Retry on timeout, circuit-break on repeated failures
    """
```

---

## 3. Standard Patterns by Type

### Technical Component Template
```python
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class TechnicalInterface(ABC):
    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> Result[Any]: pass

class ConcreteTechnical(TechnicalInterface):
    def __init__(self, config: Config):
        self._config = config
    
    def execute(self, params: Dict[str, Any]) -> Result[Any]:
        try:
            # Implementation
            return Result.success(data)
        except Exception as e:
            return Result.error(f"TECH_ERROR: {e}")
```

### Domain Component Template  
```python
@dataclass
class DomainInput:
    # Domain-specific fields

@dataclass  
class DomainOutput:
    # Business result fields
    audit_trail: List[str]  # Track rule applications

def domain_operation(input: DomainInput) -> DomainOutput:
    """
    Business operation: {describe_what_this_achieves}
    Rules: {list_key_business_rules}
    """
    audit = []
    
    # Apply business rules with audit trail
    result = apply_business_logic(input)
    audit.append(f"Applied rule X: {reason}")
    
    return DomainOutput(result=result, audit_trail=audit)
```

### Integration Component Template
```python
from circuit_breaker import CircuitBreaker
from retry import retry_with_backoff

class ExternalIntegration:
    def __init__(self, config: IntegrationConfig):
        self._client = create_client(config)
        self._circuit_breaker = CircuitBreaker()
    
    @retry_with_backoff(max_attempts=3)
    def call_external_service(self, request: Request) -> Result[Response]:
        """Call external service with fault tolerance"""
        if not self._circuit_breaker.can_execute():
            return Result.error("SERVICE_UNAVAILABLE")
        
        try:
            response = self._client.call(request)
            self._circuit_breaker.record_success()
            return Result.success(response)
        except TimeoutError:
            self._circuit_breaker.record_failure()
            raise  # Retry will handle
        except ValidationError as e:
            return Result.error(f"INVALID_REQUEST: {e}")
```

---

## 4. Error Handling Standard

### Universal Result Pattern
```python
from dataclasses import dataclass
from typing import Optional, Generic, TypeVar
from enum import Enum

T = TypeVar('T')

class ErrorType(Enum):
    VALIDATION = "validation"
    BUSINESS_RULE = "business_rule"  
    INTEGRATION = "integration"
    SYSTEM = "system"

@dataclass
class Result(Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    error_type: Optional[ErrorType] = None
    
    @classmethod
    def success(cls, data: T) -> 'Result[T]':
        return cls(success=True, data=data)
    
    @classmethod  
    def error(cls, message: str, error_type: ErrorType = ErrorType.SYSTEM) -> 'Result[T]':
        return cls(success=False, error=message, error_type=error_type)
```

---

## 5. Testing Strategy by Component Type

### Technical Component Tests
```python
def test_technical_component():
    """Test contract adherence and performance"""
    component = create_component()
    
    # Contract testing
    result = component.execute(valid_input)
    assert result.success
    
    # Error handling
    result = component.execute(invalid_input)
    assert not result.success
    assert result.error_type == ErrorType.VALIDATION
    
    # Performance (if critical)
    with timer() as t:
        component.execute(large_input)
    assert t.elapsed < MAX_RESPONSE_TIME
```

### Domain Component Tests
```python
def test_domain_business_rules():
    """Test business rule correctness"""
    # Happy path business scenario
    input = create_business_scenario("standard_case")
    result = domain_operation(input)
    assert_business_rule_applied(result, "expected_rule")
    
    # Edge cases and constraints
    edge_input = create_business_scenario("edge_case")
    result = domain_operation(edge_input)
    assert_business_constraint_respected(result)
```

### Integration Component Tests
```python
def test_integration_fault_tolerance():
    """Test external service integration"""
    integration = create_integration()
    
    # Happy path
    result = integration.call_external_service(valid_request)
    assert result.success
    
    # Fault tolerance
    with mock_service_timeout():
        result = integration.call_external_service(valid_request)
        # Should retry and eventually fail gracefully
        assert not result.success
        assert result.error_type == ErrorType.INTEGRATION
```

---

## 6. Module Structure Standard

### File Organization (All Types)
```
module_name/
├── __init__.py           # Public interface exports
├── core.py              # Main implementation  
├── types.py             # Data types and contracts
├── tests/
│   ├── test_core.py     # Core functionality tests
│   └── test_integration.py  # Integration tests (if applicable)
└── README.md            # Module documentation
```

### Token-Efficient Implementation Strategy
```python
# __init__.py - Minimal public interface
"""
{ModuleName}: {purpose}
Type: {TECHNICAL|DOMAIN|INTEGRATION}
"""
from .core import primary_function, PrimaryClass
from .types import InputType, OutputType

__all__ = ['primary_function', 'PrimaryClass', 'InputType', 'OutputType']

# core.py - Main implementation (aim for <500 lines)
# types.py - Data contracts (aim for <200 lines)  
# tests/ - Comprehensive but focused tests (aim for <300 lines total)
```

---

## 7. Context Management for AI Agents

### Pre-Generation Checklist
- [ ] Component type identified (TECHNICAL/DOMAIN/INTEGRATION)
- [ ] Token budget allocated (30k code + 15k docs + 15k tests)
- [ ] Dependencies minimized and documented
- [ ] Interface contracts defined

### During Generation
- [ ] Apply appropriate template pattern
- [ ] Include required documentation level only
- [ ] Implement standard error handling
- [ ] Focus on single responsibility per component type

### Post-Generation Validation
- [ ] Token count under 60k total
- [ ] Component type patterns followed
- [ ] Interface contracts clear and minimal
- [ ] Tests cover critical paths only

### Context Optimization Rules
```
INCLUDE: Essential interfaces, business rules, error patterns
EXCLUDE: Implementation details, verbose examples, redundant docs
FOCUS: Decision-making information that applies to this component type
MINIMIZE: Boilerplate, repetitive patterns, unnecessary complexity
```

---

## 8. Orchestrator Module Guidance

### Orchestrator Responsibilities
- Module discovery and initialization
- Interface-based communication between modules
- Error aggregation and system health monitoring
- Configuration management and dependency injection

### Orchestrator Pattern
```python
class ModuleOrchestrator:
    """
    System orchestrator: manages module lifecycle and communication
    Type: TECHNICAL (system coordination)
    """
    
    def __init__(self, config: SystemConfig):
        self._modules: Dict[str, ModuleInterface] = {}
        self._health_monitor = HealthMonitor()
    
    def register_module(self, name: str, module: ModuleInterface):
        """Register module with health monitoring"""
        self._modules[name] = module
        self._health_monitor.add_module(name, module)
    
    def execute_operation(self, module_name: str, operation: str, params: dict) -> Result:
        """Execute operation with error handling and monitoring"""
        if module_name not in self._modules:
            return Result.error(f"Module {module_name} not found", ErrorType.SYSTEM)
        
        try:
            result = self._modules[module_name].execute(operation, params)
            self._health_monitor.record_operation(module_name, result.success)
            return result
        except Exception as e:
            self._health_monitor.record_error(module_name, str(e))
            return Result.error(f"Operation failed: {e}", ErrorType.SYSTEM)
```

---

## 9. Quality Gates

### Code Quality (All Types)
- [ ] Single responsibility clear from module name
- [ ] Error handling follows Result pattern
- [ ] Dependencies explicitly declared
- [ ] Interface contracts documented

### Documentation Quality
- [ ] Purpose clear in header
- [ ] Business rules documented (DOMAIN only)
- [ ] Failure modes documented (INTEGRATION only)
- [ ] Performance notes included (TECHNICAL only)

### Test Quality  
- [ ] Critical paths covered
- [ ] Component-type-appropriate test focus
- [ ] Error conditions tested
- [ ] Integration points mocked appropriately

### Token Efficiency
- [ ] Total module under 60k tokens
- [ ] Documentation concise but complete
- [ ] Code focused on essential functionality
- [ ] Tests targeted on critical behaviors

---

This framework optimizes for token efficiency while maintaining the essential guidance for quality module development. Every section provides actionable guidance that applies to module creation decisions.