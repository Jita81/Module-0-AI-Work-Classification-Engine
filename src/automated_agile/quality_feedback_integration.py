"""
Quality Feedback Integration for Automated Agile

Integrates feedback from the Integrated Quality System (AI Review + Framework Validation)
into the automated agile process for continuous improvement and recursive optimization.
"""

import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import statistics

from ..core.quality_gates.integrated_quality_system import IntegratedQualitySystem, IntegratedQualityReport


@dataclass
class QualityTrend:
    """Quality trend analysis over time."""
    metric_name: str
    current_value: float
    previous_value: float
    trend_direction: str  # 'improving', 'declining', 'stable'
    change_percentage: float
    significance: str  # 'high', 'medium', 'low'


@dataclass
class ImprovementSuggestion:
    """Suggestion for framework improvement based on quality feedback."""
    category: str  # 'pattern', 'template', 'validation', 'threshold'
    priority: str  # 'critical', 'high', 'medium', 'low'
    description: str
    implementation_effort: str  # 'low', 'medium', 'high'
    expected_impact: str  # 'high', 'medium', 'low'
    affected_components: List[str]


@dataclass
class SprintQualityAnalysis:
    """Quality analysis for sprint retrospective."""
    sprint_id: str
    quality_trends: List[QualityTrend]
    improvement_suggestions: List[ImprovementSuggestion]
    success_metrics: Dict[str, float]
    framework_evolution_recommendations: List[str]
    generated_at: str


class QualityFeedbackIntegration:
    """
    Integrates quality feedback into automated agile processes.
    
    Uses AI Code Review and Framework Validation feedback to:
    - Identify improvement patterns
    - Optimize framework templates
    - Adjust quality thresholds
    - Generate sprint retrospective insights
    - Drive recursive self-improvement
    """
    
    def __init__(self, framework_root: str = "."):
        """Initialize quality feedback integration."""
        self.framework_root = Path(framework_root)
        self.quality_history_dir = self.framework_root / "quality-history"
        self.quality_history_dir.mkdir(exist_ok=True)
        
        self.quality_system = IntegratedQualitySystem()
        self.min_data_points = 5  # Minimum samples for trend analysis
    
    async def analyze_quality_trends(self, days_back: int = 30) -> List[QualityTrend]:
        """
        Analyze quality trends over time to identify improvement patterns.
        
        Args:
            days_back: Number of days to analyze
            
        Returns:
            List[QualityTrend]: Quality trends analysis
        """
        # Load historical quality data
        historical_data = await self._load_quality_history(days_back)
        
        if len(historical_data) < self.min_data_points:
            return []
        
        trends = []
        
        # Analyze AI Review score trends
        ai_scores = [d.get('ai_review_score', 0) for d in historical_data if d.get('ai_review_score')]
        if len(ai_scores) >= self.min_data_points:
            ai_trend = self._analyze_metric_trend('ai_review_score', ai_scores)
            trends.append(ai_trend)
        
        # Analyze Framework Validation score trends
        framework_scores = [d.get('framework_score', 0) for d in historical_data if d.get('framework_score')]
        if len(framework_scores) >= self.min_data_points:
            framework_trend = self._analyze_metric_trend('framework_validation_score', framework_scores)
            trends.append(framework_trend)
        
        # Analyze Overall Quality score trends
        overall_scores = [d.get('overall_score', 0) for d in historical_data if d.get('overall_score')]
        if len(overall_scores) >= self.min_data_points:
            overall_trend = self._analyze_metric_trend('overall_quality_score', overall_scores)
            trends.append(overall_trend)
        
        # Analyze issue frequency trends
        issue_counts = [d.get('issues_count', 0) for d in historical_data]
        if len(issue_counts) >= self.min_data_points:
            issue_trend = self._analyze_metric_trend('issues_per_analysis', issue_counts, lower_is_better=True)
            trends.append(issue_trend)
        
        return trends
    
    async def generate_improvement_suggestions(self, 
                                             quality_reports: List[IntegratedQualityReport]) -> List[ImprovementSuggestion]:
        """
        Generate improvement suggestions based on quality feedback patterns.
        
        Args:
            quality_reports: Recent quality analysis reports
            
        Returns:
            List[ImprovementSuggestion]: Improvement recommendations
        """
        suggestions = []
        
        # Analyze common AI review issues
        ai_issues = []
        for report in quality_reports:
            ai_issues.extend(report.ai_review.issues)
        
        # Pattern recognition for AI issues
        ai_suggestions = self._analyze_ai_issue_patterns(ai_issues)
        suggestions.extend(ai_suggestions)
        
        # Analyze framework validation issues
        framework_issues = []
        for report in quality_reports:
            framework_issues.extend(report.framework_validation.issues)
        
        # Pattern recognition for framework issues
        framework_suggestions = self._analyze_framework_issue_patterns(framework_issues)
        suggestions.extend(framework_suggestions)
        
        # Analyze quality score patterns
        score_suggestions = self._analyze_score_patterns(quality_reports)
        suggestions.extend(score_suggestions)
        
        # Prioritize suggestions by impact and frequency
        suggestions.sort(key=lambda s: (
            {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}[s.priority],
            {'high': 3, 'medium': 2, 'low': 1}[s.expected_impact]
        ), reverse=True)
        
        return suggestions[:10]  # Return top 10 suggestions
    
    async def generate_sprint_quality_analysis(self, sprint_id: str) -> SprintQualityAnalysis:
        """
        Generate comprehensive quality analysis for sprint retrospective.
        
        Args:
            sprint_id: Sprint identifier
            
        Returns:
            SprintQualityAnalysis: Complete sprint quality analysis
        """
        # Load sprint-specific quality data
        sprint_data = await self._load_sprint_quality_data(sprint_id)
        
        # Analyze quality trends
        quality_trends = await self.analyze_quality_trends(days_back=7)  # Sprint duration
        
        # Generate improvement suggestions
        recent_reports = await self._load_recent_quality_reports(days_back=7)
        improvement_suggestions = await self.generate_improvement_suggestions(recent_reports)
        
        # Calculate success metrics
        success_metrics = self._calculate_sprint_success_metrics(sprint_data)
        
        # Generate framework evolution recommendations
        evolution_recommendations = await self._generate_framework_evolution_recommendations(
            quality_trends, improvement_suggestions
        )
        
        return SprintQualityAnalysis(
            sprint_id=sprint_id,
            quality_trends=quality_trends,
            improvement_suggestions=improvement_suggestions,
            success_metrics=success_metrics,
            framework_evolution_recommendations=evolution_recommendations,
            generated_at=datetime.now().isoformat()
        )
    
    async def update_framework_based_on_feedback(self, 
                                               suggestions: List[ImprovementSuggestion]) -> Dict[str, Any]:
        """
        Update framework templates and patterns based on quality feedback.
        
        Args:
            suggestions: Improvement suggestions to implement
            
        Returns:
            Dict: Results of framework updates
        """
        updates_applied = []
        errors = []
        
        for suggestion in suggestions:
            if suggestion.priority in ['critical', 'high'] and suggestion.implementation_effort == 'low':
                try:
                    # Apply low-effort, high-impact improvements automatically
                    result = await self._apply_improvement_suggestion(suggestion)
                    updates_applied.append({
                        'suggestion': suggestion.description,
                        'result': result,
                        'components_updated': suggestion.affected_components
                    })
                except Exception as e:
                    errors.append({
                        'suggestion': suggestion.description,
                        'error': str(e)
                    })
        
        return {
            'updates_applied': updates_applied,
            'errors': errors,
            'total_suggestions': len(suggestions),
            'auto_applied': len(updates_applied),
            'manual_review_needed': len([s for s in suggestions 
                                       if s.implementation_effort in ['medium', 'high']])
        }
    
    def _analyze_metric_trend(self, metric_name: str, values: List[float], 
                            lower_is_better: bool = False) -> QualityTrend:
        """Analyze trend for a specific metric."""
        if len(values) < 2:
            return QualityTrend(metric_name, values[0] if values else 0, 0, 'stable', 0, 'low')
        
        recent_values = values[-5:]  # Last 5 data points
        older_values = values[:-5] if len(values) > 5 else values[:-2]
        
        current_avg = statistics.mean(recent_values)
        previous_avg = statistics.mean(older_values) if older_values else recent_values[0]
        
        change_percentage = ((current_avg - previous_avg) / previous_avg * 100) if previous_avg != 0 else 0
        
        # Determine trend direction
        if abs(change_percentage) < 5:
            trend_direction = 'stable'
            significance = 'low'
        elif (change_percentage > 0 and not lower_is_better) or (change_percentage < 0 and lower_is_better):
            trend_direction = 'improving'
            significance = 'high' if abs(change_percentage) > 15 else 'medium'
        else:
            trend_direction = 'declining'
            significance = 'high' if abs(change_percentage) > 15 else 'medium'
        
        return QualityTrend(
            metric_name=metric_name,
            current_value=current_avg,
            previous_value=previous_avg,
            trend_direction=trend_direction,
            change_percentage=change_percentage,
            significance=significance
        )
    
    def _analyze_ai_issue_patterns(self, issues: List[Dict[str, Any]]) -> List[ImprovementSuggestion]:
        """Analyze patterns in AI review issues to generate suggestions."""
        suggestions = []
        
        # Group issues by type
        issue_types = {}
        for issue in issues:
            issue_type = issue.get('type', 'unknown')
            if issue_type not in issue_types:
                issue_types[issue_type] = []
            issue_types[issue_type].append(issue)
        
        # Generate suggestions for frequent issue types
        for issue_type, type_issues in issue_types.items():
            if len(type_issues) >= 3:  # Frequent issue
                if 'security' in issue_type.lower():
                    suggestions.append(ImprovementSuggestion(
                        category='template',
                        priority='high',
                        description=f"Update templates to prevent common {issue_type} issues",
                        implementation_effort='medium',
                        expected_impact='high',
                        affected_components=['templates', 'patterns', 'generators']
                    ))
                elif 'performance' in issue_type.lower():
                    suggestions.append(ImprovementSuggestion(
                        category='pattern',
                        priority='medium',
                        description=f"Optimize framework patterns for {issue_type} improvements",
                        implementation_effort='medium',
                        expected_impact='medium',
                        affected_components=['patterns', 'generators']
                    ))
        
        return suggestions
    
    def _analyze_framework_issue_patterns(self, issues: List[Dict[str, Any]]) -> List[ImprovementSuggestion]:
        """Analyze patterns in framework validation issues."""
        suggestions = []
        
        # Group by severity
        high_severity_issues = [i for i in issues if i.get('severity') == 'high']
        
        if len(high_severity_issues) >= 2:
            suggestions.append(ImprovementSuggestion(
                category='validation',
                priority='high',
                description="Strengthen framework validation rules to catch structural issues earlier",
                implementation_effort='medium',
                expected_impact='high',
                affected_components=['quality_gates', 'validators']
            ))
        
        return suggestions
    
    def _analyze_score_patterns(self, reports: List[IntegratedQualityReport]) -> List[ImprovementSuggestion]:
        """Analyze quality score patterns for optimization opportunities."""
        suggestions = []
        
        ai_scores = [r.ai_review.score for r in reports if r.ai_review.score is not None]
        framework_scores = [r.framework_validation.score for r in reports if r.framework_validation.score is not None]
        
        if ai_scores and statistics.mean(ai_scores) < 80:
            suggestions.append(ImprovementSuggestion(
                category='template',
                priority='medium',
                description="Improve code generation templates to achieve higher AI review scores",
                implementation_effort='high',
                expected_impact='high',
                affected_components=['templates', 'generators']
            ))
        
        if framework_scores and statistics.mean(framework_scores) < 85:
            suggestions.append(ImprovementSuggestion(
                category='pattern',
                priority='medium',
                description="Enhance framework patterns to improve structural compliance",
                implementation_effort='medium',
                expected_impact='medium',
                affected_components=['patterns', 'structure']
            ))
        
        return suggestions
    
    async def _apply_improvement_suggestion(self, suggestion: ImprovementSuggestion) -> str:
        """Apply a specific improvement suggestion automatically."""
        # This would contain actual implementation logic
        # For now, return a simulation of the update
        return f"Applied improvement: {suggestion.description}"
    
    def _calculate_sprint_success_metrics(self, sprint_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate success metrics for the sprint."""
        if not sprint_data:
            return {}
        
        metrics = {}
        
        # Quality gate pass rate
        passed_analyses = len([d for d in sprint_data if d.get('passed', False)])
        metrics['quality_gate_pass_rate'] = (passed_analyses / len(sprint_data)) * 100
        
        # Average quality scores
        ai_scores = [d.get('ai_review_score', 0) for d in sprint_data if d.get('ai_review_score')]
        if ai_scores:
            metrics['average_ai_review_score'] = statistics.mean(ai_scores)
        
        framework_scores = [d.get('framework_score', 0) for d in sprint_data if d.get('framework_score')]
        if framework_scores:
            metrics['average_framework_score'] = statistics.mean(framework_scores)
        
        overall_scores = [d.get('overall_score', 0) for d in sprint_data if d.get('overall_score')]
        if overall_scores:
            metrics['average_overall_score'] = statistics.mean(overall_scores)
        
        # Issue resolution rate
        total_issues = sum(d.get('issues_count', 0) for d in sprint_data)
        resolved_issues = sum(d.get('resolved_issues', 0) for d in sprint_data)
        if total_issues > 0:
            metrics['issue_resolution_rate'] = (resolved_issues / total_issues) * 100
        
        return metrics
    
    async def _generate_framework_evolution_recommendations(self, 
                                                          trends: List[QualityTrend],
                                                          suggestions: List[ImprovementSuggestion]) -> List[str]:
        """Generate framework evolution recommendations."""
        recommendations = []
        
        # Analyze declining trends
        declining_trends = [t for t in trends if t.trend_direction == 'declining' and t.significance == 'high']
        for trend in declining_trends:
            recommendations.append(
                f"Address declining {trend.metric_name} trend (down {abs(trend.change_percentage):.1f}%)"
            )
        
        # High-priority suggestions
        critical_suggestions = [s for s in suggestions if s.priority == 'critical']
        for suggestion in critical_suggestions:
            recommendations.append(f"Critical: {suggestion.description}")
        
        # Pattern optimizations
        if any('template' in s.category for s in suggestions):
            recommendations.append("Review and optimize code generation templates based on quality feedback")
        
        if any('pattern' in s.category for s in suggestions):
            recommendations.append("Enhance framework patterns to address common quality issues")
        
        return recommendations
    
    async def _load_quality_history(self, days_back: int) -> List[Dict[str, Any]]:
        """Load historical quality data."""
        # Simulate loading historical data
        # In real implementation, this would load from stored quality reports
        return []
    
    async def _load_sprint_quality_data(self, sprint_id: str) -> List[Dict[str, Any]]:
        """Load quality data for specific sprint."""
        # Simulate loading sprint-specific data
        return []
    
    async def _load_recent_quality_reports(self, days_back: int) -> List[IntegratedQualityReport]:
        """Load recent quality reports."""
        # Simulate loading recent reports
        return []


# Integration with existing automated agile process
async def integrate_quality_feedback_into_sprint(sprint_id: str) -> Dict[str, Any]:
    """
    Integrate quality feedback into sprint retrospective and planning.
    
    Args:
        sprint_id: Sprint identifier
        
    Returns:
        Dict: Quality feedback integration results
    """
    feedback_integration = QualityFeedbackIntegration()
    
    # Generate sprint quality analysis
    sprint_analysis = await feedback_integration.generate_sprint_quality_analysis(sprint_id)
    
    # Apply automatic improvements
    update_results = await feedback_integration.update_framework_based_on_feedback(
        sprint_analysis.improvement_suggestions
    )
    
    return {
        'sprint_id': sprint_id,
        'quality_trends': len(sprint_analysis.quality_trends),
        'improvement_suggestions': len(sprint_analysis.improvement_suggestions),
        'automatic_updates': update_results['auto_applied'],
        'manual_review_needed': update_results['manual_review_needed'],
        'framework_evolution_recommendations': sprint_analysis.framework_evolution_recommendations,
        'success_metrics': sprint_analysis.success_metrics
    }


if __name__ == "__main__":
    # Demo quality feedback integration
    async def demo():
        print("🔄 Quality Feedback Integration Demo")
        
        integration = QualityFeedbackIntegration()
        
        # Analyze quality trends
        trends = await integration.analyze_quality_trends()
        print(f"📈 Quality trends analyzed: {len(trends)}")
        
        # Generate sprint analysis
        sprint_analysis = await integration.generate_sprint_quality_analysis("sprint-002")
        print(f"📋 Sprint analysis complete")
        print(f"   • Quality trends: {len(sprint_analysis.quality_trends)}")
        print(f"   • Improvement suggestions: {len(sprint_analysis.improvement_suggestions)}")
        print(f"   • Framework recommendations: {len(sprint_analysis.framework_evolution_recommendations)}")
    
    asyncio.run(demo())
