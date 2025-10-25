# Session Management Workflow Diagram

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    SESSION LIFECYCLE                             │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐
│  USER BEGINS │
│     WORK     │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│  SESSION START                                                │
│  ─────────────                                                │
│  • Generate session ID: YYYY-MM-DD-session-NNN-focus         │
│  • Create workspace folder structure                          │
│  • Initialize session.yaml metadata                          │
│  • Create summary.md template                                │
│                                                               │
│  Created:                                                     │
│    04-agents/sessions/active/2025-10-25-session-001-auth/   │
│    ├── artifacts/                                            │
│    ├── notes/                                                │
│    ├── decisions/                                            │
│    ├── snapshots/                                            │
│    ├── session.yaml                                          │
│    ├── summary.md                                            │
│    └── README.md                                             │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│  DURING SESSION                                               │
│  ──────────────                                               │
│                                                               │
│  ┌─────────────────┐    ┌──────────────────┐                │
│  │  Create Files   │    │  Track Artifacts │                │
│  │                 │───▶│                  │                │
│  │  • Code files   │    │  session.yaml:   │                │
│  │  • Docs         │    │    artifacts:    │                │
│  │  • Tests        │    │      created: [] │                │
│  │  • Notes        │    │      modified:[] │                │
│  └─────────────────┘    └──────────────────┘                │
│                                                               │
│  ┌──────────────────────────────────────────┐               │
│  │  CHECKPOINT TRIGGERS:                     │               │
│  │  • After major milestone                 │               │
│  │  • Before risky change                   │               │
│  │  • Every 30-60 minutes                   │               │
│  │  • User request                          │               │
│  └──────────────┬───────────────────────────┘               │
│                 │                                            │
│                 ▼                                            │
│  ┌──────────────────────────────────────────┐               │
│  │  CREATE CHECKPOINT                        │               │
│  │  ─────────────────                        │               │
│  │  1. Generate checkpoint ID                │               │
│  │  2. Copy artifacts to snapshots/          │               │
│  │  3. Update session.yaml                   │               │
│  │                                            │               │
│  │  snapshots/checkpoint-001-15-30-00/       │               │
│  │    ├── file1.py                           │               │
│  │    ├── file2.md                           │               │
│  │    └── ...                                │               │
│  └──────────────────────────────────────────┘               │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       │ User says "wrap up" or "end session"
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│  SESSION END                                                  │
│  ───────────                                                  │
│  1. Complete session.yaml:                                   │
│     • end_time                                               │
│     • duration_minutes                                       │
│     • metrics (files created/modified, checkpoints)          │
│     • RULEMAP score                                          │
│                                                               │
│  2. Create ZIP backup:                                       │
│     04-agents/backups/sessions/                              │
│       └── 2025-10-25-session-001-auth-backup.zip            │
│                                                               │
│  3. Move to archive:                                         │
│     04-agents/sessions/archive/                              │
│       └── 2025-10-25-session-001-auth/                      │
│                                                               │
│  4. Update TRACKING.md (optional)                            │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │  SESSION END   │
              │   COMPLETE     │
              └────────────────┘
```

## Backup Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                    BACKUP ARCHITECTURE                           │
└─────────────────────────────────────────────────────────────────┘

04-agents/backups/
│
├── sessions/               ← SESSION BACKUPS (Automatic)
│   │                         Created: On session end
│   │                         Format: ZIP archive
│   │
│   ├── 2025-10-25-session-001-auth-backup.zip
│   ├── 2025-10-25-session-002-ui-backup.zip
│   └── 2025-10-26-session-001-api-backup.zip
│
├── daily/                  ← DAILY BACKUPS (Manual)
│   │                         Created: End of day
│   │                         Content: Project state
│   │
│   ├── 2025-10-25/
│   │   ├── 00-governance/
│   │   ├── 01-specifications/
│   │   ├── 02-planning/
│   │   ├── TRACKING.md
│   │   └── manifest.json
│   │
│   └── 2025-10-26/
│       └── ...
│
└── milestones/             ← MILESTONE BACKUPS (Manual)
    │                         Created: Major achievements
    │                         Content: Full project snapshot
    │
    ├── v1.0-release/
    ├── beta-launch/
    └── production-ready/
```

## Recovery Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    RECOVERY SCENARIOS                            │
└─────────────────────────────────────────────────────────────────┘

SCENARIO 1: Need to restore recent work
┌──────────────────┐
│  List Backups    │
│  ──────────────  │
│  $ restore-      │
│    session.py    │
│    --list-       │
│    backups       │
└────────┬─────────┘
         │
         ▼
┌─────────────────────────┐
│  Choose Session Backup  │
└────────┬────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Restore Session                 │
│  $ restore-session.py            │
│    --restore-backup              │
│    2025-10-25-session-001        │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────┐
│  Files Restored to:  │
│  sessions/active/    │
│  ...-restored/       │
└──────────────────────┘

SCENARIO 2: Need specific checkpoint version
┌──────────────────────┐
│  List Checkpoints    │
│  ────────────────    │
│  $ restore-          │
│    session.py        │
│    --list-           │
│    checkpoints       │
│    <session-id>      │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────────┐
│  Choose Checkpoint       │
│  checkpoint-002-16-30-00 │
└────────┬─────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│  Restore Checkpoint                │
│  $ restore-session.py              │
│    --restore-checkpoint            │
│    <session-id>                    │
│    checkpoint-002-16-30-00         │
└────────┬───────────────────────────┘
         │
         ▼
┌──────────────────────┐
│  Files Restored to:  │
│  sessions/active/    │
│  ...-checkpoint-...  │
│  -restored/          │
└──────────────────────┘
```

## Integration Points

```
┌─────────────────────────────────────────────────────────────────┐
│              SESSION MANAGEMENT INTEGRATION                      │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│  CLAUDE CODE │         │  CLI SCRIPTS │         │  MCP SERVER  │
│              │         │              │         │              │
│  /skill      │         │  python      │         │  session_    │
│  specmap-    │◄───────▶│  scripts/    │◄───────▶│  start()     │
│  session-    │         │  session-*.py│         │              │
│  manager     │         │              │         │  session_    │
│              │         │              │         │  checkpoint()│
│  Auto mode   │         │  Manual mode │         │              │
│  • Starts    │         │  • Direct    │         │  API mode    │
│  • Tracks    │         │    control   │         │  • Program-  │
│  • Ends      │         │  • Scripts   │         │    matic     │
│              │         │              │         │              │
└──────────────┘         └──────────────┘         └──────────────┘
       │                        │                        │
       │                        │                        │
       └────────────────────────┼────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  SESSION MANAGER      │
                    │  ────────────────     │
                    │  src/specmap/         │
                    │  sessions.py          │
                    │                       │
                    │  Core API:            │
                    │  • start_session()    │
                    │  • create_checkpoint()│
                    │  • track_artifact()   │
                    │  • end_session()      │
                    │  • list_active()      │
                    │  • daily_backup()     │
                    └───────────────────────┘
```

## Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              WHEN TO USE WHAT                                    │
└─────────────────────────────────────────────────────────────────┘

Starting a session?
│
├─ Using Claude Code? ──────────────────▶ /skill specmap-session-manager
│                                         (Automatic)
│
├─ Want manual control? ────────────────▶ python scripts/session-start.py
│                                         (CLI)
│
└─ Building automation? ────────────────▶ session_start() MCP tool
                                          (API)

During session?
│
├─ Major milestone reached? ────────────▶ Create checkpoint
│                                         (Auto with skill, or manual)
│
├─ Before risky change? ────────────────▶ Create checkpoint
│                                         (Manual recommended)
│
└─ 30-60 min passed? ───────────────────▶ Create checkpoint
                                          (Auto with skill)

Ending session?
│
├─ Using Claude Code? ──────────────────▶ Tell Claude "wrap up"
│                                         (Skill handles it)
│
└─ Manual control? ─────────────────────▶ python scripts/session-end.py
                                          (CLI)

Recovery needed?
│
├─ Recent work lost? ───────────────────▶ Restore from session backup
│                                         (Last complete state)
│
├─ Need specific version? ──────────────▶ Restore from checkpoint
│                                         (Specific point in time)
│
└─ Full project recovery? ──────────────▶ Restore from daily backup
                                          (Full project state)
```

## Best Practices Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    BEST PRACTICES                                │
└─────────────────────────────────────────────────────────────────┘

Daily Workflow:
──────────────

Morning:
  1. Start new session ──▶ Clear focus area
  2. Review yesterday  ──▶ Check archive

During Work:
  3. Create checkpoints ──▶ Every 30-60 min
  4. Document decisions ──▶ Save to decisions/
  5. Track all files ────▶ Automatic with skill

End of Day:
  6. End session ────────▶ With RULEMAP score
  7. Daily backup ───────▶ Run backup-project.py
  8. Review summary ─────▶ Check session.yaml

Weekly:
  9. Review archives ────▶ Learn from past sessions
  10. Cleanup old backups ─▶ Archive important ones
```

---

**Session Management System v1.0**
Complete workflow automation for organized development
