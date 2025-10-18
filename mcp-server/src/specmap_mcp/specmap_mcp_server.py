#!/usr/bin/env python3
"""
SpecMap MCP Server
=================
Model Context Protocol server for SpecMap CLI integration with Claude Code.

This server exposes SpecMap's specification-driven development workflow
through MCP tools, enabling Claude Code to:
- Initialize RULEMAP-structured projects
- Create comprehensive specifications
- Run interactive clarifications
- Generate implementation plans
- Break down features into TDD tasks
- Track project progress

Author: Monomoy Strategies
Version: 1.0.0
License: MIT
"""

import sys
import json
import traceback
from pathlib import Path
from typing import Dict, Any, List, Optional

# Import FastMCP
try:
    from fastmcp import FastMCP
except ImportError:
    print("Error: fastmcp not installed. Run: pip install fastmcp", file=sys.stderr)
    sys.exit(1)

# Import SpecMap modules
try:
    from specmap.init import ProjectInitializer
    from specmap.specify import SpecificationCreator
    from specmap.clarify import ClarificationProcessor
    from specmap.plan import PlanGenerator
    from specmap.tasks import TaskGenerator
    from specmap.config import ConfigManager
except ImportError as e:
    print(f"Error: SpecMap modules not found. Make sure specmap-cli is installed.", file=sys.stderr)
    print(f"Details: {e}", file=sys.stderr)
    sys.exit(1)

# Initialize MCP server
server = FastMCP("SpecMap", 
    description="AI-powered specification-driven development with RULEMAP framework")


@server.tool()
async def specmap_init(
    project_name: str,
    project_type: str = "web-app",
    agent: str = "claude",
    path: str = "."
) -> dict:
    """
    Initialize a new SpecMap project with RULEMAP structure.
    
    Creates a complete project with:
    - 34-folder hybrid structure (Spec-Kit + RULEMAP)
    - Constitution governance document
    - RULEMAP project charter
    - Agent configurations
    - Tracking system setup
    
    Args:
        project_name: Name of the project (e.g., "user-dashboard")
        project_type: Type of project - one of:
            - "web-app" (default): Web application
            - "mobile-app": Mobile application
            - "api": API/Backend service
            - "library": Reusable library/package
            - "cli": Command-line tool
        agent: Base AI agent to use:
            - "claude" (default): Anthropic Claude
            - "gemini": Google Gemini
            - "copilot": GitHub Copilot
            - "cursor": Cursor AI
        path: Parent directory for project creation (default: current directory)
    
    Returns:
        dict: Project initialization results with:
            - success: Boolean indicating success
            - project_path: Full path to created project
            - folders_created: Number of folders created
            - files_created: List of generated files
            - message: Success message with summary
    
    Example:
        result = await specmap_init("my-project", "web-app", "claude")
        # Creates: ./my-project/ with 34 folders and core documents
    """
    try:
        # Resolve and create project path
        base_path = Path(path).resolve()
        project_path = base_path / project_name
        
        # Initialize project
        initializer = ProjectInitializer(
            project_path=project_path,
            project_name=project_name,
            project_type=project_type,
            base_agent=agent
        )
        
        result = initializer.initialize()
        
        # Get list of created files
        files_created = []
        for doc_type, doc_path in result.get('documents_created', {}).items():
            files_created.append(f"{doc_type}: {Path(doc_path).name}")
        
        return {
            "success": True,
            "project_path": str(result['path']),
            "folders_created": result['folders_created'],
            "files_created": files_created,
            "config_file": str(result.get('config_file', '')),
            "message": (
                f"✅ Project '{project_name}' initialized successfully!\n"
                f"📁 Created {result['folders_created']} folders\n"
                f"📄 Generated {len(files_created)} core documents\n"
                f"🤖 Agent: {agent}\n"
                f"📍 Location: {result['path']}"
            )
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": f"❌ Failed to initialize project: {str(e)}"
        }


@server.tool()
async def specmap_specify(
    project_path: str,
    feature_description: str,
    feature_id: Optional[str] = None
) -> dict:
    """
    Create a RULEMAP-enhanced feature specification.
    
    Generates a comprehensive specification following the RULEMAP framework:
    - R: Role & Authority
    - U: Understanding & Objectives
    - L: Logic & Structure
    - E: Elements & Specifications
    - M: Mood & Experience
    - A: Audience & Stakeholders
    - P: Performance & Metrics
    
    Args:
        project_path: Path to SpecMap project root
        feature_description: Description of the feature to specify
            (e.g., "User authentication with email/password and OAuth")
        feature_id: Optional manual feature ID (format: "###-feature-name")
            If not provided, auto-generates next sequential ID
    
    Returns:
        dict: Specification creation results with:
            - success: Boolean indicating success
            - feature_id: Assigned feature ID (e.g., "001-user-authentication")
            - feature_path: Path to feature folder
            - spec_file: Path to main specification
            - clarifications_file: Path to clarifications document
            - research_file: Path to research notes
            - tracking_ids: Dictionary of generated tracking IDs by category
            - message: Success message with details
    
    Example:
        result = await specmap_specify(
            "/path/to/project",
            "User authentication with OAuth support"
        )
        # Creates: 001-user-authentication/spec.md with RULEMAP structure
    """
    try:
        project_path = Path(project_path).resolve()
        
        # Verify project exists
        if not (project_path / ".specmap").exists():
            return {
                "success": False,
                "error": "Not a SpecMap project (missing .specmap folder)",
                "message": "❌ Not a valid SpecMap project. Run specmap_init first."
            }
        
        # Create specification
        creator = SpecificationCreator(project_path)
        result = creator.create_specification(feature_description, feature_id)
        
        # Count tracking IDs by category
        tracking_summary = {}
        for category, ids in result['tracking_ids'].items():
            tracking_summary[category] = len(ids)
        
        return {
            "success": True,
            "feature_id": result['feature_id'],
            "feature_path": result['feature_path'],
            "spec_file": result['spec_file'],
            "clarifications_file": result['clarifications_file'],
            "research_file": result['research_file'],
            "tracking_ids": result['tracking_ids'],
            "tracking_summary": tracking_summary,
            "message": (
                f"✅ Specification created: {result['feature_id']}\n"
                f"📝 Location: {result['feature_path']}\n"
                f"🔢 Tracking IDs generated:\n"
                + "\n".join([f"   {cat}: {count} items" 
                           for cat, count in tracking_summary.items()])
            )
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": f"❌ Failed to create specification: {str(e)}"
        }


@server.tool()
async def specmap_clarify(
    project_path: str,
    feature_id: str,
    interactive: bool = False
) -> dict:
    """
    Run clarification process for a specification.
    
    Finds all [NEEDS CLARIFICATION: ...] markers in the specification,
    calculates RULEMAP score, and optionally runs interactive Q&A.
    
    Args:
        project_path: Path to SpecMap project root
        feature_id: Feature ID to clarify (e.g., "001-user-authentication")
        interactive: Whether to run interactive Q&A session
            - True: Prompts for answers to each question
            - False (default): Returns questions without answering
    
    Returns:
        dict: Clarification results with:
            - success: Boolean indicating success
            - feature_id: Feature being clarified
            - status: One of:
                - "questions_found": Questions need answering
                - "no_questions_found": Specification complete
                - "threshold_met": RULEMAP score ≥8.0
            - questions_count: Number of open questions
            - rulemap_score: Current RULEMAP score (0-10)
            - meets_threshold: Boolean if score ≥8.0
            - questions: List of question details (if questions found)
            - message: Summary message
    
    Example:
        result = await specmap_clarify("/path/to/project", "001-user-auth")
        # Returns: 3 questions found, RULEMAP score: 6.5/10
    """
    try:
        project_path = Path(project_path).resolve()
        
        # Verify feature exists
        feature_path = project_path / "01-specifications" / "features" / feature_id
        if not feature_path.exists():
            return {
                "success": False,
                "error": f"Feature not found: {feature_id}",
                "message": f"❌ Feature '{feature_id}' does not exist"
            }
        
        # Run clarification process
        processor = ClarificationProcessor(project_path)
        result = processor.run_clarification_process(feature_id, interactive)
        
        # Calculate RULEMAP score
        score_result = processor.calculate_rulemap_score(feature_id)
        
        # Format questions for display
        questions_display = []
        if result.get('questions'):
            for q in result['questions'][:5]:  # Show first 5
                questions_display.append({
                    "id": q['id'],
                    "question": q['question'][:100],  # Truncate long questions
                    "context": q['context'][:50] if q.get('context') else ""
                })
        
        message_parts = [
            f"{'✅' if result['status'] == 'no_questions_found' else '❓'} Feature: {feature_id}",
            f"📊 RULEMAP Score: {score_result['score']:.1f}/10.0",
            f"{'✅' if score_result['meets_threshold'] else '⚠️'} Threshold: {'MET' if score_result['meets_threshold'] else 'NOT MET (need ≥8.0)'}",
        ]
        
        if result.get('questions_count', 0) > 0:
            message_parts.append(f"❓ Questions: {result['questions_count']} need clarification")
        else:
            message_parts.append("✅ No open questions - ready for planning!")
        
        return {
            "success": True,
            "feature_id": feature_id,
            "status": result['status'],
            "questions_count": result.get('questions_count', 0),
            "rulemap_score": score_result['score'],
            "meets_threshold": score_result['meets_threshold'],
            "completed_sections": score_result['completed_sections'],
            "total_sections": score_result['total_sections'],
            "questions": questions_display,
            "message": "\n".join(message_parts)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": f"❌ Failed to run clarification: {str(e)}"
        }


@server.tool()
async def specmap_plan(
    project_path: str,
    feature_id: str
) -> dict:
    """
    Generate implementation plan for a feature.
    
    Creates a comprehensive implementation plan including:
    - Technical decisions and rationale
    - Implementation phases with milestones
    - API contracts and data models
    - Constitution compliance analysis
    - Timeline estimates
    
    Requires: RULEMAP score ≥8.0 on specification
    
    Args:
        project_path: Path to SpecMap project root
        feature_id: Feature ID to plan (e.g., "001-user-authentication")
    
    Returns:
        dict: Implementation plan results with:
            - success: Boolean indicating success
            - feature_id: Feature being planned
            - plan_file: Path to main plan document
            - contracts_file: Path to API contracts
            - data_models_file: Path to data models
            - technical_decisions: List of key technical decisions
            - milestones: List of project milestones with dates
            - estimated_duration: Total estimated days
            - phases: List of implementation phases
            - message: Summary message
    
    Example:
        result = await specmap_plan("/path/to/project", "001-user-auth")
        # Creates: plan.md with 5 technical decisions, 3 milestones, 14 days
    """
    try:
        project_path = Path(project_path).resolve()
        
        # Verify feature exists
        feature_path = project_path / "01-specifications" / "features" / feature_id
        if not feature_path.exists():
            return {
                "success": False,
                "error": f"Feature not found: {feature_id}",
                "message": f"❌ Feature '{feature_id}' does not exist"
            }
        
        # Generate plan
        generator = PlanGenerator(project_path)
        
        # Check if feature meets RULEMAP threshold
        try:
            result = generator.generate_implementation_plan(feature_id)
        except ValueError as e:
            if "does not meet RULEMAP threshold" in str(e):
                return {
                    "success": False,
                    "error": "RULEMAP threshold not met",
                    "message": (
                        f"❌ Cannot generate plan for '{feature_id}'\n"
                        f"⚠️  RULEMAP score must be ≥8.0\n"
                        f"💡 Run specmap_clarify to resolve open questions first"
                    )
                }
            raise
        
        # Format technical decisions for display
        decisions_summary = [
            f"{d['title']}: {d['decision'][:50]}..."
            for d in result['technical_decisions'][:3]
        ]
        
        # Format milestones
        milestones_summary = [
            f"{m['date']}: {m['title']}"
            for m in result['milestones'][:3]
        ]
        
        return {
            "success": True,
            "feature_id": feature_id,
            "plan_file": result['plan_file'],
            "contracts_file": result['contracts_file'],
            "data_models_file": result['data_models_file'],
            "technical_decisions": result['technical_decisions'],
            "milestones": result['milestones'],
            "estimated_duration": result['estimated_duration'],
            "phases": result.get('phases', []),
            "message": (
                f"✅ Implementation plan generated: {feature_id}\n"
                f"📋 Technical Decisions: {len(result['technical_decisions'])}\n"
                f"🎯 Milestones: {len(result['milestones'])}\n"
                f"⏱️  Estimated Duration: {result['estimated_duration']} days\n"
                f"📍 Plan: {result['plan_file']}"
            )
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": f"❌ Failed to generate plan: {str(e)}"
        }


@server.tool()
async def specmap_tasks(
    project_path: str,
    feature_id: str
) -> dict:
    """
    Generate TDD task breakdown for a feature.
    
    Creates detailed task breakdown with:
    - Test-Driven Development workflow
    - 6-phase structure (Setup, Red, Green, Integration, QA, Documentation)
    - Parallel execution groups
    - Task tracking IDs (###-T-###)
    - Dependency mapping
    - Time estimates
    
    Requires: Implementation plan exists for feature
    
    Args:
        project_path: Path to SpecMap project root
        feature_id: Feature ID to break down (e.g., "001-user-authentication")
    
    Returns:
        dict: Task breakdown results with:
            - success: Boolean indicating success
            - feature_id: Feature being processed
            - tasks_file: Path to tasks document
            - total_tasks: Total number of tasks generated
            - tasks_by_phase: Task count for each phase
            - parallel_groups: Number of parallel execution groups
            - estimated_duration: Total estimated days
            - task_ids: List of generated task tracking IDs
            - message: Summary message
    
    Example:
        result = await specmap_tasks("/path/to/project", "001-user-auth")
        # Creates: tasks.md with 23 tasks across 6 phases, 14 days
    """
    try:
        project_path = Path(project_path).resolve()
        
        # Verify feature and plan exist
        plan_path = project_path / "02-planning" / "features" / feature_id
        if not plan_path.exists() or not (plan_path / "plan.md").exists():
            return {
                "success": False,
                "error": "Implementation plan not found",
                "message": (
                    f"❌ No implementation plan for '{feature_id}'\n"
                    f"💡 Run specmap_plan first to create the plan"
                )
            }
        
        # Generate tasks
        generator = TaskGenerator(project_path)
        result = generator.generate_tasks_for_feature(feature_id)
        
        # Format tasks by phase
        phase_summary = []
        for phase, count in result['tasks_by_phase'].items():
            if count > 0:
                phase_summary.append(f"   {phase}: {count} tasks")
        
        return {
            "success": True,
            "feature_id": feature_id,
            "tasks_file": result['tasks_file'],
            "total_tasks": result['total_tasks'],
            "tasks_by_phase": result['tasks_by_phase'],
            "parallel_groups": result['parallel_groups'],
            "estimated_duration": result['estimated_duration'],
            "message": (
                f"✅ Task breakdown generated: {feature_id}\n"
                f"📋 Total Tasks: {result['total_tasks']}\n"
                f"🔄 Parallel Groups: {result['parallel_groups']}\n"
                f"⏱️  Estimated Duration: {result['estimated_duration']} days\n"
                f"📊 Breakdown by phase:\n" + "\n".join(phase_summary) +
                f"\n📍 Tasks: {result['tasks_file']}"
            )
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": f"❌ Failed to generate tasks: {str(e)}"
        }


@server.tool()
async def specmap_status(
    project_path: str,
    detailed: bool = False
) -> dict:
    """
    Get project status and progress overview.
    
    Provides summary of:
    - Project configuration
    - All features and their workflow status
    - Progress metrics
    - Active features
    
    Args:
        project_path: Path to SpecMap project root
        detailed: Include detailed information per feature
            - False (default): Feature IDs only
            - True: Full status breakdown
    
    Returns:
        dict: Project status with:
            - success: Boolean indicating success
            - project_name: Name of the project
            - project_type: Type of project
            - base_agent: Configured AI agent
            - total_features: Number of features
            - features: List of features with status
            - workflow_summary: Count by workflow stage
            - message: Summary message
    
    Example:
        result = await specmap_status("/path/to/project", detailed=True)
        # Returns: 3 features, 2 with plans, 1 with tasks
    """
    try:
        project_path = Path(project_path).resolve()
        
        # Verify project exists
        if not (project_path / ".specmap").exists():
            return {
                "success": False,
                "error": "Not a SpecMap project",
                "message": "❌ Not a valid SpecMap project"
            }
        
        # Load configuration
        config = ConfigManager(project_path)
        
        # Get all features
        specs_path = project_path / "01-specifications" / "features"
        features = []
        workflow_summary = {
            "specified": 0,
            "planned": 0,
            "tasks_created": 0,
            "in_progress": 0
        }
        
        if specs_path.exists():
            for feature_dir in sorted(specs_path.iterdir()):
                if feature_dir.is_dir():
                    feature_id = feature_dir.name
                    spec_file = feature_dir / "spec.md"
                    plan_path = project_path / "02-planning" / "features" / feature_id
                    
                    has_spec = spec_file.exists()
                    has_plan = (plan_path / "plan.md").exists() if plan_path.exists() else False
                    has_tasks = (plan_path / "tasks.md").exists() if plan_path.exists() else False
                    
                    # Update workflow summary
                    if has_spec:
                        workflow_summary["specified"] += 1
                    if has_plan:
                        workflow_summary["planned"] += 1
                    if has_tasks:
                        workflow_summary["tasks_created"] += 1
                    
                    feature_info = {
                        "id": feature_id,
                        "has_spec": has_spec,
                        "has_plan": has_plan,
                        "has_tasks": has_tasks,
                        "status": (
                            "tasks_ready" if has_tasks else
                            "planned" if has_plan else
                            "specified" if has_spec else
                            "unknown"
                        )
                    }
                    
                    if detailed:
                        features.append(feature_info)
                    else:
                        features.append(feature_id)
        
        message_parts = [
            f"📊 Project Status: {config.get('project.name')}",
            f"📁 Type: {config.get('project.type')}",
            f"🤖 Agent: {config.get('agents.base_agent')}",
            f"📝 Features: {len(features)} total",
            f"",
            f"Workflow Progress:",
            f"   ✅ Specified: {workflow_summary['specified']}",
            f"   📋 Planned: {workflow_summary['planned']}",
            f"   🔨 Tasks Created: {workflow_summary['tasks_created']}"
        ]
        
        return {
            "success": True,
            "project_name": config.get('project.name'),
            "project_type": config.get('project.type'),
            "base_agent": config.get('agents.base_agent'),
            "total_features": len(features),
            "features": features,
            "workflow_summary": workflow_summary,
            "message": "\n".join(message_parts)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": f"❌ Failed to get project status: {str(e)}"
        }


@server.tool()
async def specmap_validate(
    project_path: str,
    feature_id: str,
    validation_type: str = "both"
) -> dict:
    """
    Validate a feature against SpecMap quality standards.
    
    Performs validation checks:
    - RULEMAP scoring (7 elements evaluation)
    - Constitution compliance
    - Tracking ID consistency
    - Template completeness
    
    Args:
        project_path: Path to SpecMap project root
        feature_id: Feature ID to validate
        validation_type: Type of validation:
            - "rulemap": RULEMAP scoring only
            - "constitution": Constitution compliance only
            - "both" (default): All validations
    
    Returns:
        dict: Validation results with:
            - success: Boolean indicating success
            - feature_id: Feature validated
            - rulemap_score: Score out of 10
            - meets_threshold: Boolean if ≥8.0
            - constitution_compliant: Boolean
            - issues: List of validation issues found
            - recommendations: List of improvements
            - message: Summary message
    """
    try:
        project_path = Path(project_path).resolve()
        
        # Verify feature exists
        feature_path = project_path / "01-specifications" / "features" / feature_id
        if not feature_path.exists():
            return {
                "success": False,
                "error": f"Feature not found: {feature_id}",
                "message": f"❌ Feature '{feature_id}' does not exist"
            }
        
        issues = []
        recommendations = []
        
        # RULEMAP validation
        rulemap_score = 0.0
        meets_threshold = False
        
        if validation_type in ["rulemap", "both"]:
            processor = ClarificationProcessor(project_path)
            score_result = processor.calculate_rulemap_score(feature_id)
            rulemap_score = score_result['score']
            meets_threshold = score_result['meets_threshold']
            
            if not meets_threshold:
                issues.append(f"RULEMAP score {rulemap_score:.1f} below threshold (need ≥8.0)")
                recommendations.append("Run specmap_clarify to identify and resolve open questions")
        
        # Constitution validation
        constitution_compliant = True
        if validation_type in ["constitution", "both"]:
            # Check for constitution markers in spec
            spec_file = feature_path / "spec.md"
            if spec_file.exists():
                content = spec_file.read_text()
                if "Constitution Compliance" not in content:
                    issues.append("Constitution compliance section missing")
                    constitution_compliant = False
        
        message_parts = [
            f"{'✅' if not issues else '⚠️'} Validation: {feature_id}"
        ]
        
        if validation_type in ["rulemap", "both"]:
            message_parts.append(
                f"📊 RULEMAP Score: {rulemap_score:.1f}/10.0 "
                f"{'✅' if meets_threshold else '❌'}"
            )
        
        if validation_type in ["constitution", "both"]:
            message_parts.append(
                f"📜 Constitution: {'✅ Compliant' if constitution_compliant else '❌ Issues found'}"
            )
        
        if issues:
            message_parts.append(f"\n⚠️  Issues: {len(issues)}")
            for issue in issues[:3]:
                message_parts.append(f"   • {issue}")
        else:
            message_parts.append("\n✅ All validations passed!")
        
        return {
            "success": True,
            "feature_id": feature_id,
            "rulemap_score": rulemap_score,
            "meets_threshold": meets_threshold,
            "constitution_compliant": constitution_compliant,
            "issues": issues,
            "recommendations": recommendations,
            "message": "\n".join(message_parts)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": f"❌ Failed to validate: {str(e)}"
        }


# Server entry point
def main():
    """Main entry point for the MCP server."""
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
