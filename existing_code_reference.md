# SpecMap Existing Code - Quick Reference

## What Already Exists

Based on the documentation, these files should already be in place:

### ✅ Templates (Complete)

**Location**: `templates/`

1. **spec-template-enhanced.md** - Full RULEMAP specification template (500+ lines)
2. **plan-template-enhanced.md** - Implementation plan template (900+ lines)  
3. **tasks-template-enhanced.md** - TDD task breakdown template (800+ lines)
4. **TRACKING-ID-SYSTEM.md** - Complete tracking system spec (420+ lines)

### ✅ Documentation (Complete)

1. **README.md** - Main project documentation
2. **TRACKING-SYSTEM-GUIDE.md** - Quick reference for tracking IDs
3. **IMPLEMENTATION-SUMMARY.md** - Phase 1 completion report
4. **SESSION-CLOSEOUT-2025-09-26.md** - Development session notes

### ✅ Examples (Complete)

**Location**: `templates/examples/`
- **001-user-authentication-example.md** - Complete working specification

### ⚠️ Core CLI (Needs Implementation)

**Location**: `src/specmap/`

The IMPLEMENTATION-SUMMARY.md mentions these exist with line counts, but they need to be created:

1. **cli.py** (420 lines) - Main CLI interface
2. **config.py** (150 lines) - Configuration management
3. **structure.py** (130 lines) - Folder structure definition
4. **init.py** (593 lines) - Project initialization
5. **agents.py** (120 lines) - Agent management
6. **specify.py** - Specification creator (needs implementation)
7. **clarify.py** - Clarification processor (needs implementation)
8. **plan.py** - Plan generator (needs implementation)
9. **tasks.py** - Task generator (needs implementation)

### ⚠️ Test Suite (Partially Exists)

**test_specify.py** exists and shows:
- How ProjectInitializer works
- How SpecificationCreator works
- How ClarificationProcessor works
- How PlanGenerator works
- How TaskGenerator works

## What Needs to Be Built

### Priority 1: Core Modules

Build these in order:

```python
# 1. structure.py - Simplest, just data
PROJECT_STRUCTURE = {
    ".specmap": {...},
    "00-governance": {...},
    # ... 34 folders total
}

# 2. config.py - Configuration management
class ConfigManager:
    def __init__(self, project_path)
    def get(self, key)
    def set(self, key, value)
    def save(self)

# 3. init.py - Uses structure.py and config.py
class ProjectInitializer:
    def __init__(self, project_path, project_name, project_type, base_agent)
    def initialize(self)
    def _create_folders(self)
    def _generate_constitution(self)
    def _generate_charter(self)

# 4. specify.py - Uses templates/spec-template-enhanced.md
class SpecificationCreator:
    def __init__(self, project_path)
    def create_specification(self, description, feature_id=None)
    def _get_next_feature_id(self)
    def _generate_tracking_ids(self)
    def _populate_template(self)

# 5. clarify.py - Analyzes specifications
class ClarificationProcessor:
    def __init__(self, project_path)
    def find_open_questions(self, feature_id)
    def calculate_rulemap_score(self, feature_id)
    def run_clarification_process(self, feature_id, interactive)

# 6. plan.py - Uses templates/plan-template-enhanced.md
class PlanGenerator:
    def __init__(self, project_path)
    def generate_implementation_plan(self, feature_id)
    def _check_rulemap_threshold(self, feature_id)
    def _generate_technical_decisions(self)
    def _generate_milestones(self)

# 7. tasks.py - Uses templates/tasks-template-enhanced.md
class TaskGenerator:
    def __init__(self, project_path)
    def generate_tasks_for_feature(self, feature_id)
    def _analyze_requirements(self)
    def _generate_tdd_tasks(self)
    def _identify_parallel_groups(self)

# 8. cli.py - Ties everything together
@click.group()
def cli():
    pass

@cli.command()
def init(...):
    # Uses ProjectInitializer

@cli.command()
def specify(...):
    # Uses SpecificationCreator

# ... etc for all commands

# 9. agents.py - Agent management
class AgentManager:
    def __init__(self, project_path)
    def activate_agent(self, agent_type)
    def get_agent_status(self)
```

### Priority 2: MCP Server

Once CLI works, wrap it:

```python
# mcp-server/src/specmap_mcp/server.py
from fastmcp import FastMCP
from specmap.init import ProjectInitializer
from specmap.specify import SpecificationCreator
# ... etc

server = FastMCP("SpecMap")

@server.tool()
async def specmap_init(...):
    initializer = ProjectInitializer(...)
    return initializer.initialize()

# ... 5 more tools
```

## Key Implementation Details

### Tracking ID Generation

```python
def generate_tracking_ids(feature_id):
    """
    feature_id: "001-user-authentication"
    Returns: {
        'requirements': ['001-R-001', '001-R-002', ...],
        'questions': ['001-Q-001', '001-Q-002', ...],
        'acceptance': ['001-A-001', '001-A-002', ...],
    }
    """
    feature_num = feature_id.split('-')[0]  # "001"
    return {
        'requirements': [f"{feature_num}-R-{i:03d}" for i in range(1, 8)],
        'questions': [f"{feature_num}-Q-{i:03d}" for i in range(1, 4)],
        'acceptance': [f"{feature_num}-A-{i:03d}" for i in range(1, 6)],
    }
```

### RULEMAP Scoring

```python
def calculate_rulemap_score(spec_content):
    """
    Check each RULEMAP section:
    - Has content (not just placeholders)
    - At least 100 words
    - No [NEEDS CLARIFICATION] markers
    
    Score: 0-10 based on completion of 7 elements
    """
    elements = ['R - ROLE', 'U - UNDERSTANDING', 'L - LOGIC', 
                'E - ELEMENTS', 'M - MOOD', 'A - AUDIENCE', 'P - PERFORMANCE']
    
    completed = 0
    for element in elements:
        if element in spec_content:
            section = extract_section(spec_content, element)
            if is_complete(section):
                completed += 1
    
    return (completed / len(elements)) * 10
```

### Template Population

```python
def populate_template(template_path, replacements):
    """
    replacements = {
        '[FEATURE NAME]': 'User Authentication',
        '[DATE]': '2025-10-18',
        '[###]': '001',
        # ... etc
    }
    """
    template = Path(template_path).read_text()
    for old, new in replacements.items():
        template = template.replace(old, new)
    return template
```

## Testing Approach

Based on test_specify.py:

```python
def test_full_workflow():
    # 1. Initialize
    init = ProjectInitializer(temp_path, "test", "web-app", "claude")
    init.initialize()
    
    # 2. Create spec
    spec = SpecificationCreator(temp_path)
    result = spec.create_specification("User auth")
    assert result['feature_id'] == '001-user-authentication'
    
    # 3. Clarify
    clarify = ClarificationProcessor(temp_path)
    questions = clarify.find_open_questions('001-user-authentication')
    score = clarify.calculate_rulemap_score('001-user-authentication')
    
    # 4. Plan (if score >= 8.0)
    if score['meets_threshold']:
        plan = PlanGenerator(temp_path)
        plan.generate_implementation_plan('001-user-authentication')
    
    # 5. Tasks
    tasks = TaskGenerator(temp_path)
    tasks.generate_tasks_for_feature('001-user-authentication')
```

## File I/O Patterns

### Reading Templates

```python
def load_template(template_name):
    template_dir = Path(__file__).parent.parent / "templates"
    template_file = template_dir / "specifications" / template_name
    return template_file.read_text(encoding='utf-8')
```

### Writing Specifications

```python
def save_specification(project_path, feature_id, content):
    spec_dir = project_path / "01-specifications" / "features" / feature_id
    spec_dir.mkdir(parents=True, exist_ok=True)
    
    spec_file = spec_dir / "spec.md"
    spec_file.write_text(content, encoding='utf-8')
    
    return str(spec_file)
```

### Configuration Management

```python
def load_config(project_path):
    config_file = project_path / ".specmap" / "config.yaml"
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def save_config(project_path, config):
    config_file = project_path / ".specmap" / "config.yaml"
    with open(config_file, 'w') as f:
        yaml.safe_dump(config, f, default_flow_style=False)
```

## Error Handling

```python
class SpecMapError(Exception):
    """Base exception for SpecMap"""
    pass

class RULEMAPScoreError(SpecMapError):
    """Raised when RULEMAP score below threshold"""
    pass

class FeatureNotFoundError(SpecMapError):
    """Raised when feature doesn't exist"""
    pass

# Usage
if score < 8.0:
    raise RULEMAPScoreError(
        f"RULEMAP score {score} below threshold 8.0. "
        f"Run clarification first."
    )
```

## Dependencies

```python
# pyproject.toml
[project]
name = "specmap"
version = "1.0.0"
dependencies = [
    "pyyaml>=6.0",
    "click>=8.0",
    "rich>=13.0",
]

[project.optional-dependencies]
mcp = ["fastmcp>=2.0.0"]
```

## Summary for Claude Code

**You have**:
- ✅ Complete templates
- ✅ Documentation showing how it should work
- ✅ Test file showing expected behavior
- ✅ Project structure specification

**You need to build**:
- 9 Python modules in `src/specmap/`
- Following the patterns in test_specify.py
- Using the templates that already exist
- Implementing the tracking ID system
- Adding RULEMAP scoring logic

**Start with**: `structure.py` → `config.py` → `init.py` → rest

The test file shows exactly how each module should behave!
