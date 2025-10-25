# Session Management Quick Start Guide

Get started with SpecMap's Session Management System in 5 minutes.

## What You'll Learn

- Start and manage development sessions
- Create checkpoints for your work
- Restore from backups
- Use the Claude Code skill for automation

## Prerequisites

- SpecMap installed
- Python 3.8+
- PyYAML installed (`pip install pyyaml`)

## Method 1: Automatic (Claude Code) - Recommended

### Step 1: Install the Session Manager Skill

```bash
cd your-specmap-project
specmap skill install specmap-session-manager
```

### Step 2: Activate in Claude Code

In Claude Code:
```
/skill specmap-session-manager
```

### Step 3: Start Working

Just tell Claude what you want to work on:
```
Let's work on the authentication feature
```

Claude will automatically:
- Start a session with ID `2025-10-25-session-001-authentication`
- Create organized workspace
- Track all files
- Create checkpoints
- End session when you say "wrap up"

**That's it!** Everything is automatic.

## Method 2: Manual (CLI Scripts)

### Step 1: Start a Session

```bash
python scripts/session-start.py "authentication feature" claude
```

Output:
```
Session ID: 2025-10-25-session-001-authentication
Workspace: 04-agents/sessions/active/2025-10-25-session-001-authentication/
```

### Step 2: Do Your Work

Work normally. Save files wherever they belong (src/, tests/, etc.)

### Step 3: Create Checkpoints

After completing a milestone:
```bash
python scripts/session-checkpoint.py 2025-10-25-session-001-authentication "Login implemented"
```

### Step 4: End the Session

When done:
```bash
python scripts/session-end.py 2025-10-25-session-001-authentication 8.5
```
(8.5 is the RULEMAP score)

This will:
- Archive the session
- Create a backup ZIP
- Calculate metrics

## Common Tasks

### Create a Checkpoint

**When to checkpoint:**
- After major milestone
- Before risky refactoring
- Every 30-60 minutes
- Before switching tasks

**How:**
```bash
python scripts/session-checkpoint.py <session-id> "description"
```

**Example:**
```bash
python scripts/session-checkpoint.py 2025-10-25-session-001-auth "Auth tests passing"
```

### List Active Sessions

See what sessions are currently active:

**Via Python:**
```python
from specmap.sessions import SessionManager
sm = SessionManager(".")
sessions = sm.list_active_sessions()
for s in sessions:
    print(f"{s['id']}: {s['focus']}")
```

**Via MCP (in Claude):**
```
Use session_list_active() tool
```

### Create Daily Backup

At end of day:
```bash
python scripts/backup-project.py
```

This backs up:
- Governance docs
- All specifications
- Planning docs
- Tracking files
- Session archives

Location: `04-agents/backups/daily/YYYY-MM-DD/`

### Restore from Backup

**List available backups:**
```bash
python scripts/restore-session.py --list-backups
```

**Restore a session:**
```bash
python scripts/restore-session.py --restore-backup 2025-10-25-session-001-auth
```

Restored to: `sessions/active/2025-10-25-session-001-auth-restored/`

### Restore from Checkpoint

**List checkpoints:**
```bash
python scripts/restore-session.py --list-checkpoints 2025-10-25-session-001-auth
```

**Restore specific checkpoint:**
```bash
python scripts/restore-session.py --restore-checkpoint 2025-10-25-session-001-auth checkpoint-002-16-30-00
```

## Session Workspace Tour

After starting a session, you get:

```
2025-10-25-session-001-authentication/
├── artifacts/          ← Save session-specific files here
│   ├── design-notes.md
│   └── api-draft.md
│
├── notes/             ← Scratch work and ideas
│   └── brainstorm.md
│
├── decisions/         ← Document technical decisions
│   └── jwt-vs-oauth.md
│
├── snapshots/         ← Automatic checkpoints
│   ├── checkpoint-001-15-00-00/
│   └── checkpoint-002-16-30-00/
│
├── session.yaml       ← Session metadata (auto-updated)
├── summary.md         ← Fill out at end
└── README.md          ← Session guide
```

### What Goes Where?

**Production Code** → Normal project folders (src/, tests/, etc.)
- These are your actual deliverables
- Not session-specific

**Session Artifacts** → `artifacts/`
- Design documents
- Research notes
- Temporary code experiments
- Planning documents

**Scratch Work** → `notes/`
- Ideas
- Brainstorming
- Quick notes

**Decisions** → `decisions/`
- Why you chose approach A over B
- Architecture decisions
- Trade-off analysis

## Real-World Example

### Scenario: Building User Authentication

**1. Start Session (9:00 AM)**
```bash
python scripts/session-start.py "user authentication" claude
```

**2. Work on Auth Logic (9:00 - 10:30 AM)**
- Created: `src/auth.py`
- Created: `tests/test_auth.py`
- Created: `artifacts/auth-design.md`

**3. Checkpoint After Basic Auth (10:30 AM)**
```bash
python scripts/session-checkpoint.py 2025-10-25-session-001-user-authentication "Basic auth working"
```

**4. Add OAuth Support (10:30 AM - 12:00 PM)**
- Modified: `src/auth.py`
- Created: `src/oauth.py`
- Created: `decisions/oauth-provider-choice.md`

**5. Checkpoint After OAuth (12:00 PM)**
```bash
python scripts/session-checkpoint.py 2025-10-25-session-001-user-authentication "OAuth integration complete"
```

**6. Lunch Break** (checkpoint protects your work!)

**7. Add Tests (1:00 - 3:00 PM)**
- Created: `tests/test_oauth.py`
- Modified: `tests/test_auth.py`

**8. Final Checkpoint (3:00 PM)**
```bash
python scripts/session-checkpoint.py 2025-10-25-session-001-user-authentication "All tests passing"
```

**9. End Session (3:00 PM)**
```bash
python scripts/session-end.py 2025-10-25-session-001-user-authentication 8.5
```

**Result:**
- 6 hours of work
- 5 files created
- 2 files modified
- 3 checkpoints
- Full backup created
- Session archived
- RULEMAP score: 8.5/10

If anything goes wrong, you can restore from any of the 3 checkpoints!

## Pro Tips

### 1. Descriptive Session Focus
**Good:**
```bash
python scripts/session-start.py "user authentication with OAuth" claude
```

**Bad:**
```bash
python scripts/session-start.py "coding" claude
```

### 2. Checkpoint Before Risky Changes

Before major refactoring:
```bash
python scripts/session-checkpoint.py <session-id> "Before auth refactor"
```

If it goes wrong, restore the checkpoint!

### 3. Use Claude Code Skill

Most convenient way:
```
/skill specmap-session-manager
Let's work on feature X
```

Claude handles everything automatically.

### 4. Daily Backups

Add to your end-of-day routine:
```bash
python scripts/backup-project.py
```

### 5. Document Decisions

When making important choices, document in `decisions/`:
```markdown
# JWT vs Session Tokens

Decision: Use JWT

Rationale:
- Stateless
- Scalable
- Mobile-friendly

Trade-offs:
- Can't revoke immediately
- Larger payload

Alternatives Considered:
- Session tokens (rejected: scalability)
- OAuth only (rejected: complexity)
```

## Troubleshooting

### "Session not found"

**Problem:** Can't find session ID

**Solution:**
```bash
# List all folders in active
ls 04-agents/sessions/active/

# Use the full session ID
python scripts/session-end.py 2025-10-25-session-001-authentication 8.5
```

### "Checkpoint failed"

**Problem:** Checkpoint creation errors

**Solution:**
```bash
# Create checkpoint with specific files
python scripts/session-checkpoint.py <session-id> "description" src/auth.py tests/test_auth.py
```

### "Can't restore backup"

**Problem:** Restore script errors

**Solution:**
```bash
# Check available backups
python scripts/restore-session.py --list-backups

# Verify backup exists
ls 04-agents/backups/sessions/
```

## Next Steps

1. Read full documentation: [docs/SESSION-MANAGEMENT.md](../../docs/SESSION-MANAGEMENT.md)
2. Explore workflow diagrams: [SESSION-WORKFLOW-DIAGRAM.md](SESSION-WORKFLOW-DIAGRAM.md)
3. Check MCP integration: [docs/MCP_SERVER.md](../../docs/MCP_SERVER.md)
4. Join our community: [GitHub Discussions](#)

## Cheat Sheet

```bash
# Start session
python scripts/session-start.py "feature name" claude

# Create checkpoint
python scripts/session-checkpoint.py <session-id> "description"

# End session
python scripts/session-end.py <session-id> <score>

# Daily backup
python scripts/backup-project.py

# List backups
python scripts/restore-session.py --list-backups

# Restore session
python scripts/restore-session.py --restore-backup <session-id>

# List checkpoints
python scripts/restore-session.py --list-checkpoints <session-id>

# Restore checkpoint
python scripts/restore-session.py --restore-checkpoint <session-id> <checkpoint-id>
```

## Claude Code Skill Cheat Sheet

```
# Activate skill
/skill specmap-session-manager

# Start working (automatic)
"Let's work on authentication"

# Claude creates checkpoints automatically

# End session (automatic)
"Let's wrap up for today"
```

---

**You're Ready!** Start your first session and never lose work again.

Questions? Check [docs/SESSION-MANAGEMENT.md](../../docs/SESSION-MANAGEMENT.md) or open an issue.
