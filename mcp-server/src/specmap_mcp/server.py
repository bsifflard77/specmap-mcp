#!/usr/bin/env python3
"""
SpecMap MCP Server - Production Version
"""
import sys
from pathlib import Path
from typing import Dict, Any, List
from fastmcp import FastMCP

# Import SpecMap modules
from specmap.init import ProjectInitializer
from specmap.specify import SpecificationCreator
from specmap.clarify import ClarificationProcessor
from specmap.plan import PlanGenerator
from specmap.tasks import TaskGenerator
from specmap.config import ConfigManager
from specmap.skills import SkillManager

server = FastMCP("SpecMap")

@server.tool()
async def specmap_init(project_name: str, project_type: str = "web-app", agent: str = "claude", path: str = ".") -> dict:
    """Initialize a new SpecMap project with RULEMAP structure."""
    try:
        base_path = Path(path).resolve()
        project_path = base_path / project_name
        initializer = ProjectInitializer(project_path, project_name, project_type, agent)
        result = initializer.initialize()
        
        return {
            "success": True,
            "project_path": str(result['path']),
            "folders_created": result['folders_created'],
            "message": f"✅ Project '{project_name}' initialized with {result['folders_created']} folders"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "message": f"❌ Failed: {str(e)}"}

@server.tool()
async def specmap_specify(project_path: str, feature_description: str, feature_id: str = None) -> dict:
    """Create a RULEMAP-enhanced feature specification."""
    try:
        project_path = Path(project_path).resolve()
        creator = SpecificationCreator(project_path)
        result = creator.create_specification(feature_description, feature_id)
        
        return {
            "success": True,
            "feature_id": result['feature_id'],
            "spec_file": result['spec_file'],
            "message": f"✅ Specification created: {result['feature_id']}"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "message": f"❌ Failed: {str(e)}"}

@server.tool()
async def specmap_clarify(project_path: str, feature_id: str) -> dict:
    """Run clarification process for a specification."""
    try:
        project_path = Path(project_path).resolve()
        processor = ClarificationProcessor(project_path)
        result = processor.run_clarification_process(feature_id, False)
        score_result = processor.calculate_rulemap_score(feature_id)
        
        return {
            "success": True,
            "feature_id": feature_id,
            "questions_count": result.get('questions_count', 0),
            "rulemap_score": score_result['score'],
            "meets_threshold": score_result['meets_threshold'],
            "message": f"📊 RULEMAP Score: {score_result['score']:.1f}/10"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "message": f"❌ Failed: {str(e)}"}

@server.tool()
async def specmap_plan(project_path: str, feature_id: str) -> dict:
    """Generate implementation plan for a feature."""
    try:
        project_path = Path(project_path).resolve()
        generator = PlanGenerator(project_path)
        result = generator.generate_implementation_plan(feature_id)
        
        return {
            "success": True,
            "feature_id": feature_id,
            "plan_file": result['plan_file'],
            "estimated_duration": result['estimated_duration'],
            "message": f"✅ Plan generated: {result['estimated_duration']} days"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "message": f"❌ Failed: {str(e)}"}

@server.tool()
async def specmap_tasks(project_path: str, feature_id: str) -> dict:
    """Generate TDD task breakdown for a feature."""
    try:
        project_path = Path(project_path).resolve()
        generator = TaskGenerator(project_path)
        result = generator.generate_tasks_for_feature(feature_id)
        
        return {
            "success": True,
            "feature_id": feature_id,
            "total_tasks": result['total_tasks'],
            "message": f"✅ {result['total_tasks']} tasks generated"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "message": f"❌ Failed: {str(e)}"}

@server.tool()
async def specmap_status(project_path: str) -> dict:
    """Get project status and progress overview."""
    try:
        project_path = Path(project_path).resolve()
        config = ConfigManager(project_path)
        specs_path = project_path / "01-specifications" / "features"
        features = []

        if specs_path.exists():
            for feature_dir in sorted(specs_path.iterdir()):
                if feature_dir.is_dir():
                    features.append(feature_dir.name)

        return {
            "success": True,
            "project_name": config.get('project.name'),
            "total_features": len(features),
            "features": features,
            "message": f"📊 Project has {len(features)} features"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "message": f"❌ Failed: {str(e)}"}

@server.tool()
async def create_claude_skill(
    project_path: str,
    name: str,
    description: str,
    content: str,
    metadata: dict = None
) -> dict:
    """Create a custom Claude Code skill for the SpecMap project."""
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
        return {"success": False, "error": str(e), "message": f"❌ Failed: {str(e)}"}

@server.tool()
async def install_specmap_skill_template(project_path: str, template_name: str) -> dict:
    """Install a predefined SpecMap skill template."""
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
        return {"success": False, "error": str(e), "message": f"❌ Failed: {str(e)}"}

@server.tool()
async def install_all_specmap_skills(project_path: str) -> dict:
    """Install all predefined SpecMap skill templates."""
    try:
        project_path = Path(project_path).resolve()
        skill_manager = SkillManager(project_path)
        result = skill_manager.install_all_templates()

        return {
            "success": True,
            "installed_count": result['installed_count'],
            "installed_skills": result['installed_skills'],
            "skills_dir": result['skills_dir'],
            "errors": result['errors'],
            "message": f"✅ Installed {result['installed_count']} skills"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "message": f"❌ Failed: {str(e)}"}

@server.tool()
async def list_claude_skills(project_path: str) -> dict:
    """List all installed Claude Code skills in the project."""
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
        return {"success": False, "error": str(e), "message": f"❌ Failed: {str(e)}"}

@server.tool()
async def get_skill_templates() -> dict:
    """Get list of available SpecMap skill templates."""
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
        return {"success": False, "error": str(e), "message": f"❌ Failed: {str(e)}"}

@server.tool()
async def delete_claude_skill(project_path: str, skill_name: str) -> dict:
    """Delete a Claude Code skill from the project."""
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
        return {"success": False, "error": str(e), "message": f"❌ Failed: {str(e)}"}

if __name__ == "__main__":
    server.run(transport="stdio")
