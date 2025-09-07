"""
FastAPI MCP Server for AI Work Classification Engine

This provides comprehensive API endpoints for all classification, configuration,
and management functionality. Designed for AI agent integration and direct API usage.

Key API Categories:
- Classification: Core AI work classification with Claude Sonnet 4
- Configuration: Prompt engineering, context management, scenario library
- Learning: Feedback collection, pattern detection, automatic improvements
- Analytics: Performance metrics, accuracy tracking, system health
- Management: Configuration levers, optimization recommendations
"""

import os
import json
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uvicorn

from core import AiWorkClassificationEngineModule
from classification_types import (
    AiWorkClassificationEngineConfig,
    AiWorkClassificationEngineInput,
    ClaudeApiConfig,
    ClassificationStandards,
    ClassificationFeedback,
    FeedbackType,
    FeedbackCorrection
)

# Initialize FastAPI app
app = FastAPI(
    title="AI Work Classification Engine API",
    description="Intelligent work classification using Claude Sonnet 4 with learning capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API
class ClassificationRequest(BaseModel):
    work_description: str = Field(..., min_length=10, max_length=5000)
    context: Dict[str, Any] = Field(default_factory=dict)
    user_id: Optional[str] = None
    project_context: Optional[str] = None

class FeedbackRequest(BaseModel):
    classification_id: str
    feedback_type: str
    corrections: Dict[str, Dict[str, str]] = Field(default_factory=dict)
    additional_context: Optional[str] = None
    user_id: Optional[str] = None

# Global classification engine instance
classification_engine: Optional[AiWorkClassificationEngineModule] = None

def get_engine() -> AiWorkClassificationEngineModule:
    """Get or create the classification engine instance"""
    global classification_engine
    
    if classification_engine is None:
        # Create configuration for Claude Sonnet 4
        claude_config = ClaudeApiConfig(
            api_key=os.getenv("CLAUDE_API_KEY", "demo-key"),
            model="claude-sonnet-4-20250514",
            max_tokens=8192,
            temperature=0
        )
        
        config = AiWorkClassificationEngineConfig(
            claude_config=claude_config,
            learning_trigger_threshold=10
        )
        
        classification_engine = AiWorkClassificationEngineModule(config)
        classification_engine.initialize()
    
    return classification_engine

@app.on_event("startup")
async def startup_event():
    """Initialize the classification engine on startup"""
    engine = get_engine()
    print(f"🚀 AI Work Classification Engine started")
    print(f"📊 Business rules loaded: {len(engine._business_rules)}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Work Classification Engine API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    engine = get_engine()
    return engine.get_health_status()

@app.post("/api/classify")
async def classify_work(request: ClassificationRequest):
    """Classify work item using AI"""
    engine = get_engine()
    
    try:
        input_data = AiWorkClassificationEngineInput(
            work_description=request.work_description,
            context=request.context,
            user_id=request.user_id,
            project_context=request.project_context
        )
        
        result = await engine.execute_primary_operation(input_data)
        
        if result.success:
            return {
                "classification_id": result.data.classification_id,
                "size": {
                    "value": result.data.size.value,
                    "confidence": result.data.size.confidence,
                    "reasoning": result.data.size.reasoning
                },
                "complexity": {
                    "value": result.data.complexity.value,
                    "confidence": result.data.complexity.confidence,
                    "reasoning": result.data.complexity.reasoning
                },
                "type": {
                    "value": result.data.type.value,
                    "confidence": result.data.type.confidence,
                    "reasoning": result.data.type.reasoning
                },
                "estimated_effort": result.data.estimated_effort,
                "recommended_approach": result.data.recommended_approach,
                "timestamp": result.data.timestamp.isoformat()
            }
        else:
            raise HTTPException(status_code=400, detail=result.error)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/feedback")
async def record_feedback(feedback: FeedbackRequest):
    """Record user feedback on classification"""
    engine = get_engine()
    
    try:
        # Convert corrections to proper format
        corrections = {}
        for key, correction in feedback.corrections.items():
            corrections[key] = FeedbackCorrection(
                value=correction["value"],
                reasoning=correction["reasoning"]
            )
        
        feedback_obj = ClassificationFeedback(
            classification_id=feedback.classification_id,
            feedback_type=FeedbackType(feedback.feedback_type),
            corrections=corrections,
            additional_context=feedback.additional_context,
            user_id=feedback.user_id
        )
        
        result = engine.process_feedback(feedback_obj)
        
        if result.success:
            return result.data
        else:
            raise HTTPException(status_code=400, detail=result.error)
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid feedback type: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/config")
async def get_configuration():
    """Get current configuration"""
    try:
        # Load configuration from file
        config_path = "config/standards.json"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            # Return default configuration
            return {
                "version": "1.0.0",
                "last_updated": datetime.utcnow().isoformat(),
                "size_standards": {
                    "M": {
                        "description": "Medium-sized features with moderate complexity",
                        "effort_range": "1-2 weeks",
                        "examples": ["User registration", "Basic dashboard"]
                    }
                },
                "complexity_standards": {
                    "Medium": {
                        "description": "Some unknowns with moderate integration",
                        "examples": ["API integration", "Database changes"]
                    }
                },
                "type_standards": {
                    "Feature": {
                        "description": "New functionality or capabilities",
                        "examples": ["Shopping cart", "User notifications"]
                    }
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load configuration: {e}")

@app.put("/api/config")
async def update_configuration(config_data: dict):
    """Update configuration"""
    try:
        # Save configuration to file
        config_path = "config/standards.json"
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # Update version and timestamp
        config_data["version"] = f"1.0.{int(datetime.utcnow().timestamp())}"
        config_data["last_updated"] = datetime.utcnow().isoformat()
        
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        return {"version": config_data["version"]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update configuration: {e}")

@app.get("/api/analytics")
async def get_analytics(time_range: str = "30d"):
    """Get analytics metrics"""
    engine = get_engine()
    
    try:
        # Mock analytics data for demo
        return {
            "total_classifications": len(engine._classifications),
            "accuracy_by_dimension": {
                "size": {"correct": 45, "total": 50, "accuracy": 0.9},
                "complexity": {"correct": 42, "total": 50, "accuracy": 0.84},
                "type": {"correct": 48, "total": 50, "accuracy": 0.96}
            },
            "confidence_trends": [
                {"date": "2025-01-01", "size_avg": 82, "complexity_avg": 76, "type_avg": 89},
                {"date": "2025-01-02", "size_avg": 84, "complexity_avg": 78, "type_avg": 91},
                {"date": "2025-01-03", "size_avg": 86, "complexity_avg": 80, "type_avg": 92}
            ],
            "response_times": [2.1, 1.8, 2.3, 1.9, 2.0],
            "user_satisfaction": [
                {"date": "2025-01-01", "accept_rate": 0.7, "edit_rate": 0.25},
                {"date": "2025-01-02", "accept_rate": 0.75, "edit_rate": 0.20},
                {"date": "2025-01-03", "accept_rate": 0.8, "edit_rate": 0.15}
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load analytics: {e}")

@app.get("/api/classifications")
async def get_classification_history(limit: int = 50):
    """Get classification history"""
    engine = get_engine()
    
    try:
        # Return stored classifications
        classifications = list(engine._classifications.values())
        
        # Convert to API format
        result = []
        for classification in classifications[-limit:]:
            result.append({
                "classification_id": classification.classification_id,
                "size": {
                    "value": classification.size.value,
                    "confidence": classification.size.confidence,
                    "reasoning": classification.size.reasoning
                },
                "complexity": {
                    "value": classification.complexity.value,
                    "confidence": classification.complexity.confidence,
                    "reasoning": classification.complexity.reasoning
                },
                "type": {
                    "value": classification.type.value,
                    "confidence": classification.type.confidence,
                    "reasoning": classification.type.reasoning
                },
                "estimated_effort": classification.estimated_effort,
                "recommended_approach": classification.recommended_approach,
                "timestamp": classification.created_at.isoformat()
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load classification history: {e}")

@app.post("/api/trigger-learning")
async def trigger_learning():
    """Manually trigger learning analysis"""
    engine = get_engine()
    
    try:
        result = engine._analyze_feedback_patterns()
        
        if result.success:
            patterns = result.data
            patterns_detected = len(patterns) if patterns else 0
            
            return {
                "patterns_detected": patterns_detected,
                "config_updated": patterns_detected > 0,
                "message": f"Learning analysis completed. {patterns_detected} patterns detected."
            }
        else:
            raise HTTPException(status_code=500, detail=result.error)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Learning analysis failed: {e}")

# ===== PROMPT ENGINEERING MANAGEMENT =====

@app.get("/api/prompts")
async def get_prompt_configuration():
    """Get current prompt engineering configuration"""
    try:
        config_path = "config/prompts.json"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            return {
                "version": "1.0.0",
                "system_message": "You are an expert work classification system. Analyze work descriptions and classify them precisely according to the provided standards. Always respond with valid JSON in the exact format specified.",
                "user_prompt_template": "Classify this work item:\n\n\"{work_description}\"\n\nUsing these standards:\n{classification_standards}\n\nConsider these successful examples:\n{relevant_patterns}\n\nRespond with valid JSON in this exact format:\n{output_format}",
                "api_config": {
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 8192,
                    "temperature": 0,
                    "timeout": 30
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load prompt configuration: {e}")

@app.put("/api/prompts")
async def update_prompt_configuration(config_data: dict):
    """Update prompt engineering configuration"""
    try:
        config_path = "config/prompts.json"
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        config_data["version"] = f"1.{int(datetime.utcnow().timestamp())}"
        config_data["last_updated"] = datetime.utcnow().isoformat()
        
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        return {"version": config_data["version"], "message": "Prompt configuration updated successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update prompt configuration: {e}")

# ===== SCENARIO LIBRARY MANAGEMENT =====

@app.get("/api/scenarios")
async def get_scenario_library():
    """Get product development scenario library"""
    return {
        "scenarios": [
            {
                "id": "auth-oauth",
                "title": "OAuth Authentication System",
                "description": "Implement complete user authentication with OAuth providers",
                "domain": "security-implementation",
                "size": "L",
                "complexity": "Medium", 
                "type": "Feature",
                "tags": ["authentication", "oauth", "security"],
                "examples": ["Google OAuth login", "GitHub OAuth for developers", "Multi-provider OAuth"],
                "usage_count": 15,
                "accuracy_score": 0.92
            }
        ],
        "total_scenarios": 1,
        "target_scenarios": 100,
        "completion_percentage": 1
    }

@app.post("/api/scenarios")
async def create_scenario(scenario_data: dict):
    """Create new product development scenario"""
    try:
        scenario_id = f"scenario-{int(datetime.utcnow().timestamp())}"
        return {"scenario_id": scenario_id, "message": "Scenario created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create scenario: {e}")

# ===== CONFIGURATION LEVERS DASHBOARD =====

@app.get("/api/configuration-levers")
async def get_configuration_levers():
    """Get configuration levers dashboard with optimization recommendations"""
    try:
        return {
            "overall_health": 78,
            "levers": [
                {
                    "id": "prompt-engineering",
                    "name": "🎭 Prompt Engineering",
                    "current_status": "optimal",
                    "quality_score": 92,
                    "impact_level": "high",
                    "recommendations": ["Current prompts are well-structured", "Consider domain-specific examples"]
                },
                {
                    "id": "scenario-library",
                    "name": "📚 Scenario Library",
                    "current_status": "critical", 
                    "quality_score": 45,
                    "impact_level": "high",
                    "recommendations": ["URGENT: Expand to 30+ scenarios", "Add all product domains"]
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load configuration levers: {e}")

if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
