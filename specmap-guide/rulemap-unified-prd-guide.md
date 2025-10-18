# RULEMAP™ Unified PRD System
## Complete Framework for AI-Driven Product Development

### Version 1.0 | Production Ready

---

## Quick Reference

**RULEMAP-PRD** = Systematic framework that transforms any product concept into a complete development project using RULEMAP principles for prompts, agents, and requirements.

**One Command Setup** → **Complete Project Structure** → **AI-Guided Development**

---

## System Overview

The RULEMAP-PRD system automatically creates a standardized project structure and provides AI agents to guide you from initial concept to deployment-ready features.

### Core Components
- **Project Structure Automation**: Instant folder creation and organization
- **RULEMAP-Based PRD Generation**: Structured requirements using proven framework
- **AI Agent Orchestration**: Specialized agents for each development phase
- **Progress Tracking**: Comprehensive activity monitoring and updates
- **Quality Assurance**: Built-in RULEMAP scoring and validation

---

## Project Structure Template

When you initialize any project with RULEMAP-PRD, the following structure is automatically created:

```
[PROJECT-NAME]/
├── 00-project-setup/
│   ├── project-charter.md           # RULEMAP-based project definition
│   ├── stakeholder-matrix.md        # Audience mapping
│   ├── success-metrics.md           # Performance criteria
│   └── project-config.yaml          # System configuration
│
├── 01-requirements/
│   ├── prd-[feature-name].md        # Main PRD using RULEMAP structure
│   ├── user-stories.md              # Detailed user narratives
│   ├── acceptance-criteria.md       # Testing requirements
│   ├── technical-constraints.md     # System limitations
│   └── business-rules.md            # Logic requirements
│
├── 02-design-planning/
│   ├── architecture-decisions.md    # Technical design choices
│   ├── ui-ux-requirements.md        # Interface specifications
│   ├── data-models.md               # Information architecture
│   ├── integration-points.md        # External dependencies
│   └── security-requirements.md     # Compliance and protection
│
├── 03-implementation/
│   ├── tasks-[prd-name].md          # Generated task breakdown
│   ├── development-log.md           # Daily progress tracking
│   ├── code-review-notes.md         # Quality feedback
│   ├── testing-results.md           # Validation outcomes
│   └── deployment-checklist.md      # Release preparation
│
├── 04-agents/
│   ├── agent-assignments.md         # Current agent responsibilities
│   ├── session-summaries/           # Individual session records
│   │   ├── YYYY-MM-DD-session-01.md
│   │   ├── YYYY-MM-DD-session-02.md
│   │   └── ...
│   ├── agent-configurations/        # RULEMAP agent definitions
│   │   ├── prd-agent-config.yaml
│   │   ├── task-agent-config.yaml
│   │   ├── review-agent-config.yaml
│   │   └── deploy-agent-config.yaml
│   └── agent-performance/           # Scoring and improvement
│       ├── agent-scores.md
│       ├── improvement-log.md
│       └── optimization-notes.md
│
├── 05-quality-assurance/
│   ├── rulemap-scores/              # RULEMAP evaluation results
│   │   ├── prd-scoring.md
│   │   ├── task-scoring.md
│   │   └── agent-scoring.md
│   ├── validation-reports/          # Testing and compliance
│   ├── user-feedback/               # Stakeholder input
│   └── improvement-recommendations.md
│
├── 06-documentation/
│   ├── user-guides/                 # End-user documentation
│   ├── technical-docs/              # Developer documentation
│   ├── api-specifications/          # Interface documentation
│   └── deployment-guides/           # Operations documentation
│
├── 07-project-tracking/
│   ├── timeline.md                  # Project schedule
│   ├── milestone-tracker.md         # Key deliverable status
│   ├── risk-register.md             # Issues and mitigation
│   ├── change-log.md                # Scope modifications
│   └── budget-tracking.md           # Resource utilization
│
└── 08-deliverables/
    ├── releases/                    # Version-controlled outputs
    ├── presentations/               # Stakeholder communications
    ├── final-reports/               # Project completion summaries
    └── handover-documents/          # Transition materials
```

---

## Initialization Process

### Step 1: Project Setup Command
```bash
# Initialize new RULEMAP-PRD project
rulemap-init [PROJECT-NAME] [PROJECT-TYPE]

# Example:
rulemap-init "E-commerce-Checkout" "web-application"
```

### Step 2: Automated Structure Creation
The system automatically:
1. Creates all folder structures
2. Generates template files with RULEMAP headers
3. Initializes agent configurations
4. Sets up tracking mechanisms
5. Creates initial project charter

### Step 3: Configuration Wizard
Interactive setup that captures:
- Project stakeholders and roles
- Success metrics and KPIs  
- Technical constraints and preferences
- Timeline and milestone requirements
- Quality standards and compliance needs

---

## Agent Management System

### Agent Roles and Responsibilities

#### Agent Philosophy: "Brilliant Recent Graduates"
All RULEMAP-PRD agents are designed as exceptionally talented recent graduates who:
- **✅ Have superior technical knowledge and analytical capabilities**
- **✅ Possess comprehensive understanding of their specialized domains**  
- **❌ Lack real-world experience and practical wisdom**
- **❌ Need collaboration and guidance on business context**

**Key Behavioral Requirements:**
- **Always explain reasoning in detail** - don't just state conclusions
- **Break down complex concepts** - assume collaborator needs full explanation
- **Seek validation frequently** - especially on business priorities and context
- **Collaborate rather than assume** - treat user as experienced mentor

#### 1. PRD Generator Agent
```yaml
AGENT_ID: "prd-generator-v1"
SPECIALIZATION: "Requirements Analysis & Documentation"
PERSONA: "Brilliant recent graduate with advanced training in product management and requirements analysis"

CORE_STRENGTHS:
  - Deep understanding of requirements methodologies and RULEMAP principles
  - Advanced pattern recognition for business needs and user problems
  - Superior analytical skills for breaking down complex business problems

EXPERIENCE_GAPS:
  - Limited real-world experience with stakeholder politics and competing priorities
  - Needs guidance on business context, market dynamics, and strategic implications
  - Must learn how requirements fit into broader organizational goals

COLLABORATION_STYLE:
  - "Let me walk you through my requirements analysis approach and explain why I'm structuring it this way..."
  - "I'd like to understand the business context before making recommendations..."
  - "Here's my reasoning for this requirement priority - does this align with your strategic thinking?"

OUTPUT_LOCATION: "01-requirements/"
SESSION_TRACKING: "04-agents/session-summaries/"
```

#### 2. Task Planning Agent  
```yaml
AGENT_ID: "task-planner-v1"
SPECIALIZATION: "Implementation Planning & Breakdown"
PERSONA: "Brilliant recent graduate with advanced training in software architecture and project management"

CORE_STRENGTHS:
  - Comprehensive understanding of software architecture patterns and best practices
  - Superior analytical skills for identifying dependencies and optimizing sequences
  - Advanced knowledge of development processes and testing strategies

EXPERIENCE_GAPS:
  - Limited real-world experience with team dynamics and individual developer capabilities
  - Needs guidance on organizational culture and existing technical debt
  - Must learn how technical decisions impact business timelines and resources

COLLABORATION_STYLE:
  - "Let me walk you through my technical analysis and explain why I'm recommending this implementation sequence..."
  - "I've identified several technical approaches - let me break down the trade-offs and get your input on business priorities..."
  - "Here's how I'm estimating effort and why I think these dependencies are critical..."

OUTPUT_LOCATION: "03-implementation/"
SESSION_TRACKING: "04-agents/session-summaries/"
```

#### 3. Development Guide Agent
```yaml
AGENT_ID: "dev-guide-v1"
SPECIALIZATION: "Implementation Guidance & Support"
PERSONA: "Brilliant recent graduate with advanced training in software engineering and code quality"

CORE_STRENGTHS:
  - Deep technical knowledge of coding best practices and quality standards
  - Superior debugging and optimization analytical skills
  - Comprehensive understanding of testing strategies and development tools

EXPERIENCE_GAPS:
  - Limited experience with team collaboration and individual developer mentoring
  - Needs guidance on balancing code perfection with business delivery timelines
  - Must learn how technical decisions impact team morale and productivity

COLLABORATION_STYLE:
  - "Let me explain my code review feedback and why these changes will improve maintainability..."
  - "I want to walk you through the technical approach I recommend and explain the alternatives I considered..."
  - "Here's my analysis of this technical challenge - does my debugging approach make sense given your team's constraints?"

OUTPUT_LOCATION: "03-implementation/"
SESSION_TRACKING: "04-agents/session-summaries/"
```

#### 4. Quality Assurance Agent
```yaml
AGENT_ID: "qa-monitor-v1"
SPECIALIZATION: "Quality Control & RULEMAP Scoring"
PERSONA: "Brilliant recent graduate with advanced training in quality assurance and systematic evaluation"

CORE_STRENGTHS:
  - Comprehensive understanding of quality methodologies and RULEMAP scoring
  - Superior analytical skills for identifying quality gaps and improvement opportunities
  - Deep technical knowledge of testing strategies and validation approaches

EXPERIENCE_GAPS:
  - Limited experience with business risk tolerance and acceptable quality trade-offs
  - Needs guidance on organizational quality culture and user expectations
  - Must learn how quality decisions impact business outcomes and competitive position

COLLABORATION_STYLE:
  - "Let me walk you through my quality assessment methodology and explain what I found and why it matters..."
  - "I've identified several quality risks - let me explain the business implications and what I recommend..."
  - "Here's my RULEMAP scoring analysis - does my reasoning align with your quality priorities and business constraints?"

OUTPUT_LOCATION: "05-quality-assurance/"
SESSION_TRACKING: "04-agents/session-summaries/"
```

### Agent Session Tracking

#### Session Summary Template
```markdown
# Agent Session Summary
**Date**: [YYYY-MM-DD]
**Time**: [HH:MM - HH:MM] 
**Agent**: [Agent ID and Name]
**Session ID**: [Unique Identifier]

## Session Objectives
- [Primary goal 1]
- [Primary goal 2] 
- [Primary goal 3]

## Work Completed
### Tasks Accomplished
- [x] [Completed task with outcome]
- [x] [Completed task with outcome]
- [ ] [Incomplete task - reason]

### Files Created/Modified
- `path/to/file.md` - [Description of changes]
- `path/to/another-file.yaml` - [Description of changes]

### Decisions Made
- [Key decision 1 with rationale]
- [Key decision 2 with rationale]

## Challenges Encountered
- [Challenge description and resolution]
- [Challenge description - requires follow-up]

## Next Session Planning
### Immediate Priorities
1. [Priority 1 with context]
2. [Priority 2 with context]

### Dependencies
- Waiting for: [External dependency]
- Blocked by: [Internal blocker]

## Quality Metrics
- RULEMAP Score: [X.X/10] 
- Completion Rate: [XX%]
- Stakeholder Satisfaction: [Rating/Notes]

## Session Notes
[Free-form notes about insights, observations, or recommendations]

---
**Session End**: [HH:MM]
**Next Scheduled**: [Date/Time or TBD]
```

### Agent Assignment Tracking
```markdown
# Current Agent Assignments

## Active Assignments

### PRD Generator Agent
- **Current Focus**: [Project Phase/Task]
- **Status**: [Active/Paused/Completed]
- **Progress**: [Percentage complete]
- **Next Milestone**: [Date and deliverable]
- **Dependencies**: [Any blocking items]

### Task Planning Agent  
- **Current Focus**: [Project Phase/Task]
- **Status**: [Active/Paused/Completed]
- **Progress**: [Percentage complete]
- **Next Milestone**: [Date and deliverable]
- **Dependencies**: [Any blocking items]

### Development Guide Agent
- **Current Focus**: [Project Phase/Task] 
- **Status**: [Active/Paused/Completed]
- **Progress**: [Percentage complete]
- **Next Milestone**: [Date and deliverable]
- **Dependencies**: [Any blocking items]

### Quality Assurance Agent
- **Current Focus**: [Project Phase/Task]
- **Status**: [Active/Paused/Completed] 
- **Progress**: [Percentage complete]
- **Next Milestone**: [Date and deliverable]
- **Dependencies**: [Any blocking items]

## Recent Handoffs
- [Date]: [From Agent] → [To Agent] : [Deliverable/Context]
- [Date]: [From Agent] → [To Agent] : [Deliverable/Context]

## Upcoming Assignments
- [Date]: [Agent] will begin [Task/Phase]
- [Date]: [Agent] will complete [Deliverable]
```

---

## RULEMAP-PRD Workflow

### Phase 1: Project Initialization
```yaml
TRIGGER: "New project request or concept"

PROCESS:
  1. Run project initialization script
  2. Create folder structure automatically  
  3. Launch PRD Generator Agent
  4. Conduct RULEMAP-guided requirements gathering
  5. Generate initial PRD using RULEMAP structure

OUTPUT: "Complete project structure + Initial PRD"
HANDOFF_TO: "Task Planning Agent"
```

### Phase 2: Planning & Task Generation
```yaml  
TRIGGER: "Completed and validated PRD"

PROCESS:
  1. Task Planning Agent analyzes PRD
  2. Generate implementation task hierarchy
  3. Create development roadmap
  4. Estimate effort and identify dependencies
  5. Validate plan with stakeholders

OUTPUT: "Detailed task breakdown + Implementation plan"  
HANDOFF_TO: "Development Guide Agent"
```

### Phase 3: Implementation Guidance
```yaml
TRIGGER: "Approved implementation plan"

PROCESS:
  1. Development Guide Agent begins task coordination
  2. Provide implementation guidance for each task
  3. Conduct code reviews and quality checks
  4. Manage testing and validation processes
  5. Coordinate deployment preparation

OUTPUT: "Completed feature + Deployment package"
HANDOFF_TO: "Quality Assurance Agent"  
```

### Phase 4: Quality Validation
```yaml
TRIGGER: "Implementation completion"

PROCESS:
  1. QA Agent conducts comprehensive RULEMAP scoring
  2. Validate all deliverables against requirements
  3. Generate quality assurance report
  4. Identify improvement opportunities
  5. Confirm deployment readiness

OUTPUT: "Quality validation report + Go/No-go decision"
HANDOFF_TO: "Project completion or iteration"
```

---

## RULEMAP-Enhanced PRD Structure

### Complete PRD Template
```markdown
# PRD: [Feature Name]
**Project**: [Project Name]
**Version**: [Version Number]
**Date**: [YYYY-MM-DD]
**RULEMAP Score**: [Pending/X.X]

---

## R - ROLE & AUTHORITY

### Product Owner Role
**Primary Identity**: [Specific role with expertise]
**Experience Level**: [Background and qualifications]
**Authority Boundaries**: [Decision-making scope]
**Stakeholder Representation**: [Who they advocate for]

### Technical Authority
**Development Oversight**: [Technical decision rights]
**Architecture Influence**: [Design authority level]
**Resource Allocation**: [Budget and timeline control]

---

## U - UNDERSTANDING & OBJECTIVES

### Problem Statement
**Core Problem**: [What needs solving]
**Impact Analysis**: [Cost of not solving]  
**Root Cause**: [Why this problem exists]
**Urgency Level**: [Timeline pressure]

### User Stories
```yaml
USER_STORY_1:
  as_a: "[User type]"
  i_want: "[Desired action]"
  so_that: "[Value/benefit]"
  acceptance_criteria:
    - "[Testable condition 1]"
    - "[Testable condition 2]"

USER_STORY_2:
  as_a: "[User type]"
  i_want: "[Desired action]" 
  so_that: "[Value/benefit]"
  acceptance_criteria:
    - "[Testable condition 1]"
    - "[Testable condition 2]"
```

### Business Objectives
- **Primary Goal**: [Main business outcome]
- **Secondary Goals**: [Supporting outcomes]
- **Success Metrics**: [Measurable KPIs]
- **Timeline**: [Key milestones]

---

## L - LOGIC & STRUCTURE

### Feature Architecture
**System Integration**: [How feature fits into existing system]
**Component Breakdown**: [Major functional components]
**Data Flow**: [Information movement and processing]
**User Journey**: [Step-by-step interaction flow]

### Implementation Sequence
```yaml
PHASE_1:
  name: "[Phase name]"
  objectives: ["Goal 1", "Goal 2"]
  deliverables: ["Deliverable 1", "Deliverable 2"]
  
PHASE_2:
  name: "[Phase name]"
  objectives: ["Goal 1", "Goal 2"]
  deliverables: ["Deliverable 1", "Deliverable 2"]
```

### Dependencies & Risks
**Upstream Dependencies**: [Required inputs]
**Downstream Impacts**: [Affected systems]
**Risk Assessment**: [Potential issues and mitigation]

---

## E - ELEMENTS & SPECIFICATIONS

### Functional Requirements
1. **[Requirement ID]**: [Detailed requirement description]
2. **[Requirement ID]**: [Detailed requirement description]
3. **[Requirement ID]**: [Detailed requirement description]

### Technical Constraints
- **Platform**: [Technology requirements]
- **Performance**: [Speed and scale requirements]
- **Security**: [Compliance and protection needs]
- **Integration**: [External system requirements]

### Design Requirements
- **UI/UX Standards**: [Interface guidelines]
- **Accessibility**: [Compliance requirements]
- **Responsive Design**: [Device support]
- **Brand Alignment**: [Visual consistency]

### Acceptance Criteria
```yaml
ACCEPTANCE_TEST_1:
  scenario: "[Test scenario description]"
  given: "[Initial conditions]"
  when: "[User action]"
  then: "[Expected outcome]"

ACCEPTANCE_TEST_2:
  scenario: "[Test scenario description]"
  given: "[Initial conditions]"
  when: "[User action]" 
  then: "[Expected outcome]"
```

---

## M - MOOD & EXPERIENCE

### User Experience Tone
**Emotional Goal**: [Feeling users should have]
**Interaction Style**: [Formal/casual/friendly/professional]
**Visual Aesthetics**: [Look and feel description]
**Brand Voice**: [Communication style]

### Emotional Journey
```yaml
AWARENESS_STAGE:
  user_feeling: "[Emotional state]"
  design_response: "[How we address it]"

CONSIDERATION_STAGE:
  user_feeling: "[Emotional state]"
  design_response: "[How we address it]"

DECISION_STAGE:
  user_feeling: "[Emotional state]"
  design_response: "[How we address it]"

POST_PURCHASE:
  user_feeling: "[Emotional state]"
  design_response: "[How we address it]"
```

---

## A - AUDIENCE & STAKEHOLDERS

### Primary Users
```yaml
USER_SEGMENT_1:
  demographics: "[Age, role, experience level]"
  psychographics: "[Motivations, fears, values]"
  current_behavior: "[How they work today]"
  pain_points: "[Specific problems they face]"
  success_definition: "[What they want to achieve]"

USER_SEGMENT_2:
  demographics: "[Age, role, experience level]"
  psychographics: "[Motivations, fears, values]" 
  current_behavior: "[How they work today]"
  pain_points: "[Specific problems they face]"
  success_definition: "[What they want to achieve]"
```

### Stakeholder Matrix
| Stakeholder | Interest Level | Influence Level | Engagement Strategy |
|-------------|---------------|-----------------|-------------------|
| [Role] | [High/Med/Low] | [High/Med/Low] | [How to engage] |
| [Role] | [High/Med/Low] | [High/Med/Low] | [How to engage] |

### Development Team Requirements
- **Skill Level**: [Technical expertise needed]
- **Documentation Needs**: [What level of detail required]
- **Support Requirements**: [Training and guidance needed]

---

## P - PERFORMANCE & METRICS

### Business KPIs
- **Primary Metric**: [Main success measure]
- **Secondary Metrics**: [Supporting measures]
- **Leading Indicators**: [Early warning signals]
- **Lagging Indicators**: [Outcome measures]

### User Experience Metrics
- **Usability Scores**: [Task completion rates]
- **Satisfaction Ratings**: [User feedback scores]
- **Adoption Rates**: [Feature usage statistics]
- **Support Impact**: [Ticket reduction targets]

### Technical Performance
- **Speed Requirements**: [Response time targets]
- **Scalability Needs**: [User/data volume capacity]
- **Reliability Standards**: [Uptime requirements]
- **Security Benchmarks**: [Compliance measures]

### Implementation Timeline
```yaml
MILESTONE_1:
  date: "[YYYY-MM-DD]"
  deliverable: "[What will be complete]"
  success_criteria: "[How to measure success]"

MILESTONE_2:
  date: "[YYYY-MM-DD]"
  deliverable: "[What will be complete]"
  success_criteria: "[How to measure success]"

FINAL_DELIVERY:
  date: "[YYYY-MM-DD]"
  deliverable: "[Complete feature]"
  success_criteria: "[Full acceptance criteria]"
```

---

## Implementation Notes

### Development Priorities
1. [Highest priority requirement with justification]
2. [Second priority requirement with justification]  
3. [Third priority requirement with justification]

### Technical Considerations
- **Architecture Decisions**: [Key technical choices]
- **Third-party Dependencies**: [External services needed]
- **Migration Requirements**: [Data or system transitions]

### Testing Strategy
- **Unit Testing**: [Component-level testing approach]
- **Integration Testing**: [System interaction testing]
- **User Acceptance Testing**: [Business validation approach]
- **Performance Testing**: [Load and stress testing plan]

---

## Open Questions & Future Considerations

### Unresolved Issues
- [Question 1 requiring stakeholder input]
- [Question 2 requiring technical investigation]
- [Question 3 requiring user research]

### Future Enhancements
- [Enhancement 1 for future releases]
- [Enhancement 2 for future releases] 
- [Enhancement 3 for future releases]

### Success Review Plan
- **Review Schedule**: [When to assess success]
- **Review Participants**: [Who should be involved]
- **Review Criteria**: [What to evaluate]
- **Iteration Planning**: [How to improve based on results]

---

**PRD Completion Status**: [Draft/Review/Approved/Active]
**Next Review Date**: [YYYY-MM-DD]
**Approved By**: [Stakeholder signatures/approvals]
```

---

## Rules and Automation

### Automated Folder Management
```yaml
FOLDER_RULES:
  creation_trigger: "Project initialization command"
  
  naming_convention:
    projects: "[PROJECT-NAME]-[YYYY-MM-DD]"
    sessions: "YYYY-MM-DD-session-[##]"
    versions: "[document-name]-v[#.#]"
  
  auto_cleanup:
    temp_files: "Daily at midnight"
    old_sessions: "Archive after 90 days"
    completed_projects: "Archive after 1 year"

TRACKING_AUTOMATION:
  session_logging: "Auto-start on agent activation"
  progress_updates: "Real-time task completion tracking"  
  metric_collection: "Continuous RULEMAP scoring"
  report_generation: "Weekly status reports"
```

### Quality Gates
```yaml
QUALITY_CHECKPOINTS:
  prd_completion:
    - "RULEMAP score >= 7.0"
    - "All required sections present"
    - "Stakeholder review completed"
    
  task_generation:
    - "All requirements mapped to tasks"
    - "Dependencies clearly identified"
    - "Effort estimates provided"
    
  implementation_ready:
    - "Technical feasibility confirmed"
    - "Resource allocation approved" 
    - "Timeline validated"
    
  deployment_ready:
    - "All acceptance criteria met"
    - "Testing completed successfully"
    - "Documentation updated"
```

### Agent Orchestration Rules
```yaml
HANDOFF_PROTOCOLS:
  prd_to_planning:
    trigger: "PRD RULEMAP score >= 7.0 AND stakeholder approval"
    process: "Automatic task assignment to Planning Agent"
    
  planning_to_development:
    trigger: "Task breakdown approved AND resources allocated"
    process: "Development Guide Agent activation"
    
  development_to_qa:
    trigger: "Implementation marked complete"
    process: "QA Agent begins validation process"
    
  qa_to_deployment:
    trigger: "Quality validation passed"
    process: "Deployment checklist activation"
```

---

## Getting Started

### Quick Start Commands
```bash
# Create new RULEMAP-PRD project
rulemap-init "My-New-Feature" --type="web-app"

# Activate PRD Generator Agent
rulemap-agent activate prd-generator --project="My-New-Feature"

# Generate project status report
rulemap-status --project="My-New-Feature" --format="summary"

# Score all project artifacts
rulemap-score --project="My-New-Feature" --output="detailed"
```

### First-Time Setup Checklist
- [ ] Install RULEMAP-PRD system
- [ ] Configure agent settings
- [ ] Set up project templates
- [ ] Test with sample project
- [ ] Train team on workflow
- [ ] Establish quality standards
- [ ] Create backup/archive procedures

### Integration Points
- **Version Control**: Git integration with automated commits
- **Project Management**: Jira/Asana task synchronization  
- **Communication**: Slack/Teams status updates
- **Documentation**: Confluence/Notion integration
- **Monitoring**: Dashboard and analytics integration

---

*Transform any product concept into a complete, professionally-managed development project with RULEMAP-PRD.*
