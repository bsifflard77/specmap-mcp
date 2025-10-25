# SpecMap Deployment Guide

**Complete Strategic Plan for Adding SpecMap Skills to Your Projects**

This guide shows you how to use SpecMap's powerful AI skills in your own projects, whether you're using Claude Code Desktop, Claude.ai in the browser, or integrating with the MCP server.

---

## Table of Contents

1. [Overview & Strategy](#overview--strategy)
2. [Platform Options](#platform-options)
3. [Method 1: Claude Code Desktop (Recommended)](#method-1-claude-code-desktop-recommended)
4. [Method 2: Claude.ai Browser (Projects Feature)](#method-2-claudeai-browser-projects-feature)
5. [Method 3: MCP Server Integration](#method-3-mcp-server-integration)
6. [Adding Skills to Your Own Projects](#adding-skills-to-your-own-projects)
7. [Quick Reference](#quick-reference)
8. [Troubleshooting](#troubleshooting)

---

## Overview & Strategy

### What Are SpecMap Skills?

SpecMap skills are specialized AI prompts that give Claude expert capabilities in:
- **Specification Review** (RULEMAP framework compliance)
- **Implementation Planning** (technical planning)
- **Task Generation** (TDD task breakdown)
- **Quality Assurance** (validation and scoring)
- **Session Management** (automatic file organization and backups)
- **Charter Assistance** (interactive project setup)

### Deployment Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT OPTIONS                        │
└─────────────────────────────────────────────────────────────┘

Option 1: Claude Code Desktop + Skills
├─ Best for: Local development
├─ Features: Full automation, file access, skill activation
├─ Setup time: 10 minutes
└─ Recommendation: ⭐⭐⭐⭐⭐ (BEST)

Option 2: Claude.ai Browser + Custom Instructions
├─ Best for: Quick access, any device
├─ Features: Project-specific instructions
├─ Setup time: 5 minutes
└─ Recommendation: ⭐⭐⭐ (Good for web-based work)

Option 3: MCP Server (Advanced)
├─ Best for: API integration, automation
├─ Features: Full SpecMap CLI + Session tools
├─ Setup time: 20 minutes
└─ Recommendation: ⭐⭐⭐⭐ (Advanced users)
```

---

## Platform Options

### Quick Decision Matrix

**Use Claude Code Desktop if:**
- ✅ You work on local projects
- ✅ You want automatic file organization
- ✅ You want session management
- ✅ You want the best experience

**Use Claude.ai Browser if:**
- ✅ You don't have Claude Code Desktop
- ✅ You work on web-based projects
- ✅ You want quick access from any device
- ✅ You need to share context with team

**Use MCP Server if:**
- ✅ You want full SpecMap CLI integration
- ✅ You need programmatic access
- ✅ You want session management tools
- ✅ You're comfortable with configuration

---

## Method 1: Claude Code Desktop (Recommended)

### Prerequisites
- Claude Code Desktop installed
- Your project folder

### Step-by-Step Installation

#### Step 1: Get the SpecMap Skills

**Option A: Install from this repository (if you have it)**
```bash
cd /path/to/your-project

# Copy the skills folder
cp -r /path/to/specmap-mcp/.claude/skills .claude/

# Or create .claude/skills if it doesn't exist
mkdir -p .claude/skills
```

**Option B: Manual creation (copy from templates)**
```bash
# Create skills directory
mkdir -p .claude/skills

# Copy individual skill files from specmap-mcp/.claude/skills/
# to your project's .claude/skills/
```

#### Step 2: Verify Skills Are Installed

Open your project in Claude Code Desktop:
```bash
code .
```

In Claude Code, type:
```
/help
```

You should see available skills listed (if skills are properly formatted).

#### Step 3: Activate a Skill

To use a skill:
```
/skill specmap-reviewer
```

Then provide your specification or request.

### Available Skills for Your Projects

#### 1. **specmap-reviewer** - Specification Review
**When to use:** Review specs for RULEMAP compliance

**How to use:**
```
/skill specmap-reviewer

Please review this specification:
[paste your spec]
```

**What it does:**
- Analyzes RULEMAP framework compliance
- Scores each element (R, U, L, E, M, A, P)
- Provides actionable feedback
- Suggests improvements

#### 2. **specmap-planner** - Implementation Planning
**When to use:** Generate technical implementation plans

**How to use:**
```
/skill specmap-planner

Create an implementation plan for:
[describe your feature]
```

**What it does:**
- Creates technical architecture
- Defines implementation phases
- Lists dependencies
- Estimates complexity

#### 3. **specmap-task-generator** - TDD Task Breakdown
**When to use:** Break features into TDD tasks

**How to use:**
```
/skill specmap-task-generator

Generate TDD tasks for:
[describe your feature]
```

**What it does:**
- Creates test-first task list
- Prioritizes tasks
- Defines acceptance criteria
- Follows TDD workflow

#### 4. **specmap-qa** - Quality Assurance
**When to use:** Validate code quality and compliance

**How to use:**
```
/skill specmap-qa

Review this code/feature for quality
```

**What it does:**
- Checks constitution compliance
- Validates RULEMAP scores
- Reviews code quality
- Provides improvement suggestions

#### 5. **specmap-session-manager** - Session Management
**When to use:** Automatic session organization and backups

**How to use:**
```
/skill specmap-session-manager

Let's work on the authentication feature
```

**What it does:**
- Starts organized session
- Creates checkpoints automatically
- Tracks all files
- Ends session with backup

#### 6. **specmap-charter-helper** - Project Charter
**When to use:** Set up new project governance

**How to use:**
```
/skill specmap-charter-helper

Help me complete my project charter
```

**What it does:**
- Guides through RULEMAP charter
- Asks clarifying questions
- Completes all 7 elements
- Creates governance docs

### Step 4: Create Your Project Structure (Optional)

If you want full SpecMap structure:

```bash
# Install SpecMap CLI (from specmap-mcp repo)
cd /path/to/specmap-mcp
pip install -e .

# Initialize your project with full structure
cd /path/to/your-project
specmap init . --type web-app --agent claude
```

This creates:
```
your-project/
├── .claude/skills/          # Skills installed here
├── 00-governance/          # Constitution + Charter
├── 01-specifications/      # RULEMAP specs
├── 02-planning/           # Implementation plans
├── 03-implementation/     # Dev tracking
├── 04-agents/            # Session management
├── 05-quality-assurance/ # QA validation
├── 06-documentation/     # Project docs
├── 07-project-tracking/  # Progress tracking
└── 08-deliverables/      # Final outputs
```

### Step 5: Start Using Skills

**Example Workflow:**

1. **Start a session:**
```
/skill specmap-session-manager
Let's work on user authentication
```

2. **Create specification:**
```
/skill specmap-reviewer
Review this auth spec: [paste spec]
```

3. **Generate plan:**
```
/skill specmap-planner
Create implementation plan for auth
```

4. **Generate tasks:**
```
/skill specmap-task-generator
Break down auth into TDD tasks
```

5. **Implement with guidance**

6. **Quality check:**
```
/skill specmap-qa
Review the auth implementation
```

7. **End session:**
```
Let's wrap up for today
```
(Session manager handles it automatically)

---

## Method 2: Claude.ai Browser (Projects Feature)

Claude.ai doesn't support the `/skill` command, but you can use **Projects** with **Custom Instructions** to get similar functionality.

### Step 1: Create a Project

1. Go to [claude.ai](https://claude.ai)
2. Click **Projects** (left sidebar)
3. Click **+ New Project**
4. Name it: "My Project with SpecMap"

### Step 2: Add Custom Instructions

Click on **Project Settings** → **Custom Instructions**

**For Specification Review:**
```markdown
# SpecMap Reviewer Role

You are a specification reviewer using the RULEMAP framework.

When I ask you to review a specification, analyze it using:
- R - ROLE & AUTHORITY: Who owns and decides
- U - UNDERSTANDING & OBJECTIVES: What problem we're solving
- L - LOGIC & APPROACH: How we'll solve it
- E - ELEMENTS & CONSTRAINTS: What we need and limits
- M - MOOD & EXPERIENCE: How it should feel
- A - AUDIENCE & STAKEHOLDERS: Who it's for
- P - PERFORMANCE & SUCCESS: How we measure success

Score each element 0-10. Provide specific, actionable feedback.
Highlight strengths and areas for improvement.
```

**For Implementation Planning:**
```markdown
# SpecMap Planner Role

When I ask for an implementation plan:
1. Analyze technical requirements
2. Define architecture and approach
3. Break down into phases
4. Identify dependencies
5. Estimate complexity
6. List potential risks
7. Suggest testing strategy

Format as a structured plan with clear sections.
```

**For Task Generation:**
```markdown
# SpecMap Task Generator Role

When I ask for tasks, create a TDD (Test-Driven Development) breakdown:
1. Start with failing tests
2. Implement minimal code to pass
3. Refactor and improve

Each task should have:
- Clear objective
- Acceptance criteria
- Test cases to write
- Implementation steps
- Definition of done
```

### Step 3: Add Project Knowledge

In the **Project Knowledge** section, add:

1. **Your project's constitution** (if you have one)
2. **RULEMAP framework guide** (copy from specmap-mcp/docs/RULEMAP.md)
3. **Your project's context** (README, architecture docs)

### Step 4: Use in Conversations

In the project chat:
```
Review this specification using RULEMAP:
[paste your spec]
```

Or:
```
Create an implementation plan for user authentication
```

The custom instructions guide Claude's behavior within that project.

### Advantages of Browser Method
- ✅ Works from any device
- ✅ Easy to share with team (share project)
- ✅ No installation required
- ✅ Project-specific context

### Limitations
- ❌ No `/skill` command
- ❌ No automatic file organization
- ❌ No session management
- ❌ Must copy/paste files manually

---

## Method 3: MCP Server Integration

For advanced users who want full SpecMap CLI integration.

### Prerequisites
- Claude Desktop app (not Claude Code)
- Python 3.8+
- SpecMap MCP server

### Step 1: Install SpecMap

```bash
cd /path/to/specmap-mcp

# Install the CLI
pip install -e .

# Install MCP server dependencies
cd mcp-server
pip install -e .
```

### Step 2: Configure Claude Desktop

Find your Claude Desktop config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add SpecMap MCP server:
```json
{
  "mcpServers": {
    "specmap": {
      "command": "python",
      "args": ["-m", "specmap_mcp.server"],
      "cwd": "/path/to/specmap-mcp/mcp-server"
    }
  }
}
```

**Windows example:**
```json
{
  "mcpServers": {
    "specmap": {
      "command": "python",
      "args": ["-m", "specmap_mcp.server"],
      "cwd": "d:\\Monomoy Strategies\\Projects\\specmap-mcp\\mcp-server"
    }
  }
}
```

### Step 3: Restart Claude Desktop

Restart the Claude Desktop app completely.

### Step 4: Verify MCP Connection

In Claude Desktop, you should see the MCP tools available (look for a tools icon or mention of available tools).

### Available MCP Tools

**Project Management:**
- `specmap_init()` - Initialize project
- `specmap_status()` - Get project status

**Specification Workflow:**
- `specmap_specify()` - Create specification
- `specmap_clarify()` - Run clarification
- `specmap_plan()` - Generate plan
- `specmap_tasks()` - Create tasks

**Session Management:**
- `session_start()` - Start new session
- `session_checkpoint()` - Create checkpoint
- `session_track_artifact()` - Track files
- `session_end()` - End and archive
- `session_list_active()` - List sessions
- `create_daily_backup()` - Daily backup

**Skills Management:**
- `get_skill_templates()` - List templates
- `install_specmap_skill_template()` - Install skill
- `create_claude_skill()` - Create custom skill
- `list_claude_skills()` - List skills

### Step 5: Use MCP Tools

In Claude Desktop:
```
Use the session_start tool to start a new development session focused on "user authentication"
```

Claude will automatically use the MCP tool.

### Advantages of MCP Method
- ✅ Full SpecMap CLI integration
- ✅ Programmatic access to all features
- ✅ Session management tools
- ✅ Skills can be installed via tools

### Limitations
- ❌ More complex setup
- ❌ Requires Claude Desktop (not Claude Code)
- ❌ Configuration file editing

---

## Adding Skills to Your Own Projects

### Minimal Setup (Just Skills)

If you just want the skills without the full SpecMap structure:

#### Step 1: Create Skills Folder
```bash
cd /path/to/your-project
mkdir -p .claude/skills
```

#### Step 2: Copy Skill Files

From the specmap-mcp repository, copy these files:
```
specmap-mcp/.claude/skills/
├── specmap-reviewer.md
├── specmap-planner.md
├── specmap-task-generator.md
├── specmap-qa.md
├── specmap-session-manager.md
└── specmap-charter-helper.md
```

To your project:
```
your-project/.claude/skills/
```

#### Step 3: Use in Claude Code

```
/skill specmap-reviewer
```

### Full Setup (SpecMap Structure + Skills)

If you want the complete SpecMap workflow:

#### Step 1: Install SpecMap CLI
```bash
cd /path/to/specmap-mcp
pip install -e .
```

#### Step 2: Initialize Your Project
```bash
cd /path/to/your-project
specmap init . --type web-app --agent claude
```

#### Step 3: Install Skills
```bash
specmap skill install-all
```

This installs all 6 SpecMap skills to `.claude/skills/`

#### Step 4: Set Up Governance (Optional)

Complete your project charter:
```bash
specmap charter --complete
```

Or use the skill:
```
/skill specmap-charter-helper
```

#### Step 5: Start Your Workflow

1. Create specification:
```bash
specmap specify "User authentication with OAuth"
```

2. Review with skill:
```
/skill specmap-reviewer
Please review 01-specifications/features/001-user-authentication/spec.md
```

3. Generate plan:
```
/skill specmap-planner
Create implementation plan for the auth spec
```

4. Generate tasks:
```
/skill specmap-task-generator
Create TDD tasks for auth implementation
```

5. Implement with session management:
```
/skill specmap-session-manager
Let's implement the auth tasks
```

---

## Quick Reference

### Claude Code Desktop - Skill Commands

```bash
# Activate a skill
/skill specmap-reviewer

# Deactivate
/skill off

# List skills (if available)
/help
```

### SpecMap CLI Commands

```bash
# Initialize project
specmap init <name> --type <type> --agent claude

# Install skills
specmap skill install-all
specmap skill install specmap-reviewer
specmap skill list

# Create specification
specmap specify "Feature description"

# Workflow
specmap clarify
specmap plan
specmap tasks
specmap status
```

### Session Management Scripts

```bash
# Start session
python scripts/session-start.py "feature name" claude

# Create checkpoint
python scripts/session-checkpoint.py <session-id> "description"

# End session
python scripts/session-end.py <session-id> <score>

# Daily backup
python scripts/backup-project.py
```

---

## Troubleshooting

### Skills Not Showing in Claude Code

**Problem:** `/skill` command doesn't show your skills

**Solutions:**
1. Verify files are in `.claude/skills/` folder
2. Check file format (must be `.md` with YAML frontmatter)
3. Restart Claude Code
4. Check skill file structure:
```markdown
---
name: skill-name
description: What it does
---

# Skill content here
```

### MCP Server Not Connecting

**Problem:** Tools not available in Claude Desktop

**Solutions:**
1. Verify config file location:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Check Python path in config is correct
3. Verify `cwd` path points to `mcp-server` folder
4. Test MCP server manually:
```bash
cd /path/to/specmap-mcp/mcp-server
python -m specmap_mcp.server
```
5. Restart Claude Desktop completely

### Permission Errors

**Problem:** Can't create folders or files

**Solutions:**
1. Check folder permissions
2. Run with appropriate permissions
3. Verify you're in the correct directory

### Skills Not Working in Browser

**Problem:** Claude.ai doesn't recognize `/skill`

**Solution:** Use Custom Instructions in Projects instead (see Method 2)

---

## Best Practices

### For Claude Code Desktop Users

1. **Use Session Manager Skill** for all development work
   - Automatic file organization
   - Checkpoints protect your work
   - Complete session history

2. **Start with Charter Helper** for new projects
   - Establishes governance
   - Creates constitution
   - Sets quality standards

3. **Review Specs Before Planning**
   - Use specmap-reviewer skill
   - Achieve 8.0+ RULEMAP score
   - Iterate until quality threshold met

4. **Plan Before Coding**
   - Use specmap-planner for architecture
   - Use specmap-task-generator for tasks
   - Follow TDD workflow

5. **Regular QA Checks**
   - Use specmap-qa during development
   - Validate against constitution
   - Maintain quality standards

### For Browser Users

1. **Set Up Projects** for each major effort
   - One project per feature/initiative
   - Add custom instructions
   - Include relevant context

2. **Copy Project Knowledge** from your repository
   - Constitution
   - Specifications
   - Architecture docs

3. **Maintain Context** in conversations
   - Reference previous discussions
   - Link to relevant files
   - Keep scope focused

### For All Users

1. **Document Decisions** as you work
   - Why you chose approach A over B
   - Trade-offs considered
   - Rationale for key choices

2. **Regular Backups**
   - Daily project backups
   - Checkpoint before major changes
   - Archive completed work

3. **Iterate on Quality**
   - Don't settle for first draft
   - Use RULEMAP scoring
   - Aim for 8.0+ threshold

---

## Next Steps

### New to SpecMap?
1. Start with Method 1 (Claude Code Desktop)
2. Install just 1-2 skills initially
3. Try the session manager skill
4. Expand as you get comfortable

### Ready to Go Full SpecMap?
1. Install SpecMap CLI
2. Initialize your project
3. Install all skills
4. Set up MCP server (optional)
5. Complete project charter
6. Start specification workflow

### Want to Share with Team?
1. Use Claude.ai Projects (Method 2)
2. Share custom instructions
3. Add project knowledge
4. Invite team members to project

---

## Support & Resources

- **Full Documentation**: [docs/](.)
- **Session Management**: [SESSION-MANAGEMENT.md](SESSION-MANAGEMENT.md)
- **Quick Start**: [SESSION-QUICKSTART-GUIDE.md](SESSION-QUICKSTART-GUIDE.md)
- **Workflow Diagrams**: [SESSION-WORKFLOW-DIAGRAM.md](SESSION-WORKFLOW-DIAGRAM.md)
- **Skills Guide**: [SKILLS.md](SKILLS.md)
- **MCP Server**: [MCP_SERVER.md](MCP_SERVER.md)

---

## Summary

**Fastest Start:** Copy skills to `.claude/skills/` in Claude Code Desktop

**Most Powerful:** Full SpecMap CLI + MCP server + Skills

**Most Accessible:** Claude.ai Projects with Custom Instructions

Choose the method that fits your workflow and scale up as needed!

---

**Built with Claude Code** - AI-powered specification-driven development
