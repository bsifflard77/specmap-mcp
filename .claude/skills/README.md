# Claude Code Skills for SpecMap

This directory contains custom skills for Claude Code integration with SpecMap.

## Available Skills

Skills are organized to support the SpecMap workflow:

**Specification Phase:**
- `specmap-reviewer` - Review specs for RULEMAP compliance
- `specmap-charter-helper` - Complete project charters

**Planning Phase:**
- `specmap-planner` - Generate implementation plans
- `specmap-task-generator` - Create TDD task breakdowns

**Quality Assurance:**
- `specmap-qa` - Validate compliance and quality

## Using Skills

In Claude Code, invoke a skill by name:
```
/skill specmap-reviewer
```

## Creating Custom Skills

Skills are markdown files with optional frontmatter:
```markdown
---
name: my-skill
description: What this skill does
---

# Skill Instructions

Your instructions for Claude...
```
