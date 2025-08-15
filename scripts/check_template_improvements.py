#!/usr/bin/env python3
"""
Check for template improvements based on community feedback and usage analytics
Used by GitHub Actions for automated template updates
"""

import sys
import json
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.auto_update_system import TemplateRegistry, UsageAnalytics, CommunityFeedback

async def check_improvements():
    """Check for template improvements and create update PR if needed"""
    
    analytics = UsageAnalytics()
    community = CommunityFeedback()
    
    # Get improvement suggestions
    suggestions = analytics.get_improvement_suggestions()
    community_improvements = await community.get_approved_improvements()
    
    updates_needed = False
    
    if suggestions:
        print("📊 Analytics suggest the following improvements:")
        for category, items in suggestions.items():
            print(f"  {category}: {len(items)} suggestions")
        updates_needed = True
    
    if community_improvements:
        print(f"🤝 Found {len(community_improvements)} approved community improvements")
        updates_needed = True
    
    if updates_needed:
        # Create update file for GitHub Actions to process
        update_info = {
            "analytics_suggestions": suggestions,
            "community_improvements": community_improvements,
            "timestamp": "2024-01-01T00:00:00Z"  # Would use actual timestamp
        }
        
        with open("template_updates.json", "w") as f:
            json.dump(update_info, f, indent=2)
        
        print("✅ Created template_updates.json for processing")
        
        # Exit with code 1 to trigger update workflow
        sys.exit(1)
    else:
        print("✅ No template improvements needed at this time")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(check_improvements())
