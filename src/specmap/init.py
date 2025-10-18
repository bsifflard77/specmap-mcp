"""
Project initialization module for SpecMap
Handles creation of new projects with unified structure
"""

from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import shutil

from .structure import ProjectStructure, TemplateManager
from .config import SpecMapConfig, WorkflowState


class ProjectInitializer:
    """Handles initialization of new SpecMap projects"""

    def __init__(self, project_path: Path, project_name: str, project_type: str, agent: str):
        self.project_path = Path(project_path)
        self.project_name = project_name
        self.project_type = project_type
        self.agent = agent
        self.timestamp = datetime.now().strftime("%Y-%m-%d")

    def initialize(self) -> Dict[str, Any]:
        """Initialize complete project structure"""

        # Create folder structure
        structure = ProjectStructure(self.project_path)
        created_folders = structure.create()

        # Initialize configuration
        config = SpecMapConfig(self.project_path)
        config.update({
            'project': {
                'name': self.project_name,
                'type': self.project_type,
                'created': self.timestamp,
                'version': '1.0.0'
            },
            'agents': {
                'base_agent': self.agent
            }
        })

        # Initialize workflow state
        workflow = WorkflowState(self.project_path)
        workflow.update_phase('initialization')
        workflow.save()

        # Create core documents
        self._create_constitution()
        self._create_charter()
        self._create_readme()
        self._create_gitignore()
        self._create_agent_assignments()

        return {
            'path': str(self.project_path),
            'folders_created': len(created_folders),
            'agent': self.agent,
            'type': self.project_type
        }

    def _create_constitution(self):
        """Create project constitution (quality governance)"""

        content = f"""# Project Constitution: {self.project_name}

**Created**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Type**: {self.project_type}

---

## Preamble

This constitution establishes the foundational principles and governance for the {self.project_name} project.
These principles guide all development decisions, architectural choices, and implementation approaches.

---

## Article I: Modularity Principle

Every feature SHALL be designed with clear boundaries and minimal dependencies.

**Requirements:**
- Features must be independently testable
- Components should have well-defined interfaces
- Coupling should be minimized

---

## Article II: Simplicity First

Complexity must be justified. Start simple, add complexity only when necessary.

**Requirements:**
- Prefer simple solutions over clever ones
- Document all complexity justifications
- Regularly review and simplify existing code

---

## Article III: Test-First Development

All implementation MUST follow test-driven development principles.

**Requirements:**
- Write tests before implementation
- All tests must fail initially (Red phase)
- Implementation makes tests pass (Green phase)
- Refactor while maintaining test success (Refactor phase)

---

## Article IV: Documentation Standards

Code and design decisions must be well-documented.

**Requirements:**
- All public interfaces must have documentation
- Architectural decisions must be recorded
- README files must be maintained
- API specifications must be current

---

## Article V: Quality Gates

Quality thresholds must be met before advancing phases.

**Requirements:**
- RULEMAP score >= 8.0 for specifications
- Constitution compliance for all implementations
- Test coverage >= 80% for core functionality
- Performance requirements must be validated

---

## Article VI: Stakeholder Alignment

Development must maintain alignment with business objectives.

**Requirements:**
- Regular stakeholder reviews
- Clear success criteria
- Business value justification for features
- User feedback integration

---

## Amendment Process

This constitution can be amended through:
1. Documented proposal with rationale
2. Stakeholder review and approval
3. Impact assessment on existing work
4. Version control and change tracking

---

**Status**: Active
**Version**: 1.0
**Last Updated**: {self.timestamp}
"""

        constitution_file = self.project_path / "00-governance" / "constitution.md"
        constitution_file.write_text(content, encoding='utf-8')

    def _create_charter(self):
        """Create RULEMAP project charter"""

        content = f"""# Project Charter: {self.project_name}

**Project Type**: {self.project_type}
**Created**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Status**: Initiated
**System**: SpecMap - AI-Powered Specification-Driven Development

---

## R - ROLE & AUTHORITY

### Project Owner
**Primary Stakeholder**: [To be defined]
**Decision Authority**: [To be defined]
**Accountability**: [To be defined]

### Development Team
**Team Lead**: [To be assigned]
**Team Size**: [To be determined]
**Skill Requirements**: [To be assessed]

---

## U - UNDERSTANDING & OBJECTIVES

### Project Vision
**Problem Statement**: [Define the core problem this project solves]

**Primary Objective**: [Main goal or outcome desired]

**Success Definition**: [How will we know we've succeeded?]

### Business Context
**Strategic Alignment**: [How this project supports business goals]
**User Impact**: [Who benefits and how]
**Market Opportunity**: [Business case or competitive advantage]

---

## L - LOGIC & APPROACH

### Project Phases
1. **Requirements & Planning** (Estimated: [Duration])
2. **Design & Architecture** (Estimated: [Duration])
3. **Development & Testing** (Estimated: [Duration])
4. **Deployment & Launch** (Estimated: [Duration])

### Decision Framework
**Priority Criteria**: [How to prioritize features/tasks]
**Quality Gates**: [Standards that must be met]
**Risk Management**: [How to handle uncertainties]

---

## E - ELEMENTS & CONSTRAINTS

### Technical Requirements
**Platform**: {self.project_type}
**Technology Stack**: [To be determined]
**Integration Requirements**: [Systems to connect with]
**Performance Requirements**: [Speed, scale, reliability needs]

### Resource Constraints
**Timeline**: [Project deadline or milestones]
**Budget**: [Financial limitations]
**Team Availability**: [Resource constraints]

### Compliance Requirements
**Standards**: [Industry or company standards to follow]
**Security**: [Data protection and security requirements]
**Accessibility**: [User accessibility requirements]

---

## M - MOOD & EXPERIENCE

### User Experience Goals
**Emotional Target**: [How should users feel when using this?]
**Brand Alignment**: [How does this reflect company values?]
**Aesthetic Direction**: [Visual and interaction style preferences]

---

## A - AUDIENCE & STAKEHOLDERS

### Primary Users
**User Type 1**: [Demographics and needs]
**User Type 2**: [Demographics and needs]

### Stakeholders
| Role | Interest Level | Influence | Engagement Strategy |
|------|---------------|-----------|-------------------|
| [Stakeholder] | [High/Med/Low] | [High/Med/Low] | [How to involve] |

---

## P - PERFORMANCE & SUCCESS

### Key Performance Indicators
**Business Metrics**: [ROI, revenue impact, cost savings]
**User Metrics**: [Adoption, satisfaction, usage]
**Technical Metrics**: [Performance, reliability, quality]

### Success Milestones
- [ ] Requirements approved and specifications complete
- [ ] Design and architecture validated
- [ ] MVP delivered and tested
- [ ] Full feature set implemented
- [ ] Successfully deployed and launched
- [ ] Success metrics achieved

---

## Next Steps
1. Complete stakeholder identification and engagement
2. Conduct initial requirements gathering
3. Run: specmap specify [description] to create first feature
4. Schedule regular project reviews

---

**Charter Status**: [Draft/Approved/Active]
**Next Review**: [Date]
**Approved By**: [Signatures when ready]
"""

        charter_file = self.project_path / "00-governance" / "project-charter.md"
        charter_file.write_text(content, encoding='utf-8')

    def _create_readme(self):
        """Create project README"""

        content = f"""# {self.project_name}

*{self.project_type} project using SpecMap - AI-Powered Spec-Driven Development*

## Quick Start

### 1. Complete Project Setup
- [ ] Review and complete `00-governance/project-charter.md`
- [ ] Update `00-governance/constitution.md` with project-specific principles
- [ ] Define stakeholders and success metrics

### 2. Create Your First Specification
```bash
specmap specify "Your feature description here"
```

### 3. Follow the Unified Workflow
```
Constitution + Charter → Specify → Clarify → Plan → Tasks → Implement → QA
```

## Project Structure

```
{self.project_name}/
├── .specmap/                 # System configuration
├── 00-governance/            # Constitution + Charter
├── 01-specifications/        # RULEMAP-enhanced specs
├── 02-planning/              # Implementation plans & tasks
├── 03-implementation/        # Development tracking
├── 04-agents/               # Agent management
├── 05-quality-assurance/    # Dual validation
├── 06-documentation/        # Project docs
├── 07-project-tracking/     # Progress tracking
└── 08-deliverables/        # Final outputs
```

## SpecMap Features

### Specification & PRD Development
- RULEMAP-enhanced specifications (7-element framework)
- Constitution-based governance
- Systematic clarification process
- Comprehensive tracking ID system

### AI-Guided Workflow
- Multi-platform AI agent support (Claude Code, Copilot, Cursor, Gemini)
- Specialized agent orchestration (PRD Generator, Task Planner, Dev Guide, QA Monitor)
- Complete workflow: Specify → Clarify → Plan → Tasks → Implement → Track
- Specialized agent orchestration
- Quality scoring (>= 8.0 threshold)

## Available Commands

```bash
# Project management
specmap status              # View project status
specmap check              # Check system prerequisites

# Specification workflow
specmap specify [DESC]     # Create RULEMAP-enhanced spec
specmap clarify            # Run clarification process
specmap plan              # Generate implementation plan
specmap tasks             # Create task breakdown
specmap implement         # Begin guided development

# Governance
specmap constitution      # View/edit constitution
specmap charter          # Manage project charter

# Agent management
specmap agent activate [TYPE]  # Activate specialized agent
specmap agent status          # View agent assignments
specmap agent handoff [FROM] [TO]  # Transfer between agents

# Quality assurance
specmap score             # Run quality assessment
specmap sync             # Update agent contexts
```

## Workflow Phases

### Phase 1: Initialization ✓
- Project structure created
- Governance documents initialized
- Configuration established

### Phase 2: Specification
- Create feature specifications with RULEMAP structure
- Run systematic clarification
- Achieve RULEMAP score >= 8.0

### Phase 3: Planning
- Generate implementation plans
- Create task breakdowns
- Validate technical feasibility

### Phase 4: Implementation
- Agent-guided development
- Continuous quality validation
- Session tracking

### Phase 5: Quality Assurance
- Constitution compliance validation
- RULEMAP scoring
- Deployment preparation

## Agent System

### Base Agent
**Current**: {self.agent}

### RULEMAP Specialized Agents
- **PRD Generator**: Requirements analysis and documentation
- **Task Planner**: Implementation breakdown and sequencing
- **Dev Guide**: Development guidance and support
- **QA Monitor**: Quality assurance and scoring

## Quality Standards

- All specifications must achieve RULEMAP score >= 8.0
- All implementations must comply with project constitution
- All requirements must have measurable acceptance criteria
- Continuous quality monitoring throughout development

## Getting Help

1. Review governance documents in `00-governance/`
2. Check agent status: `specmap agent status`
3. View project status: `specmap status --detailed`
4. Consult the integration design document

---

**Project Status**: Initialized
**Next Step**: Create your first feature specification
**Created**: {self.timestamp}
**System**: SpecMap v1.0.0
"""

        readme_file = self.project_path / "README.md"
        readme_file.write_text(content, encoding='utf-8')

    def _create_gitignore(self):
        """Create .gitignore file"""

        content = """# SpecMap Project .gitignore

# Temporary files
*.tmp
*.temp
*~
.DS_Store
Thumbs.db

# Agent working files
04-agents/session-summaries/.working/
04-agents/agent-performance/.cache/

# Configuration overrides
.specmap/local-config.yaml
.specmap/.env

# Backup files
*.bak
*.backup
*_backup_*

# System files
.vscode/
.idea/
*.swp
*.swo

# Quality assurance temporary files
05-quality-assurance/validation-reports/.temp/
05-quality-assurance/.scoring-cache/

# Documentation build artifacts
06-documentation/**/*.html
06-documentation/**/*.pdf
!06-documentation/**/index.html

# Draft deliverables
08-deliverables/drafts/
08-deliverables/.drafts/

# Log files
*.log
logs/

# Python
__pycache__/
*.py[cod]
*$py.class
.Python
env/
venv/
.env

# Node.js (if applicable)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
"""

        gitignore_file = self.project_path / ".gitignore"
        gitignore_file.write_text(content, encoding='utf-8')

    def _create_agent_assignments(self):
        """Create initial agent assignment tracking"""

        content = f"""# Agent Assignments - {self.timestamp}

## Current Agent Status

### Base AI Agent
**Agent**: {self.agent}
**Status**: Configured
**Purpose**: Primary AI interface for all commands

---

## RULEMAP Specialized Agents

### PRD Generator Agent
- **Status**: Ready for activation
- **Current Focus**: Awaiting first feature specification
- **Progress**: 0%
- **Next Milestone**: Complete initial specification
- **Dependencies**: Project charter completion

### Task Planning Agent
- **Status**: Standby
- **Current Focus**: N/A
- **Progress**: 0%
- **Next Milestone**: Analyze completed specification
- **Dependencies**: PRD Generator completion

### Development Guide Agent
- **Status**: Standby
- **Current Focus**: N/A
- **Progress**: 0%
- **Next Milestone**: Begin implementation guidance
- **Dependencies**: Task Planning completion

### Quality Assurance Agent
- **Status**: Standby
- **Current Focus**: N/A
- **Progress**: 0%
- **Next Milestone**: Initial quality assessment
- **Dependencies**: Specification artifacts available

---

## Agent Activation Queue

1. **PRD Generator Agent** - Ready when charter is complete
2. **Task Planning Agent** - Awaits specification completion
3. **Development Guide Agent** - Awaits task breakdown
4. **QA Agent** - Continuous monitoring once artifacts exist

---

## Handoff Protocols

### Specification → Planning
- **Trigger**: Specification achieves RULEMAP score >= 8.0
- **Process**: Automatic handoff with validation
- **Deliverables**: Complete specification + stakeholder approval

### Planning → Development
- **Trigger**: Implementation plan approved
- **Process**: Manual activation after review
- **Deliverables**: Task breakdown + resource allocation

### Development → QA
- **Trigger**: Implementation completion
- **Process**: Continuous integration + milestone reviews
- **Deliverables**: Working implementation + test results

---

**Last Updated**: {self.timestamp}
**Next Review**: After first specification completion
"""

        assignments_file = self.project_path / "04-agents" / "agent-assignments.md"
        assignments_file.write_text(content, encoding='utf-8')