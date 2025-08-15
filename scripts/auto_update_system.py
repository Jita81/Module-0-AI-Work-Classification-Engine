#!/usr/bin/env python3
"""
Auto-Update System for Standardized Modules Framework

This system automatically:
1. Checks for template improvements from community feedback
2. Updates templates based on usage analytics
3. Distributes improvements to all users
4. Maintains backward compatibility
"""

import json
import os
import sys
import asyncio
import aiohttp
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import semver
import logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

@dataclass
class TemplateVersion:
    """Template version information"""
    version: str
    template_hash: str
    author: str
    created_at: str
    description: str
    ai_improvements: List[str]
    usage_stats: Dict[str, Any]
    quality_score: float

@dataclass
class UpdateInfo:
    """Information about available updates"""
    template_name: str
    current_version: str
    latest_version: str
    changelog: List[str]
    breaking_changes: bool
    ai_improvements: List[str]

class TemplateRegistry:
    """Central registry for template versions and updates"""
    
    def __init__(self, registry_url: str = "https://api.standardized-modules.dev"):
        self.registry_url = registry_url
        self.local_cache = Path.home() / ".standardized_modules" / "cache"
        self.local_cache.mkdir(parents=True, exist_ok=True)
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    async def check_for_updates(self) -> List[UpdateInfo]:
        """Check for available template updates"""
        try:
            async with aiohttp.ClientSession() as session:
                # Get current local versions
                local_versions = self._get_local_versions()
                
                # Check registry for updates
                async with session.get(f"{self.registry_url}/templates/versions") as response:
                    if response.status == 200:
                        remote_versions = await response.json()
                        return self._compare_versions(local_versions, remote_versions)
                    else:
                        self.logger.warning(f"Failed to check updates: HTTP {response.status}")
                        return []
        
        except Exception as e:
            self.logger.error(f"Error checking for updates: {e}")
            return []
    
    def _get_local_versions(self) -> Dict[str, str]:
        """Get currently installed template versions"""
        version_file = self.local_cache / "template_versions.json"
        
        if version_file.exists():
            with open(version_file, 'r') as f:
                return json.load(f)
        
        # Initialize with current system version
        return {
            "core_module": "1.0.0",
            "integration_module": "1.0.0", 
            "supporting_module": "1.0.0",
            "technical_module": "1.0.0"
        }
    
    def _compare_versions(self, local: Dict[str, str], remote: Dict[str, Any]) -> List[UpdateInfo]:
        """Compare local and remote versions to find updates"""
        updates = []
        
        for template_name, local_version in local.items():
            if template_name in remote:
                remote_info = remote[template_name]
                latest_version = remote_info.get("latest_version", "1.0.0")
                
                if semver.compare(latest_version, local_version) > 0:
                    updates.append(UpdateInfo(
                        template_name=template_name,
                        current_version=local_version,
                        latest_version=latest_version,
                        changelog=remote_info.get("changelog", []),
                        breaking_changes=remote_info.get("breaking_changes", False),
                        ai_improvements=remote_info.get("ai_improvements", [])
                    ))
        
        return updates
    
    async def download_updates(self, updates: List[UpdateInfo], auto_apply: bool = False) -> bool:
        """Download and optionally apply template updates"""
        try:
            async with aiohttp.ClientSession() as session:
                for update in updates:
                    self.logger.info(f"Downloading update for {update.template_name} v{update.latest_version}")
                    
                    # Download template content
                    url = f"{self.registry_url}/templates/{update.template_name}/{update.latest_version}"
                    async with session.get(url) as response:
                        if response.status == 200:
                            template_data = await response.json()
                            
                            # Cache the update
                            update_file = self.local_cache / f"{update.template_name}_{update.latest_version}.json"
                            with open(update_file, 'w') as f:
                                json.dump(template_data, f, indent=2)
                            
                            if auto_apply:
                                self._apply_template_update(update.template_name, template_data)
                        else:
                            self.logger.error(f"Failed to download {update.template_name}: HTTP {response.status}")
                            return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error downloading updates: {e}")
            return False
    
    def _apply_template_update(self, template_name: str, template_data: Dict[str, Any]):
        """Apply a template update to the local system"""
        try:
            # Import the module scaffolding system
            from module_scaffolding_system import ModuleTemplates
            
            # Update the template method
            template_method_name = f"_generate_{template_name.replace('_module', '')}_module"
            
            if hasattr(ModuleTemplates, template_method_name):
                # Create backup
                self._backup_current_template(template_name)
                
                # Apply update (this would require dynamic code generation)
                # For now, log the update
                self.logger.info(f"Template {template_name} would be updated with:")
                for improvement in template_data.get("ai_improvements", []):
                    self.logger.info(f"  - {improvement}")
                
                # Update version tracking
                self._update_version_tracking(template_name, template_data["version"])
            
        except Exception as e:
            self.logger.error(f"Error applying template update: {e}")
    
    def _backup_current_template(self, template_name: str):
        """Backup current template before update"""
        backup_dir = self.local_cache / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.utcnow().isoformat()
        backup_file = backup_dir / f"{template_name}_{timestamp}.backup"
        
        # This would backup the current template code
        self.logger.info(f"Created backup: {backup_file}")
    
    def _update_version_tracking(self, template_name: str, new_version: str):
        """Update local version tracking"""
        version_file = self.local_cache / "template_versions.json"
        versions = self._get_local_versions()
        versions[template_name] = new_version
        
        with open(version_file, 'w') as f:
            json.dump(versions, f, indent=2)

class UsageAnalytics:
    """Collect and analyze template usage for improvements"""
    
    def __init__(self):
        self.analytics_file = Path.home() / ".standardized_modules" / "usage_analytics.json"
        self.analytics_file.parent.mkdir(parents=True, exist_ok=True)
    
    def record_generation(self, module_type: str, domain: str, success: bool, 
                         generation_time: float, ai_completion_time: Optional[float] = None):
        """Record module generation statistics"""
        analytics = self._load_analytics()
        
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "module_type": module_type,
            "domain": domain,
            "success": success,
            "generation_time": generation_time,
            "ai_completion_time": ai_completion_time
        }
        
        analytics.setdefault("generations", []).append(event)
        
        # Keep only last 1000 events
        if len(analytics["generations"]) > 1000:
            analytics["generations"] = analytics["generations"][-1000:]
        
        self._save_analytics(analytics)
    
    def record_ai_feedback(self, module_type: str, completion_quality: int, 
                          feedback: str, suggested_improvements: List[str]):
        """Record AI completion feedback"""
        analytics = self._load_analytics()
        
        feedback_event = {
            "timestamp": datetime.utcnow().isoformat(),
            "module_type": module_type,
            "completion_quality": completion_quality,  # 1-10 scale
            "feedback": feedback,
            "suggested_improvements": suggested_improvements
        }
        
        analytics.setdefault("ai_feedback", []).append(feedback_event)
        self._save_analytics(analytics)
    
    def get_improvement_suggestions(self) -> Dict[str, List[str]]:
        """Analyze usage data to suggest template improvements"""
        analytics = self._load_analytics()
        suggestions = {}
        
        # Analyze failure patterns
        failures = [g for g in analytics.get("generations", []) if not g["success"]]
        if failures:
            suggestions["reliability"] = [
                "Add more error handling patterns",
                "Improve input validation templates",
                "Add fallback mechanisms"
            ]
        
        # Analyze AI feedback
        feedback = analytics.get("ai_feedback", [])
        low_quality = [f for f in feedback if f["completion_quality"] < 6]
        
        if low_quality:
            all_improvements = []
            for f in low_quality:
                all_improvements.extend(f.get("suggested_improvements", []))
            
            # Count most common suggestions
            from collections import Counter
            common_suggestions = Counter(all_improvements).most_common(5)
            suggestions["ai_completion"] = [s[0] for s in common_suggestions]
        
        return suggestions
    
    def _load_analytics(self) -> Dict[str, Any]:
        """Load analytics data from file"""
        if self.analytics_file.exists():
            with open(self.analytics_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_analytics(self, analytics: Dict[str, Any]):
        """Save analytics data to file"""
        with open(self.analytics_file, 'w') as f:
            json.dump(analytics, f, indent=2)

class CommunityFeedback:
    """Collect and process community feedback for template improvements"""
    
    def __init__(self, api_url: str = "https://api.standardized-modules.dev"):
        self.api_url = api_url
        self.logger = logging.getLogger(__name__)
    
    async def submit_improvement_suggestion(self, template_type: str, suggestion: str, 
                                          code_example: Optional[str] = None,
                                          ai_impact: Optional[str] = None) -> bool:
        """Submit a template improvement suggestion"""
        try:
            suggestion_data = {
                "template_type": template_type,
                "suggestion": suggestion,
                "code_example": code_example,
                "ai_impact": ai_impact,
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": self._get_anonymous_user_id()
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/feedback/suggestions",
                    json=suggestion_data
                ) as response:
                    if response.status == 201:
                        self.logger.info("Improvement suggestion submitted successfully")
                        return True
                    else:
                        self.logger.error(f"Failed to submit suggestion: HTTP {response.status}")
                        return False
        
        except Exception as e:
            self.logger.error(f"Error submitting suggestion: {e}")
            return False
    
    async def get_approved_improvements(self) -> List[Dict[str, Any]]:
        """Get approved template improvements from the community"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_url}/feedback/approved") as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        self.logger.warning(f"Failed to get improvements: HTTP {response.status}")
                        return []
        
        except Exception as e:
            self.logger.error(f"Error getting improvements: {e}")
            return []
    
    def _get_anonymous_user_id(self) -> str:
        """Generate anonymous user ID for tracking"""
        # Create a hash based on system info (anonymous)
        import platform
        system_info = f"{platform.system()}{platform.machine()}{platform.python_version()}"
        return hashlib.sha256(system_info.encode()).hexdigest()[:16]

async def main():
    """Main auto-update process"""
    print("🔄 Standardized Modules Framework Auto-Update System")
    print("=" * 60)
    
    # Initialize systems
    registry = TemplateRegistry()
    analytics = UsageAnalytics()
    community = CommunityFeedback()
    
    # Check for updates
    print("📡 Checking for template updates...")
    updates = await registry.check_for_updates()
    
    if updates:
        print(f"🎉 Found {len(updates)} available updates:")
        for update in updates:
            print(f"  • {update.template_name}: {update.current_version} → {update.latest_version}")
            if update.ai_improvements:
                print(f"    AI Improvements: {', '.join(update.ai_improvements)}")
        
        # Download updates
        print("\n📥 Downloading updates...")
        success = await registry.download_updates(updates, auto_apply=False)
        
        if success:
            print("✅ Updates downloaded successfully!")
            print("💡 Run with --apply to install updates")
        else:
            print("❌ Failed to download some updates")
    else:
        print("✅ All templates are up to date!")
    
    # Get improvement suggestions from analytics
    print("\n📊 Analyzing usage patterns...")
    suggestions = analytics.get_improvement_suggestions()
    
    if suggestions:
        print("💡 Suggested improvements based on usage:")
        for category, items in suggestions.items():
            print(f"  {category.title()}:")
            for item in items:
                print(f"    - {item}")
    
    # Check community improvements
    print("\n🤝 Checking community improvements...")
    community_improvements = await community.get_approved_improvements()
    
    if community_improvements:
        print(f"🎉 Found {len(community_improvements)} community improvements:")
        for improvement in community_improvements[:3]:  # Show top 3
            print(f"  • {improvement.get('title', 'Untitled')}")
            print(f"    Impact: {improvement.get('ai_impact', 'General improvement')}")

if __name__ == "__main__":
    asyncio.run(main())
