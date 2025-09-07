"""
Repository Analysis Engine for AI Work Classification

This module analyzes entire repositories using the master scenario library,
classifies components, and builds contextual understanding for future consistency.
"""

import os
import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import anthropic
import subprocess
import fnmatch

from classification_types import (
    AiWorkClassificationEngineConfig,
    ClaudeApiConfig,
    OperationResult
)

logger = logging.getLogger(__name__)

class RepositoryAnalyzer:
    """Analyzes entire repositories using master scenario library"""
    
    def __init__(self, config: AiWorkClassificationEngineConfig):
        self.config = config
        self.client = anthropic.Anthropic(api_key=config.claude_config.api_key)
        self.master_scenarios = self._load_master_scenarios()
        
    def _load_master_scenarios(self) -> List[Dict[str, Any]]:
        """Load the 100 master scenarios for repository analysis"""
        # In production, load from MASTER_SCENARIO_LIBRARY.md or database
        return [
            {
                "id": "AS-002",
                "title": "OAuth Integration (Single Provider)",
                "classification": {"size": "L", "complexity": "Medium", "type": "Feature"},
                "keywords": ["oauth", "authentication", "google", "github", "login", "auth"],
                "file_patterns": ["*auth*", "*oauth*", "*login*", "*session*"],
                "code_patterns": ["OAuth", "passport", "auth0", "firebase.auth"],
                "domain": "authentication-security"
            },
            {
                "id": "PB-001", 
                "title": "Basic Payment Integration",
                "classification": {"size": "L", "complexity": "Medium", "type": "Feature"},
                "keywords": ["payment", "stripe", "paypal", "billing", "checkout"],
                "file_patterns": ["*payment*", "*billing*", "*stripe*", "*checkout*"],
                "code_patterns": ["Stripe", "PayPal", "payment", "checkout", "billing"],
                "domain": "payment-billing"
            },
            {
                "id": "API-001",
                "title": "REST API Basic CRUD",
                "classification": {"size": "M", "complexity": "Low", "type": "Feature"},
                "keywords": ["api", "rest", "crud", "endpoint", "route"],
                "file_patterns": ["*api*", "*routes*", "*controllers*", "*endpoints*"],
                "code_patterns": ["@app.route", "router", "GET", "POST", "PUT", "DELETE"],
                "domain": "api-development"
            },
            {
                "id": "UI-001",
                "title": "Component Library Creation",
                "classification": {"size": "L", "complexity": "Low", "type": "Infrastructure"},
                "keywords": ["component", "ui", "design", "library", "storybook"],
                "file_patterns": ["*component*", "*ui*", "*.tsx", "*.jsx"],
                "code_patterns": ["React.FC", "Component", "styled", "className"],
                "domain": "ui-ux-design"
            },
            {
                "id": "DB-001",
                "title": "Basic Database Schema Design",
                "classification": {"size": "M", "complexity": "Low", "type": "Infrastructure"},
                "keywords": ["database", "schema", "model", "migration", "sql"],
                "file_patterns": ["*model*", "*schema*", "*migration*", "*.sql"],
                "code_patterns": ["CREATE TABLE", "Model", "Schema", "migration", "database"],
                "domain": "database-design"
            },
            {
                "id": "TEST-001",
                "title": "Unit Testing Implementation", 
                "classification": {"size": "M", "complexity": "Low", "type": "Infrastructure"},
                "keywords": ["test", "testing", "spec", "jest", "pytest"],
                "file_patterns": ["*test*", "*spec*", "test_*", "*_test*"],
                "code_patterns": ["test", "describe", "it", "expect", "assert"],
                "domain": "testing-qa"
            }
        ]
    
    async def analyze_repository(self, repo_path: str, repo_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Comprehensive repository analysis using master scenario library
        
        Args:
            repo_path: Local path to repository
            repo_url: Optional remote repository URL
            
        Returns:
            Complete repository analysis with scenario mapping and context
        """
        try:
            logger.info(f"🔍 Starting repository analysis: {repo_path}")
            
            # Step 1: Repository structure analysis
            repo_structure = await self._analyze_repository_structure(repo_path)
            
            # Step 2: File content analysis
            file_analysis = await self._analyze_repository_files(repo_path)
            
            # Step 3: Scenario mapping
            scenario_mapping = await self._map_repository_to_scenarios(repo_structure, file_analysis)
            
            # Step 4: Context aggregation
            context_by_scenario = await self._aggregate_context_by_scenario(scenario_mapping)
            
            # Step 5: Repository classification summary
            repo_classification = await self._classify_repository_overall(
                repo_structure, scenario_mapping, context_by_scenario
            )
            
            # Step 6: Future consistency recommendations
            consistency_guidelines = await self._generate_consistency_guidelines(
                scenario_mapping, context_by_scenario
            )
            
            return {
                "repository_path": repo_path,
                "repository_url": repo_url,
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "repository_structure": repo_structure,
                "file_analysis": file_analysis,
                "scenario_mapping": scenario_mapping,
                "context_by_scenario": context_by_scenario,
                "repository_classification": repo_classification,
                "consistency_guidelines": consistency_guidelines,
                "analysis_metadata": {
                    "total_files_analyzed": len(file_analysis.get("analyzed_files", [])),
                    "scenarios_identified": len(scenario_mapping.get("mapped_scenarios", [])),
                    "context_patterns_found": len(context_by_scenario),
                    "classification_confidence": repo_classification.get("confidence", 0)
                }
            }
            
        except Exception as e:
            logger.error(f"Repository analysis failed: {e}")
            return {"error": str(e), "analysis_failed": True}
    
    async def _analyze_repository_structure(self, repo_path: str) -> Dict[str, Any]:
        """Analyze repository structure and technology stack"""
        
        structure_prompt = f"""
        You are a Repository Structure Analyst. Analyze this repository structure:
        
        Repository Path: {repo_path}
        
        {self._get_repository_file_tree(repo_path)}
        
        Identify:
        1. **Technology Stack**: Languages, frameworks, libraries used
        2. **Architecture Pattern**: Monolith, microservices, serverless, etc.
        3. **Project Type**: Web app, mobile app, API, library, etc.
        4. **Development Stage**: Early, mature, legacy, etc.
        5. **Complexity Indicators**: Number of services, dependencies, integrations
        6. **Quality Indicators**: Testing, documentation, CI/CD presence
        
        Provide structured analysis of repository characteristics.
        """
        
        message = await asyncio.to_thread(
            self.client.messages.create,
            model=self.config.claude_config.model,
            max_tokens=2048,
            temperature=0.1,
            system="You are an expert software architect analyzing repository structures for classification purposes.",
            messages=[{"role": "user", "content": structure_prompt}]
        )
        
        claude_text = message.content[0].text
        
        # Extract structured data from Claude's response
        try:
            if "```json" in claude_text:
                json_start = claude_text.find("```json") + 7
                json_end = claude_text.find("```", json_start)
                claude_text = claude_text[json_start:json_end].strip()
                return json.loads(claude_text)
        except json.JSONDecodeError:
            pass
        
        # Return text analysis if JSON parsing fails
        return {"analysis_text": claude_text, "structured_analysis": False}
    
    async def _analyze_repository_files(self, repo_path: str) -> Dict[str, Any]:
        """Analyze key repository files for scenario identification"""
        
        # Get key files for analysis
        key_files = self._identify_key_files(repo_path)
        
        analyzed_files = []
        
        for file_path in key_files[:20]:  # Limit to prevent token overflow
            try:
                file_content = self._read_file_safely(file_path)
                if file_content:
                    file_analysis = await self._analyze_single_file(file_path, file_content)
                    analyzed_files.append({
                        "file_path": file_path,
                        "analysis": file_analysis,
                        "size": len(file_content),
                        "lines": file_content.count('\n')
                    })
            except Exception as e:
                logger.warning(f"Failed to analyze file {file_path}: {e}")
        
        return {
            "analyzed_files": analyzed_files,
            "total_files_scanned": len(key_files),
            "analysis_coverage": f"{len(analyzed_files)}/{len(key_files)} files"
        }
    
    async def _analyze_single_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Analyze single file to identify scenarios and patterns"""
        
        # Truncate content if too long
        if len(content) > 4000:
            content = content[:4000] + "\n... [truncated]"
        
        file_analysis_prompt = f"""
        Analyze this code file to identify product development scenarios:
        
        File: {file_path}
        Content:
        ```
        {content}
        ```
        
        Based on the master scenario library, identify:
        
        1. **Scenario Matches**: Which scenarios from the master library does this file represent?
        2. **Implementation Patterns**: How is the scenario implemented in this code?
        3. **Complexity Indicators**: What makes this implementation complex or simple?
        4. **Context Clues**: Team experience, technology choices, quality standards evident
        5. **Integration Points**: How does this connect to other system components?
        
        Master Scenarios for Reference:
        {json.dumps([s["id"] + ": " + s["title"] for s in self.master_scenarios], indent=2)}
        
        Provide analysis focusing on scenario identification and implementation context.
        """
        
        message = await asyncio.to_thread(
            self.client.messages.create,
            model=self.config.claude_config.model,
            max_tokens=1024,
            temperature=0.1,
            system="You are a code analysis expert specializing in identifying product development patterns and scenarios.",
            messages=[{"role": "user", "content": file_analysis_prompt}]
        )
        
        return {"analysis_text": message.content[0].text}
    
    async def _map_repository_to_scenarios(self, repo_structure: Dict[str, Any], file_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Map repository components to master scenario library"""
        
        mapping_prompt = f"""
        You are a Scenario Mapping Expert. Map this repository to master product development scenarios.
        
        Repository Structure: {json.dumps(repo_structure, indent=2)}
        File Analysis: {json.dumps([f["analysis"] for f in file_analysis.get("analyzed_files", [])], indent=2)}
        
        Master Scenario Library:
        {json.dumps(self.master_scenarios, indent=2)}
        
        For each scenario you identify in the repository:
        
        1. **Scenario Match**: Which master scenario ID best matches this component?
        2. **Implementation Evidence**: What code/files prove this scenario exists?
        3. **Classification Assessment**: How would you classify this implementation?
        4. **Context Factors**: What context affects the classification?
        5. **Quality Indicators**: Implementation maturity, testing, documentation
        6. **Integration Complexity**: How does this connect to other scenarios?
        
        Respond with JSON:
        {{
          "mapped_scenarios": [
            {{
              "scenario_id": "AS-002",
              "scenario_title": "OAuth Integration",
              "evidence_files": ["auth/oauth.py", "config/auth.js"],
              "implementation_classification": {{
                "size": "L",
                "complexity": "High", 
                "type": "Feature",
                "confidence": 85,
                "reasoning": "Complex OAuth implementation with multiple providers"
              }},
              "context_factors": {{
                "technology_stack": ["Python", "FastAPI"],
                "team_experience": "senior",
                "quality_standards": ["unit_tests", "security_review"],
                "integration_complexity": "moderate"
              }},
              "implementation_maturity": "production_ready|in_development|prototype",
              "testing_coverage": "comprehensive|basic|minimal|none"
            }}
          ],
          "unmapped_components": [
            {{
              "component_description": "Custom analytics system",
              "files": ["analytics/"],
              "potential_new_scenario": true,
              "suggested_scenario_title": "Custom Analytics Implementation"
            }}
          ],
          "repository_complexity_factors": [
            "Multi-service architecture",
            "Extensive testing suite", 
            "Production deployment configuration"
          ]
        }}
        """
        
        message = await asyncio.to_thread(
            self.client.messages.create,
            model=self.config.claude_config.model,
            max_tokens=4096,
            temperature=0.2,
            system="You are an expert at mapping code repositories to standardized product development scenarios.",
            messages=[{"role": "user", "content": mapping_prompt}]
        )
        
        claude_text = message.content[0].text
        if "```json" in claude_text:
            json_start = claude_text.find("```json") + 7
            json_end = claude_text.find("```", json_start)
            claude_text = claude_text[json_start:json_end].strip()
            return json.loads(claude_text)
        
        return {"mapping_text": claude_text, "structured_mapping": False}
    
    async def _aggregate_context_by_scenario(self, scenario_mapping: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate context by scenario for future consistency"""
        
        context_aggregation_prompt = f"""
        You are a Context Aggregation Expert. Analyze mapped scenarios to build context patterns.
        
        Scenario Mapping: {json.dumps(scenario_mapping, indent=2)}
        
        For each scenario identified, aggregate context that should be applied to future work of this type:
        
        1. **Technology Context**: Stack, frameworks, libraries used for this scenario
        2. **Team Context**: Experience level, development patterns, code quality
        3. **Business Context**: Requirements, constraints, compliance needs
        4. **Integration Context**: How this scenario connects to other system components
        5. **Quality Context**: Testing standards, documentation, deployment practices
        
        Build comprehensive context profiles that can be used for future classifications:
        
        {{
          "scenario_contexts": {{
            "AS-002": {{
              "technology_context": {{
                "primary_stack": ["Python", "FastAPI"],
                "auth_libraries": ["passport", "oauth2"],
                "security_tools": ["JWT", "bcrypt"]
              }},
              "team_context": {{
                "experience_level": "senior",
                "development_velocity": "standard",
                "code_quality_standards": "high"
              }},
              "business_context": {{
                "security_requirements": "high",
                "compliance_needs": ["OWASP", "security_audit"],
                "performance_requirements": "standard"
              }},
              "integration_context": {{
                "database_integration": true,
                "api_dependencies": ["user_management", "session_management"],
                "frontend_integration": true
              }},
              "quality_context": {{
                "testing_requirements": ["unit_tests", "integration_tests", "security_tests"],
                "documentation_standards": "comprehensive",
                "deployment_complexity": "moderate"
              }},
              "future_classification_guidance": {{
                "size_factors": ["OAuth provider count", "integration complexity"],
                "complexity_factors": ["Security requirements", "Enterprise features"],
                "type_factors": ["New vs enhancement", "Scope of implementation"]
              }}
            }}
          }},
          "cross_scenario_patterns": {{
            "common_technology_stack": ["Python", "FastAPI", "PostgreSQL"],
            "consistent_quality_standards": ["unit_tests", "documentation"],
            "team_velocity_indicators": ["senior_team", "high_standards"],
            "architectural_patterns": ["microservices", "api_first"]
          }}
        }}
        """
        
        message = await asyncio.to_thread(
            self.client.messages.create,
            model=self.config.claude_config.model,
            max_tokens=3072,
            temperature=0.1,
            system="You are an expert at aggregating development context patterns for AI classification systems.",
            messages=[{"role": "user", "content": context_aggregation_prompt}]
        )
        
        claude_text = message.content[0].text
        if "```json" in claude_text:
            json_start = claude_text.find("```json") + 7
            json_end = claude_text.find("```", json_start)
            claude_text = claude_text[json_start:json_end].strip()
            return json.loads(claude_text)
        
        return {"aggregation_text": claude_text, "structured_aggregation": False}
    
    async def _classify_repository_overall(self, repo_structure: Dict[str, Any], scenario_mapping: Dict[str, Any], context_by_scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Classify the repository as a whole and its major components"""
        
        classification_prompt = f"""
        You are a Repository Classification Expert. Classify this repository and its major components.
        
        Repository Structure: {json.dumps(repo_structure, indent=2)}
        Scenario Mapping: {json.dumps(scenario_mapping, indent=2)}
        Context by Scenario: {json.dumps(context_by_scenario, indent=2)}
        
        Provide comprehensive repository classification:
        
        1. **Overall Repository Classification**:
           - Size: Based on total scope and complexity
           - Complexity: Based on architecture, integrations, technical challenges
           - Type: Epic, Platform, Application, Library, etc.
        
        2. **Major Component Classifications**:
           - Each significant scenario/component with its classification
           - Reasoning for each classification
           - Context factors that influenced the classification
        
        3. **Development Effort Estimation**:
           - Total estimated effort for the repository
           - Breakdown by major components
           - Team size and timeline recommendations
        
        4. **Future Work Guidelines**:
           - How future changes should be classified
           - Context to apply for consistency
           - Standards to maintain
        
        Respond with structured classification analysis.
        """
        
        message = await asyncio.to_thread(
            self.client.messages.create,
            model=self.config.claude_config.model,
            max_tokens=3072,
            temperature=0.1,
            system="You are an expert at classifying software repositories and estimating development effort.",
            messages=[{"role": "user", "content": classification_prompt}]
        )
        
        return {"classification_analysis": message.content[0].text}
    
    async def _generate_consistency_guidelines(self, scenario_mapping: Dict[str, Any], context_by_scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Generate guidelines for future work consistency"""
        
        guidelines_prompt = f"""
        You are a Consistency Guidelines Expert. Generate guidelines for future work on this repository.
        
        Scenario Mapping: {json.dumps(scenario_mapping, indent=2)}
        Context by Scenario: {json.dumps(context_by_scenario, indent=2)}
        
        Create comprehensive guidelines for future work classification consistency:
        
        1. **Scenario-Specific Guidelines**: For each scenario, define how future work should be classified
        2. **Context Application Rules**: What context should be automatically applied
        3. **Classification Standards**: Size, complexity, type standards for this repository
        4. **Quality Gates**: Testing, documentation, deployment standards to maintain
        5. **Integration Considerations**: How new work should integrate with existing scenarios
        
        Focus on ensuring future work gets consistent classifications based on this repository's patterns.
        
        Respond with actionable guidelines that can be programmatically applied.
        """
        
        message = await asyncio.to_thread(
            self.client.messages.create,
            model=self.config.claude_config.model,
            max_tokens=2048,
            temperature=0.1,
            system="You are an expert at creating development standards and classification guidelines.",
            messages=[{"role": "user", "content": guidelines_prompt}]
        )
        
        return {"guidelines_text": message.content[0].text}
    
    def _get_repository_file_tree(self, repo_path: str, max_depth: int = 3) -> str:
        """Get repository file tree structure"""
        try:
            # Use tree command if available, otherwise use find
            try:
                result = subprocess.run(
                    ["tree", "-L", str(max_depth), "-I", "node_modules|__pycache__|.git|venv|dist|build"],
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    return result.stdout
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
            
            # Fallback to manual directory traversal
            tree_lines = []
            for root, dirs, files in os.walk(repo_path):
                # Skip common ignore directories
                dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', 'venv', 'dist', 'build'}]
                
                level = root.replace(repo_path, '').count(os.sep)
                if level > max_depth:
                    continue
                
                indent = '  ' * level
                tree_lines.append(f"{indent}{os.path.basename(root)}/")
                
                subindent = '  ' * (level + 1)
                for file in files[:10]:  # Limit files per directory
                    tree_lines.append(f"{subindent}{file}")
                
                if len(files) > 10:
                    tree_lines.append(f"{subindent}... and {len(files) - 10} more files")
            
            return '\n'.join(tree_lines[:100])  # Limit total lines
            
        except Exception as e:
            return f"Error generating file tree: {e}"
    
    def _identify_key_files(self, repo_path: str) -> List[str]:
        """Identify key files for analysis based on patterns and importance"""
        
        key_patterns = [
            # Configuration and setup files
            "package.json", "requirements.txt", "Dockerfile", "docker-compose.yml",
            "pyproject.toml", "setup.py", "Cargo.toml", "pom.xml",
            
            # Main application files
            "main.*", "app.*", "index.*", "server.*", "api.*",
            
            # Authentication and security
            "*auth*", "*oauth*", "*login*", "*security*",
            
            # Payment and billing
            "*payment*", "*billing*", "*stripe*", "*checkout*",
            
            # Database and models
            "*model*", "*schema*", "*migration*", "*database*",
            
            # API and routes
            "*route*", "*endpoint*", "*api*", "*controller*",
            
            # UI and components
            "*component*", "*ui*", "*view*", "*template*",
            
            # Testing
            "*test*", "*spec*", "test_*", "*_test*",
            
            # Configuration
            "config.*", "settings.*", ".env*", "*.config.*"
        ]
        
        key_files = []
        
        for root, dirs, files in os.walk(repo_path):
            # Skip common ignore directories
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', 'venv', 'dist', 'build', '.next'}]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                # Check if file matches key patterns
                for pattern in key_patterns:
                    if fnmatch.fnmatch(file.lower(), pattern.lower()):
                        key_files.append(file_path)
                        break
                
                # Also include files with important extensions
                if file.endswith(('.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.go', '.rs', '.php', '.rb')):
                    if any(keyword in file.lower() for keyword in ['main', 'app', 'server', 'api', 'auth', 'payment', 'model']):
                        key_files.append(file_path)
        
        return list(set(key_files))  # Remove duplicates
    
    def _read_file_safely(self, file_path: str, max_size: int = 50000) -> Optional[str]:
        """Safely read file content with size limits"""
        try:
            if os.path.getsize(file_path) > max_size:
                return None  # Skip large files
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception:
            return None
    
    async def analyze_repository_changes(self, repo_path: str, base_analysis: Dict[str, Any], changes: List[str]) -> Dict[str, Any]:
        """Analyze repository changes against established context patterns"""
        
        change_analysis_prompt = f"""
        You are a Change Analysis Expert. Analyze repository changes for classification consistency.
        
        Base Repository Analysis: {json.dumps(base_analysis.get("scenario_mapping", {}), indent=2)}
        Context by Scenario: {json.dumps(base_analysis.get("context_by_scenario", {}), indent=2)}
        
        Recent Changes: {json.dumps(changes, indent=2)}
        
        For each change:
        1. **Scenario Classification**: Which master scenario does this change represent?
        2. **Context Application**: What context from the base analysis should apply?
        3. **Classification Prediction**: How should this change be classified?
        4. **Consistency Check**: Is this consistent with existing patterns?
        5. **Context Updates**: Should any context be updated based on this change?
        
        Ensure new work maintains consistency with established repository patterns.
        """
        
        message = await asyncio.to_thread(
            self.client.messages.create,
            model=self.config.claude_config.model,
            max_tokens=2048,
            temperature=0.1,
            system="You are an expert at maintaining classification consistency across repository changes.",
            messages=[{"role": "user", "content": change_analysis_prompt}]
        )
        
        return {"change_analysis": message.content[0].text}

class RepositoryContextManager:
    """Manages repository-specific context for consistent future classifications"""
    
    def __init__(self, config: AiWorkClassificationEngineConfig):
        self.config = config
        self.client = anthropic.Anthropic(api_key=config.claude_config.api_key)
    
    async def build_repository_context_profile(self, repo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Build comprehensive context profile for repository"""
        
        context_profile = {
            "repository_id": repo_analysis.get("repository_path", "unknown"),
            "analysis_date": datetime.utcnow().isoformat(),
            "technology_profile": self._extract_technology_profile(repo_analysis),
            "team_profile": self._extract_team_profile(repo_analysis),
            "quality_profile": self._extract_quality_profile(repo_analysis),
            "scenario_patterns": self._extract_scenario_patterns(repo_analysis),
            "context_rules": await self._generate_repository_context_rules(repo_analysis)
        }
        
        return context_profile
    
    def _extract_technology_profile(self, repo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract technology context from repository analysis"""
        
        repo_structure = repo_analysis.get("repository_structure", {})
        
        return {
            "primary_languages": repo_structure.get("technology_stack", {}).get("languages", []),
            "frameworks": repo_structure.get("technology_stack", {}).get("frameworks", []),
            "architecture_pattern": repo_structure.get("architecture_pattern", "unknown"),
            "deployment_target": repo_structure.get("deployment_indicators", []),
            "complexity_level": repo_structure.get("complexity_indicators", "medium")
        }
    
    def _extract_team_profile(self, repo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract team context from code quality and patterns"""
        
        quality_indicators = []
        scenario_mapping = repo_analysis.get("scenario_mapping", {})
        
        # Analyze implementation maturity across scenarios
        maturity_levels = []
        for scenario in scenario_mapping.get("mapped_scenarios", []):
            maturity_levels.append(scenario.get("implementation_maturity", "unknown"))
        
        # Determine team experience based on implementation quality
        if "production_ready" in maturity_levels:
            experience_level = "senior"
        elif "in_development" in maturity_levels:
            experience_level = "intermediate"
        else:
            experience_level = "mixed"
        
        return {
            "experience_level": experience_level,
            "code_quality_standards": "high" if "comprehensive" in str(scenario_mapping) else "standard",
            "development_velocity": "standard",  # Could be enhanced with git analysis
            "team_size": "medium"  # Could be enhanced with commit analysis
        }
    
    def _extract_quality_profile(self, repo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract quality standards from repository analysis"""
        
        scenario_mapping = repo_analysis.get("scenario_mapping", {})
        
        testing_coverage = []
        documentation_levels = []
        
        for scenario in scenario_mapping.get("mapped_scenarios", []):
            testing_coverage.append(scenario.get("testing_coverage", "unknown"))
        
        return {
            "testing_standards": "comprehensive" if "comprehensive" in testing_coverage else "standard",
            "documentation_standards": "high" if any("doc" in str(scenario_mapping).lower() for _ in [1]) else "standard",
            "deployment_standards": "production" if "production" in str(scenario_mapping) else "development",
            "security_standards": "high" if any(s.get("scenario_id", "").startswith("AS-") for s in scenario_mapping.get("mapped_scenarios", [])) else "standard"
        }
    
    def _extract_scenario_patterns(self, repo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract common patterns across scenarios"""
        
        scenario_mapping = repo_analysis.get("scenario_mapping", {})
        mapped_scenarios = scenario_mapping.get("mapped_scenarios", [])
        
        patterns = {
            "dominant_domains": {},
            "complexity_patterns": {},
            "size_patterns": {},
            "type_patterns": {}
        }
        
        for scenario in mapped_scenarios:
            # Count domain occurrences
            scenario_id = scenario.get("scenario_id", "")
            domain = scenario_id.split("-")[0] if "-" in scenario_id else "unknown"
            patterns["dominant_domains"][domain] = patterns["dominant_domains"].get(domain, 0) + 1
            
            # Track classification patterns
            classification = scenario.get("implementation_classification", {})
            size = classification.get("size", "unknown")
            complexity = classification.get("complexity", "unknown")
            work_type = classification.get("type", "unknown")
            
            patterns["size_patterns"][size] = patterns["size_patterns"].get(size, 0) + 1
            patterns["complexity_patterns"][complexity] = patterns["complexity_patterns"].get(complexity, 0) + 1
            patterns["type_patterns"][work_type] = patterns["type_patterns"].get(work_type, 0) + 1
        
        return patterns
    
    async def _generate_repository_context_rules(self, repo_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate context rules specific to this repository"""
        
        rules_prompt = f"""
        Generate repository-specific context rules based on this analysis:
        
        Repository Analysis: {json.dumps(repo_analysis, indent=2)}
        
        Create context rules that will ensure future work on this repository gets classified consistently:
        
        For each pattern identified, create a rule:
        {{
          "rule_name": "descriptive_name",
          "trigger_conditions": ["keywords", "file_patterns", "work_characteristics"],
          "context_additions": {{
            "technology_context": {{}},
            "team_context": {{}},
            "quality_context": {{}},
            "repository_context": {{}}
          }},
          "classification_guidance": {{
            "size_factors": ["..."],
            "complexity_factors": ["..."],
            "type_factors": ["..."]
          }},
          "confidence": 0-100
        }}
        
        Generate 5-10 rules that cover the major patterns in this repository.
        """
        
        message = await asyncio.to_thread(
            self.client.messages.create,
            model=self.config.claude_config.model,
            max_tokens=2048,
            temperature=0.2,
            system="You are an expert at generating context rules for AI classification systems.",
            messages=[{"role": "user", "content": rules_prompt}]
        )
        
        claude_text = message.content[0].text
        if "```json" in claude_text:
            json_start = claude_text.find("```json") + 7
            json_end = claude_text.find("```", json_start)
            claude_text = claude_text[json_start:json_end].strip()
            try:
                return json.loads(claude_text)
            except json.JSONDecodeError:
                pass
        
        return [{"rules_text": claude_text, "structured_rules": False}]

# Integration with main API server
class RepositoryClassificationService:
    """Service for repository-level classification and analysis"""
    
    def __init__(self, config: AiWorkClassificationEngineConfig):
        self.config = config
        self.analyzer = RepositoryAnalyzer(config)
        self.context_manager = RepositoryContextManager(config)
        self.repository_profiles = {}  # Cache for repository context profiles
    
    async def analyze_and_classify_repository(self, repo_path: str, repo_url: Optional[str] = None) -> Dict[str, Any]:
        """Complete repository analysis and classification"""
        
        # Full repository analysis
        repo_analysis = await self.analyzer.analyze_repository(repo_path, repo_url)
        
        # Build context profile
        context_profile = await self.context_manager.build_repository_context_profile(repo_analysis)
        
        # Cache for future use
        repo_id = repo_url or repo_path
        self.repository_profiles[repo_id] = {
            "analysis": repo_analysis,
            "context_profile": context_profile,
            "last_updated": datetime.utcnow().isoformat()
        }
        
        return {
            "repository_analysis": repo_analysis,
            "context_profile": context_profile,
            "repository_id": repo_id,
            "analysis_complete": True
        }
    
    async def classify_work_with_repository_context(self, work_description: str, repo_id: str, base_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Classify work using repository-specific context for consistency"""
        
        if repo_id not in self.repository_profiles:
            return {"error": "Repository not analyzed. Run repository analysis first."}
        
        repo_profile = self.repository_profiles[repo_id]
        context_profile = repo_profile["context_profile"]
        
        # Merge base context with repository context
        enhanced_context = base_context or {}
        enhanced_context.update({
            "repository_id": repo_id,
            "technology_profile": context_profile.get("technology_profile", {}),
            "team_profile": context_profile.get("team_profile", {}),
            "quality_profile": context_profile.get("quality_profile", {}),
            "repository_patterns": context_profile.get("scenario_patterns", {})
        })
        
        # Apply repository-specific context rules
        for rule in context_profile.get("context_rules", []):
            if self._rule_applies_to_work(work_description, rule):
                enhanced_context.update(rule.get("context_additions", {}))
        
        return {
            "enhanced_context": enhanced_context,
            "repository_context_applied": True,
            "context_rules_applied": len([r for r in context_profile.get("context_rules", []) if self._rule_applies_to_work(work_description, r)])
        }
    
    def _rule_applies_to_work(self, work_description: str, rule: Dict[str, Any]) -> bool:
        """Check if context rule applies to work description"""
        
        trigger_conditions = rule.get("trigger_conditions", [])
        work_lower = work_description.lower()
        
        return any(condition.lower() in work_lower for condition in trigger_conditions)
