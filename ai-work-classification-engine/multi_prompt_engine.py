"""
Multi-Prompt Engine for Self-Improving AI Work Classification

This module implements the multi-prompt architecture for enhanced accuracy,
consistency, and automatic optimization of the classification system.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import anthropic

from classification_types import (
    AiWorkClassificationEngineConfig,
    AiWorkClassificationEngineInput,
    AiWorkClassificationEngineOutput,
    ClassificationDimension,
    OperationResult
)

logger = logging.getLogger(__name__)

class MultiPromptClassificationEngine:
    """Enhanced classification engine using multiple Claude Sonnet 4 prompts"""
    
    def __init__(self, config: AiWorkClassificationEngineConfig):
        self.config = config
        self.client = anthropic.Anthropic(api_key=config.claude_config.api_key)
        
    async def enhanced_classify(self, work_description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhanced classification using multiple prompts for quality and consistency
        
        Process:
        1. Primary classification
        2. Quality assessment  
        3. Context optimization (if needed)
        4. Consistency validation
        5. Final result with confidence scoring
        """
        try:
            # Step 1: Primary classification
            primary_result = await self._primary_classify(work_description, context)
            
            # Step 2: Quality assessment
            quality_assessment = await self._assess_classification_quality(
                work_description, primary_result, context
            )
            
            # Step 3: Context optimization if quality is low
            enhanced_context = context
            if quality_assessment["quality_score"] < 85:
                context_suggestions = await self._optimize_context(
                    work_description, primary_result, quality_assessment
                )
                enhanced_context = self._merge_context(context, context_suggestions)
                
                # Re-classify with enhanced context
                primary_result = await self._primary_classify(work_description, enhanced_context)
            
            # Step 4: Consistency validation
            consistency_check = await self._validate_consistency(work_description, primary_result)
            
            # Step 5: Calculate final confidence
            final_confidence = self._calculate_overall_confidence(
                primary_result, quality_assessment, consistency_check
            )
            
            return {
                "classification": primary_result,
                "quality_assessment": quality_assessment,
                "context_enhancements": enhanced_context if enhanced_context != context else None,
                "consistency_validation": consistency_check,
                "final_confidence": final_confidence,
                "multi_prompt_analysis": True
            }
            
        except Exception as e:
            logger.error(f"Enhanced classification failed: {e}")
            # Fallback to primary classification
            return {
                "classification": await self._primary_classify(work_description, context),
                "quality_assessment": {"quality_score": 50, "issues": [str(e)]},
                "final_confidence": 50,
                "multi_prompt_analysis": False
            }
    
    async def _primary_classify(self, work_description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Primary classification prompt - same as current implementation"""
        
        prompt = f"""Classify this work item:

"{work_description}"

Context: {json.dumps(context, indent=2)}

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

Respond with valid JSON in this exact format:
{{
  "size": {{"value": "XS|S|M|L|XL|XXL", "confidence": 0-100, "reasoning": "brief explanation"}},
  "complexity": {{"value": "Low|Medium|High|Critical", "confidence": 0-100, "reasoning": "brief explanation"}},
  "type": {{"value": "Feature|Enhancement|Bug|Infrastructure|Migration|Research|Epic", "confidence": 0-100, "reasoning": "brief explanation"}},
  "estimated_effort": "human readable estimate",
  "recommended_approach": "suggested process or framework"
}}"""

        message = await asyncio.to_thread(
            self.client.messages.create,
            model=self.config.claude_config.model,
            max_tokens=self.config.claude_config.max_tokens,
            temperature=self.config.claude_config.temperature,
            system="You are an expert work classification system. Analyze work descriptions and classify them precisely according to the provided standards. Always respond with valid JSON in the exact format specified.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        claude_text = message.content[0].text
        
        # Extract JSON from response
        if "```json" in claude_text:
            json_start = claude_text.find("```json") + 7
            json_end = claude_text.find("```", json_start)
            claude_text = claude_text[json_start:json_end].strip()
        
        return json.loads(claude_text)
    
    async def _assess_classification_quality(self, work_description: str, classification: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Quality assessment prompt to evaluate classification accuracy"""
        
        quality_prompt = f"""You are a Classification Quality Auditor. Analyze this work classification for quality and accuracy.

Work Description: "{work_description}"
Context: {json.dumps(context, indent=2)}

Classification Result:
{json.dumps(classification, indent=2)}

Assess the quality by evaluating:

1. **Confidence Appropriateness**: Are the confidence scores reasonable given the information available?
2. **Reasoning Quality**: Is the reasoning detailed, specific, and logical?
3. **Consistency**: Does this classification align with typical patterns for this type of work?
4. **Context Utilization**: How well did the classification use the provided context?
5. **Missing Information**: What additional context or information would improve this classification?

Respond with JSON:
{{
  "quality_score": 0-100,
  "confidence_appropriateness": {{"score": 0-100, "reasoning": "..."}},
  "reasoning_quality": {{"score": 0-100, "issues": ["..."]}},
  "consistency_score": 0-100,
  "context_utilization": 0-100,
  "improvement_suggestions": [
    "Specific suggestion 1",
    "Specific suggestion 2"
  ],
  "missing_context": [
    "team_experience_level",
    "technology_stack_familiarity"
  ],
  "overall_assessment": "excellent|good|needs_improvement|poor"
}}"""

        message = await asyncio.to_thread(
            self.client.messages.create,
            model=self.config.claude_config.model,
            max_tokens=2048,
            temperature=0.1,
            system="You are an expert quality auditor for work classification systems. Provide detailed, constructive analysis to improve classification accuracy.",
            messages=[{"role": "user", "content": quality_prompt}]
        )
        
        claude_text = message.content[0].text
        if "```json" in claude_text:
            json_start = claude_text.find("```json") + 7
            json_end = claude_text.find("```", json_start)
            claude_text = claude_text[json_start:json_end].strip()
        
        return json.loads(claude_text)
    
    async def _optimize_context(self, work_description: str, classification: Dict[str, Any], quality_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Context optimization prompt to enhance context for better accuracy"""
        
        context_prompt = f"""You are a Context Engineering Expert. Analyze this work item and suggest context enhancements.

Work Description: "{work_description}"

Current Classification:
{json.dumps(classification, indent=2)}

Quality Issues Identified:
{json.dumps(quality_assessment.get("improvement_suggestions", []), indent=2)}

Missing Context Identified:
{json.dumps(quality_assessment.get("missing_context", []), indent=2)}

Based on this analysis, what specific context should be added to improve classification accuracy?

Consider:
- Team factors (size, experience, velocity)
- Technical factors (stack, complexity, dependencies)
- Business factors (priority, compliance, risk)
- Process factors (testing, documentation, deployment)

Respond with JSON:
{{
  "recommended_context_additions": {{
    "team_context": {{...}},
    "technical_context": {{...}},
    "business_context": {{...}},
    "process_context": {{...}}
  }},
  "dynamic_rules_suggestions": [
    {{
      "trigger_keywords": ["oauth", "authentication"],
      "context_additions": {{...}},
      "reasoning": "..."
    }}
  ],
  "expected_impact": "estimated accuracy improvement",
  "confidence": 0-100
}}"""

        message = await asyncio.to_thread(
            self.client.messages.create,
            model=self.config.claude_config.model,
            max_tokens=2048,
            temperature=0.2,
            system="You are an expert in context engineering for AI systems. Provide specific, actionable context recommendations.",
            messages=[{"role": "user", "content": context_prompt}]
        )
        
        claude_text = message.content[0].text
        if "```json" in claude_text:
            json_start = claude_text.find("```json") + 7
            json_end = claude_text.find("```", json_start)
            claude_text = claude_text[json_start:json_end].strip()
        
        return json.loads(claude_text)
    
    async def _validate_consistency(self, work_description: str, classification: Dict[str, Any]) -> Dict[str, Any]:
        """Consistency validation prompt to check against similar work patterns"""
        
        # Mock similar work for now (in production, query actual database)
        similar_work = [
            {"description": "OAuth login system", "size": "L", "complexity": "Medium", "type": "Feature"},
            {"description": "User authentication with Google", "size": "M", "complexity": "Medium", "type": "Feature"}
        ]
        
        consistency_prompt = f"""You are a Consistency Validation Expert. Check if this classification is consistent with similar work.

Current Work: "{work_description}"
Current Classification: {json.dumps(classification, indent=2)}

Similar Past Work:
{json.dumps(similar_work, indent=2)}

Analyze:
1. Is this classification consistent with similar work?
2. Are there any outliers or inconsistencies?
3. What adjustments would improve consistency?
4. How confident are you in this consistency assessment?

Respond with JSON:
{{
  "consistency_score": 0-100,
  "is_consistent": true/false,
  "outliers_detected": [
    {{
      "dimension": "size|complexity|type",
      "issue": "description of inconsistency",
      "suggested_adjustment": "..."
    }}
  ],
  "pattern_alignment": "excellent|good|poor",
  "confidence_in_assessment": 0-100,
  "recommendations": ["..."]
}}"""

        message = await asyncio.to_thread(
            self.client.messages.create,
            model=self.config.claude_config.model,
            max_tokens=1024,
            temperature=0.1,
            system="You are an expert in classification consistency analysis. Ensure similar work gets similar classifications.",
            messages=[{"role": "user", "content": consistency_prompt}]
        )
        
        claude_text = message.content[0].text
        if "```json" in claude_text:
            json_start = claude_text.find("```json") + 7
            json_end = claude_text.find("```", json_start)
            claude_text = claude_text[json_start:json_end].strip()
        
        return json.loads(claude_text)
    
    def _merge_context(self, base_context: Dict[str, Any], enhancements: Dict[str, Any]) -> Dict[str, Any]:
        """Intelligently merge context enhancements"""
        merged = base_context.copy()
        
        if "recommended_context_additions" in enhancements:
            for category, additions in enhancements["recommended_context_additions"].items():
                if isinstance(additions, dict):
                    merged.update(additions)
        
        return merged
    
    def _calculate_overall_confidence(self, classification: Dict[str, Any], quality: Dict[str, Any], consistency: Dict[str, Any]) -> int:
        """Calculate overall confidence based on multiple factors"""
        
        # Classification confidence (average of dimensions)
        class_conf = (
            classification["size"]["confidence"] + 
            classification["complexity"]["confidence"] + 
            classification["type"]["confidence"]
        ) / 3
        
        # Quality confidence
        quality_conf = quality.get("quality_score", 50)
        
        # Consistency confidence  
        consistency_conf = consistency.get("consistency_score", 50)
        
        # Weighted average (classification=50%, quality=30%, consistency=20%)
        overall = (class_conf * 0.5) + (quality_conf * 0.3) + (consistency_conf * 0.2)
        
        return int(overall)

class PatternAnalysisEngine:
    """Analyzes classification patterns for system optimization"""
    
    def __init__(self, config: AiWorkClassificationEngineConfig):
        self.config = config
        self.client = anthropic.Anthropic(api_key=config.claude_config.api_key)
    
    async def analyze_classification_patterns(self, classifications: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in classification data for optimization opportunities"""
        
        pattern_prompt = f"""You are a Pattern Recognition Expert for AI classification systems.

Analyze these {len(classifications)} work classifications for improvement opportunities:

Classifications Data:
{json.dumps(classifications[:10], indent=2)}  # Limit for prompt size

Identify:

1. **Consistency Patterns**: 
   - Similar work that gets different classifications
   - Work types with high classification variance
   - Confidence patterns by work type

2. **Accuracy Indicators**:
   - Low confidence classifications that need context
   - High confidence classifications that could be wrong
   - Missing context patterns

3. **Coverage Gaps**:
   - Work types not well represented in training
   - Edge cases causing uncertainty
   - New scenario opportunities

4. **Optimization Opportunities**:
   - Context rules that would improve accuracy
   - Prompt modifications for better consistency
   - Scenario additions for better coverage

Respond with detailed JSON analysis:
{{
  "consistency_analysis": {{
    "variance_score": 0-100,
    "inconsistent_patterns": [
      {{
        "work_type": "...",
        "variance_issue": "...",
        "examples": ["...", "..."],
        "suggested_fix": "..."
      }}
    ]
  }},
  "accuracy_indicators": {{
    "low_confidence_domains": ["...", "..."],
    "high_risk_classifications": [
      {{
        "work": "...",
        "issue": "...",
        "confidence": 0-100
      }}
    ],
    "context_gaps": ["...", "..."]
  }},
  "coverage_analysis": {{
    "well_covered_domains": ["...", "..."],
    "under_represented_domains": ["...", "..."],
    "missing_scenarios": [
      {{
        "domain": "...",
        "scenario_type": "...",
        "priority": "high|medium|low"
      }}
    ]
  }},
  "optimization_recommendations": [
    {{
      "type": "context_rule|prompt_update|scenario_addition",
      "priority": "high|medium|low",
      "description": "...",
      "expected_impact": "...",
      "implementation": "..."
    }}
  ],
  "overall_health_score": 0-100,
  "improvement_potential": "..."
}}"""

        message = await asyncio.to_thread(
            self.client.messages.create,
            model=self.config.claude_config.model,
            max_tokens=4096,
            temperature=0.2,
            system="You are an expert AI system analyst specializing in classification pattern recognition and optimization.",
            messages=[{"role": "user", "content": pattern_prompt}]
        )
        
        claude_text = message.content[0].text
        if "```json" in claude_text:
            json_start = claude_text.find("```json") + 7
            json_end = claude_text.find("```", json_start)
            claude_text = claude_text[json_start:json_end].strip()
        
        return json.loads(claude_text)

class ScenarioGenerationEngine:
    """Automatically generates new scenarios based on classification gaps"""
    
    def __init__(self, config: AiWorkClassificationEngineConfig):
        self.config = config
        self.client = anthropic.Anthropic(api_key=config.claude_config.api_key)
    
    async def generate_scenarios_for_gaps(self, gap_analysis: Dict[str, Any], current_scenarios: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate new scenarios to fill coverage gaps"""
        
        scenario_prompt = f"""You are a Product Development Scenario Expert.

Current Scenario Library ({len(current_scenarios)} scenarios):
{json.dumps(current_scenarios, indent=2)}

Gap Analysis:
{json.dumps(gap_analysis, indent=2)}

Generate 5-10 new product development scenarios to fill the identified gaps.

For each scenario, provide:

{{
  "title": "Specific scenario name",
  "description": "Detailed description of the work type",
  "domain": "web-development|mobile|api|database|devops|security|ui-ux|testing|ml|integration",
  "expected_classification": {{
    "size": "XS|S|M|L|XL|XXL",
    "complexity": "Low|Medium|High|Critical", 
    "type": "Feature|Enhancement|Bug|Infrastructure|Migration|Research|Epic"
  }},
  "tags": ["keyword1", "keyword2", "keyword3"],
  "examples": [
    "Concrete example 1",
    "Concrete example 2", 
    "Concrete example 3"
  ],
  "success_patterns": [
    "What typically works for this scenario",
    "Key success factors",
    "Common approaches"
  ],
  "context_requirements": {{
    "team_factors": ["..."],
    "technical_factors": ["..."],
    "business_factors": ["..."]
  }},
  "rationale": "Why this scenario fills an important gap"
}}

Focus on scenarios that will:
1. Improve classification consistency
2. Cover underrepresented work types  
3. Handle edge cases better
4. Provide clear classification boundaries

Respond with JSON array of scenarios."""

        message = await asyncio.to_thread(
            self.client.messages.create,
            model=self.config.claude_config.model,
            max_tokens=6144,
            temperature=0.3,
            system="You are an expert in product development patterns and scenario design. Create comprehensive, realistic scenarios that improve AI classification systems.",
            messages=[{"role": "user", "content": scenario_prompt}]
        )
        
        claude_text = message.content[0].text
        if "```json" in claude_text:
            json_start = claude_text.find("```json") + 7
            json_end = claude_text.find("```", json_start)
            claude_text = claude_text[json_start:json_end].strip()
        
        return json.loads(claude_text)

class PromptOptimizationEngine:
    """Optimizes prompts for better accuracy and consistency"""
    
    def __init__(self, config: AiWorkClassificationEngineConfig):
        self.config = config
        self.client = anthropic.Anthropic(api_key=config.claude_config.api_key)
    
    async def optimize_prompts(self, performance_data: Dict[str, Any], current_prompts: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance and suggest prompt optimizations"""
        
        optimization_prompt = f"""You are a Prompt Engineering Expert specializing in work classification systems.

Current System Performance:
{json.dumps(performance_data, indent=2)}

Current Prompts:
{json.dumps(current_prompts, indent=2)}

Analyze the performance data and current prompts to identify optimization opportunities.

Focus on:
1. **Accuracy Improvements**: How can prompts be modified to improve classification accuracy?
2. **Consistency Enhancements**: What prompt changes would reduce variance in similar work classifications?
3. **Confidence Optimization**: How can prompts be adjusted to improve confidence calibration?
4. **Domain Specialization**: Should prompts be specialized for different domains?

Provide specific, actionable prompt optimization recommendations:

{{
  "system_message_optimizations": {{
    "current_issues": ["..."],
    "recommended_changes": ["..."],
    "expected_impact": "..."
  }},
  "user_prompt_optimizations": {{
    "structure_improvements": ["..."],
    "content_enhancements": ["..."],
    "format_adjustments": ["..."]
  }},
  "domain_specific_prompts": [
    {{
      "domain": "security_work",
      "specialized_prompt": "...",
      "use_cases": ["..."],
      "expected_improvement": "..."
    }}
  ],
  "confidence_calibration": {{
    "current_issues": ["..."],
    "calibration_techniques": ["..."],
    "scoring_improvements": ["..."]
  }},
  "implementation_priority": [
    {{
      "change": "...",
      "priority": "high|medium|low",
      "effort": "...",
      "impact": "..."
    }}
  ]
}}"""

        message = await asyncio.to_thread(
            self.client.messages.create,
            model=self.config.claude_config.model,
            max_tokens=4096,
            temperature=0.2,
            system="You are a world-class prompt engineering expert. Provide specific, technical recommendations for optimizing AI classification prompts.",
            messages=[{"role": "user", "content": optimization_prompt}]
        )
        
        claude_text = message.content[0].text
        if "```json" in claude_text:
            json_start = claude_text.find("```json") + 7
            json_end = claude_text.find("```", json_start)
            claude_text = claude_text[json_start:json_end].strip()
        
        return json.loads(claude_text)

# Integration with main classification engine
class SelfImprovingClassificationEngine:
    """Main engine that orchestrates all improvement processes"""
    
    def __init__(self, config: AiWorkClassificationEngineConfig):
        self.config = config
        self.multi_prompt = MultiPromptClassificationEngine(config)
        self.pattern_analyzer = PatternAnalysisEngine(config)
        self.scenario_generator = ScenarioGenerationEngine(config)
        self.prompt_optimizer = PromptOptimizationEngine(config)
        
        self.classifications_since_analysis = 0
        self.improvement_cycle_threshold = 10
    
    async def classify_with_improvement(self, work_description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Classify work and trigger improvement cycles as needed"""
        
        # Enhanced classification
        result = await self.multi_prompt.enhanced_classify(work_description, context)
        
        # Increment counter
        self.classifications_since_analysis += 1
        
        # Trigger improvement cycle if threshold reached
        if self.classifications_since_analysis >= self.improvement_cycle_threshold:
            await self._trigger_improvement_cycle()
            self.classifications_since_analysis = 0
        
        return result
    
    async def _trigger_improvement_cycle(self):
        """Automated improvement cycle"""
        logger.info("🔄 Triggering automated improvement cycle")
        
        # Get recent classifications for analysis
        recent_classifications = []  # Load from storage
        
        # Analyze patterns
        pattern_analysis = await self.pattern_analyzer.analyze_classification_patterns(recent_classifications)
        
        # Generate new scenarios if gaps identified
        if pattern_analysis.get("coverage_analysis", {}).get("missing_scenarios"):
            new_scenarios = await self.scenario_generator.generate_scenarios_for_gaps(
                pattern_analysis, recent_classifications
            )
            # Auto-add scenarios with high confidence
            for scenario in new_scenarios:
                if scenario.get("confidence", 0) > 80:
                    await self._add_scenario_to_library(scenario)
        
        # Apply safe optimizations automatically
        for rec in pattern_analysis.get("optimization_recommendations", []):
            if rec.get("priority") == "high" and rec.get("safe_to_auto_apply", False):
                await self._apply_optimization(rec)
        
        logger.info("🎯 Improvement cycle completed")
    
    async def _add_scenario_to_library(self, scenario: Dict[str, Any]):
        """Add new scenario to library"""
        # Implementation to save scenario
        pass
    
    async def _apply_optimization(self, optimization: Dict[str, Any]):
        """Apply safe optimization automatically"""
        # Implementation to apply optimization
        pass
