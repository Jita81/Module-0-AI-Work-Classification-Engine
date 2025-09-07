# AI Work Classification Engine - Complete API Documentation

**MCP Server with Claude Sonnet 4 Integration - All functionality accessible via API**

## 🌐 Base URL: `http://localhost:8000`

---

## 🎯 **CORE CLASSIFICATION API**

### `POST /api/classify`
**Classify work items using Claude Sonnet 4**

```json
{
  "work_description": "Add user authentication system with OAuth integration",
  "context": {
    "project": "web-app",
    "team": "backend", 
    "priority": "high",
    "tech_stack": ["Python", "FastAPI"]
  },
  "user_id": "optional-user-id"
}
```

**Response:**
```json
{
  "classification_id": "uuid",
  "size": {"value": "L", "confidence": 85, "reasoning": "..."},
  "complexity": {"value": "Medium", "confidence": 80, "reasoning": "..."},
  "type": {"value": "Feature", "confidence": 95, "reasoning": "..."},
  "estimated_effort": "2-3 weeks",
  "recommended_approach": "Break into phases...",
  "timestamp": "2025-01-07T..."
}
```

### `POST /api/feedback`
**Provide feedback to improve AI accuracy**

```json
{
  "classification_id": "uuid",
  "feedback_type": "accept|edit|reject",
  "corrections": {
    "complexity": {
      "value": "High",
      "reasoning": "OAuth involves security compliance..."
    }
  },
  "user_id": "optional-user-id"
}
```

---

## 🎭 **PROMPT ENGINEERING API** (Key Lever #1)

### `GET /api/prompts`
**Get current prompt configuration**
```json
{
  "version": "1.0.0",
  "system_message": "You are an expert work classification system...",
  "user_prompt_template": "Classify this work item:\n\n\"{work_description}\"...",
  "api_config": {
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 8192,
    "temperature": 0
  }
}
```

### `PUT /api/prompts`
**Update prompt engineering configuration**
```json
{
  "system_message": "Your optimized system message...",
  "user_prompt_template": "Your custom prompt template...",
  "api_config": {
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 8192,
    "temperature": 0
  }
}
```

### `POST /api/prompts/test`
**Test prompt configuration**
```json
{
  "work_description": "Test work item",
  "context": {"project": "test"}
}
```

---

## 🎯 **CONTEXT ENGINEERING API** (Key Lever #2)

### `GET /api/context/templates`
**Get context templates for different project types**
```json
{
  "templates": [
    {
      "id": "web-app-frontend",
      "name": "Web Application Frontend",
      "template": {
        "project_type": "web-application",
        "tech_stack": ["React", "TypeScript"],
        "team_size": "small",
        "experience_level": "senior",
        "quality_standards": ["unit_tests", "accessibility"]
      },
      "usage_scenarios": ["UI components", "Frontend features"],
      "is_active": true
    }
  ]
}
```

### `POST /api/context/templates`
**Create new context template**
```json
{
  "name": "Mobile Development",
  "description": "Context for mobile app development",
  "template": {
    "project_type": "mobile-application",
    "platforms": ["iOS", "Android"],
    "tech_stack": ["React Native"]
  },
  "usage_scenarios": ["Mobile features", "Cross-platform work"]
}
```

### `GET /api/context/rules`
**Get dynamic context rules**
```json
{
  "rules": [
    {
      "id": "security-boost",
      "name": "Security Work Complexity Boost",
      "condition": "work_description contains ['security', 'authentication']",
      "context_additions": {
        "security_review_required": true,
        "complexity_modifier": "+1"
      },
      "priority": 1
    }
  ]
}
```

### `POST /api/context/test`
**Test context generation**
```json
{
  "work_description": "Add OAuth authentication",
  "base_context": {"project": "web-app"}
}
```

---

## 📚 **SCENARIO LIBRARY API** (Key Lever #3)

### `GET /api/scenarios`
**Get product development scenario library**
```json
{
  "scenarios": [
    {
      "id": "auth-oauth",
      "title": "OAuth Authentication System",
      "description": "Implement complete user authentication...",
      "domain": "security-implementation",
      "size": "L",
      "complexity": "Medium",
      "type": "Feature",
      "tags": ["authentication", "oauth", "security"],
      "examples": ["Google OAuth login", "GitHub OAuth"],
      "success_patterns": ["Use OAuth libraries", "Security testing"],
      "usage_count": 15,
      "accuracy_score": 0.92
    }
  ],
  "total_scenarios": 1,
  "target_scenarios": 100,
  "completion_percentage": 1
}
```

### `POST /api/scenarios`
**Create new scenario**
```json
{
  "title": "Payment Processing System",
  "description": "Integrate payment gateway with transaction handling",
  "domain": "api-development",
  "size": "XL",
  "complexity": "High",
  "type": "Feature",
  "tags": ["payments", "stripe", "compliance"],
  "examples": [
    "Stripe integration with subscription billing",
    "PayPal checkout with refunds"
  ],
  "success_patterns": [
    "Use payment processor SDKs",
    "Implement proper error handling"
  ]
}
```

### `POST /api/scenarios/deduplicate`
**Check for duplicate scenarios**
```json
{
  "title": "OAuth Login System",
  "description": "User authentication with OAuth",
  "tags": ["auth", "oauth"]
}
```

---

## 🎛️ **CONFIGURATION LEVERS DASHBOARD API**

### `GET /api/configuration-levers`
**Get master configuration dashboard**
```json
{
  "overall_health": 78,
  "levers": [
    {
      "id": "prompt-engineering",
      "name": "🎭 Prompt Engineering",
      "current_status": "optimal",
      "quality_score": 92,
      "impact_level": "high",
      "recommendations": ["Current prompts well-structured", "Add domain examples"]
    },
    {
      "id": "scenario-library",
      "name": "📚 Scenario Library", 
      "current_status": "critical",
      "quality_score": 45,
      "impact_level": "high",
      "recommendations": ["URGENT: Expand to 30+ scenarios"]
    }
  ],
  "priority_actions": [
    {
      "action": "Expand scenario library to 30+ scenarios",
      "impact": "High",
      "urgency": "Critical"
    }
  ]
}
```

### `POST /api/optimize`
**Get system optimization recommendations**
```json
{
  "current_state": {
    "classifications": 4,
    "feedback_items": 0,
    "overall_health": "healthy"
  },
  "optimization_priorities": [
    {
      "priority": 1,
      "area": "Scenario Library Expansion",
      "action": "Add 30+ product development scenarios",
      "impact": "High - Will improve domain-specific accuracy by 15-20%",
      "effort": "2-3 hours",
      "api_endpoint": "/api/scenarios"
    }
  ],
  "success_path": {
    "week_1": "Add 15-20 core scenarios",
    "target": "85%+ acceptance rate"
  }
}
```

---

## 📊 **ENHANCED ANALYTICS API**

### `GET /api/analytics/detailed`
**Get comprehensive analytics**
```json
{
  "classification_metrics": {
    "total_classifications": 4,
    "accuracy_by_dimension": {
      "size": {"accuracy": 0.9},
      "complexity": {"accuracy": 0.84},
      "type": {"accuracy": 0.96}
    }
  },
  "configuration_effectiveness": {
    "prompt_quality": 92,
    "context_coverage": 78,
    "scenario_completeness": 45
  },
  "improvement_recommendations": [
    {
      "area": "scenario_library",
      "priority": "high",
      "action": "Add 25+ more scenarios",
      "expected_impact": "+15% accuracy"
    }
  ]
}
```

---

## 🔧 **SYSTEM MANAGEMENT API**

### `GET /health`
**System health check**
```json
{
  "module_name": "ai-work-classification-engine",
  "status": "healthy",
  "business_rules_loaded": 4,
  "classifications_count": 4,
  "feedback_count": 0,
  "patterns_count": 0
}
```

### `POST /api/trigger-learning`
**Trigger learning analysis**
```json
{
  "patterns_detected": 0,
  "config_updated": false,
  "message": "Learning analysis completed"
}
```

---

## 🚀 **USAGE EXAMPLES**

### **Basic Classification:**
```bash
curl -X POST http://localhost:8000/api/classify \
  -H "Content-Type: application/json" \
  -d '{
    "work_description": "Add OAuth authentication with Google and GitHub providers",
    "context": {"project": "web-app", "team": "backend"}
  }'
```

### **Configuration Management:**
```bash
# Get current prompt configuration
curl http://localhost:8000/api/prompts

# Get scenario library status
curl http://localhost:8000/api/scenarios

# Get configuration levers dashboard  
curl http://localhost:8000/api/configuration-levers
```

### **System Optimization:**
```bash
# Get optimization recommendations
curl -X POST http://localhost:8000/api/optimize

# Check system health
curl http://localhost:8000/health
```

---

## 🎯 **KEY LEVERS FOR SUCCESS**

### **1. 🎭 Prompt Engineering** (`/api/prompts`)
- Control Claude Sonnet 4's instructions and behavior
- Optimize system message for your domain
- Customize output format and reasoning requirements

### **2. 🎯 Context Engineering** (`/api/context/*`)
- Add project-specific intelligence to classifications
- Create templates for different work types
- Implement dynamic rules for automatic context injection

### **3. 📚 Scenario Library** (`/api/scenarios`)
- Build comprehensive library of 30-100 product scenarios
- Train AI on your specific work patterns
- Eliminate classification inconsistencies

### **4. 🎛️ Configuration Levers** (`/api/configuration-levers`)
- Master dashboard showing optimization opportunities
- Priority actions for maximum impact
- Success path to 85%+ acceptance rate

---

## 🧠 **AI AGENT INTEGRATION**

This MCP server is designed for AI agent integration with:
- **Self-describing API**: Complete OpenAPI schema available
- **Structured responses**: Consistent JSON format
- **Error handling**: Proper HTTP status codes
- **Comprehensive functionality**: All configuration management via API

**Your AI Work Classification Engine is now a pure MCP server with complete API access to all functionality!** 🚀
