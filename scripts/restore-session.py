#!/usr/bin/env python3
"""
Restore a session from backup or checkpoint
Allows recovery of previous session state
"""

import sys
import shutil
import zipfile
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from specmap.sessions import SessionManager


def list_session_backups(backups_dir: Path):
    """List available session backups"""
    backup_path = backups_dir / "sessions"
    if not backup_path.exists():
        return []

    backups = []
    for backup_file in sorted(backup_path.glob("*.zip"), reverse=True):
        backups.append({
            'name': backup_file.stem.replace('-backup', ''),
            'path': str(backup_file),
            'size': backup_file.stat().st_size
        })
    return backups


def list_checkpoints(session_mgr: SessionManager, session_id: str):
    """List checkpoints for a session"""
    # Try active first
    session_path = session_mgr.active_dir / session_id
    if not session_path.exists():
        # Try archive
        session_path = session_mgr.archive_dir / session_id

    if not session_path.exists():
        return []

    snapshots_dir = session_path / "snapshots"
    if not snapshots_dir.exists():
        return []

    checkpoints = []
    for checkpoint_dir in sorted(snapshots_dir.iterdir()):
        if checkpoint_dir.is_dir():
            checkpoints.append({
                'id': checkpoint_dir.name,
                'path': str(checkpoint_dir)
            })
    return checkpoints


def restore_from_backup(backup_path: str, restore_to: Path):
    """Restore session from backup ZIP"""
    backup_file = Path(backup_path)
    if not backup_file.exists():
        raise FileNotFoundError(f"Backup not found: {backup_path}")

    # Extract backup
    restore_to.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(backup_file, 'r') as zip_ref:
        zip_ref.extractall(restore_to)

    return restore_to


def restore_from_checkpoint(checkpoint_path: str, restore_to: Path):
    """Restore files from checkpoint"""
    checkpoint_dir = Path(checkpoint_path)
    if not checkpoint_dir.exists():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

    # Copy checkpoint files
    restore_to.mkdir(parents=True, exist_ok=True)
    for file in checkpoint_dir.iterdir():
        if file.is_file():
            shutil.copy2(file, restore_to / file.name)

    return restore_to


def main():
    """Main entry point"""

    # Get project root
    project_root = Path(__file__).parent.parent

    # Initialize session manager
    session_mgr = SessionManager(project_root)

    print("SpecMap Session Restore")
    print("=" * 50)
    print()

    # Check what to restore
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python restore-session.py --list-backups")
        print("  python restore-session.py --restore-backup <session-id>")
        print("  python restore-session.py --list-checkpoints <session-id>")
        print("  python restore-session.py --restore-checkpoint <session-id> <checkpoint-id>")
        print()
        print("Examples:")
        print("  python restore-session.py --list-backups")
        print("  python restore-session.py --restore-backup 2025-10-25-session-001")
        print("  python restore-session.py --list-checkpoints 2025-10-25-session-001")
        print("  python restore-session.py --restore-checkpoint 2025-10-25-session-001 checkpoint-001-14-30-00")
        sys.exit(0)

    command = sys.argv[1]

    try:
        # List backups
        if command == "--list-backups":
            backups = list_session_backups(session_mgr.backups_dir)
            if not backups:
                print("No session backups found")
            else:
                print(f"Available session backups ({len(backups)}):")
                print()
                for backup in backups:
                    size_mb = backup['size'] / (1024 * 1024)
                    print(f"   {backup['name']}")
                    print(f"     Size: {size_mb:.2f} MB")
                    print(f"     Path: {backup['path']}")
                    print()

        # Restore from backup
        elif command == "--restore-backup":
            if len(sys.argv) < 3:
                print("Error: Session ID required")
                sys.exit(1)

            session_id = sys.argv[2]
            backup_path = session_mgr.backups_dir / "sessions" / f"{session_id}-backup.zip"

            if not backup_path.exists():
                print(f"[ERROR] Backup not found: {backup_path}")
                sys.exit(1)

            restore_to = session_mgr.active_dir / f"{session_id}-restored"

            print(f"Restoring session from backup...")
            print(f"  Backup: {backup_path}")
            print(f"  Restore to: {restore_to}")
            print()

            restored_path = restore_from_backup(str(backup_path), restore_to)

            print("[OK] Session restored successfully!")
            print(f" Restored to: {restored_path}")
            print()
            print("The session has been restored to the active sessions folder.")
            print("You can now continue working from this restored state.")

        # List checkpoints
        elif command == "--list-checkpoints":
            if len(sys.argv) < 3:
                print("Error: Session ID required")
                sys.exit(1)

            session_id = sys.argv[2]
            checkpoints = list_checkpoints(session_mgr, session_id)

            if not checkpoints:
                print(f"No checkpoints found for session: {session_id}")
            else:
                print(f"Available checkpoints for {session_id}:")
                print()
                for checkpoint in checkpoints:
                    print(f"  [SAVE] {checkpoint['id']}")
                    print(f"     Path: {checkpoint['path']}")
                    print()

        # Restore from checkpoint
        elif command == "--restore-checkpoint":
            if len(sys.argv) < 4:
                print("Error: Session ID and checkpoint ID required")
                sys.exit(1)

            session_id = sys.argv[2]
            checkpoint_id = sys.argv[3]

            # Find checkpoint
            session_path = session_mgr.active_dir / session_id
            if not session_path.exists():
                session_path = session_mgr.archive_dir / session_id

            checkpoint_path = session_path / "snapshots" / checkpoint_id

            if not checkpoint_path.exists():
                print(f"[ERROR] Checkpoint not found: {checkpoint_path}")
                sys.exit(1)

            restore_to = session_mgr.active_dir / f"{session_id}-{checkpoint_id}-restored"

            print(f"Restoring from checkpoint...")
            print(f"  Checkpoint: {checkpoint_path}")
            print(f"  Restore to: {restore_to}")
            print()

            restored_path = restore_from_checkpoint(str(checkpoint_path), restore_to)

            print("[OK] Checkpoint restored successfully!")
            print(f" Restored to: {restored_path}")
            print()
            print("Files from the checkpoint have been restored.")
            print("You can review and copy them as needed.")

        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
