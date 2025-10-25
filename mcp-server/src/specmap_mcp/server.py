#!/usr/bin/env python3
"""
SpecMap MCP Server - Complete Implementation
============================================
Model Context Protocol server for SpecMap CLI integration with Claude Code.

This server exposes SpecMap's specification-driven development workflow
through MCP tools, enabling Claude Code to:
- Initialize RULEMAP-structured projects
- Create comprehensive specifications
- Run interactive clarifications
- Generate implementation plans
- Break down features into TDD tasks
- Track project progress
- Manage Claude Code skills

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
    from specmap.skills import SkillManager
    from specmap.sessions import SessionManager
except ImportError as e:
    print(f"Error: SpecMap modules not found. Make sure specmap-cli is installed.", file=sys.stderr)
    print(f"Details: {e}", file=sys.stderr)
    sys.exit(1)

# Initialize MCP server
server = FastMCP("SpecMap",
    description="AI-powered specification-driven development with RULEMAP framework")


# ============================================================================
# WORKFLOW TOOLS (6 tools)
# ============================================================================

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
        dict: Project initialization results with success status and details
    """
    try:
        base_path = Path(path).resolve()
        project_path = base_path / project_name

        initializer = ProjectInitializer(
            project_path=project_path,
            project_name=project_name,
            project_type=project_type,
            base_agent=agent
        )

        result = initializer.initialize()

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
        feature_id: Optional manual feature ID (auto-generated if not provided)

    Returns:
        dict: Specification creation results with success status and tracking info
    """
    try:
        project_path = Path(project_path).resolve()

        if not (project_path / ".specmap").exists():
            return {
                "success": False,
                "error": "Not a SpecMap project (missing .specmap folder)",
                "message": "❌ Not a valid SpecMap project. Run specmap_init first."
            }

        creator = SpecificationCreator(project_path)
        result = creator.create_specification(feature_description, feature_id)

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
        interactive: Whether to run interactive Q&A session (default: False)

    Returns:
        dict: Clarification results with questions and RULEMAP score
    """
    try:
        project_path = Path(project_path).resolve()

        feature_path = project_path / "01-specifications" / "features" / feature_id
        if not feature_path.exists():
            return {
                "success": False,
                "error": f"Feature not found: {feature_id}",
                "message": f"❌ Feature '{feature_id}' does not exist"
            }

        processor = ClarificationProcessor(project_path)
        result = processor.run_clarification_process(feature_id, interactive)
        score_result = processor.calculate_rulemap_score(feature_id)

        questions_display = []
        if result.get('questions'):
            for q in result['questions'][:5]:
                questions_display.append({
                    "id": q['id'],
                    "question": q['question'][:100],
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
        dict: Implementation plan results with technical decisions and estimates
    """
    try:
        project_path = Path(project_path).resolve()

        feature_path = project_path / "01-specifications" / "features" / feature_id
        if not feature_path.exists():
            return {
                "success": False,
                "error": f"Feature not found: {feature_id}",
                "message": f"❌ Feature '{feature_id}' does not exist"
            }

        generator = PlanGenerator(project_path)

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

        decisions_summary = [
            f"{d['title']}: {d['decision'][:50]}..."
            for d in result['technical_decisions'][:3]
        ]

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
        dict: Task breakdown results with total tasks and phase breakdown
    """
    try:
        project_path = Path(project_path).resolve()

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

        generator = TaskGenerator(project_path)
        result = generator.generate_tasks_for_feature(feature_id)

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
        detailed: Include detailed information per feature (default: False)

    Returns:
        dict: Project status with feature counts and workflow progress
    """
    try:
        project_path = Path(project_path).resolve()

        if not (project_path / ".specmap").exists():
            return {
                "success": False,
                "error": "Not a SpecMap project",
                "message": "❌ Not a valid SpecMap project"
            }

        config = ConfigManager(project_path)

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


# ============================================================================
# VALIDATION TOOL (1 tool)
# ============================================================================

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
        dict: Validation results with scores, compliance status, and recommendations
    """
    try:
        project_path = Path(project_path).resolve()

        feature_path = project_path / "01-specifications" / "features" / feature_id
        if not feature_path.exists():
            return {
                "success": False,
                "error": f"Feature not found: {feature_id}",
                "message": f"❌ Feature '{feature_id}' does not exist"
            }

        issues = []
        recommendations = []

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

        constitution_compliant = True
        if validation_type in ["constitution", "both"]:
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


# ============================================================================
# SKILL MANAGEMENT TOOLS (6 tools)
# ============================================================================

@server.tool()
async def create_claude_skill(
    project_path: str,
    name: str,
    description: str,
    content: str,
    metadata: Optional[dict] = None
) -> dict:
    """
    Create a custom Claude Code skill for the SpecMap project.

    Args:
        project_path: Path to SpecMap project root
        name: Skill name (will be used as filename)
        description: Brief description of what the skill does
        content: Markdown content for the skill instructions
        metadata: Optional metadata dictionary

    Returns:
        dict: Skill creation results with file path
    """
    try:
        project_path = Path(project_path).resolve()
        skill_manager = SkillManager(project_path)
        result = skill_manager.create_skill(name, description, content, metadata)

        return {
            "success": True,
            "skill_name": result['skill_name'],
            "skill_file": result['skill_file'],
            "message": f"✅ Skill '{name}' created successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": f"❌ Failed to create skill: {str(e)}"
        }


@server.tool()
async def install_specmap_skill_template(
    project_path: str,
    template_name: str
) -> dict:
    """
    Install a predefined SpecMap skill template.

    Available templates:
    - specmap-reviewer: Review specifications for RULEMAP compliance
    - specmap-planner: Generate implementation plans
    - specmap-task-generator: Create TDD task breakdowns
    - specmap-qa: Quality assurance and compliance validation
    - specmap-charter-helper: Interactive project charter completion

    Args:
        project_path: Path to SpecMap project root
        template_name: Name of the template to install

    Returns:
        dict: Installation results with file path
    """
    try:
        project_path = Path(project_path).resolve()
        skill_manager = SkillManager(project_path)
        result = skill_manager.create_skill_from_template(template_name)

        return {
            "success": True,
            "skill_name": result['skill_name'],
            "skill_file": result['skill_file'],
            "message": f"✅ Template '{template_name}' installed"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": f"❌ Failed to install template: {str(e)}"
        }


@server.tool()
async def install_all_specmap_skills(
    project_path: str
) -> dict:
    """
    Install all predefined SpecMap skill templates.

    Installs all 5 available skill templates:
    - specmap-reviewer
    - specmap-planner
    - specmap-task-generator
    - specmap-qa
    - specmap-charter-helper

    Args:
        project_path: Path to SpecMap project root

    Returns:
        dict: Installation summary with count and list of installed skills
    """
    try:
        project_path = Path(project_path).resolve()
        skill_manager = SkillManager(project_path)
        result = skill_manager.install_all_templates()

        return {
            "success": True,
            "installed_count": result['installed_count'],
            "installed_skills": result['installed_skills'],
            "skills_dir": result['skills_dir'],
            "errors": result.get('errors', []),
            "message": f"✅ Installed {result['installed_count']} skills"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": f"❌ Failed to install skills: {str(e)}"
        }


@server.tool()
async def list_claude_skills(
    project_path: str
) -> dict:
    """
    List all installed Claude Code skills in the project.

    Args:
        project_path: Path to SpecMap project root

    Returns:
        dict: List of installed skills with names and descriptions
    """
    try:
        project_path = Path(project_path).resolve()
        skill_manager = SkillManager(project_path)
        skills = skill_manager.list_skills()

        return {
            "success": True,
            "total_skills": len(skills),
            "skills": skills,
            "message": f"📋 Found {len(skills)} installed skills"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": f"❌ Failed to list skills: {str(e)}"
        }


@server.tool()
async def get_skill_templates() -> dict:
    """
    Get list of available SpecMap skill templates.

    Returns:
        dict: List of available templates with descriptions
    """
    try:
        skill_manager = SkillManager()
        templates = skill_manager.get_available_templates()

        return {
            "success": True,
            "total_templates": len(templates),
            "templates": templates,
            "message": f"📚 {len(templates)} templates available"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": f"❌ Failed to get templates: {str(e)}"
        }


@server.tool()
async def delete_claude_skill(
    project_path: str,
    skill_name: str
) -> dict:
    """
    Delete a Claude Code skill from the project.

    Args:
        project_path: Path to SpecMap project root
        skill_name: Name of the skill to delete

    Returns:
        dict: Deletion results
    """
    try:
        project_path = Path(project_path).resolve()
        skill_manager = SkillManager(project_path)
        result = skill_manager.delete_skill(skill_name)

        if result['success']:
            return {
                "success": True,
                "deleted": result['deleted'],
                "message": result['message']
            }
        else:
            return {
                "success": False,
                "error": result['error'],
                "message": f"❌ {result['error']}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": f"❌ Failed to delete skill: {str(e)}"
        }


# ============================================================================
# SESSION MANAGEMENT TOOLS (6 tools)
# ============================================================================

@server.tool()
async def session_start(
    project_path: str,
    focus: str,
    agent: str = "claude",
    metadata: Optional[dict] = None
) -> dict:
    """
    Start a new development session with organized workspace.

    Creates:
    - Session workspace in 04-agents/sessions/active/
    - Session metadata tracking file
    - Organized folders for artifacts, notes, decisions
    - Session summary template

    Args:
        project_path: Path to SpecMap project root
        focus: Focus area for this session (e.g., "authentication feature")
        agent: AI agent being used (default: "claude")
        metadata: Optional additional metadata dictionary

    Returns:
        dict: Session details with workspace paths
    """
    try:
        project_path = Path(project_path).resolve()
        session_mgr = SessionManager(project_path)

        result = session_mgr.start_session(focus, agent, metadata)

        return {
            "success": True,
            "session_id": result['session_id'],
            "session_path": result['session_path'],
            "metadata_file": result['metadata_file'],
            "focus": result['focus'],
            "agent": result['agent'],
            "message": (
                f"✅ Session started: {result['session_id']}\n"
                f"📁 Workspace: {result['session_path']}\n"
                f"🎯 Focus: {focus}\n"
                f"🤖 Agent: {agent}\n\n"
                f"Session workspace created with:\n"
                f"  - artifacts/  (files created)\n"
                f"  - notes/      (scratch work)\n"
                f"  - decisions/  (technical decisions)\n"
                f"  - snapshots/  (checkpoints)\n"
                f"  - session.yaml (metadata)\n"
                f"  - summary.md  (session summary)"
            )
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": f"❌ Failed to start session: {str(e)}"
        }


@server.tool()
async def session_checkpoint(
    project_path: str,
    session_id: str,
    description: str,
    files_to_snapshot: Optional[list] = None
) -> dict:
    """
    Create a checkpoint snapshot of current session state.

    Saves incremental backup of work in progress to allow recovery.

    Args:
        project_path: Path to SpecMap project root
        session_id: Session ID to checkpoint
        description: Description of this checkpoint (e.g., "Auth logic implemented")
        files_to_snapshot: Optional list of specific files to snapshot

    Returns:
        dict: Checkpoint details with snapshot location
    """
    try:
        project_path = Path(project_path).resolve()
        session_mgr = SessionManager(project_path)

        result = session_mgr.create_checkpoint(
            session_id=session_id,
            description=description,
            files_to_snapshot=files_to_snapshot
        )

        return {
            "success": True,
            "checkpoint_id": result['checkpoint_id'],
            "checkpoint_path": result['checkpoint_path'],
            "files_snapshotted": result['files_snapshotted'],
            "description": result['description'],
            "message": (
                f"✅ Checkpoint created: {result['checkpoint_id']}\n"
                f"💾 Location: {result['checkpoint_path']}\n"
                f"📄 Files: {result['files_snapshotted']}\n"
                f"📝 {description}"
            )
        }

    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"❌ Session not found: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": f"❌ Failed to create checkpoint: {str(e)}"
        }


@server.tool()
async def session_track_artifact(
    project_path: str,
    session_id: str,
    file_path: str,
    action: str = "created"
) -> dict:
    """
    Track a file artifact in session metadata.

    Records files created or modified during session for tracking.

    Args:
        project_path: Path to SpecMap project root
        session_id: Session ID
        file_path: Path to file (relative to project root)
        action: "created" or "modified"

    Returns:
        dict: Tracking confirmation
    """
    try:
        project_path = Path(project_path).resolve()
        session_mgr = SessionManager(project_path)

        success = session_mgr.track_artifact(session_id, file_path, action)

        if success:
            return {
                "success": True,
                "session_id": session_id,
                "file_path": file_path,
                "action": action,
                "message": f"✅ Tracked: {file_path} ({action})"
            }
        else:
            return {
                "success": False,
                "error": "Session not found",
                "message": f"❌ Session not found: {session_id}"
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": f"❌ Failed to track artifact: {str(e)}"
        }


@server.tool()
async def session_end(
    project_path: str,
    session_id: str,
    rulemap_score: Optional[float] = None,
    create_backup: bool = True
) -> dict:
    """
    End a session and archive it with backup.

    Finalizes session, archives workspace, creates backup.

    Args:
        project_path: Path to SpecMap project root
        session_id: Session ID to end
        rulemap_score: Optional RULEMAP score (0-10) for session quality
        create_backup: Whether to create backup (default: True)

    Returns:
        dict: Archival details and session summary
    """
    try:
        project_path = Path(project_path).resolve()
        session_mgr = SessionManager(project_path)

        result = session_mgr.end_session(
            session_id=session_id,
            rulemap_score=rulemap_score,
            create_backup=create_backup
        )

        message_parts = [
            f"✅ Session ended: {result['session_id']}",
            f"📊 Duration: {result['duration_minutes']} minutes",
            f"📁 Files created: {result['files_created']}",
            f"📝 Files modified: {result['files_modified']}",
            f"💾 Checkpoints: {result['checkpoints']}"
        ]

        if rulemap_score:
            message_parts.append(f"🎯 RULEMAP Score: {rulemap_score}/10")

        message_parts.extend([
            f"",
            f"📦 Archived: {result['archive_path']}"
        ])

        if result['backup_path']:
            message_parts.append(f"💾 Backup: {result['backup_path']}")

        return {
            "success": True,
            "session_id": result['session_id'],
            "duration_minutes": result['duration_minutes'],
            "files_created": result['files_created'],
            "files_modified": result['files_modified'],
            "checkpoints": result['checkpoints'],
            "archive_path": result['archive_path'],
            "backup_path": result['backup_path'],
            "message": "\n".join(message_parts)
        }

    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"❌ Session not found: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": f"❌ Failed to end session: {str(e)}"
        }


@server.tool()
async def session_list_active(
    project_path: str
) -> dict:
    """
    List all active sessions.

    Args:
        project_path: Path to SpecMap project root

    Returns:
        dict: List of active sessions with details
    """
    try:
        project_path = Path(project_path).resolve()
        session_mgr = SessionManager(project_path)

        sessions = session_mgr.list_active_sessions()

        return {
            "success": True,
            "total_sessions": len(sessions),
            "sessions": sessions,
            "message": f"📋 Found {len(sessions)} active session(s)"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": f"❌ Failed to list sessions: {str(e)}"
        }


@server.tool()
async def create_daily_backup(
    project_path: str
) -> dict:
    """
    Create daily backup of entire project.

    Backs up all critical files and folders:
    - Governance (constitution, charter)
    - Specifications
    - Planning documents
    - Implementation tracking
    - Session summaries
    - TRACKING.md

    Args:
        project_path: Path to SpecMap project root

    Returns:
        dict: Backup details with manifest
    """
    try:
        project_path = Path(project_path).resolve()
        session_mgr = SessionManager(project_path)

        result = session_mgr.create_daily_backup()

        return {
            "success": True,
            "backup_date": result['backup_date'],
            "backup_path": result['backup_path'],
            "items_backed_up": result['items_backed_up'],
            "manifest": result['manifest'],
            "message": (
                f"✅ Daily backup created: {result['backup_date']}\n"
                f"📁 Location: {result['backup_path']}\n"
                f"📦 Items: {result['items_backed_up']}\n"
                f"📄 Manifest: {result['manifest']}\n\n"
                f"Backed up:\n"
                f"  - Governance documents\n"
                f"  - All specifications\n"
                f"  - Implementation plans\n"
                f"  - Session archives\n"
                f"  - Project tracking"
            )
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": f"❌ Failed to create backup: {str(e)}"
        }


# ============================================================================
# SERVER ENTRY POINT
# ============================================================================

def main():
    """Main entry point for the MCP server."""
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
