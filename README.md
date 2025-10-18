# SpecMap CLI

AI-powered specification-driven development system combining Spec-Kit methodology with RULEMAP framework.

## Overview

SpecMap is a comprehensive CLI tool and MCP server that enables specification-driven development with AI assistance. It provides:

- **RULEMAP Framework**: 7-element specification framework (Role, Understanding, Logic, Elements, Mood, Audience, Performance)
- **Project Constitution**: Quality governance and principles
- **Spec-Driven Workflow**: Specify → Clarify → Plan → Tasks → Implement → QA
- **AI Agent Integration**: Support for Claude Code, Copilot, Cursor, Gemini, and more
- **MCP Server**: Model Context Protocol server for seamless AI integration
- **Claude Code Skills**: Pre-built and custom skills for workflow automation

## Features

### Core Workflow
- ✅ Project initialization with governance structure
- ✅ RULEMAP-enhanced specifications
- ✅ Systematic clarification process
- ✅ Implementation planning
- ✅ TDD task generation
- ✅ Quality scoring (>= 8.0 threshold)

### AI Integration
- ✅ Multi-platform AI agent support
- ✅ MCP server for Claude integration
- ✅ **Claude Code skills** for specialized tasks
- ✅ Agent handoff protocols
- ✅ Specialized agent orchestration

### Quality Assurance
- ✅ Constitution-based governance
- ✅ RULEMAP compliance scoring
- ✅ Dual validation (spec + constitution)
- ✅ Comprehensive tracking IDs

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/specmap-cli.git
cd specmap-cli

# Install dependencies
pip install -e .
```

### Initialize a Project

```bash
specmap init my-awesome-app --type web-app --agent claude
cd my-awesome-app
```

### Install Claude Code Skills

```bash
# Install all predefined SpecMap skills
specmap skill install-all

# Or install specific skills
specmap skill install specmap-reviewer
```

### Create Your First Specification

```bash
specmap specify "User authentication with email and password"
```

### Follow the Workflow

```bash
# 1. Clarify the specification
specmap clarify

# 2. Generate implementation plan
specmap plan

# 3. Create task breakdown
specmap tasks

# 4. Check project status
specmap status
```

## Claude Code Skills

SpecMap includes powerful skills for Claude Code integration:

### Predefined Skills

1. **specmap-reviewer** - Review specifications for RULEMAP compliance
2. **specmap-planner** - Generate implementation plans
3. **specmap-task-generator** - Create TDD task breakdowns
4. **specmap-qa** - Quality assurance and compliance validation
5. **specmap-charter-helper** - Interactive project charter completion

### Using Skills

In Claude Code:
```
/skill specmap-reviewer
Please review my specification
```

### Managing Skills

```bash
# View available templates
specmap skill templates

# List installed skills
specmap skill list

# Create custom skill
specmap skill create my-skill "Description" -c "Skill content here"

# Delete a skill
specmap skill delete my-skill
```

See [SKILLS.md](docs/SKILLS.md) for complete documentation.

## MCP Server

The SpecMap MCP server provides tools for AI integration:

### Available Tools

**Project Management:**
- `specmap_init()` - Initialize new project
- `specmap_status()` - Get project status

**Specification Workflow:**
- `specmap_specify()` - Create specification
- `specmap_clarify()` - Run clarification process
- `specmap_plan()` - Generate implementation plan
- `specmap_tasks()` - Create task breakdown

**Skill Management:**
- `get_skill_templates()` - List available templates
- `install_specmap_skill_template()` - Install template
- `install_all_specmap_skills()` - Install all skills
- `create_claude_skill()` - Create custom skill
- `list_claude_skills()` - List installed skills
- `delete_claude_skill()` - Remove a skill

### Configuration

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "specmap": {
      "command": "python",
      "args": ["-m", "specmap_mcp.server"],
      "cwd": "/path/to/specmap-cli/mcp-server"
    }
  }
}
```

## Project Structure

```
my-project/
├── .claude/                  # Claude Code integration
│   └── skills/              # Claude Code skills
├── .specmap/                # System configuration
├── 00-governance/           # Constitution + Charter
│   ├── constitution.md
│   └── project-charter.md
├── 01-specifications/       # RULEMAP specs
│   └── features/
│       └── feature-001/
│           ├── spec.md
│           ├── clarifications.md
│           └── research.md
├── 02-planning/            # Implementation plans
│   └── feature-001/
│       ├── plan.md
│       ├── tasks.md
│       └── technical-decisions.md
├── 03-implementation/      # Dev tracking
├── 04-agents/             # Agent management
├── 05-quality-assurance/  # QA & validation
├── 06-documentation/      # Project docs
├── 07-project-tracking/   # Progress tracking
└── 08-deliverables/      # Final outputs
```

## CLI Commands

### Project Management
```bash
specmap init <name>         # Initialize project
specmap status             # View project status
specmap check             # Check prerequisites
```

### Specification Workflow
```bash
specmap specify <desc>     # Create specification
specmap clarify           # Run clarification
specmap plan             # Generate plan
specmap tasks            # Create tasks
```

### Governance
```bash
specmap constitution      # View/edit constitution
specmap charter          # Manage charter
```

### Agent Management
```bash
specmap agent activate <type>      # Activate agent
specmap agent status              # View agents
specmap agent handoff <from> <to> # Transfer work
```

### Skill Management
```bash
specmap skill templates           # List templates
specmap skill install <template>  # Install template
specmap skill install-all        # Install all
specmap skill list              # List installed
specmap skill create <name>     # Create custom
specmap skill delete <name>     # Remove skill
```

## RULEMAP Framework

The 7-element specification framework:

- **R - ROLE & AUTHORITY**: Who owns and decides
- **U - UNDERSTANDING & OBJECTIVES**: What problem we're solving
- **L - LOGIC & APPROACH**: How we'll solve it
- **E - ELEMENTS & CONSTRAINTS**: What we need and limits
- **M - MOOD & EXPERIENCE**: How it should feel
- **A - AUDIENCE & STAKEHOLDERS**: Who it's for
- **P - PERFORMANCE & SUCCESS**: How we measure success

Specifications must achieve a RULEMAP score >= 8.0 before proceeding to implementation.

## Workflow Phases

### 1. Initialization
- Create project structure
- Establish constitution
- Complete charter (RULEMAP)

### 2. Specification
- Create feature specs
- Run clarification
- Achieve quality threshold

### 3. Planning
- Generate implementation plan
- Create task breakdown
- Validate feasibility

### 4. Implementation
- Follow TDD workflow
- Agent-guided development
- Continuous validation

### 5. Quality Assurance
- Constitution compliance
- RULEMAP scoring
- Deployment prep

## AI Agent Support

SpecMap supports multiple AI platforms:

- **Claude Code** (recommended) - Full MCP integration + skills
- **GitHub Copilot** - IDE integration
- **Cursor** - Editor integration
- **Gemini** - Google AI integration
- **Windsurf** - Code assistant
- **Qwen/OpenCode** - Open source options

## Examples

### Complete Feature Development

```bash
# 1. Initialize project
specmap init my-saas-app --type web-app --agent claude
cd my-saas-app

# 2. Install Claude Code skills
specmap skill install-all

# 3. Complete governance
specmap charter --complete

# 4. Create feature specification
specmap specify "User authentication with OAuth2 and JWT"

# 5. Clarify and improve
specmap clarify

# 6. Generate implementation plan
specmap plan

# 7. Create TDD tasks
specmap tasks

# 8. Implement (with Claude Code)
# In Claude Code:
/skill specmap-planner
/skill specmap-task-generator

# 9. Quality validation
# In Claude Code:
/skill specmap-qa
```

### Creating Custom Skills

```bash
# Create a custom API review skill
specmap skill create api-reviewer "Review API endpoints" -c "
# API Endpoint Reviewer

Review the API endpoints for:
- RESTful design
- Proper HTTP methods
- Error handling
- Authentication
- Rate limiting
- Documentation
"

# Use it in Claude Code
# /skill api-reviewer
```

## Configuration

### Project Configuration
`.specmap/config.yaml`:
```yaml
project:
  name: my-project
  type: web-app
  version: 1.0.0
  created: 2025-10-18

agents:
  base_agent: claude

workflow:
  current_phase: specification
```

### Skill Configuration
Skills are stored in `.claude/skills/` as markdown files:
```markdown
---
name: my-skill
description: What it does
created: 2025-10-18
---

# Skill Instructions
...
```

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run specific test
pytest tests/test_skills.py
```

### MCP Server Development

```bash
cd mcp-server
python -m specmap_mcp.server
```

## Documentation

- [Skills Guide](docs/SKILLS.md) - Complete skill documentation
- [MCP Server API](docs/MCP_SERVER.md) - MCP server reference
- [RULEMAP Guide](docs/RULEMAP.md) - Framework details
- [CLI Reference](docs/CLI.md) - Command reference

## Troubleshooting

### Skills Not Loading

```bash
# Check skills directory
ls .claude/skills/

# Reinstall skills
specmap skill install-all
```

### MCP Server Issues

```bash
# Test MCP server
python -m specmap_mcp.server

# Check configuration
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Import Errors

```bash
# Ensure SpecMap is installed
pip install -e .

# Check Python path
python -c "import sys; print(sys.path)"
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Update documentation
5. Submit a pull request

## License

MIT License - see LICENSE file

## Support

- GitHub Issues: [Report bugs](https://github.com/your-org/specmap-cli/issues)
- Documentation: [Full docs](docs/)
- Examples: [Example projects](examples/)

## Roadmap

- [x] Core workflow implementation
- [x] MCP server integration
- [x] Claude Code skills system
- [ ] Web dashboard
- [ ] VS Code extension
- [ ] Team collaboration features
- [ ] Specification templates library
- [ ] CI/CD integration
- [ ] Analytics and insights

## Credits

Built with:
- FastMCP for MCP server
- Click for CLI
- Rich for terminal UI
- PyYAML for configuration

---

**Made with Claude Code** - AI-powered specification-driven development
