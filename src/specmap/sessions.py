"""
Session management for SpecMap
Handles session lifecycle, backups, and artifact organization
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import shutil
import yaml
import json


class SessionManager:
    """Manages development sessions with automatic backup and organization"""

    def __init__(self, project_path: Path):
        """
        Initialize session manager

        Args:
            project_path: Path to SpecMap project root
        """
        self.project_path = Path(project_path)
        self.sessions_dir = self.project_path / "04-agents" / "sessions"
        self.active_dir = self.sessions_dir / "active"
        self.archive_dir = self.sessions_dir / "archive"
        self.backups_dir = self.project_path / "04-agents" / "backups"

    def create_session_id(self, focus: Optional[str] = None) -> str:
        """
        Generate unique session ID

        Args:
            focus: Optional focus area for session naming

        Returns:
            Session ID in format: YYYY-MM-DD-session-NNN[-focus]
        """
        date_str = datetime.now().strftime("%Y-%m-%d")

        # Find existing sessions for today
        existing = list(self.sessions_dir.glob(f"{date_str}-session-*"))
        session_num = len(existing) + 1

        session_id = f"{date_str}-session-{session_num:03d}"

        if focus:
            # Sanitize focus for filename
            safe_focus = "".join(c if c.isalnum() or c == "-" else "-"
                               for c in focus.lower())[:30]
            session_id += f"-{safe_focus}"

        return session_id

    def start_session(
        self,
        focus: str,
        agent: str = "claude",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Start a new development session

        Creates:
        - Session workspace folder
        - Session metadata file
        - Session summary template
        - Checkpoint system

        Args:
            focus: Focus area for this session
            agent: AI agent being used
            metadata: Optional additional metadata

        Returns:
            Dict with session details and paths
        """
        # Generate session ID
        session_id = self.create_session_id(focus)
        session_path = self.active_dir / session_id

        # Create session structure
        session_path.mkdir(parents=True, exist_ok=True)
        (session_path / "artifacts").mkdir(exist_ok=True)
        (session_path / "notes").mkdir(exist_ok=True)
        (session_path / "decisions").mkdir(exist_ok=True)
        (session_path / "snapshots").mkdir(exist_ok=True)

        # Create session metadata
        session_meta = {
            'session': {
                'id': session_id,
                'date': datetime.now().strftime("%Y-%m-%d"),
                'start_time': datetime.now().strftime("%H:%M:%S"),
                'end_time': None,
                'focus': focus,
                'agent': agent,
                'status': 'active'
            },
            'artifacts': {
                'created': [],
                'modified': []
            },
            'checkpoints': [],
            'metrics': {
                'duration_minutes': 0,
                'files_created': 0,
                'files_modified': 0,
                'checkpoints': 0
            }
        }

        if metadata:
            session_meta['custom'] = metadata

        # Save metadata
        meta_path = session_path / "session.yaml"
        with open(meta_path, 'w', encoding='utf-8') as f:
            yaml.dump(session_meta, f, default_flow_style=False, sort_keys=False)

        # Create session summary template
        self._create_session_summary_template(session_path, session_id, focus)

        # Create README
        readme_content = f"""# Session: {session_id}

**Focus**: {focus}
**Agent**: {agent}
**Started**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Session Workspace

This folder contains all work from this development session:

- `artifacts/` - Files created during session
- `notes/` - Session notes and scratch work
- `decisions/` - Technical decisions documented
- `snapshots/` - Incremental state checkpoints
- `session.yaml` - Session metadata
- `summary.md` - Session summary (fill at end)

## Usage

**During Session**:
- Save all created files to `artifacts/`
- Document decisions in `decisions/`
- Create checkpoints for important milestones

**End of Session**:
- Complete `summary.md`
- Run: `specmap session end {session_id}`
- Session will be archived and backed up
"""
        (session_path / "README.md").write_text(readme_content, encoding='utf-8')

        return {
            'session_id': session_id,
            'session_path': str(session_path),
            'metadata_file': str(meta_path),
            'started': True,
            'focus': focus,
            'agent': agent
        }

    def _create_session_summary_template(
        self,
        session_path: Path,
        session_id: str,
        focus: str
    ):
        """Create session summary template"""
        template = f"""# Session Summary: {session_id}

**Date**: {datetime.now().strftime("%Y-%m-%d")}
**Focus**: {focus}
**Status**: In Progress

## Session Overview

### Focus Areas
- [Primary focus area]

### Goals
- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

## Accomplishments

### Major Features Delivered
- [ ] Feature 1
- [ ] Feature 2

### Code Metrics
- **Lines of Code**: TBD
- **Files Created**: TBD
- **Files Modified**: TBD
- **Tests Written**: TBD

## Technical Details

### Architecture Decisions
1. **Decision**: Description
   - **Rationale**: Why this was chosen
   - **Alternatives Considered**: What else was considered
   - **Impact**: What this affects

### Key Implementations
```
[Code samples or descriptions]
```

## Artifacts Created

See `artifacts/` folder for all files created during this session.

## Lessons Learned

### What Worked Well
- Item 1
- Item 2

### Challenges Overcome
- Challenge 1: Solution
- Challenge 2: Solution

### Technical Decisions
- Decision 1: Rationale
- Decision 2: Rationale

## Next Steps

### Immediate (Next Session)
- [ ] Task 1
- [ ] Task 2

### Short-term (This Week)
- [ ] Task 1
- [ ] Task 2

## Session Metrics

- **Duration**: TBD
- **Productivity Score**: TBD/10
- **Quality Score**: TBD/10

## RULEMAP Score

- **R - Role & Authority**: TBD/10
- **U - Understanding**: TBD/10
- **L - Logic**: TBD/10
- **E - Elements**: TBD/10
- **M - Mood**: TBD/10
- **A - Audience**: TBD/10
- **P - Performance**: TBD/10

**Overall**: TBD/10

## Sign-Off

- **Session Complete**: [ ]
- **Summary Complete**: [ ]
- **Artifacts Organized**: [ ]
- **Backup Created**: [ ]
"""
        (session_path / "summary.md").write_text(template, encoding='utf-8')

    def create_checkpoint(
        self,
        session_id: str,
        description: str,
        files_to_snapshot: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a checkpoint snapshot of current session state

        Args:
            session_id: Session ID
            description: Checkpoint description
            files_to_snapshot: Optional list of specific files to snapshot

        Returns:
            Dict with checkpoint details
        """
        session_path = self.active_dir / session_id

        if not session_path.exists():
            raise ValueError(f"Session not found: {session_id}")

        # Load metadata
        meta_path = session_path / "session.yaml"
        with open(meta_path, 'r', encoding='utf-8') as f:
            session_meta = yaml.safe_load(f)

        # Create checkpoint
        checkpoint_num = len(session_meta['checkpoints']) + 1
        timestamp = datetime.now().strftime("%H-%M-%S")
        checkpoint_id = f"checkpoint-{checkpoint_num:03d}-{timestamp}"
        checkpoint_path = session_path / "snapshots" / checkpoint_id
        checkpoint_path.mkdir(parents=True, exist_ok=True)

        # Snapshot files
        snapshotted = []
        if files_to_snapshot:
            for file_path in files_to_snapshot:
                src = self.project_path / file_path
                if src.exists():
                    dst = checkpoint_path / Path(file_path).name
                    shutil.copy2(src, dst)
                    snapshotted.append(file_path)
        else:
            # Snapshot all artifacts
            artifacts_dir = session_path / "artifacts"
            if artifacts_dir.exists():
                for artifact in artifacts_dir.iterdir():
                    if artifact.is_file():
                        shutil.copy2(artifact, checkpoint_path / artifact.name)
                        snapshotted.append(str(artifact.relative_to(session_path)))

        # Update metadata
        checkpoint_info = {
            'id': checkpoint_id,
            'time': datetime.now().strftime("%H:%M:%S"),
            'description': description,
            'files_snapshot': snapshotted
        }
        session_meta['checkpoints'].append(checkpoint_info)
        session_meta['metrics']['checkpoints'] += 1

        # Save metadata
        with open(meta_path, 'w', encoding='utf-8') as f:
            yaml.dump(session_meta, f, default_flow_style=False, sort_keys=False)

        return {
            'checkpoint_id': checkpoint_id,
            'checkpoint_path': str(checkpoint_path),
            'files_snapshotted': len(snapshotted),
            'description': description
        }

    def track_artifact(
        self,
        session_id: str,
        file_path: str,
        action: str = "created"
    ) -> bool:
        """
        Track a file artifact in session metadata

        Args:
            session_id: Session ID
            file_path: Path to file (relative to project root)
            action: "created" or "modified"

        Returns:
            True if tracked successfully
        """
        session_path = self.active_dir / session_id

        if not session_path.exists():
            return False

        meta_path = session_path / "session.yaml"
        with open(meta_path, 'r', encoding='utf-8') as f:
            session_meta = yaml.safe_load(f)

        # Add to appropriate list
        if action == "created":
            if file_path not in session_meta['artifacts']['created']:
                session_meta['artifacts']['created'].append(file_path)
                session_meta['metrics']['files_created'] += 1
        elif action == "modified":
            if file_path not in session_meta['artifacts']['modified']:
                session_meta['artifacts']['modified'].append(file_path)
                session_meta['metrics']['files_modified'] += 1

        # Save metadata
        with open(meta_path, 'w', encoding='utf-8') as f:
            yaml.dump(session_meta, f, default_flow_style=False, sort_keys=False)

        return True

    def end_session(
        self,
        session_id: str,
        rulemap_score: Optional[float] = None,
        create_backup: bool = True
    ) -> Dict[str, Any]:
        """
        End a session and archive it

        Args:
            session_id: Session ID to end
            rulemap_score: Optional RULEMAP score for session
            create_backup: Whether to create backup (default: True)

        Returns:
            Dict with archival details
        """
        session_path = self.active_dir / session_id

        if not session_path.exists():
            raise ValueError(f"Session not found: {session_id}")

        # Load and update metadata
        meta_path = session_path / "session.yaml"
        with open(meta_path, 'r', encoding='utf-8') as f:
            session_meta = yaml.safe_load(f)

        # Update end time
        end_time = datetime.now()
        session_meta['session']['end_time'] = end_time.strftime("%H:%M:%S")
        session_meta['session']['status'] = 'completed'

        # Calculate duration
        start_dt = datetime.strptime(
            f"{session_meta['session']['date']} {session_meta['session']['start_time']}",
            "%Y-%m-%d %H:%M:%S"
        )
        duration_minutes = int((end_time - start_dt).total_seconds() / 60)
        session_meta['metrics']['duration_minutes'] = duration_minutes

        if rulemap_score is not None:
            session_meta['rulemap_score'] = rulemap_score

        # Save updated metadata
        with open(meta_path, 'w', encoding='utf-8') as f:
            yaml.dump(session_meta, f, default_flow_style=False, sort_keys=False)

        # Create backup if requested
        backup_path = None
        if create_backup:
            backup_path = self._backup_session(session_id, session_path)

        # Move to archive
        archive_path = self.archive_dir / session_id
        shutil.move(str(session_path), str(archive_path))

        return {
            'session_id': session_id,
            'archived': True,
            'archive_path': str(archive_path),
            'backup_path': str(backup_path) if backup_path else None,
            'duration_minutes': duration_minutes,
            'files_created': session_meta['metrics']['files_created'],
            'files_modified': session_meta['metrics']['files_modified'],
            'checkpoints': session_meta['metrics']['checkpoints']
        }

    def _backup_session(self, session_id: str, session_path: Path) -> Path:
        """Create backup of session"""
        backup_dir = self.backups_dir / "sessions"
        backup_dir.mkdir(parents=True, exist_ok=True)

        backup_name = f"{session_id}-backup.zip"
        backup_path = backup_dir / backup_name

        # Create zip archive
        shutil.make_archive(
            str(backup_path.with_suffix('')),
            'zip',
            session_path
        )

        return backup_path

    def list_active_sessions(self) -> List[Dict[str, Any]]:
        """List all active sessions"""
        sessions = []

        if not self.active_dir.exists():
            return sessions

        for session_dir in sorted(self.active_dir.iterdir()):
            if session_dir.is_dir():
                meta_path = session_dir / "session.yaml"
                if meta_path.exists():
                    with open(meta_path, 'r', encoding='utf-8') as f:
                        meta = yaml.safe_load(f)
                        sessions.append({
                            'id': meta['session']['id'],
                            'focus': meta['session']['focus'],
                            'agent': meta['session']['agent'],
                            'started': meta['session']['start_time'],
                            'path': str(session_dir)
                        })

        return sessions

    def get_session_metadata(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a session (active or archived)"""
        # Check active first
        session_path = self.active_dir / session_id
        if not session_path.exists():
            # Check archive
            session_path = self.archive_dir / session_id

        if not session_path.exists():
            return None

        meta_path = session_path / "session.yaml"
        if not meta_path.exists():
            return None

        with open(meta_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def create_daily_backup(self) -> Dict[str, Any]:
        """Create daily backup of entire project"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        backup_name = f"daily-backup-{date_str}"
        backup_dir = self.backups_dir / "daily" / backup_name

        # Files/folders to backup
        backup_items = [
            "00-governance",
            "01-specifications",
            "02-planning",
            "03-implementation",
            "04-agents/session-summaries",
            "04-agents/sessions/archive",
            "TRACKING.md",
            "PROJECT-STATUS.md"
        ]

        backup_dir.mkdir(parents=True, exist_ok=True)
        backed_up = []

        for item in backup_items:
            src = self.project_path / item
            if src.exists():
                dst = backup_dir / item
                if src.is_dir():
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
                backed_up.append(item)

        # Create backup manifest
        manifest = {
            'date': date_str,
            'timestamp': datetime.now().isoformat(),
            'items_backed_up': backed_up,
            'backup_path': str(backup_dir)
        }

        manifest_path = backup_dir / "manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)

        return {
            'backup_date': date_str,
            'backup_path': str(backup_dir),
            'items_backed_up': len(backed_up),
            'manifest': str(manifest_path)
        }
