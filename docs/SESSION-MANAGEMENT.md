# Session Management & Backup System

Complete guide to SpecMap's automated session management, file organization, and backup strategy.

## Overview

The Session Management System ensures that every development session is:
- **Organized**: Consistent folder structure and naming
- **Tracked**: Complete metadata and artifact tracking
- **Backed up**: Automatic backups at session boundaries
- **Recoverable**: Restore from any checkpoint or backup

## Why Session Management?

**The Problem**: Without session management, Claude Code creates files in random locations, work gets disorganized, and there's no consistent backup strategy.

**The Solution**: Automated session lifecycle with organized workspaces, checkpoint snapshots, and automatic backups.

## Architecture

### Folder Structure

```
04-agents/
├── sessions/
│   ├── active/                    # Current sessions
│   │   └── YYYY-MM-DD-session-NNN-focus/
│   │       ├── artifacts/         # Files created
│   │       ├── notes/             # Scratch work
│   │       ├── decisions/         # Technical decisions
│   │       ├── snapshots/         # Checkpoints
│   │       ├── session.yaml       # Metadata
│   │       ├── summary.md         # Session summary
│   │       └── README.md          # Session guide
│   └── archive/                   # Completed sessions
│       └── YYYY-MM-DD-session-NNN-focus/
├── backups/
│   ├── sessions/                  # Per-session backups
│   │   └── YYYY-MM-DD-session-NNN-focus-backup.zip
│   ├── daily/                     # Daily project backups
│   │   └── YYYY-MM-DD/
│   │       └── manifest.json
│   └── milestones/                # Milestone backups
└── session-summaries/             # Session logs
    └── YYYY-MM-DD.md
```

### Session Naming Convention

**Format**: `YYYY-MM-DD-session-NNN-focus`

**Examples**:
- `2025-10-25-session-001-authentication`
- `2025-10-25-session-002-api-design`
- `2025-10-26-session-001-testing`

**Components**:
- `YYYY-MM-DD`: Date
- `session-NNN`: Sequential number for the day (001, 002, ...)
- `focus`: Brief description of session focus (sanitized, max 30 chars)

## Session Lifecycle

### 1. Start Session

**When**: Beginning of work session

**How**:

**Via Claude Code Skill**:
```
User: "Let's start working on the authentication feature"

Claude (using specmap-session-manager skill):
Uses MCP tool: session_start(project_path, "authentication feature", "claude")

Response:
✅ Session started: 2025-10-25-session-001-authentication
📁 Workspace: 04-agents/sessions/active/2025-10-25-session-001-authentication/
🎯 Focus: Authentication feature
🤖 Agent: Claude
```

**Via CLI**:
```bash
python scripts/session-start.py "authentication feature" claude
```

**Via MCP**:
```python
session_start(
    project_path="/path/to/project",
    focus="authentication feature",
    agent="claude"
)
```

**Creates**:
- Session workspace folder
- `artifacts/`, `notes/`, `decisions/`, `snapshots/` folders
- `session.yaml` metadata file
- `summary.md` template
- `README.md` guide

### 2. During Session

**File Organization**:

**ALWAYS**:
- Save production code to appropriate project folders (src/, etc.)
- Save session-specific files to session workspace
- Document decisions in `decisions/`
- Keep scratch notes in `notes/`

**Checkpoint Creation**:

Create checkpoints:
- After major milestones
- Before risky changes
- Every 30-60 minutes
- Before refactoring

**Via Claude Code Skill**:
```
Claude automatically creates checkpoints and announces:
💾 Checkpoint created: "Authentication logic implemented"
📁 Files snapshotted: auth.py, test_auth.py
```

**Via CLI**:
```bash
python scripts/session-checkpoint.py 2025-10-25-session-001 "Auth implemented"
```

**Via MCP**:
```python
session_checkpoint(
    project_path="/path/to/project",
    session_id="2025-10-25-session-001-authentication",
    description="Auth logic implemented",
    files_to_snapshot=["src/auth.py", "tests/test_auth.py"]
)
```

**Artifact Tracking**:

Track all files created/modified:

```python
session_track_artifact(
    project_path="/path/to/project",
    session_id="2025-10-25-session-001-authentication",
    file_path="src/auth.py",
    action="created"  # or "modified"
)
```

### 3. End Session

**When**: Finishing work for the day

**How**:

**Via Claude Code Skill**:
```
User: "Let's wrap up for today"

Claude (using specmap-session-manager skill):
- Completes session summary
- Requests RULEMAP score
- Uses: session_end(session_id, rulemap_score)
- Archives session
- Creates backup
- Updates TRACKING.md

Response:
✅ Session completed: 2025-10-25-session-001-authentication
📊 Duration: 125 minutes
📁 Files created: 5
📝 Files modified: 3
💾 Checkpoints: 3
🎯 RULEMAP Score: 8.5/10
📦 Backup: 04-agents/backups/sessions/2025-10-25-session-001-authentication-backup.zip
```

**Via CLI**:
```bash
python scripts/session-end.py 2025-10-25-session-001-authentication 8.5
```

**Via MCP**:
```python
session_end(
    project_path="/path/to/project",
    session_id="2025-10-25-session-001-authentication",
    rulemap_score=8.5,
    create_backup=True
)
```

**Actions**:
- Finalizes session metadata
- Calculates duration and metrics
- Archives session to `sessions/archive/`
- Creates ZIP backup in `backups/sessions/`
- Updates project tracking

## Session Metadata

Each session has a `session.yaml` file:

```yaml
session:
  id: "2025-10-25-session-001-authentication"
  date: "2025-10-25"
  start_time: "14:30:00"
  end_time: "18:45:00"
  focus: "Authentication feature"
  agent: "claude"
  status: "completed"

artifacts:
  created:
    - "src/auth.py"
    - "src/auth_utils.py"
    - "tests/test_auth.py"
  modified:
    - "src/main.py"
    - "docs/API.md"

checkpoints:
  - id: "checkpoint-001-15-00-00"
    time: "15:00:00"
    description: "Auth logic implemented"
    files_snapshot:
      - "src/auth.py"
      - "tests/test_auth.py"
  - id: "checkpoint-002-16-30-00"
    time: "16:30:00"
    description: "Tests passing"
    files_snapshot:
      - "tests/test_auth.py"

metrics:
  duration_minutes: 255
  files_created: 3
  files_modified: 2
  checkpoints: 2

rulemap_score: 8.5
```

## Backup Strategy

### Session Backups (Automatic)

**When**: Session ends

**What**: Complete session workspace

**Format**: ZIP archive

**Location**: `04-agents/backups/sessions/`

**Naming**: `{session-id}-backup.zip`

**Contains**:
- All artifacts
- All notes
- All decisions
- All checkpoints
- session.yaml
- summary.md

### Daily Backups (Manual/Scheduled)

**When**: End of day or on demand

**What**: Entire project state

**Via CLI**:
```bash
python scripts/backup-project.py
```

**Via MCP**:
```python
create_daily_backup(project_path="/path/to/project")
```

**Location**: `04-agents/backups/daily/YYYY-MM-DD/`

**Backs up**:
- `00-governance/` (constitution, charter)
- `01-specifications/` (all specs)
- `02-planning/` (plans)
- `03-implementation/` (tracking)
- `04-agents/session-summaries/`
- `04-agents/sessions/archive/`
- `TRACKING.md`
- `PROJECT-STATUS.md`

**Creates manifest**:
```json
{
  "date": "2025-10-25",
  "timestamp": "2025-10-25T18:45:00",
  "items_backed_up": [
    "00-governance",
    "01-specifications",
    ...
  ],
  "backup_path": "04-agents/backups/daily/2025-10-25"
}
```

### Milestone Backups (Manual)

**When**: Major achievements

**What**: Full project snapshot

**How**: Create with custom name
```bash
# Future: python scripts/backup-milestone.py "v1.0-release"
```

**Location**: `04-agents/backups/milestones/`

## Recovery & Restore

### Restore from Session Backup

**List available backups**:
```bash
python scripts/restore-session.py --list-backups
```

**Restore session**:
```bash
python scripts/restore-session.py --restore-backup 2025-10-25-session-001-authentication
```

**Result**: Session restored to `sessions/active/{session-id}-restored/`

### Restore from Checkpoint

**List checkpoints for session**:
```bash
python scripts/restore-session.py --list-checkpoints 2025-10-25-session-001-authentication
```

**Restore checkpoint**:
```bash
python scripts/restore-session.py --restore-checkpoint 2025-10-25-session-001-authentication checkpoint-002-16-30-00
```

**Result**: Checkpoint files restored to `sessions/active/{session-id}-{checkpoint-id}-restored/`

## Claude Code Integration

### specmap-session-manager Skill

The `specmap-session-manager` skill automates the entire session lifecycle.

**Installation**:
```bash
specmap skill install specmap-session-manager
```

**Activation**:
```
/skill specmap-session-manager
```

**Behavior**:

**Automatic**:
- Starts session when user begins work
- Creates checkpoints at appropriate times
- Tracks all file operations
- Ends session and creates backup when requested

**Proactive**:
- Announces session start
- Confirms checkpoint creation
- Reports file organization
- Summarizes at session end

**Example Session**:
```
User: "Let's work on the authentication feature"

Claude (with specmap-session-manager):
✅ Session started: 2025-10-25-session-001-authentication
📁 Workspace: 04-agents/sessions/active/2025-10-25-session-001-authentication/
🎯 Focus: Authentication feature

I'll organize all our work automatically. Let's begin!

[Work happens... Claude creates auth.py]

Claude:
✅ Tracked: src/auth.py (created)

[30 minutes later]

Claude:
💾 Checkpoint created: "Authentication logic implemented"
📁 Files snapshotted: src/auth.py, tests/test_auth.py

[More work...]

User: "Let's wrap up for today"

Claude:
Completing session summary...

✅ Session completed: 2025-10-25-session-001-authentication
📊 Duration: 125 minutes
📁 Files created: 5
📝 Files modified: 3
💾 Checkpoints: 3
🎯 RULEMAP Score: 8.5/10
📦 Backup: 04-agents/backups/sessions/2025-10-25-session-001-authentication-backup.zip

Great work today! All files are organized and backed up.
```

## MCP Tools Reference

### session_start

Start a new session.

**Parameters**:
- `project_path` (str): Project root path
- `focus` (str): Session focus description
- `agent` (str): AI agent name (default: "claude")
- `metadata` (dict, optional): Additional metadata

**Returns**: Session details with workspace paths

### session_checkpoint

Create checkpoint snapshot.

**Parameters**:
- `project_path` (str): Project root path
- `session_id` (str): Session ID
- `description` (str): Checkpoint description
- `files_to_snapshot` (list, optional): Specific files to snapshot

**Returns**: Checkpoint details

### session_track_artifact

Track file artifact.

**Parameters**:
- `project_path` (str): Project root path
- `session_id` (str): Session ID
- `file_path` (str): File path relative to project root
- `action` (str): "created" or "modified"

**Returns**: Tracking confirmation

### session_end

End and archive session.

**Parameters**:
- `project_path` (str): Project root path
- `session_id` (str): Session ID
- `rulemap_score` (float, optional): RULEMAP score 0-10
- `create_backup` (bool): Create backup (default: True)

**Returns**: Archival details and summary

### session_list_active

List active sessions.

**Parameters**:
- `project_path` (str): Project root path

**Returns**: List of active sessions

### create_daily_backup

Create daily project backup.

**Parameters**:
- `project_path` (str): Project root path

**Returns**: Backup details with manifest

## CLI Scripts Reference

### session-start.py

Start new session.

```bash
python scripts/session-start.py <focus> [agent]
```

**Example**:
```bash
python scripts/session-start.py "authentication feature" claude
```

### session-checkpoint.py

Create checkpoint.

```bash
python scripts/session-checkpoint.py <session-id> <description> [files...]
```

**Example**:
```bash
python scripts/session-checkpoint.py 2025-10-25-session-001 "Auth implemented"
python scripts/session-checkpoint.py 2025-10-25-session-001 "Bug fix" src/auth.py
```

### session-end.py

End session.

```bash
python scripts/session-end.py <session-id> [rulemap-score]
```

**Example**:
```bash
python scripts/session-end.py 2025-10-25-session-001-authentication 8.5
```

### backup-project.py

Create daily backup.

```bash
python scripts/backup-project.py
```

### restore-session.py

Restore from backup or checkpoint.

```bash
# List backups
python scripts/restore-session.py --list-backups

# Restore backup
python scripts/restore-session.py --restore-backup <session-id>

# List checkpoints
python scripts/restore-session.py --list-checkpoints <session-id>

# Restore checkpoint
python scripts/restore-session.py --restore-checkpoint <session-id> <checkpoint-id>
```

## Best Practices

### Session Organization

**DO**:
- Start a session at beginning of work
- Use descriptive focus names
- Create checkpoints frequently
- Track all file operations
- Complete session summary at end
- Calculate honest RULEMAP score

**DON'T**:
- Skip session start/end
- Create files outside workspace
- Forget checkpoint creation
- Leave session summary incomplete
- Skip backups

### Checkpoint Strategy

Create checkpoints:
- ✅ After completing a feature
- ✅ Before refactoring
- ✅ After fixing bugs
- ✅ Every 30-60 minutes
- ✅ Before risky operations
- ✅ Before switching tasks

### Backup Hygiene

**Session backups**: Automatic on session end

**Daily backups**: Run at end of each day
```bash
python scripts/backup-project.py
```

**Before major changes**: Create checkpoint
```bash
python scripts/session-checkpoint.py <session-id> "Before major refactor"
```

## Troubleshooting

### Session Not Found

**Symptom**: "Session not found" error

**Solution**: List active sessions
```bash
# Via MCP
session_list_active(project_path="/path/to/project")

# Or check directory
ls 04-agents/sessions/active/
```

### Checkpoint Failed

**Symptom**: Checkpoint creation fails

**Solution**:
1. Verify session is active
2. Check file paths are valid
3. Try with fewer files

### Backup Failed

**Symptom**: Backup creation fails

**Solution**:
1. Check disk space
2. Verify permissions
3. Create manual backup:
   ```bash
   # Copy session manually
   cp -r 04-agents/sessions/active/session-id backups/manual/
   ```

### Lost Session Work

**Symptom**: Need to recover lost work

**Solution**: Restore from most recent checkpoint
```bash
python scripts/restore-session.py --list-checkpoints <session-id>
python scripts/restore-session.py --restore-checkpoint <session-id> <checkpoint-id>
```

## Integration with SpecMap Workflow

Session management integrates with the complete SpecMap workflow:

1. **Project Init**: Creates session folders
2. **Specify**: Work organized in specification session
3. **Plan**: Planning work tracked in planning session
4. **Implement**: Implementation work in dev sessions
5. **QA**: QA work tracked in validation sessions

All sessions are:
- Organized consistently
- Tracked in metadata
- Backed up automatically
- Linked to TRACKING.md

## Related Documentation

- [SpecMap CLI Reference](CLI.md)
- [MCP Server API](MCP_SERVER.md)
- [Skills Guide](SKILLS.md)
- [Session Summaries README](../session-summaries/README.md)
- [TRACKING System](../TRACKING.md)

## Support

If you encounter issues:
1. Check session status: `session_list_active()`
2. Review session metadata: `cat 04-agents/sessions/active/{session-id}/session.yaml`
3. List backups: `python scripts/restore-session.py --list-backups`
4. Restore from checkpoint if needed

## Future Enhancements

Planned features:
- [ ] Milestone backup automation
- [ ] Session analytics dashboard
- [ ] Automatic session merge
- [ ] Session templates
- [ ] Multi-user session support
- [ ] Cloud backup integration
- [ ] Session replay/review mode

---

**Session Management System**: v1.0.0
**Status**: Active
**Maintenance**: Monomoy Strategies
