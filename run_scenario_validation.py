#!/usr/bin/env python3
"""
Comprehensive Scenario Validation Test Runner
Tests AI pattern recognition with 20 positive + 10 negative examples
"""

import asyncio
import aiohttp
import json
from typing import List, Dict
import time

# Test data for AS-002: OAuth Integration (Single Provider)
POSITIVE_EXAMPLES = [
    "Integrate Google OAuth authentication into our web application with user profile synchronization and automatic account creation",
    "Add GitHub OAuth login to our developer portal so users can authenticate with their GitHub accounts and access repository information", 
    "Implement Microsoft OAuth authentication for enterprise users with Azure AD integration and automatic role assignment",
    "Add Facebook OAuth login to our social application with friend list import and profile picture synchronization",
    "Integrate LinkedIn OAuth authentication for our professional networking platform with profile data import",
    "Implement Twitter OAuth login with tweet posting capabilities and follower synchronization for our content management system",
    "Add Discord OAuth authentication to our gaming platform with server membership verification and user role synchronization",
    "Integrate Slack OAuth for our productivity app with workspace member verification and channel access permissions",
    "Implement Spotify OAuth authentication for our music discovery app with playlist access and listening history import",
    "Add Dropbox OAuth login to our file management system with folder access permissions and automatic file synchronization",
    "Integrate Zoom OAuth authentication for our scheduling app with meeting creation capabilities and calendar synchronization",
    "Implement Salesforce OAuth login for our sales dashboard with contact synchronization and opportunity tracking",
    "Add Shopify OAuth authentication to our e-commerce analytics tool with store data access and product synchronization",
    "Integrate Twitch OAuth for our streaming analytics platform with channel data access and viewer statistics import",
    "Implement Reddit OAuth authentication for our community management tool with subreddit access and post synchronization",
    "Add GitLab OAuth login to our DevOps dashboard with repository access, pipeline monitoring, and issue tracking",
    "Integrate Figma OAuth authentication for our design collaboration tool with file access and comment synchronization",
    "Implement Notion OAuth login for our productivity dashboard with workspace access and page content synchronization",
    "Add Stripe OAuth authentication to our financial dashboard with account data access and transaction history import",
    "Integrate Atlassian OAuth for our project management tool with Jira access, issue synchronization, and project tracking"
]

NEGATIVE_EXAMPLES = [
    "Build comprehensive OAuth system supporting Google, Microsoft, GitHub, and Facebook with unified user management",  # Multi-provider
    "Create email/password authentication system with password reset and session management",  # Basic auth
    "Add two-factor authentication to existing login system with SMS codes and authenticator app support",  # 2FA
    "Implement enterprise Single Sign-On with SAML 2.0 and Active Directory integration for corporate users",  # SSO/SAML
    "Fix OAuth callback URL configuration issue causing authentication failures on production",  # Bug fix
    "Implement role-based permissions system with admin, moderator, and user roles throughout the application",  # RBAC
    "Improve user session handling with timeout management, multi-device support, and session security",  # Session mgmt
    "Update password requirements, implement secure password reset flow, and add account lockout protection",  # Password security
    "Implement API authentication with JWT tokens, API key management, and rate limiting for third-party developers",  # API auth
    "Create simple user registration form with email verification and basic profile setup"  # Basic registration
]

EXPECTED_OAUTH_PATTERN = {"size": "L", "complexity": "Medium", "type": "Feature"}

async def classify_work(session: aiohttp.ClientSession, work_description: str) -> Dict:
    """Classify a work description using the API"""
    async with session.post(
        "http://localhost:8000/api/classify",
        headers={"Content-Type": "application/json"},
        json={"work_description": work_description, "context": {"test": "scenario_validation"}}
    ) as response:
        if response.status == 200:
            return await response.json()
        else:
            error_text = await response.text()
            return {"error": f"API Error {response.status}: {error_text}"}

def matches_oauth_pattern(classification: Dict) -> bool:
    """Check if classification matches expected OAuth pattern"""
    return (
        classification.get("size", {}).get("value") == EXPECTED_OAUTH_PATTERN["size"] and
        classification.get("complexity", {}).get("value") == EXPECTED_OAUTH_PATTERN["complexity"] and
        classification.get("type", {}).get("value") == EXPECTED_OAUTH_PATTERN["type"]
    )

def calculate_confidence(classification: Dict) -> float:
    """Calculate average confidence score"""
    size_conf = classification.get("size", {}).get("confidence", 0)
    complexity_conf = classification.get("complexity", {}).get("confidence", 0)
    type_conf = classification.get("type", {}).get("confidence", 0)
    return (size_conf + complexity_conf + type_conf) / 3

async def run_validation_tests():
    """Run comprehensive scenario validation tests"""
    print("🧪 COMPREHENSIVE OAUTH SCENARIO VALIDATION TEST")
    print("=" * 50)
    print()
    
    async with aiohttp.ClientSession() as session:
        # Test positive examples
        print("✅ TESTING POSITIVE EXAMPLES (Should match L/Medium/Feature):")
        print("-" * 60)
        
        positive_results = []
        for i, example in enumerate(POSITIVE_EXAMPLES, 1):
            print(f"Test {i:2d}: {example[:60]}...")
            
            result = await classify_work(session, example)
            if "error" in result:
                print(f"         ❌ ERROR: {result['error']}")
                continue
            
            matches = matches_oauth_pattern(result)
            confidence = calculate_confidence(result)
            classification = f"{result['size']['value']}/{result['complexity']['value']}/{result['type']['value']}"
            
            print(f"         🎯 Result: {classification} {'✅ MATCH' if matches else '❌ MISS'} (Conf: {confidence:.0f}%)")
            
            positive_results.append({
                "example": example,
                "matches_pattern": matches,
                "classification": classification,
                "confidence": confidence,
                "size_correct": result['size']['value'] == EXPECTED_OAUTH_PATTERN["size"],
                "complexity_correct": result['complexity']['value'] == EXPECTED_OAUTH_PATTERN["complexity"],
                "type_correct": result['type']['value'] == EXPECTED_OAUTH_PATTERN["type"]
            })
            
            await asyncio.sleep(0.5)  # Rate limiting
        
        print()
        print("❌ TESTING NEGATIVE EXAMPLES (Should NOT match L/Medium/Feature):")
        print("-" * 60)
        
        negative_results = []
        for i, example in enumerate(NEGATIVE_EXAMPLES, 1):
            print(f"Test {i:2d}: {example[:60]}...")
            
            result = await classify_work(session, example)
            if "error" in result:
                print(f"         ❌ ERROR: {result['error']}")
                continue
            
            matches_oauth = matches_oauth_pattern(result)
            confidence = calculate_confidence(result)
            classification = f"{result['size']['value']}/{result['complexity']['value']}/{result['type']['value']}"
            
            print(f"         🎯 Result: {classification} {'✅ CORRECTLY DIFFERENT' if not matches_oauth else '❌ INCORRECTLY SAME'} (Conf: {confidence:.0f}%)")
            
            negative_results.append({
                "example": example,
                "incorrectly_matches_oauth": matches_oauth,
                "classification": classification,
                "confidence": confidence
            })
            
            await asyncio.sleep(0.5)  # Rate limiting
        
        # Calculate validation metrics
        print()
        print("📊 VALIDATION RESULTS:")
        print("=" * 30)
        
        # Positive example metrics
        positive_matches = sum(1 for r in positive_results if r["matches_pattern"])
        positive_accuracy = (positive_matches / len(positive_results)) * 100 if positive_results else 0
        avg_positive_confidence = sum(r["confidence"] for r in positive_results) / len(positive_results) if positive_results else 0
        
        print(f"✅ Positive Examples: {positive_matches}/{len(positive_results)} matches ({positive_accuracy:.1f}% accuracy)")
        print(f"   📊 Average Confidence: {avg_positive_confidence:.1f}%")
        
        # Negative example metrics  
        negative_correct = sum(1 for r in negative_results if not r["incorrectly_matches_oauth"])
        negative_accuracy = (negative_correct / len(negative_results)) * 100 if negative_results else 0
        avg_negative_confidence = sum(r["confidence"] for r in negative_results) / len(negative_results) if negative_results else 0
        
        print(f"❌ Negative Examples: {negative_correct}/{len(negative_results)} correctly different ({negative_accuracy:.1f}% accuracy)")
        print(f"   📊 Average Confidence: {avg_negative_confidence:.1f}%")
        
        # Overall metrics
        overall_accuracy = ((positive_matches + negative_correct) / (len(positive_results) + len(negative_results))) * 100
        
        print()
        print(f"🎯 OVERALL PATTERN RECOGNITION: {overall_accuracy:.1f}%")
        print(f"🎯 BOUNDARY DETECTION: {negative_accuracy:.1f}%")
        print(f"📊 CONFIDENCE CALIBRATION: {(avg_positive_confidence + avg_negative_confidence)/2:.1f}%")
        
        # Detailed analysis
        print()
        print("📋 DETAILED ANALYSIS:")
        print("-" * 20)
        
        size_accuracy = sum(1 for r in positive_results if r["size_correct"]) / len(positive_results) * 100 if positive_results else 0
        complexity_accuracy = sum(1 for r in positive_results if r["complexity_correct"]) / len(positive_results) * 100 if positive_results else 0
        type_accuracy = sum(1 for r in positive_results if r["type_correct"]) / len(positive_results) * 100 if positive_results else 0
        
        print(f"   Size Classification Accuracy: {size_accuracy:.1f}%")
        print(f"   Complexity Classification Accuracy: {complexity_accuracy:.1f}%")
        print(f"   Type Classification Accuracy: {type_accuracy:.1f}%")
        
        # Recommendations
        print()
        print("💡 RECOMMENDATIONS:")
        print("-" * 18)
        if overall_accuracy >= 90:
            print("   🎉 Excellent pattern recognition! AI understands OAuth scenario boundaries.")
        elif overall_accuracy >= 75:
            print("   👍 Good pattern recognition. Consider refining examples for edge cases.")
        else:
            print("   ⚠️  Pattern recognition needs improvement. Add more training examples.")
            
        if negative_accuracy >= 90:
            print("   🎯 Excellent boundary detection! AI distinguishes OAuth from other auth methods.")
        else:
            print("   🔧 Boundary detection needs work. Refine scenario definitions for clarity.")
            
        print()
        print("🚀 AI SELF-IMPROVEMENT READY: System can now use these results to optimize itself!")

if __name__ == "__main__":
    asyncio.run(run_validation_tests())
