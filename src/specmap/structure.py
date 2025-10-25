"""
Project structure management for SpecMap
AI-powered specification-driven development system
"""

from pathlib import Path
from typing import Dict, List
from datetime import datetime


class ProjectStructure:
    """Manages the SpecMap project folder structure"""

    # Complete folder structure for spec-driven development
    FOLDER_STRUCTURE = [
        # Root configuration
        ".specmap",

        # Governance (constitution and project charter)
        "00-governance",

        # Specifications (RULEMAP-enhanced specifications)
        "01-specifications",
        "01-specifications/features",

        # Planning (implementation plans and task breakdown)
        "02-planning",
        "02-planning/features",

        # Implementation (development tracking)
        "03-implementation",
        "03-implementation/features",

        # Agents (AI agent management)
        "04-agents",
        "04-agents/session-summaries",
        "04-agents/sessions",
        "04-agents/sessions/active",
        "04-agents/sessions/archive",
        "04-agents/backups",
        "04-agents/backups/daily",
        "04-agents/backups/sessions",
        "04-agents/backups/milestones",
        "04-agents/agent-configurations",
        "04-agents/agent-configurations/claude",
        "04-agents/agent-configurations/gemini",
        "04-agents/agent-configurations/copilot",
        "04-agents/agent-configurations/cursor",
        "04-agents/agent-configurations/rulemap",
        "04-agents/agent-configurations/unified",
        "04-agents/agent-performance",

        # Quality Assurance (integrated validation)
        "05-quality-assurance",
        "05-quality-assurance/constitution-validation",
        "05-quality-assurance/rulemap-scoring",
        "05-quality-assurance/validation-reports",
        "05-quality-assurance/user-feedback",

        # Documentation
        "06-documentation",
        "06-documentation/user-guides",
        "06-documentation/technical-docs",
        "06-documentation/api-specifications",
        "06-documentation/deployment-guides",

        # Project Tracking
        "07-project-tracking",

        # Deliverables
        "08-deliverables",
        "08-deliverables/releases",
        "08-deliverables/presentations",
        "08-deliverables/final-reports",
        "08-deliverables/handover-documents",
    ]

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)

    def create(self) -> List[str]:
        """Create the complete folder structure"""
        created_folders = []

        for folder in self.FOLDER_STRUCTURE:
            folder_path = self.project_path / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            created_folders.append(str(folder))

        return created_folders

    def get_feature_path(self, feature_id: str) -> Dict[str, Path]:
        """Get paths for a specific feature"""
        return {
            'spec': self.project_path / "01-specifications" / "features" / feature_id,
            'plan': self.project_path / "02-planning" / "features" / feature_id,
            'implementation': self.project_path / "03-implementation" / "features" / feature_id
        }

    def create_feature_structure(self, feature_id: str):
        """Create folder structure for a new feature"""
        paths = self.get_feature_path(feature_id)
        for path in paths.values():
            path.mkdir(parents=True, exist_ok=True)
        return paths

    def validate_structure(self) -> Dict[str, bool]:
        """Validate that project structure is complete"""
        validation = {}
        for folder in self.FOLDER_STRUCTURE:
            folder_path = self.project_path / folder
            validation[folder] = folder_path.exists()
        return validation


class TemplateManager:
    """Manages template files for the unified system"""

    def __init__(self, templates_dir: Path):
        self.templates_dir = Path(templates_dir)

    def get_template(self, template_name: str) -> str:
        """Load a template file"""
        template_path = self.templates_dir / f"{template_name}.md"
        if template_path.exists():
            return template_path.read_text(encoding='utf-8')
        raise FileNotFoundError(f"Template not found: {template_name}")

    def render_template(self, template_name: str, variables: Dict[str, str]) -> str:
        """Load and render a template with variables"""
        template_content = self.get_template(template_name)

        # Simple variable substitution
        for key, value in variables.items():
            placeholder = f"[{key.upper()}]"
            template_content = template_content.replace(placeholder, value)

        return template_content

    def save_rendered_template(self, content: str, output_path: Path):
        """Save rendered template to file"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding='utf-8')


def sanitize_name(name: str) -> str:
    """Convert project/feature name to safe folder name"""
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in name).strip("-")


def generate_feature_id(name: str, existing_features: List[str]) -> str:
    """Generate next feature ID (e.g., 001-feature-name)"""
    # Extract existing feature numbers
    numbers = []
    for feature in existing_features:
        if feature and feature[0].isdigit():
            try:
                num = int(feature.split('-')[0])
                numbers.append(num)
            except (ValueError, IndexError):
                continue

    # Get next number
    next_num = max(numbers) + 1 if numbers else 1

    # Format: 001-feature-name
    safe_name = sanitize_name(name)
    return f"{next_num:03d}-{safe_name}"