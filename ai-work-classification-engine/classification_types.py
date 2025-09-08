"""
Type definitions for ai-work-classification-engine

This module defines all data types for the AI Work Classification Engine,
including classification inputs/outputs, configuration, and domain entities.
"""

from typing import Dict, Any, List, Optional, Generic, TypeVar
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

T = TypeVar('T')

# Classification Enums
class WorkSize(Enum):
    """Work size classification"""
    XS = "XS"  # < 1 day
    S = "S"    # 1-3 days
    M = "M"    # 1-2 weeks
    L = "L"    # 2-4 weeks
    XL = "XL"  # 1-2 months
    XXL = "XXL" # 2+ months

class WorkComplexity(Enum):
    """Work complexity classification"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class WorkType(Enum):
    """Work type classification"""
    FEATURE = "Feature"
    ENHANCEMENT = "Enhancement"
    BUG = "Bug"
    INFRASTRUCTURE = "Infrastructure"
    MIGRATION = "Migration"
    RESEARCH = "Research"
    EPIC = "Epic"

class FeedbackType(Enum):
    """Types of user feedback"""
    ACCEPT = "accept"
    EDIT = "edit"
    REJECT = "reject"

# Configuration Types
@dataclass
class ClaudeApiConfig:
    """Configuration for Claude API integration"""
    api_key: str
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 1000
    temperature: float = 0.1
    timeout: int = 30

@dataclass
class ClassificationStandards:
    """Standards for work classification"""
    size_standards: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    complexity_standards: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    type_standards: Dict[str, Dict[str, Any]] = field(default_factory=dict)

@dataclass
class AiWorkClassificationEngineConfig:
    """Configuration for ai-work-classification-engine module"""
    domain: str = "ai-analysis"
    persist_audit_trail: bool = True
    max_audit_events: int = 1000
    
    # Claude API configuration
    claude_config: ClaudeApiConfig = None
    
    # Classification configuration
    classification_standards: ClassificationStandards = field(default_factory=ClassificationStandards)
    
    # Learning configuration
    learning_trigger_threshold: int = 10  # Number of feedback items to trigger learning
    pattern_confidence_threshold: float = 0.5  # Minimum confidence for pattern detection
    auto_update_config: bool = True  # Whether to automatically update configuration
    
    # MVP Feature Flags - Addressing critical feedback about over-engineering
    enable_multi_prompt_system: bool = False  # Single prompt by default (cost control)
    enable_repository_intelligence: bool = False  # No repository analysis by default
    enable_master_scenarios: bool = True  # Keep scenarios (proven value, low cost)
    enable_web_interface: bool = True  # Restore web interface as originally specified
    enable_advanced_learning: bool = False  # Basic learning only by default
    
    # File paths
    config_dir: str = "config"
    data_dir: str = "data"
    patterns_dir: str = "patterns"

# Input/Output Types
@dataclass
class ClassificationDimension:
    """A single classification dimension result"""
    value: str
    confidence: int  # 0-100
    reasoning: str

@dataclass
class AiWorkClassificationEngineInput:
    """Input data for work classification operations"""
    work_description: str
    context: Dict[str, Any] = field(default_factory=dict)
    user_id: Optional[str] = None
    project_context: Optional[str] = None

@dataclass
class AiWorkClassificationEngineOutput:
    """Output data from work classification operations"""
    classification_id: str
    size: ClassificationDimension
    complexity: ClassificationDimension
    type: ClassificationDimension
    estimated_effort: str
    recommended_approach: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    audit_trail: List[Dict[str, Any]] = field(default_factory=list)

# Feedback Types
@dataclass
class FeedbackCorrection:
    """Correction for a classification dimension"""
    value: str
    reasoning: str

@dataclass
class ClassificationFeedback:
    """User feedback on a classification"""
    classification_id: str
    feedback_type: FeedbackType
    corrections: Dict[str, FeedbackCorrection] = field(default_factory=dict)
    additional_context: Optional[str] = None
    user_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)

# Learning Types
@dataclass
class PatternDetection:
    """Detected pattern from user feedback"""
    pattern_name: str
    work_characteristics: List[str]
    correction_pattern: Dict[str, str]  # dimension -> correction pattern
    frequency: int
    confidence: float
    examples: List[str]

@dataclass
class ConfigurationUpdate:
    """Configuration update based on learning"""
    version: str
    changes: Dict[str, Any]
    pattern_source: PatternDetection
    timestamp: datetime = field(default_factory=datetime.utcnow)
    applied: bool = False

# Domain Entities
@dataclass
class WorkClassification:
    """A completed work classification"""
    classification_id: str
    work_description: str
    size: ClassificationDimension
    complexity: ClassificationDimension
    type: ClassificationDimension
    estimated_effort: str
    recommended_approach: str
    context: Dict[str, Any]
    feedback: Optional[ClassificationFeedback] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class DomainEntity:
    """Base domain entity for ai-work-classification-engine"""
    entity_id: str
    entity_type: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BusinessRule:
    """Business rule definition"""
    name: str
    description: str
    validation_function: callable = None
    is_active: bool = True



class OperationResult(Generic[T]):
    """Standard result wrapper for all operations"""
    
    def __init__(self, success: bool, data: T = None, error: str = None, error_code: str = None):
        self.success = success
        self.data = data
        self.error = error
        self.error_code = error_code
        self.timestamp = datetime.utcnow()
    
    @classmethod
    def success(cls, data: T = None) -> 'OperationResult[T]':
        """Create a successful result"""
        return cls(success=True, data=data)
    
    @classmethod
    def error(cls, error: str, error_code: str = None) -> 'OperationResult[T]':
        """Create an error result"""
        return cls(success=False, error=error, error_code=error_code)
    
    def __bool__(self) -> bool:
        return self.success

class ModuleStatus(Enum):
    """Module status enumeration"""
    INITIALIZING = "initializing"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    SHUTTING_DOWN = "shutting_down"
    SHUTDOWN = "shutdown"