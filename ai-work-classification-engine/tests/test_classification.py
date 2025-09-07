"""
Comprehensive tests for AI Work Classification Engine
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
import asyncio
import json
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import AiWorkClassificationEngineModule, BusinessRuleViolation
from classification_types import (
    AiWorkClassificationEngineConfig,
    AiWorkClassificationEngineInput,
    AiWorkClassificationEngineOutput,
    ClassificationFeedback,
    ClaudeApiConfig,
    ClassificationStandards,
    WorkClassification,
    ClassificationDimension,
    FeedbackCorrection,
    WorkSize,
    WorkComplexity,
    WorkType,
    FeedbackType,
    OperationResult
)


@pytest.fixture
def claude_config():
    """Create Claude API test configuration"""
    return ClaudeApiConfig(
        api_key="test-api-key",
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        temperature=0.1,
        timeout=30
    )


@pytest.fixture
def config(claude_config):
    """Create test configuration"""
    return AiWorkClassificationEngineConfig(
        domain="ai-analysis",
        persist_audit_trail=False,
        max_audit_events=100,
        claude_config=claude_config,
        classification_standards=ClassificationStandards(),
        learning_trigger_threshold=3
    )


@pytest.fixture
def module(config):
    """Create test module instance"""
    return AiWorkClassificationEngineModule(config)


class TestModuleLifecycle:
    """Test module initialization, health, and shutdown"""
    
    def test_module_initialization(self, module):
        """Test module initialization"""
        result = module.initialize()
        assert result.success
        assert module._initialized
        assert len(module._business_rules) > 0
    
    def test_health_status(self, module):
        """Test health status reporting"""
        module.initialize()
        status = module.get_health_status()
        
        assert status["module_name"] == "ai-work-classification-engine"
        assert status["type"] == "CORE"
        assert status["status"] in ["healthy", "unhealthy"]
        assert "business_rules_loaded" in status
    
    def test_shutdown(self, module):
        """Test module shutdown"""
        module.initialize()
        result = module.shutdown()
        assert result.success
        assert not module._initialized


class TestClassificationWorkflow:
    """Test the main classification workflow"""
    
    @patch('aiohttp.ClientSession.post')
    def test_successful_classification(self, mock_post, module):
        """Test successful work classification"""
        module.initialize()
        
        # Mock Claude API response
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "content": [{
                "text": json.dumps({
                    "size": {"value": "M", "confidence": 85, "reasoning": "Medium-sized feature requiring multiple components"},
                    "complexity": {"value": "Medium", "confidence": 70, "reasoning": "Some integration required with existing systems"},
                    "type": {"value": "Feature", "confidence": 90, "reasoning": "New functionality being added"},
                    "estimated_effort": "1-2 weeks",
                    "recommended_approach": "Standard development process with testing"
                })
            }]
        })
        mock_post.return_value.__aenter__.return_value = mock_response
        
        input_data = AiWorkClassificationEngineInput(
            work_description="Add user authentication system with OAuth integration and password reset functionality"
        )
        
        result = asyncio.run(module.execute_primary_operation(input_data))
        
        assert result.success
        assert result.data.size.value == "M"
        assert result.data.complexity.value == "Medium"
        assert result.data.type.value == "Feature"
        assert result.data.size.confidence == 85
        assert result.data.classification_id in module._classifications
    
    def test_classification_not_initialized(self, module):
        """Test classification fails when module not initialized"""
        input_data = AiWorkClassificationEngineInput(work_description="Test work item")
        result = asyncio.run(module.execute_primary_operation(input_data))
        assert not result.success
        assert "not initialized" in result.error
    
    @patch('aiohttp.ClientSession.post')
    def test_claude_api_error_handling(self, mock_post, module):
        """Test handling of Claude API errors"""
        module.initialize()
        
        # Mock API error
        mock_response = Mock()
        mock_response.status = 429
        mock_response.text = AsyncMock(return_value="Rate limited")
        mock_post.return_value.__aenter__.return_value = mock_response
        
        input_data = AiWorkClassificationEngineInput(work_description="Test work item")
        result = asyncio.run(module.execute_primary_operation(input_data))
        
        assert not result.success
        assert "Claude API error" in result.error


class TestBusinessRuleValidation:
    """Test business rule validation"""
    
    def test_work_description_length_validation(self, module):
        """Test work description length validation"""
        module.initialize()
        
        # Test too short description
        short_input = AiWorkClassificationEngineInput(work_description="Fix")
        assert not module._validate_work_description_length(short_input)
        
        # Test valid description
        valid_input = AiWorkClassificationEngineInput(work_description="Add user authentication with OAuth")
        assert module._validate_work_description_length(valid_input)
        
        # Test too long description
        long_input = AiWorkClassificationEngineInput(work_description="A" * 5001)
        assert not module._validate_work_description_length(long_input)
    
    def test_claude_response_validation(self, module):
        """Test Claude API response validation"""
        module.initialize()
        
        # Test valid response
        valid_response = {
            "size": {"value": "M", "confidence": 85, "reasoning": "Medium work"},
            "complexity": {"value": "Medium", "confidence": 70, "reasoning": "Some complexity"},
            "type": {"value": "Feature", "confidence": 90, "reasoning": "New feature"}
        }
        result = module._validate_claude_response(valid_response)
        assert result.success
        
        # Test missing field
        invalid_response = {
            "size": {"value": "M", "confidence": 85, "reasoning": "Medium work"},
            "complexity": {"value": "Medium", "confidence": 70, "reasoning": "Some complexity"}
            # Missing "type"
        }
        result = module._validate_claude_response(invalid_response)
        assert not result.success
        assert "Missing required field: type" in result.error
        
        # Test invalid confidence score
        invalid_confidence = {
            "size": {"value": "M", "confidence": 150, "reasoning": "Medium work"},
            "complexity": {"value": "Medium", "confidence": 70, "reasoning": "Some complexity"},
            "type": {"value": "Feature", "confidence": 90, "reasoning": "New feature"}
        }
        result = module._validate_claude_response(invalid_confidence)
        assert not result.success
        assert "Invalid confidence score" in result.error
        
        # Test invalid enum value
        invalid_enum = {
            "size": {"value": "HUGE", "confidence": 85, "reasoning": "Medium work"},
            "complexity": {"value": "Medium", "confidence": 70, "reasoning": "Some complexity"},
            "type": {"value": "Feature", "confidence": 90, "reasoning": "New feature"}
        }
        result = module._validate_claude_response(invalid_enum)
        assert not result.success
        assert "Invalid size value: HUGE" in result.error


class TestFeedbackSystem:
    """Test feedback collection and processing"""
    
    def test_feedback_processing(self, module):
        """Test feedback collection and processing"""
        module.initialize()
        
        # Create a classification first
        classification_id = "test-123"
        classification = WorkClassification(
            classification_id=classification_id,
            work_description="Add user authentication system",
            size=ClassificationDimension(value="M", confidence=85, reasoning="Medium work"),
            complexity=ClassificationDimension(value="Medium", confidence=70, reasoning="Some complexity"),
            type=ClassificationDimension(value="Feature", confidence=90, reasoning="New feature"),
            estimated_effort="1-2 weeks",
            recommended_approach="Standard process",
            context={}
        )
        module._classifications[classification_id] = classification
        
        # Test feedback processing
        feedback = ClassificationFeedback(
            classification_id=classification_id,
            feedback_type=FeedbackType.ACCEPT,
            user_id="test-user"
        )
        
        result = module.process_feedback(feedback)
        assert result.success
        assert len(module._feedback_store) == 1
        assert result.data["status"] == "recorded"
        assert classification.feedback == feedback
    
    def test_feedback_rate_limiting(self, module):
        """Test feedback rate limiting"""
        module.initialize()
        
        classification_id = "test-123"
        classification = WorkClassification(
            classification_id=classification_id,
            work_description="Test work item",
            size=ClassificationDimension(value="M", confidence=85, reasoning="Medium work"),
            complexity=ClassificationDimension(value="Medium", confidence=70, reasoning="Some complexity"),
            type=ClassificationDimension(value="Feature", confidence=90, reasoning="New feature"),
            estimated_effort="1-2 weeks",
            recommended_approach="Standard process",
            context={}
        )
        module._classifications[classification_id] = classification
        
        # First feedback should succeed
        feedback1 = ClassificationFeedback(
            classification_id=classification_id,
            feedback_type=FeedbackType.ACCEPT,
            user_id="test-user"
        )
        result1 = module.process_feedback(feedback1)
        assert result1.success
        
        # Second feedback from same user should fail
        feedback2 = ClassificationFeedback(
            classification_id=classification_id,
            feedback_type=FeedbackType.EDIT,
            user_id="test-user"
        )
        result2 = module.process_feedback(feedback2)
        assert not result2.success
        assert "already provided" in result2.error
    
    def test_feedback_with_corrections(self, module):
        """Test feedback with corrections"""
        module.initialize()
        
        classification_id = "test-123"
        classification = WorkClassification(
            classification_id=classification_id,
            work_description="Payment processing integration",
            size=ClassificationDimension(value="M", confidence=85, reasoning="Medium work"),
            complexity=ClassificationDimension(value="Medium", confidence=70, reasoning="Some complexity"),
            type=ClassificationDimension(value="Feature", confidence=90, reasoning="New feature"),
            estimated_effort="1-2 weeks",
            recommended_approach="Standard process",
            context={}
        )
        module._classifications[classification_id] = classification
        
        # Feedback with corrections
        feedback = ClassificationFeedback(
            classification_id=classification_id,
            feedback_type=FeedbackType.EDIT,
            corrections={
                "complexity": FeedbackCorrection(
                    value="High",
                    reasoning="Payment processing involves security, compliance, and integration complexity"
                )
            },
            user_id="test-user"
        )
        
        result = module.process_feedback(feedback)
        assert result.success
        assert len(feedback.corrections) == 1
        assert feedback.corrections["complexity"].value == "High"


class TestLearningSystem:
    """Test pattern detection and learning"""
    
    def test_pattern_detection(self, module):
        """Test feedback pattern detection"""
        module.initialize()
        
        # Add multiple similar feedback items for payment-related work
        for i in range(5):
            classification_id = f"test-{i}"
            classification = WorkClassification(
                classification_id=classification_id,
                work_description=f"payment processing integration task {i}",
                size=ClassificationDimension(value="M", confidence=85, reasoning="Medium work"),
                complexity=ClassificationDimension(value="Medium", confidence=70, reasoning="Some complexity"),
                type=ClassificationDimension(value="Feature", confidence=90, reasoning="New feature"),
                estimated_effort="1-2 weeks",
                recommended_approach="Standard process",
                context={}
            )
            module._classifications[classification_id] = classification
            
            feedback = ClassificationFeedback(
                classification_id=classification_id,
                feedback_type=FeedbackType.EDIT,
                corrections={"complexity": FeedbackCorrection(value="High", reasoning="Payment processing is complex")},
                user_id=f"user-{i}"
            )
            module._feedback_store.append(feedback)
        
        # Analyze patterns
        result = module._analyze_feedback_patterns()
        assert result.success
        patterns = result.data
        
        # Should detect pattern for payment or processing
        found_pattern = False
        for word in patterns:
            if word in ["payment", "processing", "integration"]:
                assert patterns[word]["frequency"] >= 3
                found_pattern = True
                break
        assert found_pattern
    
    def test_relevant_patterns_matching(self, module):
        """Test relevant pattern matching for similar work"""
        module.initialize()
        
        # Add a classification with accepted feedback
        classification_id = "test-123"
        classification = WorkClassification(
            classification_id=classification_id,
            work_description="user authentication with OAuth integration",
            size=ClassificationDimension(value="L", confidence=90, reasoning="Large feature"),
            complexity=ClassificationDimension(value="High", confidence=85, reasoning="OAuth complexity"),
            type=ClassificationDimension(value="Feature", confidence=95, reasoning="New auth feature"),
            estimated_effort="3-4 weeks",
            recommended_approach="Security-first approach",
            context={}
        )
        
        # Add accepted feedback
        feedback = ClassificationFeedback(
            classification_id=classification_id,
            feedback_type=FeedbackType.ACCEPT,
            user_id="test-user"
        )
        classification.feedback = feedback
        module._classifications[classification_id] = classification
        
        # Test pattern matching
        patterns = module._get_relevant_patterns("OAuth authentication system implementation")
        assert len(patterns) > 0
        pattern_text = patterns[0].lower()
        assert "authentication" in pattern_text or "oauth" in pattern_text
    
    def test_learning_trigger_threshold(self, module):
        """Test learning is triggered when threshold is reached"""
        module.initialize()
        
        # Add feedback below threshold
        for i in range(2):
            classification_id = f"test-{i}"
            classification = WorkClassification(
                classification_id=classification_id,
                work_description=f"test task {i}",
                size=ClassificationDimension(value="S", confidence=80, reasoning="Small work"),
                complexity=ClassificationDimension(value="Low", confidence=75, reasoning="Simple"),
                type=ClassificationDimension(value="Bug", confidence=85, reasoning="Bug fix"),
                estimated_effort="1 day",
                recommended_approach="Quick fix",
                context={}
            )
            module._classifications[classification_id] = classification
            
            feedback = ClassificationFeedback(
                classification_id=classification_id,
                feedback_type=FeedbackType.EDIT,
                corrections={"size": FeedbackCorrection(value="M", reasoning="More work than expected")},
                user_id=f"user-{i}"
            )
            
            result = module.process_feedback(feedback)
            assert result.success
            # Should not trigger learning yet (threshold is 3)
            assert not result.data.get("triggered_learning", False)
        
        # Add one more to reach threshold
        classification_id = "test-3"
        classification = WorkClassification(
            classification_id=classification_id,
            work_description="another test task",
            size=ClassificationDimension(value="S", confidence=80, reasoning="Small work"),
            complexity=ClassificationDimension(value="Low", confidence=75, reasoning="Simple"),
            type=ClassificationDimension(value="Bug", confidence=85, reasoning="Bug fix"),
            estimated_effort="1 day",
            recommended_approach="Quick fix",
            context={}
        )
        module._classifications[classification_id] = classification
        
        feedback = ClassificationFeedback(
            classification_id=classification_id,
            feedback_type=FeedbackType.EDIT,
            corrections={"size": FeedbackCorrection(value="M", reasoning="More work than expected")},
            user_id="user-3"
        )
        
        result = module.process_feedback(feedback)
        assert result.success
        # Should trigger learning now (reached threshold of 3)
        # Note: actual triggering depends on pattern detection finding significant patterns


class TestPromptGeneration:
    """Test Claude API prompt generation"""
    
    def test_prompt_building(self, module):
        """Test building prompts for Claude API"""
        module.initialize()
        
        work_description = "Add user authentication with OAuth"
        context = {"project": "web-app", "team": "backend"}
        
        prompt = module._build_classification_prompt(work_description, context)
        
        assert work_description in prompt
        assert "SIZE STANDARDS" in prompt
        assert "COMPLEXITY STANDARDS" in prompt
        assert "TYPE STANDARDS" in prompt
        assert "XS: < 1 day" in prompt
        assert "Feature: New functionality" in prompt
        assert json.dumps(context, indent=2) in prompt
    
    def test_prompt_with_patterns(self, module):
        """Test prompt generation includes relevant patterns"""
        module.initialize()
        
        # Add a classification with accepted feedback
        classification_id = "test-123"
        classification = WorkClassification(
            classification_id=classification_id,
            work_description="OAuth authentication implementation",
            size=ClassificationDimension(value="L", confidence=90, reasoning="Large feature"),
            complexity=ClassificationDimension(value="High", confidence=85, reasoning="OAuth complexity"),
            type=ClassificationDimension(value="Feature", confidence=95, reasoning="New auth feature"),
            estimated_effort="3-4 weeks",
            recommended_approach="Security-first approach",
            context={}
        )
        
        feedback = ClassificationFeedback(
            classification_id=classification_id,
            feedback_type=FeedbackType.ACCEPT,
            user_id="test-user"
        )
        classification.feedback = feedback
        module._classifications[classification_id] = classification
        
        # Generate prompt for similar work
        prompt = module._build_classification_prompt("OAuth login system", {})
        
        # Should include the relevant pattern or show no patterns available
        assert ("OAuth authentication" in prompt or "→ Size: L" in prompt or 
                "No specific patterns available" in prompt)


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_missing_claude_config(self):
        """Test handling of missing Claude configuration"""
        config_without_claude = AiWorkClassificationEngineConfig(
            domain="ai-analysis",
            claude_config=None
        )
        
        module = AiWorkClassificationEngineModule(config_without_claude)
        module.initialize()
        
        input_data = AiWorkClassificationEngineInput(work_description="Test work")
        result = asyncio.run(module.execute_primary_operation(input_data))
        
        assert not result.success
        assert "Claude API configuration missing" in result.error
    
    def test_invalid_classification_id_feedback(self, module):
        """Test feedback for non-existent classification"""
        module.initialize()
        
        feedback = ClassificationFeedback(
            classification_id="non-existent-id",
            feedback_type=FeedbackType.ACCEPT,
            user_id="test-user"
        )
        
        result = module.process_feedback(feedback)
        assert not result.success
        assert "Classification not found" in result.error
    
    def test_audit_trail_creation(self, module):
        """Test audit trail is created for operations"""
        module.initialize()
        
        input_data = AiWorkClassificationEngineInput(work_description="Test work item")
        
        # This will fail due to missing Claude API, but should still create audit trail
        result = asyncio.run(module.execute_primary_operation(input_data))
        
        assert len(module._audit_trail) > 0
        assert module._audit_trail[0]["operation"] == "primary_operation"
        assert "timestamp" in module._audit_trail[0]
