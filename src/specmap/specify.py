"""
SpecMap Specify Command Implementation
Creates RULEMAP-enhanced specifications with tracking IDs
"""

import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from .structure import ProjectStructure, TemplateManager, generate_feature_id, sanitize_name
from .config import WorkflowState


class SpecificationCreator:
    """Handles creation of feature specifications with RULEMAP structure"""

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.structure = ProjectStructure(project_path)

        # Template manager
        templates_dir = Path(__file__).parent.parent.parent / "templates" / "specifications"
        self.template_manager = TemplateManager(templates_dir)

        # Workflow state
        self.workflow = WorkflowState(project_path)
        self.workflow.load()

    def get_existing_features(self) -> List[str]:
        """Get list of existing feature IDs"""
        features_dir = self.project_path / "01-specifications" / "features"
        if not features_dir.exists():
            return []

        features = []
        for item in features_dir.iterdir():
            if item.is_dir() and re.match(r'^\d{3}-', item.name):
                features.append(item.name)

        return sorted(features)

    def generate_tracking_ids(self, feature_id: str) -> Dict[str, List[str]]:
        """Generate initial tracking IDs for the feature"""

        # Extract feature number
        feature_num = feature_id.split('-')[0]

        tracking_ids = {
            'requirements': [
                f"{feature_num}-R-001",  # Initial requirement ID
            ],
            'questions': [
                f"{feature_num}-Q-001",  # Initial question ID
            ],
            'decisions': [
                f"{feature_num}-D-001",  # Initial decision ID
            ],
            'milestones': [
                f"{feature_num}-M-001",  # Initial milestone ID
            ],
            'tasks': [
                f"{feature_num}-T-001",  # Initial task ID (for planning phase)
            ]
        }

        return tracking_ids

    def create_clarifications_file(self, feature_path: Path, feature_id: str) -> str:
        """Create initial clarifications.md file"""

        feature_num = feature_id.split('-')[0]

        content = f"""# Clarifications: {feature_id}

**Feature**: {feature_id}
**Created**: {datetime.now().strftime('%Y-%m-%d')}
**Status**: Active

---

## Clarification Sessions

### Session {datetime.now().strftime('%Y-%m-%d')}
*Initial specification clarifications*

#### Outstanding Questions
- [ ] **{feature_num}-Q-001**: [Question requiring stakeholder input]
- [ ] **{feature_num}-Q-002**: [Question requiring technical investigation]
- [ ] **{feature_num}-Q-003**: [Question requiring user research]

#### Resolved Questions
*None yet*

---

## Question Categories

### Functional Requirements
*Questions about what the system should do*

### Non-Functional Requirements
*Questions about how the system should perform*

### User Experience
*Questions about user interactions and experience*

### Technical Constraints
*Questions about technical limitations and decisions*

### Business Rules
*Questions about business logic and processes*

---

## Clarification Process

1. **Identify** unclear or missing requirements
2. **Document** questions with tracking IDs
3. **Research** and gather information
4. **Validate** answers with stakeholders
5. **Update** specification with clarifications

---

**Next Steps**: Run `specmap clarify` to begin interactive clarification process
"""

        clarifications_file = feature_path / "clarifications.md"
        clarifications_file.write_text(content, encoding='utf-8')
        return str(clarifications_file)

    def create_research_file(self, feature_path: Path, feature_id: str) -> str:
        """Create initial research.md file"""

        feature_num = feature_id.split('-')[0]

        content = f"""# Research: {feature_id}

**Feature**: {feature_id}
**Created**: {datetime.now().strftime('%Y-%m-%d')}
**Status**: Active

---

## Research Areas

### User Research
- [ ] **{feature_num}-R-001**: User interviews and feedback
- [ ] **{feature_num}-R-002**: Competitive analysis
- [ ] **{feature_num}-R-003**: User journey mapping

### Technical Research
- [ ] **{feature_num}-R-004**: Technology stack evaluation
- [ ] **{feature_num}-R-005**: Performance requirements analysis
- [ ] **{feature_num}-R-006**: Security considerations

### Business Research
- [ ] **{feature_num}-R-007**: Market analysis
- [ ] **{feature_num}-R-008**: Business impact assessment
- [ ] **{feature_num}-R-009**: Cost-benefit analysis

---

## Research Findings

### Key Insights
*Document important discoveries here*

### Assumptions Validated
*Track which assumptions were confirmed*

### Assumptions Invalidated
*Track which assumptions were proven wrong*

### New Requirements Discovered
*Document any new requirements found during research*

---

## Research Sources

### Internal Sources
- Stakeholder interviews
- Internal documentation
- Existing system analysis

### External Sources
- Industry reports
- Competitor analysis
- User feedback

### Technical Sources
- Documentation reviews
- Technical feasibility studies
- Performance benchmarks

---

**Research Status**: In Progress
**Next Review**: {datetime.now().strftime('%Y-%m-%d')}
"""

        research_file = feature_path / "research.md"
        research_file.write_text(content, encoding='utf-8')
        return str(research_file)

    def create_specification(self, description: str, feature_id: Optional[str] = None) -> Dict:
        """Create a new feature specification with RULEMAP structure"""

        # Validate project structure
        if not (self.project_path / "01-specifications").exists():
            raise ValueError("Not in a SpecMap project directory. Run 'specmap init' first.")

        # Generate feature ID if not provided
        if not feature_id:
            existing_features = self.get_existing_features()
            # Get first 3 words and create a clean name
            words = description.split()[0:3]
            feature_name = '-'.join(words)
            feature_id = generate_feature_id(feature_name, existing_features)

        # Create feature folder structure
        feature_paths = self.structure.create_feature_structure(feature_id)
        feature_path = feature_paths['spec']

        # Generate tracking IDs
        tracking_ids = self.generate_tracking_ids(feature_id)

        # Prepare template variables
        feature_name = feature_id.replace('-', ' ').title()
        template_vars = {
            'FEATURE NAME': feature_name,
            '###': feature_id.split('-')[0],
            'feature-name': feature_id,
            'DATE': datetime.now().strftime('%Y-%m-%d'),
        }

        # Render and save the specification template
        try:
            spec_content = self.template_manager.render_template(
                'spec-template-enhanced',
                template_vars
            )

            # Add description to the specification
            spec_content = self._add_description_to_spec(spec_content, description)

            spec_file = feature_path / "spec.md"
            spec_file.write_text(spec_content, encoding='utf-8')

        except FileNotFoundError:
            # Fallback if template not found
            spec_content = self._create_basic_spec(feature_id, feature_name, description)
            spec_file = feature_path / "spec.md"
            spec_file.write_text(spec_content, encoding='utf-8')

        # Create clarifications and research files
        clarifications_file = self.create_clarifications_file(feature_path, feature_id)
        research_file = self.create_research_file(feature_path, feature_id)

        # Update workflow state
        self.workflow.add_feature(feature_id, {
            'status': 'specification',
            'created': datetime.now().isoformat(),
            'description': description,
            'tracking_ids': tracking_ids
        })

        # Update workflow phase if this is the first feature
        if not self.get_existing_features():
            self.workflow.update_phase('specification')

        return {
            'feature_id': feature_id,
            'feature_path': str(feature_path),
            'spec_file': str(spec_file),
            'clarifications_file': clarifications_file,
            'research_file': research_file,
            'tracking_ids': tracking_ids
        }

    def _add_description_to_spec(self, spec_content: str, description: str) -> str:
        """Add the provided description to the specification template"""

        # Replace the problem statement placeholder with actual description
        problem_statement_section = "**Core Problem**: [What needs solving]"
        updated_section = f"**Core Problem**: {description}"

        spec_content = spec_content.replace(problem_statement_section, updated_section)

        # Also add to the primary user story
        user_story_placeholder = "I want to [desired action],"
        # Extract a simple user action from description
        action = description.lower().replace('i want to ', '').replace('we need to ', '')
        updated_story = f"I want to {action},"

        spec_content = spec_content.replace(user_story_placeholder, updated_story)

        return spec_content

    def _create_basic_spec(self, feature_id: str, feature_name: str, description: str) -> str:
        """Create a basic specification if template is not available"""

        feature_num = feature_id.split('-')[0]

        return f"""# Feature Specification: {feature_name} (SpecMap Enhanced)

**Feature Branch**: `{feature_id}`
**Created**: {datetime.now().strftime('%Y-%m-%d')}
**Status**: Draft
**RULEMAP Score**: [Pending]
**System**: SpecMap (Unified Spec-Kit + RULEMAP-PRD)

---

## Problem Statement

**Core Problem**: {description}

**Impact Analysis**: [To be determined during clarification]
**Root Cause**: [To be determined during clarification]
**Urgency Level**: [To be determined during clarification]

---

## User Story

```
As a [user type],
I want to {description.lower()},
So that [value/benefit - to be clarified]
```

---

## Initial Requirements

- **{feature_num}-R-001**: System MUST [specific capability - to be clarified]
- **{feature_num}-R-002**: System MUST [specific capability - to be clarified]
- **{feature_num}-R-003**: Users MUST be able to [key interaction - to be clarified]

---

## Next Steps

1. Run `specmap clarify` to resolve open questions
2. Complete all RULEMAP sections
3. Achieve RULEMAP score >= 8.0
4. Get stakeholder approval

---

**Specification Status**: Draft
**Next Phase**: Clarification (run: specmap clarify)
"""