# Vortxx Project - SpecMap Deployment Plan

**Custom deployment strategy for adding SpecMap skills to the Vortxx project**

**Challenge:** Vortxx project is on a different computer
**Solution:** Two-phase deployment (browser first, then local skills)

---

## Quick Overview

```
Phase 1: IMMEDIATE (From Any Computer)
└─ Use Claude.ai Browser with Custom Instructions
   └─ Setup time: 5 minutes
   └─ Access: From any device
   └─ Get: All SpecMap guidance immediately

Phase 2: ENHANCED (When at Vortxx Computer)
└─ Add Claude Code Skills to local project
   └─ Setup time: 10 minutes
   └─ Access: Local development only
   └─ Get: Full automation + session management
```

---

## Phase 1: Immediate Access (Browser-Based)

**Do this RIGHT NOW from this computer to start using SpecMap with Vortxx**

### Step 1: Create Vortxx Project on Claude.ai

1. Go to [claude.ai](https://claude.ai)
2. Click **Projects** (left sidebar)
3. Click **+ New Project**
4. Name it: **"Vortxx Development"**

### Step 2: Add Custom Instructions

Click **Project Settings** → **Custom Instructions** and add:

```markdown
# Vortxx Development with SpecMap Framework

You are helping develop the Vortxx project using the SpecMap specification-driven development framework.

## RULEMAP Framework

When reviewing specifications or planning features, use RULEMAP:

### R - ROLE & AUTHORITY
- Who owns this feature/decision?
- What authority/permissions are needed?
- Who are the decision makers?

### U - UNDERSTANDING & OBJECTIVES
- What problem are we solving?
- What are the clear, measurable goals?
- What does success look like?

### L - LOGIC & APPROACH
- How will we solve this problem?
- What's our technical approach?
- What patterns/architectures apply?

### E - ELEMENTS & CONSTRAINTS
- What resources do we need?
- What are the technical constraints?
- What dependencies exist?
- What limitations must we work within?

### M - MOOD & EXPERIENCE
- How should this feel to users?
- What's the desired user experience?
- What emotions/reactions do we want?

### A - AUDIENCE & STAKEHOLDERS
- Who are the end users?
- Who are all stakeholders?
- What are their needs/concerns?

### P - PERFORMANCE & SUCCESS
- How do we measure success?
- What are the KPIs/metrics?
- How do we validate we've succeeded?

## Your Capabilities

### When I ask for SPECIFICATION REVIEW:
1. Analyze using all 7 RULEMAP elements
2. Score each element 0-10
3. Provide overall RULEMAP score (average)
4. Highlight strengths
5. Identify gaps and provide specific improvements
6. Target: 8.0+ score before moving to implementation

### When I ask for IMPLEMENTATION PLAN:
1. Analyze technical requirements
2. Define architecture and approach
3. Break down into implementation phases
4. Identify dependencies and prerequisites
5. List potential risks and mitigations
6. Suggest testing strategy
7. Estimate complexity and timeline

### When I ask for TASK BREAKDOWN:
Create TDD (Test-Driven Development) tasks:
1. Each task starts with failing tests
2. Implement minimal code to pass tests
3. Refactor and improve
4. Each task includes:
   - Clear objective
   - Acceptance criteria
   - Test cases to write first
   - Implementation steps
   - Definition of done

### When I ask for QA/QUALITY CHECK:
1. Validate against RULEMAP framework
2. Check code quality and standards
3. Review test coverage
4. Identify potential issues
5. Suggest improvements
6. Rate overall quality

### When I ask for SESSION GUIDANCE:
1. Suggest organizing work into focused sessions
2. Recommend checkpoints for major milestones
3. Encourage documenting decisions
4. Promote iterative quality improvement

## Quality Standards

- Specifications must score >= 8.0 on RULEMAP before implementation
- All features should follow TDD approach
- Document important technical decisions
- Maintain clear traceability from spec → plan → tasks → code

## Your Role

You are a senior technical advisor using the SpecMap framework to ensure high-quality, well-specified, and well-planned development for Vortxx.

Be proactive, specific, and actionable in your guidance.
```

### Step 3: Add Vortxx Project Knowledge

In **Project Knowledge**, add files from Vortxx:

**Option A: Upload Files**
- README.md
- Architecture docs
- API documentation
- Any existing specifications

**Option B: Copy/Paste Key Info**
If you can't upload files directly:
1. Copy key documentation
2. Paste into Project Knowledge as text files
3. Name them clearly (e.g., "Vortxx Architecture")

### Step 4: Start Using SpecMap Guidance

Now you can work on Vortxx from ANY computer!

**Example conversations:**

```
Review this Vortxx feature specification using RULEMAP:

[Feature: User Authentication]
We need users to log in with email/password...
```

Or:

```
Create an implementation plan for adding OAuth to Vortxx
```

Or:

```
Generate TDD tasks for the Vortxx payment integration feature
```

Claude will respond using SpecMap framework and quality standards!

---

## Phase 2: Local Skills (When at Vortxx Computer)

**Do this when you're physically at the computer with Vortxx project**

### Prerequisites
- Claude Code Desktop installed on Vortxx computer
- Access to SpecMap repository (this repo)

### Step 1: Transfer Skills to Vortxx Computer

**Option A: Clone SpecMap Repo**
```bash
# On Vortxx computer
cd ~/projects  # or wherever you keep code
git clone https://github.com/bsifflard77/specmap-mcp.git
```

**Option B: USB/Cloud Transfer**
Copy just the `.claude/skills/` folder:
1. From this computer: Copy `specmap-mcp/.claude/skills/`
2. Put on USB drive or upload to Dropbox/Google Drive
3. On Vortxx computer: Download the folder

**Option C: Manual Recreation**
I can create a single package file you can copy/paste to recreate all skills.

### Step 2: Copy Skills to Vortxx Project

```bash
# On Vortxx computer
cd /path/to/vortxx

# Create skills folder if it doesn't exist
mkdir -p .claude/skills

# Copy skills from SpecMap
cp -r /path/to/specmap-mcp/.claude/skills/* .claude/skills/
```

**Windows version:**
```cmd
cd C:\path\to\vortxx
mkdir .claude\skills
xcopy C:\path\to\specmap-mcp\.claude\skills .claude\skills /E /I
```

### Step 3: Verify Installation

Open Vortxx in Claude Code Desktop:
```bash
code .
```

In Claude Code, try:
```
/skill specmap-reviewer
```

If it activates, you're good! If not, check troubleshooting section.

### Step 4: Optional - Add Session Management

If you want automatic file organization and backups:

1. Copy session management scripts:
```bash
# In Vortxx project root
mkdir -p scripts
cp /path/to/specmap-mcp/scripts/session-*.py scripts/
cp /path/to/specmap-mcp/scripts/backup-project.py scripts/
cp /path/to/specmap-mcp/scripts/restore-session.py scripts/
```

2. Copy session module:
```bash
# Copy the sessions.py module
cp /path/to/specmap-mcp/src/specmap/sessions.py vortxx/utils/sessions.py
# (adjust path as needed for your Vortxx structure)
```

3. Use the session manager skill:
```
/skill specmap-session-manager
Let's work on the Vortxx payment integration
```

---

## Recommended Workflow for Vortxx

### Daily Workflow with SpecMap

#### Morning (Planning)
1. Open Claude.ai → Vortxx Development Project
2. Review what you want to accomplish today
3. Create/review specifications using RULEMAP
4. Generate implementation plan
5. Generate TDD task list

#### During Development (On Vortxx Computer)
1. Open Vortxx in Claude Code Desktop
2. Activate session manager:
   ```
   /skill specmap-session-manager
   Let's work on [feature name]
   ```
3. Claude automatically:
   - Creates organized session workspace
   - Tracks all files
   - Creates checkpoints
   - Manages backups

#### During Development (Remote/Other Computer)
1. Use Claude.ai Vortxx Project
2. Get guidance and reviews
3. Copy/paste code for review
4. Document decisions in Project

#### End of Day
1. If using local skills: Claude ends session automatically
2. If using browser: Summarize work in Project chat
3. Create daily notes/decisions

### Feature Development Workflow

```
1. SPECIFY (Browser or Desktop)
   └─ "Review this Vortxx feature spec using RULEMAP"
   └─ Iterate until 8.0+ score

2. PLAN (Browser or Desktop)
   └─ "Create implementation plan for this feature"
   └─ Review architecture and approach

3. TASKS (Browser or Desktop)
   └─ "Generate TDD tasks for implementation"
   └─ Get detailed task breakdown

4. IMPLEMENT (Desktop with Skills)
   └─ /skill specmap-session-manager
   └─ Work through tasks with automatic organization

5. QA (Browser or Desktop)
   └─ "Review this implementation for quality"
   └─ Validate against spec and constitution

6. DOCUMENT (Desktop with Skills)
   └─ Session manager tracks everything
   └─ Add decisions to Project Knowledge
```

---

## File Organization for Vortxx

### Option 1: Minimal (Just Skills)
```
vortxx/
├── .claude/
│   └── skills/                    # SpecMap skills
│       ├── specmap-reviewer.md
│       ├── specmap-planner.md
│       ├── specmap-task-generator.md
│       ├── specmap-qa.md
│       ├── specmap-session-manager.md
│       └── specmap-charter-helper.md
└── [your existing Vortxx structure]
```

### Option 2: Light Structure (Skills + Sessions)
```
vortxx/
├── .claude/
│   └── skills/                    # SpecMap skills
├── docs/
│   ├── specifications/            # Feature specs
│   ├── planning/                  # Implementation plans
│   └── decisions/                 # Technical decisions
├── sessions/                      # Dev sessions (optional)
│   ├── active/
│   └── archive/
└── [your existing Vortxx structure]
```

### Option 3: Full SpecMap Structure (Maximum Power)
```
vortxx/
├── .claude/
│   └── skills/
├── 00-governance/                 # Constitution + Charter
├── 01-specifications/             # RULEMAP specs
├── 02-planning/                   # Implementation plans
├── 03-implementation/             # Dev tracking
├── 04-agents/                     # Session management
│   ├── sessions/
│   │   ├── active/
│   │   └── archive/
│   └── backups/
└── [your existing Vortxx structure]
```

**Recommendation:** Start with Option 1, add structure as needed.

---

## Transferring Skills to Vortxx Computer

Since the computers are different, here are your transfer options:

### Method 1: Git Repository (Easiest)
```bash
# This computer (where SpecMap is)
cd /path/to/specmap-mcp
git push origin main  # (already done)

# Vortxx computer
git clone https://github.com/bsifflard77/specmap-mcp.git
cd vortxx
cp -r ../specmap-mcp/.claude/skills .claude/
```

### Method 2: Cloud Transfer
1. **From this computer:**
   - Zip up `.claude/skills/` folder
   - Upload to Dropbox/Google Drive/OneDrive
2. **On Vortxx computer:**
   - Download the zip
   - Extract to `vortxx/.claude/skills/`

### Method 3: USB Drive
1. Copy `specmap-mcp/.claude/skills/` to USB
2. Move USB to Vortxx computer
3. Copy from USB to `vortxx/.claude/skills/`

### Method 4: Network Transfer
If both computers are on same network:
```bash
# From this computer
cd /path/to/specmap-mcp
# Use scp, rsync, or Windows file sharing to transfer
```

### Method 5: Self-Contained Package (No Files Needed)
I can create a **single script** that recreates all skills. You copy/paste the script and run it on Vortxx computer - it creates all skill files automatically.

Would you like me to create that self-contained package?

---

## Troubleshooting

### Skills Not Showing in Claude Code
1. Verify files are in `.claude/skills/` folder
2. Check file extensions are `.md`
3. Restart Claude Code Desktop
4. Check file format has YAML frontmatter

### Custom Instructions Not Working in Browser
1. Make sure you're in the Project (not general chat)
2. Custom Instructions are Project-specific
3. Try asking explicitly: "Review this using RULEMAP"

### Session Management Not Working
1. Verify session scripts are copied
2. Check Python path and dependencies
3. Test manually: `python scripts/session-start.py "test" claude`

---

## Next Steps

### Right Now (Phase 1)
1. [ ] Create Vortxx project on claude.ai
2. [ ] Add custom instructions (copy from above)
3. [ ] Add Vortxx project knowledge
4. [ ] Test: "Review this spec using RULEMAP"

### When at Vortxx Computer (Phase 2)
1. [ ] Transfer skills to Vortxx computer
2. [ ] Copy to `.claude/skills/` folder
3. [ ] Open in Claude Code Desktop
4. [ ] Test: `/skill specmap-reviewer`
5. [ ] Optional: Add session management

---

## Quick Reference

### Browser Commands (Phase 1)
```
Review this specification using RULEMAP:
[paste spec]

Create an implementation plan for:
[describe feature]

Generate TDD tasks for:
[describe feature]

Review this code for quality:
[paste code]
```

### Desktop Commands (Phase 2)
```
/skill specmap-reviewer
[provide spec]

/skill specmap-planner
[describe feature]

/skill specmap-task-generator
[describe feature]

/skill specmap-qa
[provide code/feature]

/skill specmap-session-manager
Let's work on [feature]
```

---

## Support

- Full guide: [SPECMAP-DEPLOYMENT-GUIDE.md](SPECMAP-DEPLOYMENT-GUIDE.md)
- Session management: [SESSION-MANAGEMENT.md](SESSION-MANAGEMENT.md)
- Skills guide: [SKILLS.md](SKILLS.md)

---

**Ready to deploy!** Start with Phase 1 (browser) today, add Phase 2 (local skills) when convenient.
