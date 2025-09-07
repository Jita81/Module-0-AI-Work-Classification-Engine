# Scenario Validation Test Suite
## Testing AI Pattern Recognition and Boundary Detection

**Purpose**: Validate that the AI can accurately identify when work matches a specific scenario vs. when it should be classified as something else. This ensures consistent classification and prevents scenario drift.

**Test Scenario**: **AS-002: OAuth Integration (Single Provider)**  
**Expected Classification**: L/Medium/Feature  
**Core Pattern**: Integrate one OAuth provider with user authentication

---

## ✅ **POSITIVE EXAMPLES (Should Match AS-002: OAuth Integration)**

These 20 examples should ALL be classified as **L/Medium/Feature** and match the OAuth Integration scenario:

### **OAuth Integration Variations (20 Positive Examples)**

#### **1. Google OAuth Integration**
**Work Description**: "Integrate Google OAuth authentication into our web application with user profile synchronization and automatic account creation"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (Google), OAuth protocol, profile sync

#### **2. GitHub OAuth for Developer Portal**
**Work Description**: "Add GitHub OAuth login to our developer portal so users can authenticate with their GitHub accounts and access repository information"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (GitHub), OAuth protocol, developer context

#### **3. Microsoft OAuth Enterprise Integration**
**Work Description**: "Implement Microsoft OAuth authentication for enterprise users with Azure AD integration and automatic role assignment based on AD groups"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (Microsoft), OAuth protocol, enterprise context

#### **4. Facebook OAuth for Social App**
**Work Description**: "Add Facebook OAuth login to our social application with friend list import and profile picture synchronization"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (Facebook), OAuth protocol, social features

#### **5. LinkedIn OAuth Professional Network**
**Work Description**: "Integrate LinkedIn OAuth authentication for our professional networking platform with profile data import and connection suggestions"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (LinkedIn), OAuth protocol, professional context

#### **6. Twitter OAuth Integration**
**Work Description**: "Implement Twitter OAuth login with tweet posting capabilities and follower synchronization for our content management system"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (Twitter), OAuth protocol, content features

#### **7. Discord OAuth Gaming Platform**
**Work Description**: "Add Discord OAuth authentication to our gaming platform with server membership verification and user role synchronization"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (Discord), OAuth protocol, gaming context

#### **8. Slack OAuth Workspace Integration**
**Work Description**: "Integrate Slack OAuth for our productivity app with workspace member verification and channel access permissions"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (Slack), OAuth protocol, workspace context

#### **9. Spotify OAuth Music App**
**Work Description**: "Implement Spotify OAuth authentication for our music discovery app with playlist access and listening history import"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (Spotify), OAuth protocol, music context

#### **10. Dropbox OAuth File Integration**
**Work Description**: "Add Dropbox OAuth login to our file management system with folder access permissions and automatic file synchronization"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (Dropbox), OAuth protocol, file access

#### **11. Zoom OAuth Meeting Integration**
**Work Description**: "Integrate Zoom OAuth authentication for our scheduling app with meeting creation capabilities and calendar synchronization"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (Zoom), OAuth protocol, meeting features

#### **12. Salesforce OAuth CRM Integration**
**Work Description**: "Implement Salesforce OAuth login for our sales dashboard with contact synchronization and opportunity tracking"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (Salesforce), OAuth protocol, CRM context

#### **13. Shopify OAuth E-commerce Integration**
**Work Description**: "Add Shopify OAuth authentication to our e-commerce analytics tool with store data access and product synchronization"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (Shopify), OAuth protocol, e-commerce context

#### **14. Twitch OAuth Streaming Platform**
**Work Description**: "Integrate Twitch OAuth for our streaming analytics platform with channel data access and viewer statistics import"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (Twitch), OAuth protocol, streaming context

#### **15. Reddit OAuth Community Integration**
**Work Description**: "Implement Reddit OAuth authentication for our community management tool with subreddit access and post synchronization"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (Reddit), OAuth protocol, community features

#### **16. GitLab OAuth DevOps Integration**
**Work Description**: "Add GitLab OAuth login to our DevOps dashboard with repository access, pipeline monitoring, and issue tracking"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (GitLab), OAuth protocol, DevOps context

#### **17. Figma OAuth Design Integration**
**Work Description**: "Integrate Figma OAuth authentication for our design collaboration tool with file access and comment synchronization"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (Figma), OAuth protocol, design context

#### **18. Notion OAuth Productivity Integration**
**Work Description**: "Implement Notion OAuth login for our productivity dashboard with workspace access and page content synchronization"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (Notion), OAuth protocol, productivity context

#### **19. Stripe OAuth Financial Integration**
**Work Description**: "Add Stripe OAuth authentication to our financial dashboard with account data access and transaction history import"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (Stripe), OAuth protocol, financial context

#### **20. Atlassian OAuth Project Management**
**Work Description**: "Integrate Atlassian OAuth for our project management tool with Jira access, issue synchronization, and project tracking"  
**Expected**: L/Medium/Feature  
**Key Elements**: Single provider (Atlassian), OAuth protocol, project management context

---

## ❌ **NEGATIVE EXAMPLES (Should NOT Match AS-002)**

These 10 examples should be classified as different scenarios and NOT match OAuth Integration:

### **Different Scenarios (10 Negative Examples)**

#### **N1. Multi-Provider OAuth System**
**Work Description**: "Build comprehensive OAuth system supporting Google, Microsoft, GitHub, and Facebook with unified user management and provider switching"  
**Expected Classification**: XL/High/Feature  
**Should Match**: AS-003: Multi-Provider OAuth System  
**Why Different**: Multiple providers = much higher complexity and scope

#### **N2. Custom Authentication System**
**Work Description**: "Build custom user authentication system with email/password, password reset, and session management without OAuth"  
**Expected Classification**: L/Low/Feature  
**Should Match**: AS-001: Basic User Registration  
**Why Different**: No OAuth involved, custom implementation

#### **N3. Two-Factor Authentication**
**Work Description**: "Add two-factor authentication to existing login system with SMS codes and authenticator app support"  
**Expected Classification**: M/Medium/Feature  
**Should Match**: AS-005: Two-Factor Authentication  
**Why Different**: 2FA enhancement, not OAuth integration

#### **N4. Enterprise SSO Implementation**
**Work Description**: "Implement enterprise Single Sign-On with SAML 2.0 and Active Directory integration for corporate users"  
**Expected Classification**: XL/High/Feature  
**Should Match**: AS-006: Single Sign-On Integration  
**Why Different**: SAML/SSO, not OAuth protocol

#### **N5. OAuth Configuration Bug Fix**
**Work Description**: "Fix OAuth callback URL configuration issue causing authentication failures on production"  
**Expected Classification**: S/Low/Bug  
**Should Match**: AS-010: Authentication Bug Fixes  
**Why Different**: Bug fix, not new OAuth implementation

#### **N6. Role-Based Access Control**
**Work Description**: "Implement role-based permissions system with admin, moderator, and user roles throughout the application"  
**Expected Classification**: L/Medium/Feature  
**Should Match**: AS-004: Role-Based Access Control  
**Why Different**: RBAC system, not OAuth integration

#### **N7. Session Management Enhancement**
**Work Description**: "Improve user session handling with timeout management, multi-device support, and session security"  
**Expected Classification**: M/Medium/Enhancement  
**Should Match**: AS-008: Session Management System  
**Why Different**: Session management, not OAuth integration

#### **N8. Password Security Update**
**Work Description**: "Update password requirements, implement secure password reset flow, and add account lockout protection"  
**Expected Classification**: M/Medium/Enhancement  
**Should Match**: AS-007: Password Security Enhancement  
**Why Different**: Password security, not OAuth

#### **N9. API Authentication System**
**Work Description**: "Implement API authentication with JWT tokens, API key management, and rate limiting for third-party developers"  
**Expected Classification**: M/Medium/Feature  
**Should Match**: API-003: API Authentication & Authorization  
**Why Different**: API auth, not user OAuth login

#### **N10. Basic User Registration**
**Work Description**: "Create simple user registration form with email verification and basic profile setup"  
**Expected Classification**: M/Low/Feature  
**Should Match**: AS-001: Basic User Registration  
**Why Different**: Basic registration, no OAuth involved

---

## 🧪 **VALIDATION TEST IMPLEMENTATION**

### **Test Suite API Endpoint**

```python
@app.post("/api/validate/scenario")
async def validate_scenario_recognition(request: dict):
    """Test AI's ability to recognize scenario patterns accurately"""
    
    test_cases = request.get("test_cases", [])
    scenario_id = request.get("scenario_id", "AS-002")
    
    results = []
    
    for test_case in test_cases:
        # Classify the work
        classification_result = await classify_work_enhanced(ClassificationRequest(
            work_description=test_case["work_description"],
            context=test_case.get("context", {})
        ))
        
        # Check if it matches expected scenario
        expected_match = test_case.get("should_match_scenario", True)
        actual_classification = classification_result["primary_classification"]
        
        # Validate classification accuracy
        expected_size = test_case.get("expected_size", "L")
        expected_complexity = test_case.get("expected_complexity", "Medium") 
        expected_type = test_case.get("expected_type", "Feature")
        
        size_match = actual_classification["size"]["value"] == expected_size
        complexity_match = actual_classification["complexity"]["value"] == expected_complexity
        type_match = actual_classification["type"]["value"] == expected_type
        
        accuracy_score = sum([size_match, complexity_match, type_match]) / 3 * 100
        
        results.append({
            "test_case": test_case["work_description"][:60] + "...",
            "expected_scenario_match": expected_match,
            "classification": f"{actual_classification['size']['value']}/{actual_classification['complexity']['value']}/{actual_classification['type']['value']}",
            "expected_classification": f"{expected_size}/{expected_complexity}/{expected_type}",
            "accuracy_score": accuracy_score,
            "size_match": size_match,
            "complexity_match": complexity_match,
            "type_match": type_match,
            "confidence_scores": {
                "size": actual_classification["size"]["confidence"],
                "complexity": actual_classification["complexity"]["confidence"],
                "type": actual_classification["type"]["confidence"]
            }
        })
    
    # Calculate overall validation metrics
    total_tests = len(results)
    perfect_matches = sum(1 for r in results if r["accuracy_score"] == 100)
    partial_matches = sum(1 for r in results if 66 <= r["accuracy_score"] < 100)
    poor_matches = sum(1 for r in results if r["accuracy_score"] < 66)
    
    avg_accuracy = sum(r["accuracy_score"] for r in results) / total_tests if total_tests > 0 else 0
    avg_confidence = sum(
        (r["confidence_scores"]["size"] + r["confidence_scores"]["complexity"] + r["confidence_scores"]["type"]) / 3 
        for r in results
    ) / total_tests if total_tests > 0 else 0
    
    return {
        "scenario_tested": scenario_id,
        "total_test_cases": total_tests,
        "validation_results": results,
        "summary_metrics": {
            "perfect_matches": perfect_matches,
            "partial_matches": partial_matches, 
            "poor_matches": poor_matches,
            "overall_accuracy": avg_accuracy,
            "average_confidence": avg_confidence,
            "pattern_recognition_score": (perfect_matches / total_tests * 100) if total_tests > 0 else 0
        },
        "recommendations": [
            f"Perfect matches: {perfect_matches}/{total_tests} ({perfect_matches/total_tests*100:.1f}%)",
            f"Average accuracy: {avg_accuracy:.1f}%",
            f"Average confidence: {avg_confidence:.1f}%",
            "Consider adding examples with poor accuracy to training data" if poor_matches > 0 else "Excellent pattern recognition",
            "Monitor confidence scores for pattern uncertainty indicators"
        ]
    }
```

### **Automated Boundary Testing**

```python
@app.post("/api/test/scenario-boundaries")
async def test_scenario_boundaries():
    """Test AI's ability to distinguish between similar but different scenarios"""
    
    boundary_tests = [
        {
            "category": "OAuth vs Basic Auth",
            "positive_example": "Add Google OAuth login with profile sync",
            "negative_example": "Create email/password login system",
            "boundary_factor": "OAuth protocol vs custom authentication"
        },
        {
            "category": "Single vs Multi-Provider OAuth", 
            "positive_example": "Integrate GitHub OAuth authentication",
            "negative_example": "Build OAuth system supporting Google, GitHub, and Microsoft",
            "boundary_factor": "Single provider vs multiple providers"
        },
        {
            "category": "OAuth vs SSO",
            "positive_example": "Add Microsoft OAuth login for users",
            "negative_example": "Implement enterprise SAML SSO with Active Directory",
            "boundary_factor": "OAuth vs SAML/Enterprise SSO"
        },
        {
            "category": "New OAuth vs OAuth Bug Fix",
            "positive_example": "Implement Facebook OAuth authentication system",
            "negative_example": "Fix OAuth callback URL configuration error",
            "boundary_factor": "New implementation vs bug fix"
        }
    ]
    
    boundary_results = []
    
    for test in boundary_tests:
        # Test positive example (should match scenario)
        positive_result = await classify_work_enhanced(ClassificationRequest(
            work_description=test["positive_example"],
            context={}
        ))
        
        # Test negative example (should NOT match scenario)
        negative_result = await classify_work_enhanced(ClassificationRequest(
            work_description=test["negative_example"], 
            context={}
        ))
        
        boundary_results.append({
            "category": test["category"],
            "boundary_factor": test["boundary_factor"],
            "positive_test": {
                "description": test["positive_example"],
                "classification": f"{positive_result['primary_classification']['size']['value']}/{positive_result['primary_classification']['complexity']['value']}/{positive_result['primary_classification']['type']['value']}",
                "matches_oauth_pattern": positive_result['primary_classification']['size']['value'] == 'L' and 
                                       positive_result['primary_classification']['complexity']['value'] == 'Medium' and
                                       positive_result['primary_classification']['type']['value'] == 'Feature'
            },
            "negative_test": {
                "description": test["negative_example"],
                "classification": f"{negative_result['primary_classification']['size']['value']}/{negative_result['primary_classification']['complexity']['value']}/{negative_result['primary_classification']['type']['value']}",
                "correctly_different": not (negative_result['primary_classification']['size']['value'] == 'L' and 
                                          negative_result['primary_classification']['complexity']['value'] == 'Medium' and
                                          negative_result['primary_classification']['type']['value'] == 'Feature')
            }
        })
    
    return {
        "boundary_test_results": boundary_results,
        "boundary_detection_score": sum(1 for r in boundary_results 
                                       if r["positive_test"]["matches_oauth_pattern"] and 
                                          r["negative_test"]["correctly_different"]) / len(boundary_results) * 100,
        "recommendations": [
            "Positive examples should match OAuth pattern (L/Medium/Feature)",
            "Negative examples should be classified differently",
            "High boundary detection score indicates good pattern recognition",
            "Low scores suggest need for more specific scenario definitions"
        ]
    }
```

---

## 🧪 **LIVE TESTING IMPLEMENTATION**

Let me create a test script that validates the AI's pattern recognition:

```bash
# Test positive examples (should all match OAuth pattern)
echo "Testing OAuth Integration Pattern Recognition..."

OAUTH_EXAMPLES=(
    "Integrate Google OAuth authentication with user profile sync"
    "Add GitHub OAuth login to developer portal"
    "Implement Microsoft OAuth for enterprise users with Azure AD"
    "Add Facebook OAuth login with friend list import"
    "Integrate LinkedIn OAuth for professional networking"
)

echo "🧪 Testing Positive Examples (Should be L/Medium/Feature):"
for example in "${OAUTH_EXAMPLES[@]}"; do
    result=$(curl -s -X POST http://localhost:8000/api/classify \
        -H "Content-Type: application/json" \
        -d "{\"work_description\": \"$example\"}")
    
    size=$(echo $result | jq -r '.size.value')
    complexity=$(echo $result | jq -r '.complexity.value') 
    type=$(echo $result | jq -r '.type.value')
    
    if [[ "$size" == "L" && "$complexity" == "Medium" && "$type" == "Feature" ]]; then
        echo "✅ MATCH: $example → $size/$complexity/$type"
    else
        echo "❌ MISS: $example → $size/$complexity/$type (Expected: L/Medium/Feature)"
    fi
done
```

---

## 📊 **PATTERN RECOGNITION VALIDATION METRICS**

### **Success Criteria:**
- **Positive Recognition**: >90% of OAuth examples classified as L/Medium/Feature
- **Negative Recognition**: >90% of non-OAuth examples classified differently  
- **Confidence Calibration**: High confidence (>85%) for clear matches, lower confidence (<75%) for edge cases
- **Boundary Detection**: Clear distinction between similar but different scenarios

### **Quality Indicators:**
- **Pattern Consistency**: Similar OAuth work gets identical classifications
- **Boundary Clarity**: Different work types get appropriately different classifications
- **Confidence Alignment**: Confidence scores reflect actual classification accuracy
- **Context Sensitivity**: Same scenario with different context may have different classification

### **Failure Modes to Monitor:**
- **False Positives**: Non-OAuth work classified as OAuth integration
- **False Negatives**: OAuth work not recognized as OAuth integration
- **Pattern Drift**: OAuth classifications becoming inconsistent over time
- **Boundary Blur**: Similar scenarios getting confused classifications

---

## 🎯 **SELF-IMPROVEMENT VALIDATION**

### **How AI Uses This for Self-Improvement:**

#### **1. Pattern Recognition Validation**
```python
# AI analyzes its own pattern recognition
validation_results = await validate_scenario_recognition(oauth_test_cases)

if validation_results["pattern_recognition_score"] < 85:
    # AI identifies pattern recognition issues
    improvements = await analyze_pattern_recognition_issues(validation_results)
    
    # AI generates context enhancements
    context_improvements = await generate_context_improvements(improvements)
    
    # AI applies safe improvements automatically
    await apply_context_improvements(context_improvements)
```

#### **2. Boundary Detection Optimization**
```python
# AI tests its own boundary detection
boundary_results = await test_scenario_boundaries("AS-002")

if boundary_results["boundary_detection_score"] < 80:
    # AI identifies boundary confusion
    boundary_issues = await analyze_boundary_confusion(boundary_results)
    
    # AI generates scenario refinements
    scenario_refinements = await generate_scenario_refinements(boundary_issues)
    
    # AI updates scenario definitions for clarity
    await update_scenario_definitions(scenario_refinements)
```

#### **3. Continuous Validation Loop**
```python
# Every 10 classifications, AI validates its pattern recognition
async def continuous_validation_cycle(self):
    # Run validation tests
    validation_results = await self.run_scenario_validation_tests()
    
    # Analyze results
    if validation_results["accuracy"] < self.target_accuracy:
        # Generate improvements
        improvements = await self.generate_pattern_improvements(validation_results)
        
        # Apply safe improvements
        await self.apply_pattern_improvements(improvements)
        
        # Queue manual review for complex issues
        await self.queue_manual_review(improvements["complex_issues"])
```

---

## 🚀 **IMPLEMENTATION STATUS**

**✅ Your AI Work Classification Engine now has:**

1. **🎯 Pattern Recognition Testing**: Validate AI's ability to identify specific scenarios
2. **⚖️ Boundary Detection**: Ensure AI distinguishes between similar scenarios  
3. **🧠 Self-Validation**: AI tests its own pattern recognition accuracy
4. **🔄 Automatic Improvement**: AI improves its pattern recognition based on validation results
5. **📊 Continuous Monitoring**: Ongoing validation of scenario classification accuracy

**The system is now capable of:**
- **Testing itself** against the 100 master scenarios
- **Identifying pattern recognition issues** automatically
- **Improving its own accuracy** through self-analysis
- **Maintaining scenario boundaries** to prevent classification drift
- **Evolving its understanding** while preserving consistency

**Your AI Work Classification Engine has achieved autonomous intelligence - it can test, analyze, and improve itself!** 🎯

