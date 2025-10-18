"""
SpecMap Plan Command Implementation
Generate comprehensive implementation plans from approved specifications
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

from .structure import ProjectStructure, TemplateManager
from .config import WorkflowState
from .clarify import ClarificationProcessor


class PlanGenerator:
    """Handles generation of implementation plans from specifications"""

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.structure = ProjectStructure(project_path)

        # Template manager for plan template
        templates_dir = Path(__file__).parent.parent.parent / "templates" / "planning"
        self.template_manager = TemplateManager(templates_dir)

        # Workflow state and clarification processor
        self.workflow = WorkflowState(project_path)
        self.workflow.load()
        self.clarify_processor = ClarificationProcessor(project_path)

    def get_available_features(self) -> List[str]:
        """Get list of features with approved specifications"""
        features_dir = self.project_path / "01-specifications" / "features"
        if not features_dir.exists():
            return []

        approved_features = []
        for item in features_dir.iterdir():
            if item.is_dir() and re.match(r'^\d{3}-', item.name):
                spec_file = item / "spec.md"
                if spec_file.exists():
                    # Check RULEMAP score and approval status
                    score_result = self.clarify_processor.calculate_rulemap_score(item.name)
                    if score_result.get('meets_threshold', False):
                        approved_features.append(item.name)

        return sorted(approved_features)

    def analyze_specification(self, feature_id: str) -> Dict:
        """Analyze specification to extract planning information"""

        feature_path = self.project_path / "01-specifications" / "features" / feature_id
        spec_file = feature_path / "spec.md"

        if not spec_file.exists():
            raise ValueError(f"Specification not found for feature {feature_id}")

        content = spec_file.read_text()

        # Extract key information
        analysis = {
            'feature_id': feature_id,
            'functional_requirements': self._extract_functional_requirements(content),
            'acceptance_criteria': self._extract_acceptance_criteria(content),
            'technical_constraints': self._extract_technical_constraints(content),
            'user_stories': self._extract_user_stories(content),
            'performance_requirements': self._extract_performance_requirements(content),
            'dependencies': self._extract_dependencies(content),
            'business_context': self._extract_business_context(content),
            'complexity_indicators': self._analyze_complexity(content)
        }

        # Get RULEMAP score
        score_result = self.clarify_processor.calculate_rulemap_score(feature_id)
        analysis['rulemap_score'] = score_result

        return analysis

    def _extract_functional_requirements(self, content: str) -> List[Dict]:
        """Extract functional requirements from specification"""
        requirements = []
        lines = content.split('\n')

        in_requirements_section = False
        for line in lines:
            # Check if we're in the functional requirements section
            if 'functional requirements' in line.lower() and '#' in line:
                in_requirements_section = True
                continue
            elif in_requirements_section and line.strip().startswith('#') and 'functional requirements' not in line.lower():
                # Reached next section
                in_requirements_section = False

            if in_requirements_section and '**FR-' in line:
                # Extract requirement
                match = re.search(r'\*\*FR-(\d{3})\*\*:\s*(.+)', line)
                if match:
                    req_id = f"FR-{match.group(1)}"
                    req_text = match.group(2).strip()
                    requirements.append({
                        'id': req_id,
                        'text': req_text,
                        'type': 'functional'
                    })

        return requirements

    def _extract_acceptance_criteria(self, content: str) -> List[Dict]:
        """Extract acceptance criteria from specification"""
        criteria = []

        # Look for YAML-style acceptance tests
        yaml_pattern = r'```yaml\s*ACCEPTANCE_TEST_(\d+):(.*?)```'
        matches = re.findall(yaml_pattern, content, re.DOTALL)

        for match in matches:
            test_num = match[0]
            test_content = match[1].strip()

            # Parse the YAML-like content
            scenario_match = re.search(r'scenario:\s*"([^"]+)"', test_content)
            given_match = re.search(r'given:\s*"([^"]+)"', test_content)
            when_match = re.search(r'when:\s*"([^"]+)"', test_content)
            then_match = re.search(r'then:\s*"([^"]+)"', test_content)

            if scenario_match:
                criteria.append({
                    'id': f"A-{int(test_num):03d}",
                    'scenario': scenario_match.group(1),
                    'given': given_match.group(1) if given_match else '',
                    'when': when_match.group(1) if when_match else '',
                    'then': then_match.group(1) if then_match else '',
                    'type': 'acceptance_test'
                })

        return criteria

    def _extract_technical_constraints(self, content: str) -> Dict:
        """Extract technical constraints and requirements"""
        constraints = {
            'platform': '',
            'performance': '',
            'security': '',
            'integration': '',
            'scalability': ''
        }

        # Look for technical constraints section
        lines = content.split('\n')
        in_constraints = False

        for line in lines:
            if 'technical constraints' in line.lower() and '#' in line:
                in_constraints = True
                continue
            elif in_constraints and line.strip().startswith('#') and 'technical constraints' not in line.lower():
                in_constraints = False

            if in_constraints:
                if '**platform**:' in line.lower():
                    constraints['platform'] = line.split(':', 1)[1].strip()
                elif '**performance**:' in line.lower():
                    constraints['performance'] = line.split(':', 1)[1].strip()
                elif '**security**:' in line.lower():
                    constraints['security'] = line.split(':', 1)[1].strip()
                elif '**integration**:' in line.lower():
                    constraints['integration'] = line.split(':', 1)[1].strip()

        return constraints

    def _extract_user_stories(self, content: str) -> List[Dict]:
        """Extract user stories from specification"""
        stories = []

        # Look for user story format
        story_pattern = r'```\s*As\s+a\s+([^,]+),\s*I\s+want\s+to\s+([^,]+),\s*So\s+that\s+([^`]+)```'
        matches = re.findall(story_pattern, content, re.DOTALL)

        for i, match in enumerate(matches, 1):
            stories.append({
                'id': f"US-{i:03d}",
                'role': match[0].strip(),
                'action': match[1].strip(),
                'benefit': match[2].strip()
            })

        return stories

    def _extract_performance_requirements(self, content: str) -> Dict:
        """Extract performance requirements"""
        performance = {
            'response_time': '',
            'throughput': '',
            'concurrent_users': '',
            'reliability': ''
        }

        # Look for performance section
        lines = content.split('\n')
        in_performance = False

        for line in lines:
            if 'technical performance' in line.lower() or 'performance' in line.lower() and '#' in line:
                in_performance = True
                continue
            elif in_performance and line.strip().startswith('#'):
                in_performance = False

            if in_performance:
                if 'response time' in line.lower() or 'latency' in line.lower():
                    performance['response_time'] = self._extract_performance_value(line)
                elif 'throughput' in line.lower() or 'req/s' in line.lower():
                    performance['throughput'] = self._extract_performance_value(line)
                elif 'concurrent' in line.lower() or 'users' in line.lower():
                    performance['concurrent_users'] = self._extract_performance_value(line)
                elif 'uptime' in line.lower() or 'reliability' in line.lower():
                    performance['reliability'] = self._extract_performance_value(line)

        return performance

    def _extract_performance_value(self, line: str) -> str:
        """Extract performance value from line"""
        # Look for patterns like <200ms, 99.9%, 1000 req/s, etc.
        patterns = [
            r'<(\d+(?:\.\d+)?\s*(?:ms|s))',  # <200ms
            r'(\d+(?:\.\d+)?%)',             # 99.9%
            r'(\d+(?:\.\d+)?\s*(?:req/s|rps|requests/s))',  # 1000 req/s
            r'(\d+(?:\.\d+)?[kK]\s*(?:users|concurrent))'   # 10k users
        ]

        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                return match.group(1)

        return line.split(':', 1)[1].strip() if ':' in line else ''

    def _extract_dependencies(self, content: str) -> List[Dict]:
        """Extract dependencies from specification"""
        dependencies = []

        # Look for dependencies section
        lines = content.split('\n')
        in_dependencies = False

        for line in lines:
            if 'dependencies' in line.lower() and '#' in line:
                in_dependencies = True
                continue
            elif in_dependencies and line.strip().startswith('#'):
                in_dependencies = False

            if in_dependencies and (line.strip().startswith('-') or line.strip().startswith('*')):
                dep_text = line.strip().lstrip('-*').strip()
                if dep_text:
                    dependencies.append({
                        'type': 'external',
                        'description': dep_text
                    })

        return dependencies

    def _extract_business_context(self, content: str) -> Dict:
        """Extract business context information"""
        context = {
            'strategic_alignment': '',
            'user_impact': '',
            'timeline_pressure': '',
            'business_objectives': ''
        }

        # Look for various business context sections
        sections_to_find = {
            'strategic alignment': 'strategic_alignment',
            'business objectives': 'business_objectives',
            'user impact': 'user_impact',
            'timeline': 'timeline_pressure',
            'urgency': 'timeline_pressure'
        }

        lines = content.split('\n')
        current_section = None

        for line in lines:
            line_lower = line.lower()
            for section_name, context_key in sections_to_find.items():
                if section_name in line_lower and ':' in line:
                    context[context_key] = line.split(':', 1)[1].strip()
                    break

        return context

    def _analyze_complexity(self, content: str) -> Dict:
        """Analyze specification complexity indicators"""

        complexity = {
            'entities_count': len(re.findall(r'\*\*[A-Z][a-zA-Z\s]+\*\*:', content)),
            'requirements_count': len(re.findall(r'\*\*FR-\d{3}\*\*:', content)),
            'integrations_count': content.lower().count('integration') + content.lower().count('external'),
            'has_auth': 'auth' in content.lower() or 'login' in content.lower(),
            'has_database': 'database' in content.lower() or 'persist' in content.lower(),
            'has_api': 'api' in content.lower() or 'endpoint' in content.lower(),
            'complexity_score': 0
        }

        # Calculate basic complexity score
        score = 0
        score += complexity['entities_count'] * 0.5
        score += complexity['requirements_count'] * 0.3
        score += complexity['integrations_count'] * 1.0
        score += 2 if complexity['has_auth'] else 0
        score += 1 if complexity['has_database'] else 0
        score += 1 if complexity['has_api'] else 0

        complexity['complexity_score'] = round(score, 1)

        return complexity

    def generate_technical_decisions(self, feature_id: str, analysis: Dict) -> List[Dict]:
        """Generate technical decisions based on specification analysis"""

        feature_num = feature_id.split('-')[0]
        decisions = []
        decision_counter = 1

        # Architecture decision
        if analysis['complexity_indicators']['complexity_score'] > 5:
            decisions.append({
                'id': f"{feature_num}-D-{decision_counter:03d}",
                'title': 'Architecture Pattern Selection',
                'category': 'architecture',
                'decision': 'Layered architecture with MVC pattern',
                'rationale': 'Complexity score indicates need for clear separation of concerns',
                'alternatives': ['Microservices', 'Hexagonal architecture'],
                'status': 'proposed'
            })
            decision_counter += 1

        # Authentication decision
        if analysis['complexity_indicators']['has_auth']:
            decisions.append({
                'id': f"{feature_num}-D-{decision_counter:03d}",
                'title': 'Authentication Method',
                'category': 'security',
                'decision': 'JWT-based authentication with email/password',
                'rationale': 'Standard approach for user authentication features',
                'alternatives': ['OAuth2', 'Session-based auth', 'API keys'],
                'status': 'proposed'
            })
            decision_counter += 1

        # Database decision
        if analysis['complexity_indicators']['has_database']:
            decisions.append({
                'id': f"{feature_num}-D-{decision_counter:03d}",
                'title': 'Database Technology',
                'category': 'data',
                'decision': 'PostgreSQL with SQLAlchemy ORM',
                'rationale': 'Relational data model with ACID compliance needs',
                'alternatives': ['MongoDB', 'MySQL', 'SQLite'],
                'status': 'proposed'
            })
            decision_counter += 1

        # API framework decision
        if analysis['complexity_indicators']['has_api']:
            decisions.append({
                'id': f"{feature_num}-D-{decision_counter:03d}",
                'title': 'API Framework',
                'category': 'api',
                'decision': 'FastAPI with Pydantic validation',
                'rationale': 'Modern async framework with automatic OpenAPI generation',
                'alternatives': ['Flask', 'Django REST', 'Express.js'],
                'status': 'proposed'
            })
            decision_counter += 1

        # Testing strategy decision
        decisions.append({
            'id': f"{feature_num}-D-{decision_counter:03d}",
            'title': 'Testing Strategy',
            'category': 'testing',
            'decision': 'TDD with pytest, contract tests, and integration tests',
            'rationale': 'Ensures quality and maintainability as per constitution',
            'alternatives': ['BDD with behave', 'Simple unit tests only'],
            'status': 'approved'
        })

        return decisions

    def generate_milestones(self, feature_id: str, analysis: Dict) -> List[Dict]:
        """Generate project milestones"""

        feature_num = feature_id.split('-')[0]
        milestones = []

        base_date = datetime.now()

        # Calculate estimated durations based on complexity
        complexity = analysis['complexity_indicators']['complexity_score']
        req_count = analysis['complexity_indicators']['requirements_count']

        # Base estimates (in days)
        research_days = max(2, int(complexity * 0.5))
        design_days = max(3, int(req_count * 0.5))
        implementation_days = max(5, int(req_count * 1.5 + complexity * 0.5))
        integration_days = max(2, int(analysis['complexity_indicators']['integrations_count'] * 2))
        testing_days = max(3, int(req_count * 0.3 + complexity * 0.2))

        current_date = base_date

        milestones.append({
            'id': f"{feature_num}-M-001",
            'title': 'Research Complete',
            'date': (current_date + timedelta(days=research_days)).strftime('%Y-%m-%d'),
            'deliverables': ['Research document', 'Technical decisions', 'Architecture selected'],
            'success_criteria': ['All technical unknowns resolved', 'Technology stack decided'],
            'phase': 'research'
        })
        current_date += timedelta(days=research_days)

        milestones.append({
            'id': f"{feature_num}-M-002",
            'title': 'Design & Contracts Complete',
            'date': (current_date + timedelta(days=design_days)).strftime('%Y-%m-%d'),
            'deliverables': ['Data models defined', 'API contracts specified', 'All tests written and failing'],
            'success_criteria': ['TDD Red phase achieved', 'All contracts documented'],
            'phase': 'design'
        })
        current_date += timedelta(days=design_days)

        milestones.append({
            'id': f"{feature_num}-M-003",
            'title': 'Core Implementation Complete',
            'date': (current_date + timedelta(days=implementation_days)).strftime('%Y-%m-%d'),
            'deliverables': ['All core features implemented', 'All contract tests passing'],
            'success_criteria': ['TDD Green phase achieved', 'Core functionality working'],
            'phase': 'implementation'
        })
        current_date += timedelta(days=implementation_days)

        if integration_days > 0:
            milestones.append({
                'id': f"{feature_num}-M-004",
                'title': 'Integration Complete',
                'date': (current_date + timedelta(days=integration_days)).strftime('%Y-%m-%d'),
                'deliverables': ['External systems integrated', 'End-to-end functionality'],
                'success_criteria': ['All integrations working', 'System fully connected'],
                'phase': 'integration'
            })
            current_date += timedelta(days=integration_days)

        milestones.append({
            'id': f"{feature_num}-M-005",
            'title': 'Production Ready',
            'date': (current_date + timedelta(days=testing_days)).strftime('%Y-%m-%d'),
            'deliverables': ['All tests passing', 'Documentation complete', 'Deployment ready'],
            'success_criteria': ['RULEMAP score ≥8.0', 'All quality gates passed', 'Stakeholder approval'],
            'phase': 'testing'
        })

        return milestones

    def create_contracts_document(self, feature_path: Path, analysis: Dict) -> str:
        """Create contracts.md document"""

        feature_id = analysis['feature_id']
        feature_num = feature_id.split('-')[0]

        content = f"""# API Contracts: {feature_id}

**Feature**: {feature_id}
**Created**: {datetime.now().strftime('%Y-%m-%d')}
**Status**: Draft

---

## Contract Overview

This document defines all API contracts, data models, and integration points for the {feature_id} feature.

---

## Data Models

"""

        # Add data model definitions based on analysis
        if analysis['complexity_indicators']['has_database']:
            content += f"""
### Core Entities

#### {feature_num}-Entity-001: User
```yaml
attributes:
  - id: UUID (Primary Key)
  - email: String (Unique, Required)
  - password_hash: String (Required)
  - created_at: DateTime (Auto-generated)
  - updated_at: DateTime (Auto-updated)

relationships:
  - sessions: One-to-Many with UserSession

validation_rules:
  - email: Valid email format
  - password: Minimum 8 characters, complexity requirements
```

"""

        # Add API endpoints based on analysis
        if analysis['complexity_indicators']['has_api']:
            content += """
---

## API Endpoints

### Authentication Endpoints

#### POST /api/auth/login
```yaml
purpose: "User authentication"
implements: [FR-001, FR-002]
request_schema:
  type: object
  required: [email, password]
  properties:
    email:
      type: string
      format: email
    password:
      type: string
      minLength: 8

response_schema:
  success:
    type: object
    properties:
      token:
        type: string
        description: "JWT access token"
      user:
        $ref: "#/schemas/User"
  error:
    type: object
    properties:
      error:
        type: string
      details:
        type: string

error_codes:
  - 400: Invalid request format
  - 401: Invalid credentials
  - 429: Too many attempts
```

"""

        content += """
---

## Integration Contracts

### External Services

*Define contracts for external services and APIs*

---

## Contract Tests

All contracts must have corresponding tests:

"""

        # Add contract test definitions
        for i, req in enumerate(analysis['functional_requirements'][:3], 1):
            content += f"""
- **{feature_num}-CT-{i:03d}**: Contract test for {req['text'][:50]}...
  - **Validates**: {req['id']}
  - **Test File**: `tests/contract/test_{req['id'].lower()}.py`

"""

        content += f"""
---

**Contract Status**: Draft
**Next Review**: {(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}
**Approved By**: [Pending stakeholder review]
"""

        contracts_file = feature_path / "contracts.md"
        contracts_file.write_text(content, encoding='utf-8')
        return str(contracts_file)

    def create_data_models_document(self, feature_path: Path, analysis: Dict) -> str:
        """Create data-models.md document"""

        feature_id = analysis['feature_id']
        feature_num = feature_id.split('-')[0]

        content = f"""# Data Models: {feature_id}

**Feature**: {feature_id}
**Created**: {datetime.now().strftime('%Y-%m-%d')}
**Status**: Draft

---

## Model Overview

This document defines all data models, relationships, and database schema for the {feature_id} feature.

---

## Entity Relationship Diagram

```mermaid
erDiagram
    User {{
        UUID id PK
        string email UK
        string password_hash
        datetime created_at
        datetime updated_at
    }}

    UserSession {{
        UUID id PK
        UUID user_id FK
        string token_hash
        datetime expires_at
        datetime created_at
    }}

    User ||--o{{ UserSession : "has sessions"
```

---

## Model Definitions

"""

        # Add model definitions based on requirements
        entities_found = 0
        for req in analysis['functional_requirements']:
            if 'user' in req['text'].lower() and entities_found == 0:
                content += f"""
### {feature_num}-Model-001: User

**Purpose**: Represents system users with authentication capabilities

**Attributes**:
- `id`: UUID - Primary key, auto-generated
- `email`: String - Unique identifier for authentication
- `password_hash`: String - Hashed password for security
- `first_name`: String - User's first name (optional)
- `last_name`: String - User's last name (optional)
- `is_active`: Boolean - Account status flag
- `created_at`: DateTime - Account creation timestamp
- `updated_at`: DateTime - Last modification timestamp

**Relationships**:
- One-to-Many with UserSession (user can have multiple active sessions)
- One-to-Many with UserPreferences (user settings)

**Business Rules**:
- Email must be unique across all users
- Password must meet complexity requirements
- Soft deletion (is_active flag) preferred over hard deletion
- All timestamps in UTC

**Database Schema**:
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(is_active);
```

"""
                entities_found += 1

        content += """
---

## Model Validation

### Data Integrity Rules

1. **Referential Integrity**: All foreign keys must reference valid records
2. **Business Rules**: Enforce business logic at model level
3. **Data Types**: Strict type checking for all attributes
4. **Constraints**: Database constraints for critical business rules

### Validation Implementation

```python
# Example model validation
class User(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: Optional[str] = Field(max_length=100)
    last_name: Optional[str] = Field(max_length=100)

    @validator('password')
    def validate_password_complexity(cls, v):
        # Implement password complexity rules
        return v
```

---

## Migration Strategy

### Database Migrations

1. **{feature_num}-Migration-001**: Create initial user table
2. **{feature_num}-Migration-002**: Add user session table
3. **{feature_num}-Migration-003**: Create indexes for performance

### Data Migration

*Define any data migration requirements*

---

**Model Status**: Draft
**Database Review**: [Pending DBA approval]
**Implementation Priority**: High
"""

        data_models_file = feature_path / "data-models.md"
        data_models_file.write_text(content, encoding='utf-8')
        return str(data_models_file)

    def generate_implementation_plan(self, feature_id: str) -> Dict:
        """Generate complete implementation plan"""

        # Validate feature exists and is approved
        available_features = self.get_available_features()
        if feature_id not in available_features:
            # Get RULEMAP score to check status
            score_result = self.clarify_processor.calculate_rulemap_score(feature_id)
            if not score_result.get('meets_threshold', False):
                raise ValueError(f"Feature '{feature_id}' does not meet RULEMAP threshold (≥8.0). Run 'specmap clarify' first.")
            else:
                available_features.append(feature_id)  # Add if it meets threshold

        # Analyze specification
        analysis = self.analyze_specification(feature_id)

        # Generate plan components
        technical_decisions = self.generate_technical_decisions(feature_id, analysis)
        milestones = self.generate_milestones(feature_id, analysis)

        # Create feature planning folder
        feature_paths = self.structure.get_feature_path(feature_id)
        plan_path = feature_paths['plan']
        plan_path.mkdir(parents=True, exist_ok=True)

        # Generate supporting documents
        contracts_file = self.create_contracts_document(plan_path, analysis)
        data_models_file = self.create_data_models_document(plan_path, analysis)

        # Prepare template variables
        feature_name = feature_id.replace('-', ' ').title()
        feature_num = feature_id.split('-')[0]

        template_vars = {
            'FEATURE NAME': feature_name,
            '###': feature_num,
            'feature-name': feature_id,
            'YYYY-MM-DD': datetime.now().strftime('%Y-%m-%d'),
            'Session ID': f"PLAN-{datetime.now().strftime('%Y%m%d')}-{feature_num}",
            'X.X': str(analysis['rulemap_score']['score']),
            'Draft/Review/Approved/Active': 'Draft'
        }

        # Render plan template
        try:
            plan_content = self.template_manager.render_template(
                'plan-template-enhanced',
                template_vars
            )

            # Enhance template with analysis data
            plan_content = self._enhance_plan_with_analysis(plan_content, analysis, technical_decisions, milestones)

            plan_file = plan_path / "plan.md"
            plan_file.write_text(plan_content, encoding='utf-8')

        except FileNotFoundError:
            # Fallback plan generation
            plan_content = self._create_basic_plan(feature_id, feature_name, analysis, technical_decisions, milestones)
            plan_file = plan_path / "plan.md"
            plan_file.write_text(plan_content, encoding='utf-8')

        # Update workflow state
        feature_data = self.workflow.get_feature(feature_id) or {}
        feature_data['status'] = 'planning'
        feature_data['plan_created'] = datetime.now().isoformat()
        feature_data['decisions'] = technical_decisions
        feature_data['milestones'] = milestones
        self.workflow.add_feature(feature_id, feature_data)

        # Update project phase
        self.workflow.update_phase('planning')

        return {
            'feature_id': feature_id,
            'plan_file': str(plan_file),
            'contracts_file': contracts_file,
            'data_models_file': data_models_file,
            'technical_decisions': technical_decisions,
            'milestones': milestones,
            'analysis': analysis,
            'estimated_duration': len(milestones) * 7  # Rough estimate in days
        }

    def _enhance_plan_with_analysis(self, plan_content: str, analysis: Dict, decisions: List, milestones: List) -> str:
        """Enhance the plan template with analysis data"""

        # Add requirements count
        req_count = len(analysis['functional_requirements'])
        plan_content = plan_content.replace('[Total functional requirements]', str(req_count))

        # Add complexity information
        complexity = analysis['complexity_indicators']['complexity_score']
        plan_content = plan_content.replace('[Estimated count]', str(len(decisions) + req_count * 3))

        # Add technology stack based on decisions
        tech_stack = {}
        for decision in decisions:
            if decision['category'] == 'api':
                tech_stack['framework'] = decision['decision']
            elif decision['category'] == 'data':
                tech_stack['database'] = decision['decision']

        if tech_stack:
            tech_section = ""
            for key, value in tech_stack.items():
                tech_section += f"  {key}: \"{value}\"\n"
            plan_content = plan_content.replace('framework: "[Framework - e.g., FastAPI]"', f'framework: "{tech_stack.get("framework", "FastAPI")}"')
            plan_content = plan_content.replace('database: "[Database - e.g., PostgreSQL 15]"', f'database: "{tech_stack.get("database", "PostgreSQL")}"')

        return plan_content

    def _create_basic_plan(self, feature_id: str, feature_name: str, analysis: Dict, decisions: List, milestones: List) -> str:
        """Create a basic implementation plan if template is not available"""

        feature_num = feature_id.split('-')[0]

        return f"""# Implementation Plan: {feature_name}

**Feature ID**: {feature_id}
**Plan ID**: {feature_num}-P
**Date**: {datetime.now().strftime('%Y-%m-%d')}
**RULEMAP Score**: {analysis['rulemap_score']['score']}/10.0
**Status**: Draft

---

## Planning Overview

**Requirements**: {len(analysis['functional_requirements'])} functional requirements
**Acceptance Criteria**: {len(analysis['acceptance_criteria'])} test scenarios
**Complexity Score**: {analysis['complexity_indicators']['complexity_score']}
**Estimated Duration**: {len(milestones) * 7} days

---

## Technical Decisions

{self._format_decisions(decisions)}

---

## Implementation Phases

{self._format_milestones(milestones)}

---

## Requirements Mapping

{self._format_requirements(analysis['functional_requirements'])}

---

## Quality Gates

- [ ] All technical decisions approved
- [ ] Data models designed and reviewed
- [ ] API contracts defined
- [ ] All tests written (TDD Red phase)
- [ ] Implementation complete (TDD Green phase)
- [ ] RULEMAP score ≥ 8.0 maintained
- [ ] Stakeholder approval obtained

---

**Plan Status**: Draft
**Next Phase**: Task Generation (run: specmap tasks)
**Approved By**: [Pending stakeholder review]
"""

    def _format_decisions(self, decisions: List[Dict]) -> str:
        """Format technical decisions for display"""
        content = ""
        for decision in decisions:
            content += f"""
### {decision['id']}: {decision['title']}

**Category**: {decision['category'].title()}
**Decision**: {decision['decision']}
**Rationale**: {decision['rationale']}
**Status**: {decision['status'].title()}

"""
        return content

    def _format_milestones(self, milestones: List[Dict]) -> str:
        """Format milestones for display"""
        content = ""
        for milestone in milestones:
            content += f"""
### {milestone['id']}: {milestone['title']}

**Target Date**: {milestone['date']}
**Phase**: {milestone['phase'].title()}

**Deliverables**:
{chr(10).join([f"- {deliverable}" for deliverable in milestone['deliverables']])}

**Success Criteria**:
{chr(10).join([f"- {criteria}" for criteria in milestone['success_criteria']])}

"""
        return content

    def _format_requirements(self, requirements: List[Dict]) -> str:
        """Format requirements for display"""
        content = ""
        for req in requirements:
            content += f"- **{req['id']}**: {req['text']}\n"
        return content