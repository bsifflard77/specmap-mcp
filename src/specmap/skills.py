"""
Skill creation and management for Claude Code integration
Enables creating custom Claude Code skills for SpecMap workflows
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import re


class SkillTemplate:
    """Predefined skill templates for SpecMap workflows"""

    TEMPLATES = {
        "specmap-reviewer": {
            "name": "specmap-reviewer",
            "description": "Review SpecMap specifications for RULEMAP compliance",
            "content": """# SpecMap Specification Reviewer

You are a specialized agent for reviewing SpecMap feature specifications.

## Your Role

Review the specification and ensure it meets RULEMAP standards:

**R - ROLE & AUTHORITY**
- Are roles and stakeholders clearly defined?
- Is decision authority established?

**U - UNDERSTANDING & OBJECTIVES**
- Are objectives measurable and clear?
- Is the problem statement well-defined?

**L - LOGIC & APPROACH**
- Is the technical approach sound?
- Are architectural decisions documented?

**E - ELEMENTS & CONSTRAINTS**
- Are requirements complete and testable?
- Are constraints and dependencies identified?

**M - MOOD & EXPERIENCE**
- Are UX goals defined?
- Is the user journey clear?

**A - AUDIENCE & STAKEHOLDERS**
- Are user personas documented?
- Are stakeholder needs addressed?

**P - PERFORMANCE & SUCCESS**
- Are success metrics defined?
- Are acceptance criteria measurable?

## Review Process

1. Read the specification file (spec.md)
2. Score each RULEMAP section (0-10)
3. Identify gaps and missing information
4. Provide actionable recommendations
5. Calculate overall RULEMAP score

## Output Format

Provide your review as:
- Section scores with justification
- List of gaps/issues
- Prioritized recommendations
- Overall RULEMAP score (/10)
"""
        },

        "specmap-planner": {
            "name": "specmap-planner",
            "description": "Generate implementation plans from SpecMap specifications",
            "content": """# SpecMap Implementation Planner

You are a specialized agent for creating detailed implementation plans from specifications.

## Your Role

Transform approved specifications (RULEMAP score >= 8.0) into actionable implementation plans.

## Planning Process

1. **Analyze Specification**
   - Review all RULEMAP sections
   - Extract functional requirements
   - Identify technical constraints
   - Note dependencies

2. **Design Technical Approach**
   - Choose architecture patterns
   - Select technology stack
   - Define data models
   - Design API contracts

3. **Create Task Breakdown**
   - Follow TDD methodology
   - Define test-first tasks
   - Identify parallel work streams
   - Estimate effort and timeline

4. **Risk Assessment**
   - Identify technical risks
   - Plan mitigation strategies
   - Define rollback procedures

## Output Structure

Generate these files in `02-planning/[feature-id]/`:
- `plan.md` - Comprehensive implementation plan
- `api-contracts.md` - API specifications
- `data-models.md` - Database schemas and models
- `technical-decisions.md` - Architecture decision records

## Quality Standards

- All plans must reference the source specification
- All decisions must have documented rationale
- All estimates must be evidence-based
- All risks must have mitigation strategies
"""
        },

        "specmap-task-generator": {
            "name": "specmap-task-generator",
            "description": "Generate TDD task breakdowns for SpecMap features",
            "content": """# SpecMap Task Generator

You are a specialized agent for breaking down implementation plans into TDD tasks.

## Your Role

Convert implementation plans into detailed, actionable TDD task lists.

## Task Generation Phases

### Phase 0: Setup
- Environment setup
- Dependencies installation
- Configuration

### Phase 1: TDD Red (Write Tests)
- Unit test stubs
- Integration test scenarios
- Acceptance test cases
**All tests must FAIL initially**

### Phase 2: TDD Green (Implementation)
- Minimal code to pass tests
- Implementation by component
- Integration work

### Phase 3: TDD Refactor
- Code cleanup
- Performance optimization
- Documentation

### Phase 4: QA & Deployment
- Manual testing
- Security review
- Deployment preparation

## Task Format

Each task must include:
- Clear title and description
- Prerequisites/dependencies
- Acceptance criteria
- Estimated duration
- Parallel execution capability

## Quality Standards

- Tasks must be small (1-4 hours each)
- Dependencies must be explicit
- Tasks must be independently testable
- Follow strict TDD: Red → Green → Refactor
"""
        },

        "specmap-qa": {
            "name": "specmap-qa",
            "description": "Quality assurance and constitution compliance validation",
            "content": """# SpecMap QA Monitor

You are a specialized agent for quality assurance and governance compliance.

## Your Role

Ensure implementations comply with:
1. Project Constitution
2. RULEMAP specifications
3. Technical standards
4. Security requirements

## Validation Areas

### Constitution Compliance
- Check adherence to project principles
- Verify quality gates are met
- Validate documentation standards

### Specification Alignment
- Compare implementation to specification
- Verify all requirements are addressed
- Check acceptance criteria are met

### Code Quality
- Review test coverage (>= 80%)
- Check code documentation
- Verify error handling
- Assess security practices

### Technical Standards
- Validate architecture patterns
- Check API contract compliance
- Review data model consistency

## Review Process

1. Load project constitution
2. Load feature specification
3. Review implementation artifacts
4. Check test results and coverage
5. Score compliance (0-10)
6. Generate QA report

## Output Format

Provide:
- Compliance score by category
- List of violations/issues
- Risk assessment
- Recommendations
- Go/No-go decision with rationale
"""
        },

        "specmap-charter-helper": {
            "name": "specmap-charter-helper",
            "description": "Interactive project charter completion assistant",
            "content": """# SpecMap Charter Helper

You help users complete their SpecMap project charter using the RULEMAP framework.

## Your Role

Guide users through completing each RULEMAP section of their project charter.

## Charter Sections

Work through each section systematically:

1. **R - ROLE & AUTHORITY**
   - Identify stakeholders
   - Define decision makers
   - Establish accountability

2. **U - UNDERSTANDING & OBJECTIVES**
   - Define the problem
   - Set clear objectives
   - Define success criteria

3. **L - LOGIC & APPROACH**
   - Plan project phases
   - Establish decision framework
   - Define quality gates

4. **E - ELEMENTS & CONSTRAINTS**
   - Technical requirements
   - Resource constraints
   - Compliance needs

5. **M - MOOD & EXPERIENCE**
   - User experience goals
   - Brand alignment
   - Emotional targets

6. **A - AUDIENCE & STAKEHOLDERS**
   - Define user personas
   - Map stakeholder influence
   - Plan engagement strategy

7. **P - PERFORMANCE & SUCCESS**
   - Set KPIs
   - Define milestones
   - Establish metrics

## Interaction Style

- Ask focused questions for each section
- Provide examples and templates
- Validate responses for completeness
- Suggest improvements
- Help prioritize and focus

## Output

Generate a completed charter with:
- All RULEMAP sections filled
- Measurable objectives
- Clear success criteria
- Stakeholder alignment
"""
        }
    }


class SkillManager:
    """Manages Claude Code skill creation and management for SpecMap"""

    def __init__(self, project_path: Optional[Path] = None):
        """
        Initialize skill manager

        Args:
            project_path: Path to SpecMap project. If None, uses current directory
        """
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.skills_dir = self.project_path / ".claude" / "skills"

    def create_skills_directory(self) -> Path:
        """Create .claude/skills directory if it doesn't exist"""
        self.skills_dir.mkdir(parents=True, exist_ok=True)

        # Create README for skills directory
        readme_path = self.skills_dir / "README.md"
        if not readme_path.exists():
            readme_content = """# Claude Code Skills for SpecMap

This directory contains custom skills for Claude Code integration with SpecMap.

## Available Skills

Skills are organized to support the SpecMap workflow:

**Specification Phase:**
- `specmap-reviewer` - Review specs for RULEMAP compliance
- `specmap-charter-helper` - Complete project charters

**Planning Phase:**
- `specmap-planner` - Generate implementation plans
- `specmap-task-generator` - Create TDD task breakdowns

**Quality Assurance:**
- `specmap-qa` - Validate compliance and quality

## Using Skills

In Claude Code, invoke a skill by name:
```
/skill specmap-reviewer
```

## Creating Custom Skills

Skills are markdown files with optional frontmatter:
```markdown
---
name: my-skill
description: What this skill does
---

# Skill Instructions

Your instructions for Claude...
```
"""
            readme_path.write_text(readme_content, encoding='utf-8')

        return self.skills_dir

    def create_skill_from_template(self, template_name: str) -> Dict[str, Any]:
        """
        Create a skill from a predefined template

        Args:
            template_name: Name of the template to use

        Returns:
            Dict with skill creation result
        """
        if template_name not in SkillTemplate.TEMPLATES:
            available = ", ".join(SkillTemplate.TEMPLATES.keys())
            raise ValueError(f"Unknown template '{template_name}'. Available: {available}")

        template = SkillTemplate.TEMPLATES[template_name]
        return self.create_skill(
            name=template['name'],
            description=template['description'],
            content=template['content']
        )

    def create_skill(
        self,
        name: str,
        description: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a custom Claude Code skill

        Args:
            name: Skill name (used as filename)
            description: Brief description of the skill
            content: The skill instructions/content
            metadata: Optional additional metadata

        Returns:
            Dict with creation result including file path
        """
        # Ensure skills directory exists
        self.create_skills_directory()

        # Sanitize name for filename
        safe_name = re.sub(r'[^a-z0-9-]', '', name.lower().replace(' ', '-'))
        skill_file = self.skills_dir / f"{safe_name}.md"

        # Build skill content with frontmatter
        frontmatter = f"""---
name: {name}
description: {description}
created: {datetime.now().strftime("%Y-%m-%d")}
"""

        if metadata:
            for key, value in metadata.items():
                frontmatter += f"{key}: {value}\n"

        frontmatter += "---\n\n"

        full_content = frontmatter + content

        # Write skill file
        skill_file.write_text(full_content, encoding='utf-8')

        return {
            'skill_name': name,
            'skill_file': str(skill_file),
            'description': description,
            'created': True
        }

    def install_all_templates(self) -> Dict[str, Any]:
        """
        Install all predefined SpecMap skill templates

        Returns:
            Dict with installation results
        """
        self.create_skills_directory()

        installed = []
        errors = []

        for template_name in SkillTemplate.TEMPLATES.keys():
            try:
                result = self.create_skill_from_template(template_name)
                installed.append(result['skill_name'])
            except Exception as e:
                errors.append(f"{template_name}: {str(e)}")

        return {
            'installed_count': len(installed),
            'installed_skills': installed,
            'errors': errors,
            'skills_dir': str(self.skills_dir)
        }

    def list_skills(self) -> List[Dict[str, str]]:
        """
        List all installed skills

        Returns:
            List of skill information dicts
        """
        if not self.skills_dir.exists():
            return []

        skills = []
        for skill_file in sorted(self.skills_dir.glob("*.md")):
            if skill_file.name == "README.md":
                continue

            content = skill_file.read_text(encoding='utf-8')

            # Extract metadata from frontmatter
            name = skill_file.stem
            description = ""

            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    for line in frontmatter.split('\n'):
                        if line.startswith('description:'):
                            description = line.split(':', 1)[1].strip()
                        elif line.startswith('name:'):
                            name = line.split(':', 1)[1].strip()

            skills.append({
                'name': name,
                'description': description,
                'file': str(skill_file)
            })

        return skills

    def get_available_templates(self) -> List[Dict[str, str]]:
        """
        Get list of available skill templates

        Returns:
            List of template information
        """
        return [
            {
                'name': name,
                'description': template['description']
            }
            for name, template in SkillTemplate.TEMPLATES.items()
        ]

    def delete_skill(self, skill_name: str) -> Dict[str, Any]:
        """
        Delete a skill

        Args:
            skill_name: Name of skill to delete

        Returns:
            Dict with deletion result
        """
        safe_name = re.sub(r'[^a-z0-9-]', '', skill_name.lower().replace(' ', '-'))
        skill_file = self.skills_dir / f"{safe_name}.md"

        if not skill_file.exists():
            return {
                'success': False,
                'error': f"Skill '{skill_name}' not found"
            }

        skill_file.unlink()

        return {
            'success': True,
            'deleted': skill_name,
            'message': f"Skill '{skill_name}' deleted"
        }
