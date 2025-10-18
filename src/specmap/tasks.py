"""
SpecMap Tasks Command Implementation
Generate detailed task breakdown from implementation plans
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

from .structure import ProjectStructure, TemplateManager
from .config import WorkflowState
from .plan import PlanGenerator


class TaskGenerator:
    """Handles generation of detailed task breakdown from implementation plans"""

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.structure = ProjectStructure(project_path)

        # Template manager for tasks template
        templates_dir = Path(__file__).parent.parent.parent / "templates" / "planning"
        self.template_manager = TemplateManager(templates_dir)

        # Workflow state and plan generator
        self.workflow = WorkflowState(project_path)
        self.workflow.load()
        self.plan_generator = PlanGenerator(project_path)

    def get_features_with_plans(self) -> List[str]:
        """Get list of features that have implementation plans"""
        features_dir = self.project_path / "02-planning" / "features"
        if not features_dir.exists():
            return []

        features_with_plans = []
        for item in features_dir.iterdir():
            if item.is_dir() and re.match(r'^\d{3}-', item.name):
                plan_file = item / "plan.md"
                if plan_file.exists():
                    features_with_plans.append(item.name)

        return sorted(features_with_plans)

    def analyze_implementation_plan(self, feature_id: str) -> Dict:
        """Analyze implementation plan to extract task generation information"""

        plan_path = self.project_path / "02-planning" / "features" / feature_id / "plan.md"

        if not plan_path.exists():
            raise ValueError(f"Implementation plan not found for feature {feature_id}")

        content = plan_path.read_text()

        # Extract key information from plan
        analysis = {
            'feature_id': feature_id,
            'technical_decisions': self._extract_decisions_from_plan(content),
            'milestones': self._extract_milestones_from_plan(content),
            'requirements_mapping': self._extract_requirements_from_plan(content),
            'technology_stack': self._extract_technology_stack(content),
            'complexity_indicators': self._analyze_plan_complexity(content),
            'performance_requirements': self._extract_performance_requirements_from_plan(content),
            'integration_points': self._extract_integration_points(content)
        }

        return analysis

    def _extract_decisions_from_plan(self, content: str) -> List[Dict]:
        """Extract technical decisions from implementation plan"""
        decisions = []

        # Look for decision sections in the plan
        decision_pattern = r'### (\d{3}-D-\d{3}): (.+?)\n\n\*\*Category\*\*: (.+?)\n\*\*Decision\*\*: (.+?)\n\*\*Rationale\*\*: (.+?)\n'
        matches = re.findall(decision_pattern, content, re.DOTALL)

        for match in matches:
            decisions.append({
                'id': match[0],
                'title': match[1].strip(),
                'category': match[2].strip(),
                'decision': match[3].strip(),
                'rationale': match[4].strip()
            })

        return decisions

    def _extract_milestones_from_plan(self, content: str) -> List[Dict]:
        """Extract milestones from implementation plan"""
        milestones = []

        # Look for milestone sections
        milestone_pattern = r'### (\d{3}-M-\d{3}): (.+?)\n\n\*\*Target Date\*\*: (.+?)\n\*\*Phase\*\*: (.+?)\n'
        matches = re.findall(milestone_pattern, content, re.DOTALL)

        for match in matches:
            milestones.append({
                'id': match[0],
                'title': match[1].strip(),
                'date': match[2].strip(),
                'phase': match[3].strip()
            })

        return milestones

    def _extract_requirements_from_plan(self, content: str) -> List[Dict]:
        """Extract requirements mapping from plan"""
        requirements = []

        # Look for requirement references
        req_pattern = r'(\d{3}-R-\d{3})'
        req_matches = re.findall(req_pattern, content)

        for req_id in set(req_matches):  # Remove duplicates
            requirements.append({
                'id': req_id,
                'description': f"Requirement {req_id}",  # Would be filled from spec
                'priority': 'high'  # Default, could be extracted from spec
            })

        return requirements

    def _extract_technology_stack(self, content: str) -> Dict:
        """Extract technology stack information from plan"""
        stack = {
            'language': '',
            'framework': '',
            'database': '',
            'testing': '',
            'deployment': ''
        }

        # Look for technology stack section
        if 'technology_stack:' in content.lower():
            lines = content.split('\n')
            in_stack_section = False

            for line in lines:
                if 'technology_stack:' in line.lower():
                    in_stack_section = True
                    continue
                elif in_stack_section and line.strip().startswith('language:'):
                    stack['language'] = line.split(':', 1)[1].strip().strip('"')
                elif in_stack_section and line.strip().startswith('framework:'):
                    stack['framework'] = line.split(':', 1)[1].strip().strip('"')
                elif in_stack_section and line.strip().startswith('database:'):
                    stack['database'] = line.split(':', 1)[1].strip().strip('"')
                elif in_stack_section and line.strip().startswith('testing:'):
                    stack['testing'] = line.split(':', 1)[1].strip().strip('"')
                elif in_stack_section and (line.strip().startswith('deployment:') or line.strip().startswith('platform:')):
                    stack['deployment'] = line.split(':', 1)[1].strip().strip('"')
                elif in_stack_section and line.strip() and not line.strip().startswith(' '):
                    # End of stack section
                    break

        return stack

    def _analyze_plan_complexity(self, content: str) -> Dict:
        """Analyze complexity indicators from the plan"""
        complexity = {
            'has_database': 'database' in content.lower() or 'model' in content.lower(),
            'has_api': 'api' in content.lower() or 'endpoint' in content.lower(),
            'has_auth': 'auth' in content.lower() or 'login' in content.lower(),
            'has_external_integrations': 'integration' in content.lower() or 'external' in content.lower(),
            'entity_count': len(re.findall(r'entity', content, re.IGNORECASE)),
            'endpoint_count': len(re.findall(r'endpoint|api', content, re.IGNORECASE)),
            'decision_count': len(re.findall(r'\d{3}-D-\d{3}', content)),
            'milestone_count': len(re.findall(r'\d{3}-M-\d{3}', content))
        }

        # Calculate complexity score
        score = 0
        score += 2 if complexity['has_database'] else 0
        score += 2 if complexity['has_api'] else 0
        score += 3 if complexity['has_auth'] else 0
        score += 2 if complexity['has_external_integrations'] else 0
        score += complexity['entity_count'] * 0.5
        score += complexity['endpoint_count'] * 0.3

        complexity['complexity_score'] = round(score, 1)

        return complexity

    def _extract_performance_requirements_from_plan(self, content: str) -> Dict:
        """Extract performance requirements from plan"""
        performance = {
            'response_time': '',
            'throughput': '',
            'concurrent_users': '',
            'availability': ''
        }

        # Look for performance section
        lines = content.split('\n')
        in_performance = False

        for line in lines:
            if 'performance' in line.lower() and ':' in line:
                in_performance = True
                continue
            elif in_performance and line.strip().startswith('#'):
                in_performance = False

            if in_performance:
                if 'response' in line.lower() or 'latency' in line.lower():
                    performance['response_time'] = self._extract_performance_value(line)
                elif 'throughput' in line.lower() or 'req/s' in line.lower():
                    performance['throughput'] = self._extract_performance_value(line)
                elif 'concurrent' in line.lower() or 'users' in line.lower():
                    performance['concurrent_users'] = self._extract_performance_value(line)
                elif 'uptime' in line.lower() or 'availability' in line.lower():
                    performance['availability'] = self._extract_performance_value(line)

        return performance

    def _extract_performance_value(self, line: str) -> str:
        """Extract performance value from line"""
        # Look for patterns like <200ms, 99.9%, 1000 req/s, etc.
        patterns = [
            r'<(\d+(?:\.\d+)?\s*(?:ms|s))',  # <200ms
            r'(\d+(?:\.\d+)?%)',             # 99.9%
            r'(\d+(?:\.\d+)?\s*(?:req/s|rps))',  # 1000 req/s
            r'(\d+[kK]\s*(?:users|concurrent))'   # 10k users
        ]

        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                return match.group(1)

        return ''

    def _extract_integration_points(self, content: str) -> List[Dict]:
        """Extract external integration points from plan"""
        integrations = []

        # Look for integration mentions
        integration_patterns = [
            r'integrate with (.+?)(?:\n|$)',
            r'external (.+?) integration',
            r'(\w+) service integration'
        ]

        for pattern in integration_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                integrations.append({
                    'name': match.strip(),
                    'type': 'external_service'
                })

        return integrations

    def generate_task_breakdown(self, feature_id: str, analysis: Dict) -> Dict:
        """Generate comprehensive task breakdown"""

        feature_num = feature_id.split('-')[0]
        task_counter = 1
        tasks = {
            'setup': [],
            'tdd_red': [],
            'tdd_green': [],
            'integration': [],
            'qa': [],
            'docs_deploy': []
        }

        # Phase 0: Setup & Prerequisites
        tasks['setup'] = self._generate_setup_tasks(feature_num, task_counter, analysis)
        task_counter += len(tasks['setup'])

        # Phase 1: TDD Red Phase (Tests First)
        tasks['tdd_red'] = self._generate_tdd_red_tasks(feature_num, task_counter, analysis)
        task_counter += len(tasks['tdd_red'])

        # Phase 2: TDD Green Phase (Implementation)
        tasks['tdd_green'] = self._generate_tdd_green_tasks(feature_num, task_counter, analysis)
        task_counter += len(tasks['tdd_green'])

        # Phase 3: Integration & Enhancement
        tasks['integration'] = self._generate_integration_tasks(feature_num, task_counter, analysis)
        task_counter += len(tasks['integration'])

        # Phase 4: QA & Testing
        tasks['qa'] = self._generate_qa_tasks(feature_num, task_counter, analysis)
        task_counter += len(tasks['qa'])

        # Phase 5: Documentation & Deployment
        tasks['docs_deploy'] = self._generate_docs_deploy_tasks(feature_num, task_counter, analysis)

        # Calculate dependencies and parallel execution
        all_tasks = []
        for phase_tasks in tasks.values():
            all_tasks.extend(phase_tasks)

        self._calculate_dependencies(all_tasks)
        self._mark_parallel_execution(all_tasks)

        return {
            'feature_id': feature_id,
            'tasks_by_phase': tasks,
            'all_tasks': all_tasks,
            'total_tasks': len(all_tasks),
            'estimated_duration': self._calculate_total_duration(all_tasks),
            'parallel_groups': self._identify_parallel_groups(all_tasks)
        }

    def _generate_setup_tasks(self, feature_num: str, start_counter: int, analysis: Dict) -> List[Dict]:
        """Generate Phase 0: Setup tasks"""
        tasks = []
        counter = start_counter

        # Project initialization
        tasks.append({
            'id': f"{feature_num}-T-{counter:03d}",
            'title': 'Initialize project structure',
            'type': 'Setup',
            'file': 'Project root',
            'description': 'Set up initial project structure and configuration',
            'estimated': '0.5 hours',
            'parallel': False,
            'depends_on': [],
            'implements': '',
            'phase': 'setup',
            'status': 'pending'
        })
        counter += 1

        # Dependencies installation
        stack = analysis.get('technology_stack', {})
        tasks.append({
            'id': f"{feature_num}-T-{counter:03d}",
            'title': 'Install and configure dependencies',
            'type': 'Setup',
            'file': 'requirements.txt / package.json',
            'description': f"Install {stack.get('framework', 'framework')} and other dependencies",
            'estimated': '1 hour',
            'parallel': False,
            'depends_on': [f"{feature_num}-T-{counter-1:03d}"],
            'implements': '',
            'phase': 'setup',
            'status': 'pending'
        })
        counter += 1

        # Development tools
        tasks.append({
            'id': f"{feature_num}-T-{counter:03d}",
            'title': 'Configure development tools',
            'type': 'Setup',
            'file': '.eslintrc, .prettierrc, pyproject.toml',
            'description': 'Set up linting, formatting, and code quality tools',
            'estimated': '1 hour',
            'parallel': True,
            'depends_on': [f"{feature_num}-T-{counter-1:03d}"],
            'implements': '',
            'phase': 'setup',
            'status': 'pending'
        })
        counter += 1

        # Testing framework
        testing_framework = stack.get('testing', 'pytest')
        tasks.append({
            'id': f"{feature_num}-T-{counter:03d}",
            'title': 'Setup testing framework',
            'type': 'Setup',
            'file': f'{testing_framework}.ini, test config',
            'description': f'Configure {testing_framework} testing framework',
            'estimated': '1 hour',
            'parallel': True,
            'depends_on': [f"{feature_num}-T-{counter-1:03d}"],
            'implements': '',
            'phase': 'setup',
            'status': 'pending'
        })

        return tasks

    def _generate_tdd_red_tasks(self, feature_num: str, start_counter: int, analysis: Dict) -> List[Dict]:
        """Generate Phase 1: TDD Red Phase tasks (tests that must fail)"""
        tasks = []
        counter = start_counter

        complexity = analysis.get('complexity_indicators', {})

        # Contract tests (if has API)
        if complexity.get('has_api', False):
            # POST endpoint test
            tasks.append({
                'id': f"{feature_num}-T-{counter:03d}",
                'title': 'Contract test POST /api/resource',
                'type': 'Contract Test',
                'file': 'tests/contract/test_resource_post.py',
                'description': 'Test API contract for POST endpoint - MUST FAIL initially',
                'estimated': '2 hours',
                'parallel': True,
                'depends_on': [f"{feature_num}-T-{start_counter-1:03d}"],  # Setup framework
                'implements': f"{feature_num}-R-001",
                'validates': f"{feature_num}-A-001",
                'must_fail': True,
                'phase': 'tdd_red',
                'status': 'pending'
            })
            counter += 1

            # GET endpoint test
            tasks.append({
                'id': f"{feature_num}-T-{counter:03d}",
                'title': 'Contract test GET /api/resource/{id}',
                'type': 'Contract Test',
                'file': 'tests/contract/test_resource_get.py',
                'description': 'Test API contract for GET endpoint - MUST FAIL initially',
                'estimated': '2 hours',
                'parallel': True,
                'depends_on': [f"{feature_num}-T-{start_counter-1:03d}"],
                'implements': f"{feature_num}-R-002",
                'validates': f"{feature_num}-A-002",
                'must_fail': True,
                'phase': 'tdd_red',
                'status': 'pending'
            })
            counter += 1

        # Integration tests
        tasks.append({
            'id': f"{feature_num}-T-{counter:03d}",
            'title': 'Integration test for primary user story',
            'type': 'Integration Test',
            'file': 'tests/integration/test_user_story_1.py',
            'description': 'End-to-end test for main user workflow - MUST FAIL initially',
            'estimated': '3 hours',
            'parallel': True,
            'depends_on': [f"{feature_num}-T-{start_counter-1:03d}"],
            'implements': f"{feature_num}-R-003",
            'validates': f"{feature_num}-A-003",
            'must_fail': True,
            'phase': 'tdd_red',
            'status': 'pending'
        })
        counter += 1

        # Model tests (if has database)
        if complexity.get('has_database', False):
            tasks.append({
                'id': f"{feature_num}-T-{counter:03d}",
                'title': 'Tests for User model',
                'type': 'Model Test',
                'file': 'tests/models/test_user.py',
                'description': 'Test User entity creation and validation - MUST FAIL initially',
                'estimated': '2 hours',
                'parallel': True,
                'depends_on': [f"{feature_num}-T-{start_counter-1:03d}"],
                'implements': f"{feature_num}-R-004",
                'must_fail': True,
                'phase': 'tdd_red',
                'status': 'pending'
            })
            counter += 1

            # Add more entity tests based on complexity
            if complexity.get('entity_count', 0) > 1:
                tasks.append({
                    'id': f"{feature_num}-T-{counter:03d}",
                    'title': 'Tests for Session model',
                    'type': 'Model Test',
                    'file': 'tests/models/test_session.py',
                    'description': 'Test Session entity and relationships - MUST FAIL initially',
                    'estimated': '2 hours',
                    'parallel': True,
                    'depends_on': [f"{feature_num}-T-{start_counter-1:03d}"],
                    'implements': f"{feature_num}-R-005",
                    'must_fail': True,
                    'phase': 'tdd_red',
                    'status': 'pending'
                })

        return tasks

    def _generate_tdd_green_tasks(self, feature_num: str, start_counter: int, analysis: Dict) -> List[Dict]:
        """Generate Phase 2: TDD Green Phase tasks (implementation to make tests pass)"""
        tasks = []
        counter = start_counter

        complexity = analysis.get('complexity_indicators', {})

        # Model implementations (if has database)
        if complexity.get('has_database', False):
            tasks.append({
                'id': f"{feature_num}-T-{counter:03d}",
                'title': 'Implement User model',
                'type': 'Model Implementation',
                'file': 'src/models/user.py',
                'description': 'Implement User entity to make model tests pass',
                'estimated': '3 hours',
                'parallel': True,
                'depends_on': [f"{feature_num}-T-{start_counter-1:03d}"],  # Last test task
                'implements': f"{feature_num}-R-004",
                'makes_pass': [f"{feature_num}-T-{start_counter-1:03d}"],  # User model test
                'phase': 'tdd_green',
                'status': 'pending'
            })
            counter += 1

            if complexity.get('entity_count', 0) > 1:
                tasks.append({
                    'id': f"{feature_num}-T-{counter:03d}",
                    'title': 'Implement Session model',
                    'type': 'Model Implementation',
                    'file': 'src/models/session.py',
                    'description': 'Implement Session entity to make tests pass',
                    'estimated': '3 hours',
                    'parallel': True,
                    'depends_on': [f"{feature_num}-T-{start_counter:03d}"],  # Session test
                    'implements': f"{feature_num}-R-005",
                    'makes_pass': [f"{feature_num}-T-{start_counter:03d}"],
                    'phase': 'tdd_green',
                    'status': 'pending'
                })
                counter += 1

        # Service layer implementation
        tasks.append({
            'id': f"{feature_num}-T-{counter:03d}",
            'title': 'Implement authentication service',
            'type': 'Service Implementation',
            'file': 'src/services/auth_service.py',
            'description': 'Implement business logic for authentication',
            'estimated': '4 hours',
            'parallel': True,
            'depends_on': [f"{feature_num}-T-{counter-1:03d}"] if complexity.get('has_database') else [f"{feature_num}-T-{start_counter-1:03d}"],
            'implements': f"{feature_num}-R-001",
            'makes_pass': [f"{feature_num}-T-{start_counter-2:03d}"],  # Integration test
            'phase': 'tdd_green',
            'status': 'pending'
        })
        counter += 1

        # Validation middleware
        tasks.append({
            'id': f"{feature_num}-T-{counter:03d}",
            'title': 'Implement validation middleware',
            'type': 'Middleware',
            'file': 'src/middleware/validation.py',
            'description': 'Implement request validation middleware',
            'estimated': '3 hours',
            'parallel': False,
            'depends_on': [f"{feature_num}-T-{counter-1:03d}"],
            'implements': f"{feature_num}-R-002",
            'phase': 'tdd_green',
            'status': 'pending'
        })
        counter += 1

        # API implementation (if has API)
        if complexity.get('has_api', False):
            tasks.append({
                'id': f"{feature_num}-T-{counter:03d}",
                'title': 'Implement POST /api/auth/login',
                'type': 'API Endpoint',
                'file': 'src/api/auth_endpoints.py',
                'description': 'Implement login endpoint to make contract tests pass',
                'estimated': '3 hours',
                'parallel': False,
                'depends_on': [f"{feature_num}-T-{counter-1:03d}"],
                'implements': f"{feature_num}-R-001",
                'makes_pass': [f"{feature_num}-T-{start_counter-3:03d}"],  # POST contract test
                'phase': 'tdd_green',
                'status': 'pending'
            })
            counter += 1

            tasks.append({
                'id': f"{feature_num}-T-{counter:03d}",
                'title': 'Implement GET /api/auth/status',
                'type': 'API Endpoint',
                'file': 'src/api/auth_endpoints.py',
                'description': 'Implement status endpoint',
                'estimated': '2 hours',
                'parallel': False,
                'depends_on': [f"{feature_num}-T-{counter-1:03d}"],  # Same file dependency
                'implements': f"{feature_num}-R-002",
                'makes_pass': [f"{feature_num}-T-{start_counter-2:03d}"],  # GET contract test
                'phase': 'tdd_green',
                'status': 'pending'
            })

        return tasks

    def _generate_integration_tasks(self, feature_num: str, start_counter: int, analysis: Dict) -> List[Dict]:
        """Generate Phase 3: Integration tasks"""
        tasks = []
        counter = start_counter

        complexity = analysis.get('complexity_indicators', {})

        # Database integration (if has database)
        if complexity.get('has_database', False):
            tasks.append({
                'id': f"{feature_num}-T-{counter:03d}",
                'title': 'Create database migration scripts',
                'type': 'Database',
                'file': 'migrations/001_initial_schema.sql',
                'description': 'Create database schema migration',
                'estimated': '3 hours',
                'parallel': False,
                'depends_on': [f"{feature_num}-T-{start_counter-1:03d}"],  # Last implementation task
                'implements': 'Data model from plan',
                'phase': 'integration',
                'status': 'pending'
            })
            counter += 1

            tasks.append({
                'id': f"{feature_num}-T-{counter:03d}",
                'title': 'Connect models to database',
                'type': 'Database Integration',
                'file': 'src/database/connection.py',
                'description': 'Set up ORM and database connections',
                'estimated': '2 hours',
                'parallel': False,
                'depends_on': [f"{feature_num}-T-{counter-1:03d}"],
                'phase': 'integration',
                'status': 'pending'
            })
            counter += 1

        # Authentication middleware (if has auth)
        if complexity.get('has_auth', False):
            tasks.append({
                'id': f"{feature_num}-T-{counter:03d}",
                'title': 'Implement authentication middleware',
                'type': 'Middleware',
                'file': 'src/middleware/auth.py',
                'description': 'Implement JWT authentication middleware',
                'estimated': '5 hours',
                'parallel': True,
                'depends_on': [f"{feature_num}-T-{start_counter-1:03d}"],
                'implements': f"{feature_num}-R-006",
                'phase': 'integration',
                'status': 'pending'
            })
            counter += 1

        # External integrations
        integrations = analysis.get('integration_points', [])
        if integrations:
            tasks.append({
                'id': f"{feature_num}-T-{counter:03d}",
                'title': f'Integrate with {integrations[0]["name"]}',
                'type': 'External Integration',
                'file': f'src/integrations/{integrations[0]["name"].lower()}.py',
                'description': f'Implement {integrations[0]["name"]} integration',
                'estimated': '4 hours',
                'parallel': True,
                'depends_on': [f"{feature_num}-T-{start_counter-1:03d}"],
                'implements': f"{feature_num}-R-007",
                'phase': 'integration',
                'status': 'pending'
            })
            counter += 1

        # Error handling
        tasks.append({
            'id': f"{feature_num}-T-{counter:03d}",
            'title': 'Implement error handling middleware',
            'type': 'Middleware',
            'file': 'src/middleware/error_handler.py',
            'description': 'Global error handling and logging',
            'estimated': '3 hours',
            'parallel': True,
            'depends_on': [f"{feature_num}-T-{counter-1:03d}"],
            'phase': 'integration',
            'status': 'pending'
        })

        return tasks

    def _generate_qa_tasks(self, feature_num: str, start_counter: int, analysis: Dict) -> List[Dict]:
        """Generate Phase 4: QA and testing tasks"""
        tasks = []
        counter = start_counter

        # Performance testing
        performance = analysis.get('performance_requirements', {})
        if performance.get('response_time') or performance.get('throughput'):
            tasks.append({
                'id': f"{feature_num}-T-{counter:03d}",
                'title': 'Load testing',
                'type': 'Performance Test',
                'file': 'tests/performance/load_test.py',
                'description': 'Test system performance under load',
                'estimated': '4 hours',
                'parallel': True,
                'depends_on': [f"{feature_num}-T-{start_counter-1:03d}"],
                'validates': f"{feature_num}-R-008",
                'phase': 'qa',
                'status': 'pending'
            })
            counter += 1

        # Security testing (if has auth)
        complexity = analysis.get('complexity_indicators', {})
        if complexity.get('has_auth', False):
            tasks.append({
                'id': f"{feature_num}-T-{counter:03d}",
                'title': 'Security audit',
                'type': 'Security Test',
                'file': 'tests/security/security_audit.py',
                'description': 'Comprehensive security testing',
                'estimated': '5 hours',
                'parallel': True,
                'depends_on': [f"{feature_num}-T-{start_counter-1:03d}"],
                'validates': f"{feature_num}-R-009",
                'phase': 'qa',
                'status': 'pending'
            })
            counter += 1

        # Manual validation
        tasks.append({
            'id': f"{feature_num}-T-{counter:03d}",
            'title': 'Execute quickstart validation scenarios',
            'type': 'Manual Testing',
            'file': 'Manual test scenarios',
            'description': 'Manual validation of all acceptance criteria',
            'estimated': '4 hours',
            'parallel': False,
            'depends_on': [f"{feature_num}-T-{counter-1:03d}"] if counter > start_counter else [f"{feature_num}-T-{start_counter-1:03d}"],
            'validates': 'All acceptance criteria',
            'phase': 'qa',
            'status': 'pending'
        })

        return tasks

    def _generate_docs_deploy_tasks(self, feature_num: str, start_counter: int, analysis: Dict) -> List[Dict]:
        """Generate Phase 5: Documentation and deployment tasks"""
        tasks = []
        counter = start_counter

        # User documentation
        tasks.append({
            'id': f"{feature_num}-T-{counter:03d}",
            'title': 'Write user documentation',
            'type': 'Documentation',
            'file': '06-documentation/user-guides/feature.md',
            'description': 'Create comprehensive user guides',
            'estimated': '4 hours',
            'parallel': True,
            'depends_on': [f"{feature_num}-T-{start_counter-1:03d}"],
            'phase': 'docs_deploy',
            'status': 'pending'
        })
        counter += 1

        # Technical documentation
        tasks.append({
            'id': f"{feature_num}-T-{counter:03d}",
            'title': 'Write technical documentation',
            'type': 'Documentation',
            'file': '06-documentation/technical-docs/feature.md',
            'description': 'Create technical documentation and API reference',
            'estimated': '3 hours',
            'parallel': True,
            'depends_on': [f"{feature_num}-T-{start_counter-1:03d}"],
            'phase': 'docs_deploy',
            'status': 'pending'
        })
        counter += 1

        # Deployment preparation
        tasks.append({
            'id': f"{feature_num}-T-{counter:03d}",
            'title': 'Create deployment checklist',
            'type': 'Documentation',
            'file': '08-deliverables/deployment-checklist.md',
            'description': 'Prepare deployment procedures and checklist',
            'estimated': '2 hours',
            'parallel': False,
            'depends_on': [f"{feature_num}-T-{counter-1:03d}"],
            'phase': 'docs_deploy',
            'status': 'pending'
        })

        return tasks

    def _calculate_dependencies(self, tasks: List[Dict]):
        """Calculate and validate task dependencies"""
        task_map = {task['id']: task for task in tasks}

        for task in tasks:
            # Validate that all dependencies exist
            valid_deps = []
            for dep_id in task.get('depends_on', []):
                if dep_id in task_map:
                    valid_deps.append(dep_id)
            task['depends_on'] = valid_deps

            # Add blocks field (reverse dependency)
            task['blocks'] = []

        # Calculate what each task blocks
        for task in tasks:
            for dep_id in task.get('depends_on', []):
                if dep_id in task_map:
                    task_map[dep_id]['blocks'].append(task['id'])

    def _mark_parallel_execution(self, tasks: List[Dict]):
        """Mark tasks that can be executed in parallel"""
        file_map = {}

        # Group tasks by file they modify
        for task in tasks:
            file_path = task.get('file', '')
            if file_path not in file_map:
                file_map[file_path] = []
            file_map[file_path].append(task)

        # Mark parallel execution
        for task in tasks:
            file_path = task.get('file', '')

            # Can be parallel if:
            # 1. Different files OR
            # 2. Test files (can run in parallel) OR
            # 3. Documentation files
            can_be_parallel = (
                task.get('parallel', False) and
                (task['type'] in ['Test', 'Documentation', 'Setup'] or
                 len(file_map[file_path]) == 1)
            )

            task['parallel'] = can_be_parallel

    def _calculate_total_duration(self, tasks: List[Dict]) -> int:
        """Calculate estimated total duration in days"""
        total_hours = 0

        for task in tasks:
            estimate = task.get('estimated', '1 hour')
            hours = self._parse_time_estimate(estimate)
            total_hours += hours

        # Convert to days (assuming 8 hours per day)
        return max(1, int(total_hours / 8))

    def _parse_time_estimate(self, estimate: str) -> float:
        """Parse time estimate string to hours"""
        estimate = estimate.lower()

        if 'hour' in estimate:
            hours_match = re.search(r'(\d+(?:\.\d+)?)\s*hour', estimate)
            return float(hours_match.group(1)) if hours_match else 1.0
        elif 'day' in estimate:
            days_match = re.search(r'(\d+(?:\.\d+)?)\s*day', estimate)
            return float(days_match.group(1)) * 8 if days_match else 8.0
        else:
            return 1.0

    def _identify_parallel_groups(self, tasks: List[Dict]) -> List[List[str]]:
        """Identify groups of tasks that can run in parallel"""
        parallel_groups = []
        current_group = []

        for task in tasks:
            if task.get('parallel', False):
                current_group.append(task['id'])
            else:
                if current_group:
                    parallel_groups.append(current_group)
                    current_group = []

        if current_group:
            parallel_groups.append(current_group)

        return parallel_groups

    def create_tasks_document(self, feature_id: str, task_breakdown: Dict) -> str:
        """Create the tasks.md document"""

        feature_path = self.project_path / "02-planning" / "features" / feature_id
        tasks_file = feature_path / "tasks.md"

        # Prepare template variables
        feature_name = feature_id.replace('-', ' ').title()
        feature_num = feature_id.split('-')[0]

        template_vars = {
            'FEATURE NAME': feature_name,
            '###': feature_num,
            'feature-name': feature_id,
            'YYYY-MM-DD': datetime.now().strftime('%Y-%m-%d'),
            'X weeks': str(task_breakdown['estimated_duration'] // 7),
            'XX%': '0'  # Initial progress
        }

        # Try to render template
        try:
            tasks_content = self.template_manager.render_template(
                'tasks-template-enhanced',
                template_vars
            )

            # Enhance with actual task data
            tasks_content = self._enhance_tasks_template(tasks_content, task_breakdown)

        except FileNotFoundError:
            # Fallback: create basic tasks document
            tasks_content = self._create_basic_tasks_document(feature_id, task_breakdown)

        tasks_file.write_text(tasks_content, encoding='utf-8')
        return str(tasks_file)

    def _enhance_tasks_template(self, template_content: str, task_breakdown: Dict) -> str:
        """Enhance template with actual task data"""

        # Update task counts
        template_content = template_content.replace('[###]', str(task_breakdown['total_tasks']))

        # Add task sections for each phase
        phases_content = ""
        for phase_name, phase_tasks in task_breakdown['tasks_by_phase'].items():
            if phase_tasks:
                phases_content += f"\n\n### {phase_name.replace('_', ' ').title()} Tasks\n\n"
                for task in phase_tasks:
                    phases_content += self._format_task_for_template(task)

        # Insert task content (this would need more sophisticated template replacement)
        return template_content

    def _format_task_for_template(self, task: Dict) -> str:
        """Format a single task for the template"""
        parallel_marker = "[P] " if task.get('parallel', False) else ""

        content = f"""
#### {task['id']}: {parallel_marker}{task['title']}
- **Type**: {task['type']}
- **File**: {task['file']}
- **Description**: {task['description']}
- **Estimated**: {task['estimated']}
- **Implements**: {task.get('implements', 'N/A')}
- **Depends on**: {', '.join(task.get('depends_on', []))}
- **Status**: {task['status']}

"""
        return content

    def _create_basic_tasks_document(self, feature_id: str, task_breakdown: Dict) -> str:
        """Create basic tasks document if template is not available"""

        feature_name = feature_id.replace('-', ' ').title()
        feature_num = feature_id.split('-')[0]

        content = f"""# Tasks: {feature_name}

**Feature ID**: {feature_id}
**Generated**: {datetime.now().strftime('%Y-%m-%d')}
**Total Tasks**: {task_breakdown['total_tasks']}
**Estimated Duration**: {task_breakdown['estimated_duration']} days

---

## Task Breakdown by Phase

"""

        # Add tasks by phase
        for phase_name, phase_tasks in task_breakdown['tasks_by_phase'].items():
            if phase_tasks:
                content += f"### {phase_name.replace('_', ' ').title()} ({len(phase_tasks)} tasks)\n\n"

                for task in phase_tasks:
                    parallel_marker = "[P] " if task.get('parallel', False) else ""
                    content += f"- **{task['id']}**: {parallel_marker}{task['title']}\n"
                    content += f"  - File: {task['file']}\n"
                    content += f"  - Estimated: {task['estimated']}\n"
                    if task.get('depends_on'):
                        content += f"  - Depends on: {', '.join(task['depends_on'])}\n"
                    content += "\n"

        content += f"""
---

## Summary

- **Total Tasks**: {task_breakdown['total_tasks']}
- **Estimated Duration**: {task_breakdown['estimated_duration']} days
- **Parallel Groups**: {len(task_breakdown['parallel_groups'])}

**Status**: Ready for implementation
"""

        return content

    def generate_tasks_for_feature(self, feature_id: str) -> Dict:
        """Generate complete task breakdown for a feature"""

        # Validate feature has implementation plan
        features_with_plans = self.get_features_with_plans()
        if feature_id not in features_with_plans:
            raise ValueError(f"No implementation plan found for feature '{feature_id}'. Run 'specmap plan' first.")

        # Analyze implementation plan
        analysis = self.analyze_implementation_plan(feature_id)

        # Generate task breakdown
        task_breakdown = self.generate_task_breakdown(feature_id, analysis)

        # Create tasks document
        tasks_file = self.create_tasks_document(feature_id, task_breakdown)

        # Update workflow state
        feature_data = self.workflow.get_feature(feature_id) or {}
        feature_data['status'] = 'tasks_generated'
        feature_data['tasks_created'] = datetime.now().isoformat()
        feature_data['total_tasks'] = task_breakdown['total_tasks']
        feature_data['estimated_duration'] = task_breakdown['estimated_duration']
        self.workflow.add_feature(feature_id, feature_data)

        # Update project phase
        self.workflow.update_phase('task_generation')

        return {
            'feature_id': feature_id,
            'tasks_file': tasks_file,
            'total_tasks': task_breakdown['total_tasks'],
            'estimated_duration': task_breakdown['estimated_duration'],
            'tasks_by_phase': {phase: len(tasks) for phase, tasks in task_breakdown['tasks_by_phase'].items()},
            'parallel_groups': len(task_breakdown['parallel_groups']),
            'analysis': analysis
        }