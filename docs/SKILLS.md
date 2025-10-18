# Claude Code Skills for SpecMap

SpecMap provides comprehensive support for creating and managing Claude Code skills that enhance the AI-powered specification-driven development workflow.

## Overview

Skills are specialized instructions that guide Claude through specific SpecMap tasks. They're stored in the `.claude/skills/` directory of your project and can be invoked in Claude Code.

## Quick Start

### Install All SpecMap Skills

```bash
specmap skill install-all
```

This installs 5 predefined skills optimized for the SpecMap workflow:
- `specmap-reviewer` - Review specifications for RULEMAP compliance
- `specmap-planner` - Generate implementation plans
- `specmap-task-generator` - Create TDD task breakdowns
- `specmap-qa` - Quality assurance and compliance validation
- `specmap-charter-helper` - Complete project charters

### Use a Skill in Claude Code

```
/skill specmap-reviewer
```

Or via the MCP server:
```
Use the specmap-reviewer skill to review my specification
```

## Available Commands

### View Available Templates

```bash
specmap skill templates
```

Lists all predefined SpecMap skill templates with descriptions.

### Install a Specific Template

```bash
specmap skill install specmap-reviewer
```

Installs a single skill template.

### List Installed Skills

```bash
specmap skill list
```

Shows all skills currently installed in your project.

### Create a Custom Skill

```bash
specmap skill create my-custom-skill "Description of skill"
```

Creates a new custom skill. You'll be prompted to enter the skill content.

**Example with content:**
```bash
specmap skill create code-reviewer "Review code for best practices" -c "
# Code Reviewer

Review the code and check for:
- Code style consistency
- Error handling
- Documentation
- Test coverage
"
```

### Delete a Skill

```bash
specmap skill delete my-skill
```

Removes a skill from your project.

## Using the MCP Server

The SpecMap MCP server provides tools for skill management:

### `get_skill_templates()`
Get list of available skill templates
```json
{
  "success": true,
  "total_templates": 5,
  "templates": [...]
}
```

### `install_specmap_skill_template(project_path, template_name)`
Install a specific skill template
```json
{
  "project_path": "/path/to/project",
  "template_name": "specmap-reviewer"
}
```

### `install_all_specmap_skills(project_path)`
Install all predefined skills at once
```json
{
  "project_path": "/path/to/project"
}
```

### `create_claude_skill(project_path, name, description, content, metadata?)`
Create a custom skill
```json
{
  "project_path": "/path/to/project",
  "name": "my-skill",
  "description": "Custom skill description",
  "content": "# Skill Instructions\n...",
  "metadata": {"author": "Your Name"}
}
```

### `list_claude_skills(project_path)`
List all installed skills
```json
{
  "project_path": "/path/to/project"
}
```

### `delete_claude_skill(project_path, skill_name)`
Delete a skill
```json
{
  "project_path": "/path/to/project",
  "skill_name": "skill-to-delete"
}
```

## Predefined Skills

### 1. SpecMap Reviewer
**Name:** `specmap-reviewer`

Reviews feature specifications for RULEMAP compliance. Scores each section and provides actionable recommendations.

**Use when:**
- You've created a new specification
- You want to improve spec quality
- You need to validate RULEMAP completeness

**Example:**
```
/skill specmap-reviewer

Please review the specification in 01-specifications/features/feature-001/spec.md
```

### 2. SpecMap Planner
**Name:** `specmap-planner`

Generates comprehensive implementation plans from approved specifications.

**Use when:**
- Specification has RULEMAP score >= 8.0
- You're ready to start planning implementation
- You need technical architecture decisions

**Example:**
```
/skill specmap-planner

Create an implementation plan for feature-001
```

### 3. SpecMap Task Generator
**Name:** `specmap-task-generator`

Creates detailed TDD task breakdowns following the Red-Green-Refactor workflow.

**Use when:**
- Implementation plan is approved
- You're ready to start development
- You need granular task assignments

**Example:**
```
/skill specmap-task-generator

Generate TDD tasks for the authentication feature
```

### 4. SpecMap QA
**Name:** `specmap-qa`

Validates implementations against specifications and project constitution.

**Use when:**
- Implementation is complete
- You need compliance validation
- You're preparing for deployment

**Example:**
```
/skill specmap-qa

Validate the user-management implementation
```

### 5. Charter Helper
**Name:** `specmap-charter-helper`

Guides you through completing the RULEMAP project charter interactively.

**Use when:**
- Starting a new project
- Charter needs completion
- You want structured project planning

**Example:**
```
/skill specmap-charter-helper

Help me complete the project charter
```

## Creating Custom Skills

### Skill File Format

Skills are markdown files with YAML frontmatter:

```markdown
---
name: skill-name
description: Brief description
created: 2025-10-18
author: Your Name
version: 1.0
---

# Skill Title

Instructions for Claude on what to do...

## Section 1

Details...

## Section 2

More details...
```

### Best Practices

1. **Clear Instructions**: Be specific about what Claude should do
2. **Structured Format**: Use sections to organize the skill
3. **Examples**: Include examples when helpful
4. **Context**: Explain the role and purpose
5. **Output Format**: Specify expected output structure

### Example Custom Skill

```markdown
---
name: api-documenter
description: Generate API documentation from code
author: Team
version: 1.0
---

# API Documentation Generator

You are an expert at creating comprehensive API documentation.

## Your Task

1. Analyze the provided code files
2. Extract API endpoints, methods, and parameters
3. Generate OpenAPI/Swagger documentation
4. Include request/response examples

## Documentation Format

For each endpoint provide:
- HTTP method and path
- Description
- Parameters (path, query, body)
- Request example
- Response example
- Error codes

## Quality Standards

- All endpoints must be documented
- Examples must be valid JSON
- Include authentication requirements
- Document rate limits if applicable
```

## Integration Patterns

### Workflow Integration

Skills integrate seamlessly with the SpecMap workflow:

```
1. Charter Helper → Complete project charter
2. Specify → Create feature spec
3. Reviewer → Validate spec (RULEMAP)
4. Planner → Generate implementation plan
5. Task Generator → Create TDD tasks
6. [Development happens]
7. QA → Validate implementation
```

### MCP Server Usage

```python
# Python example using the MCP server
from specmap_mcp import SpecMapMCP

client = SpecMapMCP()

# Install all skills
result = client.install_all_specmap_skills("/path/to/project")
print(f"Installed {result['installed_count']} skills")

# Create custom skill
client.create_claude_skill(
    project_path="/path/to/project",
    name="database-reviewer",
    description="Review database schemas",
    content="# Database Schema Reviewer\n..."
)

# List skills
skills = client.list_claude_skills("/path/to/project")
for skill in skills['skills']:
    print(f"- {skill['name']}: {skill['description']}")
```

### Command Line Usage

```bash
# Complete workflow
specmap init my-project
cd my-project

# Install skills
specmap skill install-all

# Use skills as you work
# (In Claude Code)
/skill specmap-charter-helper  # Complete charter
/skill specmap-reviewer        # Review specs
/skill specmap-planner         # Create plans
/skill specmap-task-generator  # Generate tasks
/skill specmap-qa             # Validate work
```

## Troubleshooting

### Skills Not Found

If Claude can't find your skills:
1. Verify `.claude/skills/` directory exists
2. Check skill files have `.md` extension
3. Ensure frontmatter is properly formatted

```bash
# Check skills directory
ls .claude/skills/

# List installed skills
specmap skill list
```

### Skills Not Loading

If skills don't load properly:
1. Validate YAML frontmatter syntax
2. Check for special characters in names
3. Ensure files are UTF-8 encoded

```bash
# Reinstall a skill
specmap skill delete problematic-skill
specmap skill install problematic-skill
```

### MCP Server Issues

If the MCP server can't access skills:
1. Verify project path is correct
2. Check file permissions
3. Ensure SpecMap is properly installed

```bash
# Test MCP server
python -m specmap_mcp.server
```

## Advanced Usage

### Skill Composition

Create specialized skills for your team's workflow:

```bash
# Security review skill
specmap skill create security-reviewer "Security-focused code review" -c "
# Security Reviewer

Check for:
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication flaws
- Authorization issues
- Sensitive data exposure
- CSRF protection
"

# Performance review skill
specmap skill create perf-reviewer "Performance optimization reviewer" -c "
# Performance Reviewer

Analyze:
- Database query efficiency
- N+1 query problems
- Caching opportunities
- Bundle size
- Lazy loading usage
"
```

### Team Standards

Create skills that enforce team standards:

```bash
specmap skill create team-standards "Enforce team coding standards" -c "
# Team Standards Enforcer

Verify:
- TypeScript strict mode enabled
- ESLint rules followed
- Jest test coverage >= 80%
- No console.log statements
- Proper error handling
- JSDoc comments on public APIs
"
```

### Project-Specific Skills

Tailor skills to your project's needs:

```bash
specmap skill create api-validator "Validate API against OpenAPI spec" -c "
# API Validator

Compare implementation against:
- OpenAPI specification in docs/api-spec.yaml
- Ensure all endpoints match spec
- Validate request/response schemas
- Check authentication matches spec
- Verify error responses
"
```

## Best Practices

### When to Create Custom Skills

Create custom skills when:
- You have repetitive review tasks
- You need to enforce specific standards
- You want to codify team knowledge
- You have project-specific workflows

### Skill Naming

- Use lowercase with hyphens: `my-skill`
- Be descriptive: `api-security-reviewer` not `api-rev`
- Include context: `specmap-reviewer` not just `reviewer`

### Skill Maintenance

- Version your skills with metadata
- Document changes in skill content
- Review and update skills regularly
- Share useful skills with the team

### Performance Tips

- Keep skills focused on one task
- Don't make skills too long (Claude has context limits)
- Reference external docs rather than duplicating content
- Use clear, actionable language

## Examples

### Complete Example: Adding Security Review

```bash
# 1. Create the skill
specmap skill create security-scanner "Comprehensive security review" -c "
# Security Scanner

Perform comprehensive security review covering:

## Authentication & Authorization
- JWT token validation
- Session management
- Password hashing (bcrypt/argon2)
- Permission checks

## Input Validation
- SQL injection prevention
- XSS prevention
- CSRF protection
- File upload validation

## Data Protection
- Sensitive data encryption
- PII handling
- Secure communication (HTTPS)
- API key management

## Output
Provide:
1. Security score (0-10)
2. List of vulnerabilities found
3. Recommended fixes
4. Risk assessment (Critical/High/Medium/Low)
"

# 2. Use it
# In Claude Code:
/skill security-scanner
Please review src/api/auth.ts for security issues
```

### Complete Example: Code Style Enforcement

```bash
specmap skill create style-enforcer "Enforce project code style" -c "
# Code Style Enforcer

Ensure code follows project guidelines:

## TypeScript
- Strict mode enabled
- No 'any' types
- Interfaces over types for objects
- Proper null checks

## React
- Functional components only
- Custom hooks for logic
- PropTypes or TypeScript interfaces
- No inline styles

## Testing
- Jest + React Testing Library
- Test file naming: *.test.ts(x)
- Coverage >= 80%
- Integration tests for features

## Documentation
- JSDoc for public APIs
- README for each module
- Inline comments for complex logic

Report violations with line numbers and fixes.
"
```

## Related Documentation

- [SpecMap CLI Reference](CLI.md)
- [MCP Server API](MCP_SERVER.md)
- [RULEMAP Framework](RULEMAP.md)
- [Project Structure](STRUCTURE.md)

## Support

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review existing skills: `specmap skill list`
3. View skill templates: `specmap skill templates`
4. Create an issue on GitHub

## Contributing

To contribute new skill templates:
1. Create the skill and test it
2. Add it to `src/specmap/skills.py` in the `TEMPLATES` dict
3. Document the skill in this guide
4. Submit a pull request
