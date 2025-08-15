# AI Completion Guide: user-management (CORE Domain Module)

## 🎯 Your Task
Complete the business logic implementation for this ecommerce domain module.
The framework structure is already provided - you only need to fill in the business-specific parts.

## 📋 What You Need to Complete

### 1. Business Context (HIGH PRIORITY)
**File: `core.py` - Update module docstring**
```python
"""
user-management: [YOUR BUSINESS PURPOSE HERE]
Type: CORE
Intent: [WHY THIS MODULE EXISTS IN BUSINESS TERMS]
Contracts: [INPUTS] → [OUTPUTS] → [SIDE EFFECTS]
Dependencies: [LIST REQUIRED MODULES]
"""
```

**What to document:**
- What business problem this solves
- Key business concepts and entities
- Important business rules and constraints
- How it fits into the overall ecommerce domain

### 2. Business Rules Implementation (HIGH PRIORITY)
**File: `core.py` - Complete these methods:**

#### `_initialize_business_rules()` method:
```python
def _initialize_business_rules(self) -> List[BusinessRule]:
    # Define your business rules here
    return [
        BusinessRule(
            name="your_rule_name",
            description="what this rule enforces",
            validation_function=self._validate_your_rule
        ),
        # Add more rules...
    ]
```

#### `execute_primary_operation()` method:
Replace the `# AI_IMPLEMENTATION_REQUIRED` section with:
1. Input validation according to your business rules
2. Business calculations and logic
3. Domain entity updates
4. Constraint enforcement
5. Result generation

#### `_validate_business_input()` method:
```python
def _validate_business_input(self, input_data: UserManagementInput) -> OperationResult:
    # Implement your validation logic:
    # - Check required fields
    # - Validate business constraints
    # - Ensure data integrity
    # - Apply domain-specific rules
    pass
```

### 3. Data Types (MEDIUM PRIORITY)
**File: `types.py` - Define your domain-specific types:**

```python
@dataclass
class UserManagementInput:
    # Define input fields for your domain
    pass

@dataclass  
class UserManagementOutput:
    # Define output fields for your domain
    pass

@dataclass
class DomainEntity:
    # Define your main business entity
    pass
```

### 4. Tests (MEDIUM PRIORITY)
**File: `tests/test_core.py` - Add business scenario tests:**

```python
def test_main_business_scenario(self):
    """Test the primary business use case"""
    # Given: business scenario setup
    # When: execute operation
    # Then: verify business rules applied correctly

def test_business_rule_validation(self):
    """Test business rule enforcement"""
    # Test that invalid business inputs are rejected

def test_edge_cases(self):
    """Test business edge cases and boundary conditions"""
    # Test unusual but valid business scenarios
```

## 🚀 Getting Started

1. **Start with business context**: Update the module docstring with clear business purpose
2. **Define your data types**: What inputs/outputs does this module handle?
3. **Implement core business logic**: Fill in the `execute_primary_operation` method
4. **Add validation**: Implement `_validate_business_input` with your rules
5. **Test thoroughly**: Add tests that verify business scenarios work correctly

## 💡 Framework Features Already Available

✅ **Complete error handling** - Uses OperationResult pattern
✅ **Audit trail system** - Automatically tracks all operations  
✅ **Logging integration** - Structured logging throughout
✅ **Health monitoring** - Built-in health status reporting
✅ **Configuration management** - Handles module configuration
✅ **Interface compliance** - Implements standardized interface
✅ **Test scaffolding** - Test structure ready for your tests

## 🎯 Quality Checklist

Before completing, ensure:
- [ ] Business purpose clearly documented
- [ ] All business rules explicitly implemented and tested
- [ ] Input validation covers all business constraints  
- [ ] Main business scenarios have test coverage
- [ ] Error conditions properly handled
- [ ] Domain terminology used consistently
- [ ] Business logic separated from technical concerns

## 🔧 Token Budget Optimization

This scaffolding used ~15k tokens, leaving you ~45k for:
- Business logic implementation (~20k tokens)
- Documentation completion (~10k tokens)  
- Test implementation (~15k tokens)

Focus on business value - the technical infrastructure is handled!

## 📞 Need Help?

- Check `interface.py` for the complete contract you need to implement
- Review `types.py` for the data structures you're working with
- Look at existing tests in `tests/` for patterns to follow
- The framework handles all the technical complexity - focus on business logic!
