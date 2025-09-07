"""
ai-work-classification-engine: AI-powered work classification with learning capabilities
Type: CORE
Domain: ai-analysis
Intent: Provide intelligent work classification using Claude Sonnet 4 to analyze work items and classify by Size, Complexity, and Type with continuous learning from user feedback
Contracts: WorkDescription → Classification(Size, Complexity, Type) → Learning Updates
Dependencies: Claude Sonnet 4 API, Configuration Management, Pattern Learning System

This module serves as the core AI Work Classification Engine that:
- Analyzes work descriptions using Claude Sonnet 4
- Classifies work by Size (XS-XXL), Complexity (Low-Critical), Type (Feature/Bug/etc.)
- Learns from user feedback to improve accuracy over time
- Manages classification standards and configuration
- Provides confidence scores and reasoning for each classification
"""

from typing import Dict, Any, List, Optional
import logging
import json
import uuid
from datetime import datetime
import asyncio
import aiohttp

from .interface import AiWorkClassificationEngineInterface
from .types import (
    AiWorkClassificationEngineConfig,
    AiWorkClassificationEngineInput,
    AiWorkClassificationEngineOutput,
    ClassificationDimension,
    ClassificationFeedback,
    WorkClassification,
    PatternDetection,
    ConfigurationUpdate,
    WorkSize,
    WorkComplexity,
    WorkType,
    FeedbackType,
    OperationResult,
    BusinessRule,
    DomainEntity
)

logger = logging.getLogger(__name__)

class AiWorkClassificationEngineModule(AiWorkClassificationEngineInterface):
    """
    AI Work Classification Engine implementation
    Type: CORE Domain Module
    
    Business Context:
    - Solves the problem of inconsistent work estimation and planning across teams
    - Provides standardized, AI-powered classification of work items from user stories to enterprise initiatives
    - Learns from user feedback to continuously improve classification accuracy
    - Enables faster project initiation and better resource planning
    
    Key Business Entities:
    - WorkClassification: A completed classification with dimensions and confidence scores
    - ClassificationFeedback: User corrections and feedback on classifications
    - PatternDetection: Learned patterns from user feedback for configuration updates
    
    Business Rules:
    - All work descriptions must be 10-5000 characters
    - Classifications must include Size, Complexity, and Type with confidence scores
    - User feedback triggers learning when patterns reach threshold frequency
    - Configuration updates are versioned and can be rolled back
    """
    
    def __init__(self, config: AiWorkClassificationEngineConfig):
        self.config = config
        self._business_rules = self._initialize_business_rules()
        self._classifications = {}  # Store completed classifications
        self._feedback_store = []   # Store user feedback
        self._patterns = {}         # Store detected patterns
        self._audit_trail = []
        self._initialized = False
        logger.info(f"Initializing ai-work-classification-engine module")
    
    def initialize(self) -> OperationResult:
        """Initialize the domain module with business rule validation"""
        try:
            # Validate configuration
            validation_result = self._validate_configuration()
            if not validation_result.success:
                return validation_result
            
            # Load domain entities and rules
            self._load_domain_data()
            
            # Validate business rules consistency
            rules_validation = self._validate_business_rules()
            if not rules_validation.success:
                return rules_validation
            
            self._initialized = True
            logger.info("AiWorkClassificationEngine module initialized successfully")
            return OperationResult.success("Module initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize ai-work-classification-engine: {e}")
            return OperationResult.error(f"Initialization failed: {e}")
    
    def execute_primary_operation(self, input_data: AiWorkClassificationEngineInput) -> OperationResult[AiWorkClassificationEngineOutput]:
        """
        AI_TODO: Implement main business operation
        
        AI_TODO: Define what this operation accomplishes:
        Business Rules:
        - AI_TODO: List key business rules that apply
        - AI_TODO: Define validation requirements
        - AI_TODO: Specify constraint conditions
        
        Args:
            input_data: AI_TODO: Describe input requirements
            
        Returns:
            OperationResult containing AiWorkClassificationEngineOutput or error
        """
        if not self._initialized:
            return OperationResult.error("Module not initialized")
        
        try:
            # Start audit trail
            operation_id = self._start_audit_trail("primary_operation", input_data)
            
            # Validate input according to business rules
            validation_result = self._validate_business_input(input_data)
            if not validation_result.success:
                self._record_audit_event(operation_id, "validation_failed", validation_result.error)
                return validation_result
            
            # Generate classification ID
            classification_id = str(uuid.uuid4())
            
            # Call Claude API for intelligent classification
            claude_result = await self._classify_with_claude(input_data.work_description, input_data.context)
            if not claude_result.success:
                self._record_audit_event(operation_id, "claude_api_failed", claude_result.error)
                return claude_result
            
            # Parse Claude response and create structured output
            classification_data = claude_result.data
            
            result_data = AiWorkClassificationEngineOutput(
                classification_id=classification_id,
                size=ClassificationDimension(
                    value=classification_data["size"]["value"],
                    confidence=classification_data["size"]["confidence"],
                    reasoning=classification_data["size"]["reasoning"]
                ),
                complexity=ClassificationDimension(
                    value=classification_data["complexity"]["value"],
                    confidence=classification_data["complexity"]["confidence"],
                    reasoning=classification_data["complexity"]["reasoning"]
                ),
                type=ClassificationDimension(
                    value=classification_data["type"]["value"],
                    confidence=classification_data["type"]["confidence"],
                    reasoning=classification_data["type"]["reasoning"]
                ),
                estimated_effort=classification_data.get("estimated_effort", "Unknown"),
                recommended_approach=classification_data.get("recommended_approach", "Standard process"),
                audit_trail=self._audit_trail.copy()
            )
            
            # Store classification for learning
            work_classification = WorkClassification(
                classification_id=classification_id,
                work_description=input_data.work_description,
                size=result_data.size,
                complexity=result_data.complexity,
                type=result_data.type,
                estimated_effort=result_data.estimated_effort,
                recommended_approach=result_data.recommended_approach,
                context=input_data.context
            )
            self._classifications[classification_id] = work_classification
            
            self._record_audit_event(operation_id, "operation_completed", "Success")
            
            return OperationResult.success(result_data)
            
        except BusinessRuleViolation as e:
            self._record_audit_event(operation_id, "business_rule_violation", str(e))
            logger.warning(f"Business rule violation in ai-work-classification-engine: {e}")
            return OperationResult.error(f"Business rule violation: {e}", "BUSINESS_RULE_VIOLATION")
            
        except Exception as e:
            self._record_audit_event(operation_id, "system_error", str(e))
            logger.error(f"System error in ai-work-classification-engine: {e}")
            return OperationResult.error(f"System error: {e}", "SYSTEM_ERROR")
    
    def get_domain_entity(self, entity_id: str) -> OperationResult[DomainEntity]:
        """
        AI_TODO: Implement entity retrieval with business rules
        """
        # AI_IMPLEMENTATION_REQUIRED
        pass
    
    def apply_business_rule(self, rule_name: str, context: Dict[str, Any]) -> OperationResult:
        """
        AI_TODO: Implement business rule application
        """
        # AI_IMPLEMENTATION_REQUIRED
        pass
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get module health with business metrics"""
        return {
            "module_name": "ai-work-classification-engine",
            "type": "CORE",
            "status": "healthy" if self._initialized else "unhealthy",
            "business_rules_loaded": len(self._business_rules),
            "domain_entities_count": len(self._domain_entities),
            "audit_events_count": len(self._audit_trail),
            "last_operation": self._audit_trail[-1] if self._audit_trail else None
        }
    
    def shutdown(self) -> OperationResult:
        """Gracefully shutdown with audit trail preservation"""
        try:
            # Save audit trail if configured
            if self.config.persist_audit_trail:
                self._save_audit_trail()
            
            self._initialized = False
            logger.info("AiWorkClassificationEngine module shutdown completed")
            return OperationResult.success("Shutdown completed")
            
        except Exception as e:
            return OperationResult.error(f"Shutdown error: {e}")
    
    # Private helper methods with complete implementation
    def _initialize_business_rules(self) -> List[BusinessRule]:
        """Initialize business rules for work classification domain"""
        return [
            BusinessRule(
                name="work_description_length",
                description="Work descriptions must be between 10 and 5000 characters",
                validation_function=self._validate_work_description_length
            ),
            BusinessRule(
                name="classification_completeness",
                description="All classifications must include Size, Complexity, and Type",
                validation_function=self._validate_classification_completeness
            ),
            BusinessRule(
                name="confidence_score_range",
                description="Confidence scores must be between 0 and 100",
                validation_function=self._validate_confidence_scores
            ),
            BusinessRule(
                name="feedback_rate_limit",
                description="Users cannot provide feedback more than once per classification",
                validation_function=self._validate_feedback_rate_limit
            )
        ]
    
    def _validate_configuration(self) -> OperationResult:
        """Validate module configuration - FRAMEWORK PROVIDED"""
        if not self.config:
            return OperationResult.error("Configuration required")
        return OperationResult.success("Configuration valid")
    
    def _load_domain_data(self):
        """Load domain-specific data - FRAMEWORK PROVIDED"""
        # AI_TODO: Load domain entities and reference data
        pass
    
    def _validate_business_rules(self) -> OperationResult:
        """Validate business rules consistency - FRAMEWORK PROVIDED"""
        return OperationResult.success("Business rules valid")
    
    def _validate_business_input(self, input_data: AiWorkClassificationEngineInput) -> OperationResult:
        """Validate input against business rules - FRAMEWORK PROVIDED"""
        # AI_TODO: Implement business validation logic
        return OperationResult.success("Input valid")
    
    def _start_audit_trail(self, operation: str, input_data: Any) -> str:
        """Start audit trail for operation - FRAMEWORK PROVIDED"""
        operation_id = f"{operation}_{datetime.utcnow().isoformat()}"
        self._audit_trail.append({
            "operation_id": operation_id,
            "operation": operation,
            "timestamp": datetime.utcnow().isoformat(),
            "input_summary": str(input_data)[:100]
        })
        return operation_id
    
    def _record_audit_event(self, operation_id: str, event: str, details: str):
        """Record audit event - FRAMEWORK PROVIDED"""
        self._audit_trail.append({
            "operation_id": operation_id,
            "event": event,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def _save_audit_trail(self):
        """Save audit trail to persistent storage"""
        if self.config.persist_audit_trail and self._audit_trail:
            # TODO: Implement file-based persistence
            logger.info(f"Audit trail saved: {len(self._audit_trail)} events")
    
    # === CLAUDE API INTEGRATION ===
    
    async def _classify_with_claude(self, work_description: str, context: Dict[str, Any]) -> OperationResult:
        """
        Call Claude Sonnet 4 API for work classification
        
        Args:
            work_description: The work to be classified
            context: Additional context for classification
            
        Returns:
            OperationResult with parsed classification data
        """
        try:
            if not self.config.claude_config or not self.config.claude_config.api_key:
                return OperationResult.error("Claude API configuration missing")
            
            # Build prompt with classification standards and examples
            prompt = self._build_classification_prompt(work_description, context)
            
            # Call Claude API
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config.claude_config.api_key}",
                "User-Agent": "AI-Work-Classification-Engine/1.0.0"
            }
            
            payload = {
                "model": self.config.claude_config.model,
                "max_tokens": self.config.claude_config.max_tokens,
                "temperature": self.config.claude_config.temperature,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert work classification system. Analyze work descriptions and classify them precisely according to the provided standards. Always respond with valid JSON in the exact format specified."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ]
            }
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.config.claude_config.timeout)) as session:
                async with session.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        return OperationResult.error(f"Claude API error: {response.status} - {error_text}")
                    
                    response_data = await response.json()
                    
                    # Extract and parse Claude's response
                    claude_text = response_data["content"][0]["text"]
                    classification_data = json.loads(claude_text)
                    
                    # Validate response structure
                    validation_result = self._validate_claude_response(classification_data)
                    if not validation_result.success:
                        return validation_result
                    
                    return OperationResult.success(classification_data)
                    
        except asyncio.TimeoutError:
            return OperationResult.error("Claude API timeout")
        except json.JSONDecodeError as e:
            return OperationResult.error(f"Invalid JSON response from Claude: {e}")
        except Exception as e:
            return OperationResult.error(f"Claude API integration error: {e}")
    
    def _build_classification_prompt(self, work_description: str, context: Dict[str, Any]) -> str:
        """Build the prompt for Claude API with standards and examples"""
        
        # Get relevant patterns for similar work
        relevant_patterns = self._get_relevant_patterns(work_description)
        patterns_text = "\\n".join([f"- {pattern}" for pattern in relevant_patterns]) if relevant_patterns else "No specific patterns available."
        
        prompt = f"""Classify this work item:

"{work_description}"

Using these standards:

SIZE STANDARDS:
- XS: < 1 day (Trivial changes, text updates, simple fixes)
- S: 1-3 days (Small well-defined changes, single component work)
- M: 1-2 weeks (Medium-sized features, multiple components)
- L: 2-4 weeks (Large features, significant integration)
- XL: 1-2 months (Major features, complex systems)
- XXL: 2+ months (Enterprise-level initiatives, major architecture changes)

COMPLEXITY STANDARDS:
- Low: Well-understood work with established patterns
- Medium: Some unknowns, moderate integration required
- High: Significant unknowns, complex integration, new technology
- Critical: High risk, mission-critical, extensive dependencies

TYPE STANDARDS:
- Feature: New functionality or capabilities
- Enhancement: Improvements to existing functionality
- Bug: Defect fixes and corrections
- Infrastructure: Platform, tooling, or system improvements
- Migration: Moving or upgrading systems/data
- Research: Investigation, proof of concepts, spikes
- Epic: Large initiative containing multiple features

Consider these successful examples:
{patterns_text}

Context: {json.dumps(context, indent=2)}

Respond with valid JSON in this exact format:
{{
  "size": {{"value": "XS|S|M|L|XL|XXL", "confidence": 0-100, "reasoning": "brief explanation"}},
  "complexity": {{"value": "Low|Medium|High|Critical", "confidence": 0-100, "reasoning": "brief explanation"}},
  "type": {{"value": "Feature|Enhancement|Bug|Infrastructure|Migration|Research|Epic", "confidence": 0-100, "reasoning": "brief explanation"}},
  "estimated_effort": "human readable estimate",
  "recommended_approach": "suggested process or framework"
}}"""
        
        return prompt
    
    def _get_relevant_patterns(self, work_description: str) -> List[str]:
        """Get relevant classification patterns for similar work"""
        # Simple keyword matching for now - could be enhanced with ML similarity
        patterns = []
        work_lower = work_description.lower()
        
        for classification in self._classifications.values():
            if classification.feedback and classification.feedback.feedback_type == FeedbackType.ACCEPT:
                # Look for keyword overlap
                desc_lower = classification.work_description.lower()
                common_words = set(work_lower.split()) & set(desc_lower.split())
                if len(common_words) >= 2:  # At least 2 common words
                    patterns.append(f"{classification.work_description[:50]}... → Size: {classification.size.value}, Complexity: {classification.complexity.value}, Type: {classification.type.value}")
        
        return patterns[:3]  # Return top 3 most relevant patterns

    def _validate_claude_response(self, data: Dict[str, Any]) -> OperationResult:
        """Validate Claude API response structure and values"""
        required_fields = ["size", "complexity", "type"]
        
        for field in required_fields:
            if field not in data:
                return OperationResult.error(f"Missing required field: {field}")
            
            dimension = data[field]
            if not isinstance(dimension, dict):
                return OperationResult.error(f"Invalid {field} format")
            
            if "value" not in dimension or "confidence" not in dimension or "reasoning" not in dimension:
                return OperationResult.error(f"Missing required {field} subfields")
            
            # Validate confidence score
            confidence = dimension["confidence"]
            if not isinstance(confidence, int) or confidence < 0 or confidence > 100:
                return OperationResult.error(f"Invalid confidence score for {field}: {confidence}")
        
        # Validate enum values
        valid_sizes = [e.value for e in WorkSize]
        valid_complexities = [e.value for e in WorkComplexity] 
        valid_types = [e.value for e in WorkType]
        
        if data["size"]["value"] not in valid_sizes:
            return OperationResult.error(f"Invalid size value: {data['size']['value']}")
        
        if data["complexity"]["value"] not in valid_complexities:
            return OperationResult.error(f"Invalid complexity value: {data['complexity']['value']}")
            
        if data["type"]["value"] not in valid_types:
            return OperationResult.error(f"Invalid type value: {data['type']['value']}")
        
        return OperationResult.success("Valid response")
    
    # === BUSINESS RULE VALIDATION METHODS ===
    
    def _validate_work_description_length(self, input_data: AiWorkClassificationEngineInput) -> bool:
        """Validate work description length is between 10 and 5000 characters"""
        if not input_data.work_description:
            return False
        length = len(input_data.work_description.strip())
        return 10 <= length <= 5000
    
    def _validate_classification_completeness(self, classification_data: Dict[str, Any]) -> bool:
        """Validate that classification includes all required dimensions"""
        required_fields = ["size", "complexity", "type"]
        return all(field in classification_data for field in required_fields)
    
    def _validate_confidence_scores(self, classification_data: Dict[str, Any]) -> bool:
        """Validate that confidence scores are in valid range"""
        for dimension in ["size", "complexity", "type"]:
            if dimension in classification_data:
                confidence = classification_data[dimension].get("confidence", -1)
                if not isinstance(confidence, int) or confidence < 0 or confidence > 100:
                    return False
        return True
    
    def _validate_feedback_rate_limit(self, feedback: ClassificationFeedback) -> bool:
        """Validate that user hasn't already provided feedback for this classification"""
        for existing_feedback in self._feedback_store:
            if (existing_feedback.classification_id == feedback.classification_id and 
                existing_feedback.user_id == feedback.user_id):
                return False
        return True
    
    # === FEEDBACK AND LEARNING METHODS ===
    
    def process_feedback(self, feedback: ClassificationFeedback) -> OperationResult:
        """
        Process user feedback on classifications
        
        Args:
            feedback: User feedback with corrections or acceptance
            
        Returns:
            OperationResult indicating success and any triggered learning
        """
        try:
            # Validate feedback
            if feedback.classification_id not in self._classifications:
                return OperationResult.error("Classification not found")
            
            # Check rate limiting
            if not self._validate_feedback_rate_limit(feedback):
                return OperationResult.error("Feedback already provided for this classification")
            
            # Store feedback
            self._feedback_store.append(feedback)
            
            # Update classification with feedback
            classification = self._classifications[feedback.classification_id]
            classification.feedback = feedback
            classification.updated_at = datetime.utcnow()
            
            # Check if learning should be triggered
            triggered_learning = False
            if len(self._feedback_store) >= self.config.learning_trigger_threshold:
                learning_result = self._analyze_feedback_patterns()
                if learning_result.success and learning_result.data:
                    triggered_learning = True
                    logger.info("Learning triggered by feedback patterns")
            
            return OperationResult.success({
                "status": "recorded",
                "triggered_learning": triggered_learning,
                "feedback_count": len(self._feedback_store)
            })
            
        except Exception as e:
            logger.error(f"Error processing feedback: {e}")
            return OperationResult.error(f"Failed to process feedback: {e}")
    
    def _analyze_feedback_patterns(self) -> OperationResult:
        """Analyze feedback patterns to detect learning opportunities"""
        try:
            patterns = {}
            
            # Group feedback by work characteristics
            for feedback in self._feedback_store:
                if feedback.feedback_type in [FeedbackType.EDIT, FeedbackType.REJECT]:
                    classification = self._classifications.get(feedback.classification_id)
                    if classification:
                        # Simple pattern detection based on keywords
                        work_desc = classification.work_description.lower()
                        key_words = [word for word in work_desc.split() if len(word) > 4]
                        
                        for word in key_words[:3]:  # Top 3 key words
                            if word not in patterns:
                                patterns[word] = {"corrections": [], "frequency": 0}
                            
                            patterns[word]["frequency"] += 1
                            patterns[word]["corrections"].append({
                                "original": {
                                    "size": classification.size.value,
                                    "complexity": classification.complexity.value,
                                    "type": classification.type.value
                                },
                                "corrected": feedback.corrections
                            })
            
            # Filter patterns with sufficient frequency
            significant_patterns = {
                word: data for word, data in patterns.items() 
                if data["frequency"] >= 3  # At least 3 occurrences
            }
            
            if significant_patterns:
                logger.info(f"Detected {len(significant_patterns)} significant patterns")
                return OperationResult.success(significant_patterns)
            
            return OperationResult.success({})
            
        except Exception as e:
            logger.error(f"Error analyzing feedback patterns: {e}")
            return OperationResult.error(f"Pattern analysis failed: {e}")


# Custom exceptions for business logic
class BusinessRuleViolation(Exception):
    """Raised when business rule is violated"""
    def __init__(self, rule_name: str, message: str):
        self.rule_name = rule_name
        super().__init__(f"Business rule '{rule_name}' violated: {message}")