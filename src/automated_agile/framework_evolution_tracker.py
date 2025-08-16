"""
Framework Evolution Tracker

Tracks framework improvements and optimizations based on quality feedback,
enabling recursive self-improvement through data-driven decisions.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EvolutionEvent:
    """Single framework evolution event."""
    event_id: str
    timestamp: str
    event_type: str  # 'pattern_update', 'template_optimization', 'quality_threshold_adjustment'
    trigger: str  # 'quality_feedback', 'manual', 'automated_analysis'
    description: str
    affected_components: List[str]
    quality_impact: Optional[Dict[str, float]]  # Before/after quality metrics
    success_metrics: Dict[str, Any]


@dataclass
class FrameworkEvolutionSummary:
    """Summary of framework evolution over time."""
    total_events: int
    events_by_type: Dict[str, int]
    events_by_trigger: Dict[str, int]
    quality_improvements: Dict[str, float]
    most_improved_components: List[str]
    success_rate: float
    generated_at: str


class FrameworkEvolutionTracker:
    """
    Tracks and analyzes framework evolution for recursive self-improvement.
    
    This tracker:
    - Records all framework changes and their triggers
    - Analyzes the impact of changes on quality metrics
    - Identifies successful evolution patterns
    - Guides future framework improvements
    - Enables data-driven recursive self-improvement
    """
    
    def __init__(self, framework_root: str = "."):
        """Initialize framework evolution tracker."""
        self.framework_root = Path(framework_root)
        self.evolution_log = self.framework_root / "framework-evolution.json"
        self.evolution_history = self._load_evolution_history()
    
    def record_evolution_event(self, 
                             event_type: str,
                             trigger: str,
                             description: str,
                             affected_components: List[str],
                             quality_impact: Optional[Dict[str, float]] = None) -> str:
        """
        Record a framework evolution event.
        
        Args:
            event_type: Type of evolution (pattern_update, template_optimization, etc.)
            trigger: What triggered this change (quality_feedback, manual, etc.)
            description: Description of the change
            affected_components: Components that were modified
            quality_impact: Quality metrics before/after if available
            
        Returns:
            str: Event ID
        """
        event_id = f"evolution_{len(self.evolution_history) + 1:03d}_{int(datetime.now().timestamp())}"
        
        event = EvolutionEvent(
            event_id=event_id,
            timestamp=datetime.now().isoformat(),
            event_type=event_type,
            trigger=trigger,
            description=description,
            affected_components=affected_components,
            quality_impact=quality_impact,
            success_metrics={}
        )
        
        self.evolution_history.append(event)
        self._save_evolution_history()
        
        return event_id
    
    def update_event_success_metrics(self, event_id: str, success_metrics: Dict[str, Any]):
        """Update success metrics for an evolution event."""
        for event in self.evolution_history:
            if event.event_id == event_id:
                event.success_metrics = success_metrics
                self._save_evolution_history()
                break
    
    def analyze_evolution_patterns(self) -> Dict[str, Any]:
        """
        Analyze patterns in framework evolution to guide future improvements.
        
        Returns:
            Dict: Analysis of evolution patterns and success factors
        """
        if not self.evolution_history:
            return {'status': 'no_data', 'message': 'No evolution events recorded yet'}
        
        analysis = {
            'total_events': len(self.evolution_history),
            'event_types': self._analyze_event_types(),
            'trigger_analysis': self._analyze_triggers(),
            'success_patterns': self._analyze_success_patterns(),
            'component_impact': self._analyze_component_impact(),
            'quality_trends': self._analyze_quality_trends(),
            'recommendations': self._generate_evolution_recommendations()
        }
        
        return analysis
    
    def get_evolution_summary(self) -> FrameworkEvolutionSummary:
        """Get summary of framework evolution."""
        events_by_type = {}
        events_by_trigger = {}
        quality_improvements = {}
        
        for event in self.evolution_history:
            # Count by type
            events_by_type[event.event_type] = events_by_type.get(event.event_type, 0) + 1
            
            # Count by trigger
            events_by_trigger[event.trigger] = events_by_trigger.get(event.trigger, 0) + 1
            
            # Track quality improvements
            if event.quality_impact:
                for metric, improvement in event.quality_impact.items():
                    if metric not in quality_improvements:
                        quality_improvements[metric] = []
                    quality_improvements[metric].append(improvement)
        
        # Calculate average improvements
        avg_improvements = {}
        for metric, improvements in quality_improvements.items():
            avg_improvements[metric] = sum(improvements) / len(improvements)
        
        # Identify most improved components
        component_frequency = {}
        for event in self.evolution_history:
            for component in event.affected_components:
                component_frequency[component] = component_frequency.get(component, 0) + 1
        
        most_improved = sorted(component_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Calculate success rate (events with positive quality impact)
        successful_events = len([e for e in self.evolution_history 
                               if e.quality_impact and any(v > 0 for v in e.quality_impact.values())])
        success_rate = (successful_events / len(self.evolution_history)) * 100 if self.evolution_history else 0
        
        return FrameworkEvolutionSummary(
            total_events=len(self.evolution_history),
            events_by_type=events_by_type,
            events_by_trigger=events_by_trigger,
            quality_improvements=avg_improvements,
            most_improved_components=[comp for comp, _ in most_improved],
            success_rate=success_rate,
            generated_at=datetime.now().isoformat()
        )
    
    def get_improvement_suggestions(self) -> List[Dict[str, Any]]:
        """Get data-driven suggestions for framework improvements."""
        if len(self.evolution_history) < 3:
            return [{
                'type': 'info',
                'message': 'Need more evolution data to generate specific suggestions',
                'recommendation': 'Continue using the framework and quality feedback integration'
            }]
        
        suggestions = []
        patterns = self.analyze_evolution_patterns()
        
        # Analyze successful patterns
        if patterns.get('success_patterns'):
            successful_types = patterns['success_patterns'].get('successful_event_types', [])
            if successful_types:
                suggestions.append({
                    'type': 'pattern_optimization',
                    'priority': 'high',
                    'message': f"Most successful evolution types: {', '.join(successful_types)}",
                    'recommendation': f"Focus on {successful_types[0]} improvements for maximum impact"
                })
        
        # Analyze component impact
        if patterns.get('component_impact'):
            high_impact_components = patterns['component_impact'].get('high_impact_components', [])
            if high_impact_components:
                suggestions.append({
                    'type': 'component_focus',
                    'priority': 'medium',
                    'message': f"Components with highest improvement impact: {', '.join(high_impact_components)}",
                    'recommendation': f"Prioritize improvements to {high_impact_components[0]} for maximum quality gains"
                })
        
        # Analyze trigger effectiveness
        if patterns.get('trigger_analysis'):
            effective_triggers = patterns['trigger_analysis'].get('most_effective_triggers', [])
            if effective_triggers:
                suggestions.append({
                    'type': 'process_optimization',
                    'priority': 'medium',
                    'message': f"Most effective improvement triggers: {', '.join(effective_triggers)}",
                    'recommendation': f"Increase use of {effective_triggers[0]} for better results"
                })
        
        return suggestions
    
    def _analyze_event_types(self) -> Dict[str, Any]:
        """Analyze distribution and success of different event types."""
        type_counts = {}
        type_success = {}
        
        for event in self.evolution_history:
            event_type = event.event_type
            type_counts[event_type] = type_counts.get(event_type, 0) + 1
            
            # Determine success (positive quality impact)
            if event.quality_impact and any(v > 0 for v in event.quality_impact.values()):
                type_success[event_type] = type_success.get(event_type, 0) + 1
        
        # Calculate success rates
        success_rates = {}
        for event_type, count in type_counts.items():
            success_rates[event_type] = (type_success.get(event_type, 0) / count) * 100
        
        return {
            'distribution': type_counts,
            'success_rates': success_rates,
            'most_common': max(type_counts, key=type_counts.get) if type_counts else None,
            'most_successful': max(success_rates, key=success_rates.get) if success_rates else None
        }
    
    def _analyze_triggers(self) -> Dict[str, Any]:
        """Analyze what triggers lead to successful improvements."""
        trigger_counts = {}
        trigger_success = {}
        
        for event in self.evolution_history:
            trigger = event.trigger
            trigger_counts[trigger] = trigger_counts.get(trigger, 0) + 1
            
            if event.quality_impact and any(v > 0 for v in event.quality_impact.values()):
                trigger_success[trigger] = trigger_success.get(trigger, 0) + 1
        
        success_rates = {}
        for trigger, count in trigger_counts.items():
            success_rates[trigger] = (trigger_success.get(trigger, 0) / count) * 100
        
        return {
            'distribution': trigger_counts,
            'success_rates': success_rates,
            'most_effective_triggers': sorted(success_rates, key=success_rates.get, reverse=True)[:3]
        }
    
    def _analyze_success_patterns(self) -> Dict[str, Any]:
        """Identify patterns in successful evolution events."""
        successful_events = [e for e in self.evolution_history 
                           if e.quality_impact and any(v > 0 for v in e.quality_impact.values())]
        
        if not successful_events:
            return {'status': 'no_successful_events'}
        
        # Analyze successful event types
        successful_types = {}
        for event in successful_events:
            successful_types[event.event_type] = successful_types.get(event.event_type, 0) + 1
        
        # Analyze successful components
        successful_components = {}
        for event in successful_events:
            for component in event.affected_components:
                successful_components[component] = successful_components.get(component, 0) + 1
        
        return {
            'successful_event_types': sorted(successful_types, key=successful_types.get, reverse=True),
            'successful_components': sorted(successful_components, key=successful_components.get, reverse=True)[:5],
            'success_rate': (len(successful_events) / len(self.evolution_history)) * 100
        }
    
    def _analyze_component_impact(self) -> Dict[str, Any]:
        """Analyze which components have the highest improvement impact."""
        component_impacts = {}
        
        for event in self.evolution_history:
            if event.quality_impact:
                avg_impact = sum(event.quality_impact.values()) / len(event.quality_impact)
                for component in event.affected_components:
                    if component not in component_impacts:
                        component_impacts[component] = []
                    component_impacts[component].append(avg_impact)
        
        # Calculate average impact per component
        avg_impacts = {}
        for component, impacts in component_impacts.items():
            avg_impacts[component] = sum(impacts) / len(impacts)
        
        return {
            'component_impacts': avg_impacts,
            'high_impact_components': sorted(avg_impacts, key=avg_impacts.get, reverse=True)[:3]
        }
    
    def _analyze_quality_trends(self) -> Dict[str, Any]:
        """Analyze quality improvement trends over time."""
        if not self.evolution_history:
            return {}
        
        # Track quality metrics over time
        quality_timeline = []
        for event in self.evolution_history:
            if event.quality_impact:
                quality_timeline.append({
                    'timestamp': event.timestamp,
                    'metrics': event.quality_impact
                })
        
        if len(quality_timeline) < 2:
            return {'status': 'insufficient_data'}
        
        # Calculate trends
        first_metrics = quality_timeline[0]['metrics']
        last_metrics = quality_timeline[-1]['metrics']
        
        trends = {}
        for metric in first_metrics:
            if metric in last_metrics:
                change = last_metrics[metric] - first_metrics[metric]
                trends[metric] = {
                    'change': change,
                    'trend': 'improving' if change > 0 else 'declining' if change < 0 else 'stable'
                }
        
        return {
            'quality_trends': trends,
            'overall_trend': 'improving' if sum(t['change'] for t in trends.values()) > 0 else 'declining'
        }
    
    def _generate_evolution_recommendations(self) -> List[str]:
        """Generate recommendations for future framework evolution."""
        recommendations = []
        
        if len(self.evolution_history) < 5:
            recommendations.append("Collect more evolution data to improve recommendations")
            return recommendations
        
        patterns = self.analyze_evolution_patterns()
        
        # Based on successful event types
        if patterns.get('event_types', {}).get('most_successful'):
            most_successful = patterns['event_types']['most_successful']
            recommendations.append(f"Focus on {most_successful} improvements (highest success rate)")
        
        # Based on trigger analysis
        if patterns.get('trigger_analysis', {}).get('most_effective_triggers'):
            effective_trigger = patterns['trigger_analysis']['most_effective_triggers'][0]
            recommendations.append(f"Use {effective_trigger} as primary improvement trigger")
        
        # Based on component impact
        if patterns.get('component_impact', {}).get('high_impact_components'):
            high_impact = patterns['component_impact']['high_impact_components'][0]
            recommendations.append(f"Prioritize improvements to {high_impact} component")
        
        return recommendations
    
    def _load_evolution_history(self) -> List[EvolutionEvent]:
        """Load evolution history from file."""
        if not self.evolution_log.exists():
            return []
        
        try:
            with open(self.evolution_log, 'r') as f:
                data = json.load(f)
            
            return [EvolutionEvent(**event_data) for event_data in data]
        except Exception:
            return []
    
    def _save_evolution_history(self):
        """Save evolution history to file."""
        try:
            data = [event.__dict__ for event in self.evolution_history]
            with open(self.evolution_log, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save evolution history: {e}")


# Integration functions for automated agile process
def record_quality_based_improvement(improvement_type: str, 
                                    description: str,
                                    components: List[str],
                                    quality_before: Dict[str, float],
                                    quality_after: Dict[str, float]) -> str:
    """
    Record a framework improvement triggered by quality feedback.
    
    Args:
        improvement_type: Type of improvement made
        description: Description of the improvement
        components: Components that were improved
        quality_before: Quality metrics before improvement
        quality_after: Quality metrics after improvement
        
    Returns:
        str: Event ID for tracking
    """
    tracker = FrameworkEvolutionTracker()
    
    quality_impact = {}
    for metric in quality_before:
        if metric in quality_after:
            quality_impact[metric] = quality_after[metric] - quality_before[metric]
    
    return tracker.record_evolution_event(
        event_type=improvement_type,
        trigger='quality_feedback',
        description=description,
        affected_components=components,
        quality_impact=quality_impact
    )


def get_framework_evolution_status() -> Dict[str, Any]:
    """Get current framework evolution status for sprint reporting."""
    tracker = FrameworkEvolutionTracker()
    summary = tracker.get_evolution_summary()
    suggestions = tracker.get_improvement_suggestions()
    
    return {
        'evolution_summary': summary.__dict__,
        'improvement_suggestions': suggestions,
        'analysis': tracker.analyze_evolution_patterns()
    }


if __name__ == "__main__":
    # Demo framework evolution tracking
    tracker = FrameworkEvolutionTracker()
    
    print("🔄 Framework Evolution Tracker Demo")
    print(f"📊 Total evolution events: {len(tracker.evolution_history)}")
    
    if tracker.evolution_history:
        summary = tracker.get_evolution_summary()
        print(f"📈 Success rate: {summary.success_rate:.1f}%")
        print(f"🔧 Most improved components: {', '.join(summary.most_improved_components[:3])}")
        
        suggestions = tracker.get_improvement_suggestions()
        print(f"💡 Improvement suggestions: {len(suggestions)}")
        for suggestion in suggestions[:3]:
            print(f"   • {suggestion['message']}")
    else:
        print("📋 No evolution events recorded yet - start using quality feedback integration!")
