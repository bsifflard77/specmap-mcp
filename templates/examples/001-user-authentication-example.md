# Example: Complete Workflow for Feature 001 - User Authentication

**Purpose**: Demonstrate how Spec → Plan → Tasks templates work together
**Feature**: User authentication with email/password and OAuth

---

## Template Flow

```
1. SPECIFY (spec-template-enhanced.md)
   ↓
   Creates: 001-user-authentication/spec.md
   Defines: Requirements (001-R-###), Questions (001-Q-###)

2. PLAN (plan-template-enhanced.md)
   ↓
   Creates: 001-user-authentication/plan.md
   Defines: Tasks (001-T-###), Decisions (001-D-###)

3. TASKS (tasks-template-enhanced.md)
   ↓
   Creates: 001-user-authentication/tasks.md
   Details: Full task breakdown with dependencies
```

---

## 1. Specification Phase

**File**: `01-specifications/features/001-user-authentication/spec.md`

### Key Requirements Defined

```markdown
## Requirements

### 001-R-001: Email/Password Authentication
System MUST support user authentication via email and password

### 001-R-002: OAuth Provider Support
System MUST support OAuth authentication with Google and GitHub

### 001-R-003: Password Complexity
System MUST enforce password complexity:
- Minimum 8 characters
- At least one uppercase letter
- At least one number

### 001-R-004: Session Management
System MUST maintain user sessions with 24-hour expiration

### 001-R-005: Password Reset
Users MUST be able to reset forgotten passwords via email
```

### Questions Tracked

```markdown
## Questions

### 001-Q-001: OAuth Providers
**Q**: Which OAuth providers should we support?
**A**: Google and GitHub (resolved 2025-09-20)
**Creates**: 001-R-002

### 001-Q-002: Password Complexity
**Q**: What password complexity requirements?
**A**: 8+ chars, uppercase, number (resolved 2025-09-20)
**Creates**: 001-R-003

### 001-Q-003: Session Storage
**Q**: How should we store sessions?
**A**: Redis with JWT tokens (resolved 2025-09-21)
**Creates**: 001-D-001
```

### Acceptance Criteria

```markdown
## Acceptance Criteria

### 001-A-001: User can register with email/password
**Given** I am on the registration page
**When** I enter valid email and password
**Then** Account is created and I am logged in

### 001-A-002: User can login with email/password
**Given** I have an existing account
**When** I enter correct credentials
**Then** I am authenticated and redirected to dashboard

### 001-A-003: User can login with Google OAuth
**Given** I am on the login page
**When** I click "Sign in with Google"
**Then** I am redirected to Google auth and back to app when authenticated
```

**Specification Status**: ✅ Approved (RULEMAP Score: 8.5/10)

---

## 2. Planning Phase

**File**: `02-planning/features/001-user-authentication/plan.md`

### Technical Decisions Made

```markdown
## Decisions

### 001-D-001: Use JWT for Session Tokens
**Status**: Approved
**Date**: 2025-09-21
**Rationale**:
- Industry standard
- Stateless (horizontally scalable)
- Wide library support
**Affects**: 001-T-050, 001-T-051, 001-T-070
**Resolves**: 001-Q-003

### 001-D-002: Use bcrypt for Password Hashing
**Status**: Approved
**Date**: 2025-09-21
**Rationale**:
- Strong security
- Built-in salting
- Configurable work factor
**Affects**: 001-T-052, 001-T-060
**Implements**: 001-R-003

### 001-D-003: Use Passport.js for OAuth
**Status**: Approved
**Date**: 2025-09-22
**Rationale**:
- Well-established library
- Supports multiple providers
- Easy integration
**Affects**: 001-T-080, 001-T-081
**Implements**: 001-R-002
```

### Task Outline (High-Level)

```markdown
## Phase 0: Research & Foundation (5 tasks)
- 001-T-001 to 001-T-005: Project setup, dependencies

## Phase 1: Design & Contracts (15 tasks)
- 001-T-010 to 001-T-025: Data models, API contracts, tests (TDD Red)

## Phase 2: Core Implementation (25 tasks)
- 001-T-030 to 001-T-055: Models, services, APIs (TDD Green)

## Phase 3: Integration (8 tasks)
- 001-T-060 to 001-T-068: OAuth, database, error handling

## Phase 4: Testing & QA (6 tasks)
- 001-T-070 to 001-T-076: Additional tests, security audit

## Phase 5: Documentation (4 tasks)
- 001-T-080 to 001-T-084: Docs and deployment prep
```

**Planning Status**: ✅ Approved

---

## 3. Tasks Phase

**File**: `02-planning/features/001-user-authentication/tasks.md`

### Detailed Task Breakdown

#### Phase 0: Setup (5 tasks)

```markdown
### 001-T-001: Initialize Node.js project
- **Type**: Setup
- **Command**: `npm init -y`
- **File**: package.json
- **Estimated**: 0.5 hours
- **Status**: ✅ Complete

### 001-T-002: Install dependencies
- **Type**: Setup
- **Dependencies**: express, bcrypt, jsonwebtoken, passport, mongoose
- **Command**: `npm install express bcrypt jsonwebtoken passport mongoose`
- **Depends on**: 001-T-001
- **Estimated**: 1 hour
- **Status**: ✅ Complete

### 001-T-003: Configure ESLint and Prettier
- **Type**: Setup
- **Files**: .eslintrc.json, .prettierrc
- **Parallel**: [P]
- **Estimated**: 1 hour
- **Status**: ✅ Complete

### 001-T-004: Setup Jest testing framework
- **Type**: Setup
- **Files**: jest.config.js
- **Parallel**: [P]
- **Command**: `npm install --save-dev jest supertest`
- **Estimated**: 1 hour
- **Status**: ✅ Complete

### 001-T-005: Create project structure
- **Type**: Setup
- **Directories**: src/models, src/services, src/api, tests/
- **Estimated**: 0.5 hours
- **Status**: ✅ Complete
```

#### Phase 1: TDD Red Phase (15 tasks)

```markdown
### 001-T-010: [P] Contract test POST /api/auth/register
- **Type**: Contract Test
- **File**: tests/contract/test_auth_register.test.js
- **Validates**: 001-A-001
- **Implements**: 001-R-001
- **Must Fail**: Yes (TDD Red phase)
- **Parallel**: [P]
- **Estimated**: 2 hours
- **Status**: ✅ Complete (Failing as expected)

### 001-T-011: [P] Contract test POST /api/auth/login
- **Type**: Contract Test
- **File**: tests/contract/test_auth_login.test.js
- **Validates**: 001-A-002
- **Must Fail**: Yes
- **Parallel**: [P]
- **Estimated**: 2 hours
- **Status**: ✅ Complete (Failing as expected)

### 001-T-012: [P] Contract test GET /api/auth/oauth/google
- **Type**: Contract Test
- **File**: tests/contract/test_auth_oauth.test.js
- **Validates**: 001-A-003
- **Must Fail**: Yes
- **Parallel**: [P]
- **Estimated**: 2 hours
- **Status**: ✅ Complete (Failing as expected)

### 001-T-013: [P] Integration test for full registration flow
- **Type**: Integration Test
- **File**: tests/integration/test_registration_flow.test.js
- **Tests**: Complete user registration and login
- **Must Fail**: Yes
- **Parallel**: [P]
- **Estimated**: 3 hours
- **Status**: ✅ Complete (Failing as expected)

### 001-T-014: [P] Tests for User model
- **Type**: Model Test
- **File**: tests/models/test_user.test.js
- **Tests**: User creation, validation, password hashing
- **Must Fail**: Yes
- **Parallel**: [P]
- **Estimated**: 2 hours
- **Status**: ✅ Complete (Failing as expected)

### 001-T-015: [P] Tests for Session model
- **Type**: Model Test
- **File**: tests/models/test_session.test.js
- **Must Fail**: Yes
- **Parallel**: [P]
- **Estimated**: 1.5 hours
- **Status**: 🔄 In Progress
```

#### Phase 2: TDD Green Phase (25 tasks)

```markdown
### 001-T-030: [P] Implement User model
- **Type**: Model Implementation
- **File**: src/models/User.js
- **Implements**: 001-R-001
- **Makes Pass**: 001-T-014
- **Depends on**: 001-T-014 (test must exist first)
- **Parallel**: [P]
- **Estimated**: 3 hours
- **Status**: 🔄 In Progress
- **Implementation**:
  - email field (unique, validated)
  - passwordHash field
  - timestamps
  - validation methods

### 001-T-031: [P] Implement Session model
- **Type**: Model Implementation
- **File**: src/models/Session.js
- **Implements**: 001-R-004
- **Makes Pass**: 001-T-015
- **Parallel**: [P]
- **Estimated**: 2 hours
- **Status**: 📋 Pending
- **Implementation**:
  - userId reference
  - token field
  - expiresAt field
  - isValid method

### 001-T-032: Implement password hashing service
- **Type**: Service Implementation
- **File**: src/services/passwordService.js
- **Implements**: 001-R-003
- **Based on**: 001-D-002 (bcrypt decision)
- **Depends on**: 001-T-030
- **Estimated**: 2 hours
- **Status**: 📋 Pending
- **Functions**:
  - hashPassword(password)
  - comparePassword(password, hash)
  - validatePasswordComplexity(password)

### 001-T-033: Implement JWT token service
- **Type**: Service Implementation
- **File**: src/services/tokenService.js
- **Implements**: 001-R-004
- **Based on**: 001-D-001 (JWT decision)
- **Depends on**: 001-T-031
- **Estimated**: 2.5 hours
- **Status**: 📋 Pending
- **Functions**:
  - generateToken(userId)
  - verifyToken(token)
  - refreshToken(oldToken)

### 001-T-034: Implement authentication service
- **Type**: Service Implementation
- **File**: src/services/authService.js
- **Makes Pass**: 001-T-013 (integration test)
- **Depends on**: 001-T-030, 001-T-032, 001-T-033
- **Estimated**: 4 hours
- **Status**: 📋 Pending
- **Functions**:
  - register(email, password)
  - login(email, password)
  - logout(token)
  - validateSession(token)

### 001-T-040: Implement POST /api/auth/register
- **Type**: API Endpoint
- **File**: src/api/authEndpoints.js
- **Implements**: 001-R-001
- **Makes Pass**: 001-T-010 (contract test)
- **Depends on**: 001-T-034
- **Estimated**: 3 hours
- **Status**: 📋 Pending
- **Endpoint**:
  - Request: { email, password }
  - Response: { token, user }
  - Errors: 400 (validation), 409 (email exists)

### 001-T-041: Implement POST /api/auth/login
- **Type**: API Endpoint
- **File**: src/api/authEndpoints.js (same file)
- **Makes Pass**: 001-T-011
- **Depends on**: 001-T-040 (same file, sequential)
- **Estimated**: 2.5 hours
- **Status**: 📋 Pending
```

#### Phase 3: Integration (8 tasks)

```markdown
### 001-T-060: Integrate Passport.js for OAuth
- **Type**: External Integration
- **File**: src/services/oauthService.js
- **Implements**: 001-R-002
- **Based on**: 001-D-003 (Passport decision)
- **Estimated**: 5 hours
- **Status**: 📋 Pending
- **Providers**:
  - Google OAuth strategy
  - GitHub OAuth strategy
  - Callback handling

### 001-T-061: Implement GET /api/auth/oauth/google
- **Type**: API Endpoint
- **File**: src/api/authEndpoints.js
- **Makes Pass**: 001-T-012
- **Depends on**: 001-T-060
- **Estimated**: 3 hours
- **Status**: 📋 Pending

### 001-T-062: Connect to MongoDB
- **Type**: Database Integration
- **File**: src/database/connection.js
- **Depends on**: 001-T-030, 001-T-031
- **Estimated**: 2 hours
- **Status**: 📋 Pending

### 001-T-063: Implement error handling middleware
- **Type**: Middleware
- **File**: src/middleware/errorHandler.js
- **Estimated**: 3 hours
- **Status**: 📋 Pending
```

#### Phase 4: QA (6 tasks)

```markdown
### 001-T-070: Security audit
- **Type**: Security Test
- **Validation ID**: 001-V-001
- **Tool**: OWASP ZAP
- **Estimated**: 4 hours
- **Status**: 📋 Pending
- **Checks**:
  - SQL injection
  - XSS vulnerabilities
  - CSRF protection
  - Session fixation

### 001-T-071: Load testing
- **Type**: Performance Test
- **Validation ID**: 001-V-002
- **Tool**: Artillery
- **Estimated**: 3 hours
- **Status**: 📋 Pending
- **Target**: 1000 req/s, <200ms p95
```

#### Phase 5: Documentation (4 tasks)

```markdown
### 001-T-080: [P] Write user documentation
- **Type**: Documentation
- **File**: 06-documentation/user-guides/authentication.md
- **Parallel**: [P]
- **Estimated**: 3 hours
- **Status**: 📋 Pending

### 001-T-081: [P] Write API documentation
- **Type**: Documentation
- **File**: 06-documentation/api-specifications/auth-api.yaml
- **Parallel**: [P]
- **Estimated**: 2 hours
- **Status**: 📋 Pending
```

### Task Summary

```markdown
**Total Tasks**: 63
**Completed**: 10 (16%)
**In Progress**: 2 (3%)
**Pending**: 51 (81%)
**Blocked**: 0

**Estimated Duration**: 4 weeks
**Current Week**: Week 1 (Phase 1)
**On Track**: Yes
```

---

## Tracking Integration Example

**File**: `02-planning/features/001-user-authentication/tracking.md`

```markdown
# Feature Tracking: 001 - User Authentication

## Quick Status

| Metric | Value |
|--------|-------|
| **Progress** | 16% |
| **Current Phase** | Phase 1 (TDD Red) |
| **Next Milestone** | 001-M-002 on 2025-10-05 |
| **Blockers** | 0 |
| **Open Questions** | 0 |

## This Week's Focus

**Week 1 (Sep 23-27)**
- ✅ Complete project setup (001-T-001 to 001-T-005)
- 🔄 Write all contract tests (001-T-010 to 001-T-012)
- 🔄 Write integration tests (001-T-013)
- 📋 Write model tests (001-T-014, 001-T-015)

**Completed**:
- ✅ 001-T-001: Project initialization
- ✅ 001-T-002: Dependencies installed
- ✅ 001-T-003: Linting configured
- ✅ 001-T-004: Jest setup
- ✅ 001-T-005: Project structure
- ✅ 001-T-010: Register contract test (failing ✓)
- ✅ 001-T-011: Login contract test (failing ✓)
- ✅ 001-T-012: OAuth contract test (failing ✓)
- ✅ 001-T-013: Integration test (failing ✓)
- ✅ 001-T-014: User model test (failing ✓)

**In Progress**:
- 🔄 001-T-015: Session model test
- 🔄 001-T-030: User model implementation

**Next Week (Sep 30 - Oct 4)**:
- Complete TDD Green phase (001-T-030 to 001-T-041)
- Begin integration work (001-T-060)
```

---

## Communication Examples

### Daily Standup

```markdown
**Sep 26 Standup**

**Yesterday**:
- ✅ Completed 001-T-010, 001-T-011, 001-T-012 (all contract tests failing as expected)
- ✅ Completed 001-T-013 (integration test failing as expected)

**Today**:
- 🔄 Working on 001-T-014 (User model tests)
- 🔄 Will start 001-T-015 (Session model tests)

**Blockers**: None

**Notes**: TDD Red phase on track, all tests failing as expected (this is correct!)
```

### Pull Request

```markdown
## PR: Implement User Authentication Core

### Implements Requirements
- 001-R-001: Email/password authentication
- 001-R-003: Password complexity enforcement
- 001-R-004: Session management

### Tasks Completed
- ✅ 001-T-030: User model
- ✅ 001-T-031: Session model
- ✅ 001-T-032: Password hashing service
- ✅ 001-T-033: JWT token service
- ✅ 001-T-034: Authentication service

### Tests Passing
- ✅ 001-T-014: User model tests (now passing)
- ✅ 001-T-015: Session model tests (now passing)
- ✅ 001-T-013: Integration test (now passing)

### Based on Decisions
- 001-D-001: JWT for sessions
- 001-D-002: bcrypt for password hashing

### Next Steps
- Ready for 001-T-040 (Register endpoint)
- Ready for 001-T-041 (Login endpoint)
```

---

## Benefits Demonstrated

### 1. Clear Traceability
```
Requirement → Decision → Task → Test → Implementation → Validation
001-R-001 → 001-D-002 → 001-T-032 → 001-T-014 → 001-T-030 → 001-A-001
```

### 2. Unambiguous Communication
```
✅ "Completed 001-T-030"
   Everyone knows: User model implementation is done

❌ "Finished the user thing"
   Unclear: Which user-related task?
```

### 3. Progress Visibility
```
Phase 1: 10/15 tasks complete (67%)
Phase 2: 2/25 in progress (8%)
Overall: 12/63 complete (19%)
```

### 4. Dependency Management
```
001-T-040 depends on:
├── 001-T-034 (auth service)
│   ├── 001-T-030 (user model)
│   ├── 001-T-032 (password service)
│   └── 001-T-033 (token service)
└── 001-T-010 (contract test)
```

### 5. Agent Coordination
```
PRD Generator:    Created 001-R-001 to 001-R-005
Task Planner:     Created 001-T-001 to 001-T-084
Dev Guide:        Tracking 001-T-030 (in progress)
QA Monitor:       Will validate 001-V-001, 001-V-002
```

---

## Summary

This example demonstrates:
- ✅ Complete workflow from spec to tasks
- ✅ Tracking ID integration throughout
- ✅ TDD workflow (Red → Green phases)
- ✅ Clear dependencies and parallel execution
- ✅ Constitution compliance
- ✅ Agent coordination
- ✅ Practical communication patterns

**All three templates work together seamlessly to provide a comprehensive, trackable development workflow.**