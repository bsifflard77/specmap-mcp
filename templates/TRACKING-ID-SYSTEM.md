# SpecMap Tracking ID System

**Version**: 1.0
**Purpose**: Provide a comprehensive numbering system for all trackable items in SpecMap projects

---

## Overview

The SpecMap Tracking ID System provides a hierarchical, structured approach to identifying and referencing all items in a project, including tasks, questions, issues, decisions, and more.

## ID Structure

### Format
```
[FEATURE]-[CATEGORY]-[NUMBER]
```

**Example**: `001-T-042` = Feature 001, Task 042

### Components

1. **Feature ID**: `###` (3-digit feature number)
2. **Category Code**: Letter(s) indicating item type
3. **Item Number**: Sequential number within category

---

## Category Codes

### Primary Categories

| Code | Type | Description | Example |
|------|------|-------------|---------|
| **F** | Feature | Feature specification | `001-F` |
| **T** | Task | Implementation task | `001-T-001` |
| **Q** | Question | Question requiring answer | `001-Q-001` |
| **D** | Decision | Architecture/design decision | `001-D-001` |
| **I** | Issue | Problem or blocker | `001-I-001` |
| **R** | Requirement | Functional requirement | `001-R-001` |
| **A** | Acceptance | Acceptance criterion | `001-A-001` |
| **M** | Milestone | Project milestone | `001-M-001` |

### Workflow Phase Categories

| Code | Type | Description | Example |
|------|------|-------------|---------|
| **S** | Specification | Spec-phase item | `001-S-001` |
| **P** | Planning | Planning-phase item | `001-P-001` |
| **C** | Clarification | Clarification question | `001-C-001` |
| **V** | Validation | QA/validation item | `001-V-001` |

### Status Indicators (Optional Suffix)

| Suffix | Status | Description |
|--------|--------|-------------|
| `-O` | Open | Not yet started |
| `-IP` | In Progress | Currently being worked |
| `-B` | Blocked | Waiting on dependency |
| `-R` | Resolved | Completed/answered |
| `-C` | Closed | Finalized and archived |

**Example**: `001-Q-005-B` = Feature 001, Question 5, Blocked

---

## Usage Examples

### Feature Development Workflow

```markdown
# Feature 001: User Authentication System

## Specification Phase
- 001-F: Feature specification document
- 001-R-001: System MUST support email/password login
- 001-R-002: System MUST support OAuth providers
- 001-Q-001: Which OAuth providers to support? [OPEN]
- 001-Q-002: Password complexity requirements? [RESOLVED]
- 001-C-001: Clarify session timeout behavior
- 001-D-001: Use JWT for session tokens

## Planning Phase
- 001-P-001: Technical architecture plan
- 001-P-002: Database schema design
- 001-D-002: Choose bcrypt for password hashing
- 001-M-001: Complete authentication MVP by 2025-10-15

## Implementation Phase
- 001-T-001: Create User model
- 001-T-002: Implement password hashing service
- 001-T-003: Create login API endpoint
- 001-T-004: Implement OAuth integration
- 001-I-001: OAuth callback URL configuration issue [BLOCKED]

## Validation Phase
- 001-A-001: User can login with email/password
- 001-A-002: User can login with Google OAuth
- 001-V-001: Security penetration test
- 001-V-002: Load testing for 1000 concurrent users
```

### Cross-Feature References

When referencing items from different features:

```markdown
# Feature 002: User Profile Management

## Dependencies
- Depends on: 001-T-001 (User model from Authentication feature)
- Blocked by: 001-I-001 (OAuth issue must be resolved first)

## Questions
- 002-Q-001: How does this integrate with 001-R-002 (OAuth requirement)?
```

---

## ID Assignment Rules

### Automatic Assignment
- **Feature IDs**: Auto-generated sequentially (001, 002, 003...)
- **Item Numbers**: Sequential within feature and category
- **First item**: Always starts at 001

### Manual Assignment
- Can be assigned manually in documents
- Must follow sequential order within category
- No gaps in numbering (avoid 001, 003, 007 - use 001, 002, 003)

### Retired IDs
- Never reuse retired IDs
- Mark retired items with `[RETIRED]` tag
- Keep in history for reference

---

## Templates with ID Integration

### Task Template
```markdown
## Task: [TASK_ID] - [Task Name]

**ID**: 001-T-042
**Feature**: 001-user-authentication
**Status**: In Progress
**Assigned**: Development Guide Agent
**Dependencies**: 001-T-038, 001-T-041
**Blocks**: 001-T-043, 001-T-044

### Description
[Detailed task description]

### Acceptance Criteria
- [x] Criterion 1
- [ ] Criterion 2

### Related Items
- Implements: 001-R-015
- Addresses: 001-I-003
- Answers: 001-Q-007
```

### Question Template
```markdown
## Question: [QUESTION_ID] - [Question Summary]

**ID**: 001-Q-007
**Feature**: 001-user-authentication
**Status**: Open
**Priority**: High
**Asked By**: PRD Generator Agent
**Date**: 2025-09-26

### Question
[Detailed question text]

### Context
- Related to: 001-R-004 (Password requirements)
- Needed for: 001-T-023 (Password validation implementation)
- Blocks: 001-P-005 (Security plan finalization)

### Answer
[Answer when resolved]

### Resolution Date
[Date when answered]

### Follow-up Items
- Created: 001-D-008 (Decision based on answer)
```

### Decision Template
```markdown
## Decision: [DECISION_ID] - [Decision Title]

**ID**: 001-D-003
**Feature**: 001-user-authentication
**Status**: Approved
**Made By**: Task Planning Agent
**Date**: 2025-09-26
**Approved By**: [Stakeholder]

### Context
[Why this decision was needed]

### Options Considered
1. **Option A**: [Description]
   - Pros: [List]
   - Cons: [List]
2. **Option B**: [Description]
   - Pros: [List]
   - Cons: [List]

### Decision
[Chosen option and rationale]

### Impact
- Affects: 001-T-015, 001-T-016
- Resolves: 001-Q-004
- Creates: 001-T-032 (Implementation task)

### Constitution Compliance
- Aligns with: Article III (Simplicity First)
- Justification: [If adds complexity]
```

---

## Tracking Files

### Master Tracking Document
Location: `02-planning/features/[###-feature-name]/tracking.md`

```markdown
# Tracking: Feature 001 - User Authentication

## Quick Reference
- Feature: 001-user-authentication
- Total Tasks: 45
- Total Questions: 12
- Total Decisions: 8
- Status: In Progress

## Active Items

### Open Questions (3)
- 001-Q-009: Session timeout configuration? [HIGH]
- 001-Q-011: Multi-factor authentication requirements? [MEDIUM]
- 001-Q-012: Password reset email template? [LOW]

### In Progress Tasks (5)
- 001-T-023: Implement password validation [Alice]
- 001-T-024: Create OAuth callback handler [Bob]
- 001-T-026: Write authentication middleware [Charlie]

### Blocked Items (2)
- 001-T-030: Integration tests [Blocked by 001-I-001]
- 001-P-008: Deployment plan [Blocked by 001-Q-009]

## Statistics
- Tasks: 45 total (23 completed, 5 in progress, 15 pending, 2 blocked)
- Questions: 12 total (9 resolved, 3 open)
- Decisions: 8 total (8 approved)
- Issues: 3 total (1 resolved, 2 active)

## Timeline
- Started: 2025-09-15
- Target: 2025-10-15
- Current Phase: Implementation
```

---

## CLI Integration

### Commands

```bash
# Create tracked item
specmap track create --type=task --feature=001 --title="Implement login"
# Output: Created 001-T-046

# List items
specmap track list --feature=001 --type=question --status=open

# Update status
specmap track update 001-T-046 --status=in-progress

# Link items
specmap track link 001-T-046 --implements=001-R-005 --blocks=001-T-047

# Generate report
specmap track report --feature=001
```

---

## Best Practices

### 1. Consistent Numbering
- Always use 3 digits for feature IDs: `001`, not `1`
- Always use 3 digits for item numbers: `001-T-005`, not `001-T-5`

### 2. Meaningful Titles
```markdown
✓ Good: 001-T-023 - Implement password validation with bcrypt
✗ Bad:  001-T-023 - Do password stuff
```

### 3. Cross-Referencing
Always link related items:
```markdown
## Task: 001-T-023 - Implement password validation

### Related Items
- Implements: 001-R-004 (Password complexity requirement)
- Depends on: 001-D-002 (Bcrypt hashing decision)
- Blocks: 001-T-031 (Login endpoint)
- Related to: 001-Q-002 (Password requirements question)
```

### 4. Status Updates
Keep status current:
```markdown
## 2025-09-26 Update
- 001-T-023: Open → In Progress
- 001-Q-009: Open → Resolved
- 001-I-002: Active → Resolved
```

### 5. Archive Completed Items
Move completed items to archive:
```markdown
## Completed Items (Archive)
- 001-T-001: Create User model [Completed 2025-09-20]
- 001-T-002: Implement password hashing [Completed 2025-09-22]
```

---

## Integration with RULEMAP Agents

### PRD Generator Agent
**Creates**:
- `001-R-###`: Requirements
- `001-Q-###`: Clarification questions
- `001-A-###`: Acceptance criteria

**References**:
- Links requirements to user stories
- Tags questions with priority
- Creates requirement IDs automatically

### Task Planning Agent
**Creates**:
- `001-P-###`: Planning documents
- `001-D-###`: Architecture decisions
- `001-T-###`: Implementation tasks
- `001-M-###`: Milestones

**References**:
- Links tasks to requirements
- Identifies dependencies
- Creates task hierarchy

### Development Guide Agent
**Creates**:
- `001-I-###`: Implementation issues
- Updates task status
- Adds implementation notes

**References**:
- Updates task progress
- Documents blockers
- Creates follow-up tasks

### QA Monitor Agent
**Creates**:
- `001-V-###`: Validation items
- Quality assessment reports

**References**:
- Links validations to acceptance criteria
- Tracks quality metrics
- Documents issues found

---

## Example: Complete Feature Tracking

```markdown
# Feature 001: User Authentication System

## Feature Overview
**ID**: 001-F
**Status**: In Progress
**RULEMAP Score**: 8.5/10

## Requirements (R)
- 001-R-001: Email/password authentication [IMPLEMENTED]
- 001-R-002: OAuth provider support [IN PROGRESS]
- 001-R-003: Session management [PLANNED]
- 001-R-004: Password complexity rules [IMPLEMENTED]

## Questions (Q)
- 001-Q-001: OAuth providers? → RESOLVED: Google, GitHub
- 001-Q-002: Password complexity? → RESOLVED: 8+ chars, mixed case
- 001-Q-003: Session timeout? → OPEN
- 001-Q-004: MFA support? → OPEN

## Decisions (D)
- 001-D-001: Use JWT tokens [APPROVED]
- 001-D-002: bcrypt for hashing [APPROVED]
- 001-D-003: Redis for sessions [APPROVED]

## Tasks (T)
### Specification (10 tasks)
- 001-T-001 through 001-T-010: All completed

### Planning (8 tasks)
- 001-T-011 through 001-T-018: All completed

### Implementation (30 tasks)
- 001-T-019 through 001-T-038: 15 completed, 5 in progress, 10 pending
- 001-T-039: BLOCKED by 001-I-002

### Testing (5 tasks)
- 001-T-044 through 001-T-048: All pending

## Issues (I)
- 001-I-001: OAuth callback URL → RESOLVED
- 001-I-002: Redis connection timeout → ACTIVE
- 001-I-003: Password validation bug → RESOLVED

## Milestones (M)
- 001-M-001: Spec complete [ACHIEVED 2025-09-18]
- 001-M-002: Planning complete [ACHIEVED 2025-09-22]
- 001-M-003: MVP complete [TARGET 2025-10-05]
- 001-M-004: Full feature complete [TARGET 2025-10-15]

## Validation (V)
- 001-V-001: Security audit [PENDING]
- 001-V-002: Performance test [PENDING]
- 001-V-003: RULEMAP scoring [IN PROGRESS]

## Current Status
- **Phase**: Implementation
- **Progress**: 60% complete
- **Blockers**: 1 (001-I-002)
- **Open Questions**: 2
- **Next Milestone**: 001-M-003 (5 days)
```

---

## Quick Reference Card

### Common Patterns

```
Feature:        001-F
Requirement:    001-R-042
Task:           001-T-156
Question:       001-Q-017
Decision:       001-D-009
Issue:          001-I-004
Acceptance:     001-A-023
Milestone:      001-M-003
Validation:     001-V-012
```

### Status Suffixes

```
-O   Open
-IP  In Progress
-B   Blocked
-R   Resolved
-C   Closed
```

### Complete Example

```
001-T-042-IP = Feature 001, Task 42, In Progress
002-Q-008-R  = Feature 002, Question 8, Resolved
003-I-001-B  = Feature 003, Issue 1, Blocked
```

---

**SpecMap Tracking ID System** - Comprehensive, hierarchical item identification for clear project communication