#!/usr/bin/env python3
"""
Create a checkpoint snapshot of current session state
Saves incremental backup of work in progress
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from specmap.sessions import SessionManager


def main():
    """Main entry point"""

    # Get project root
    project_root = Path(__file__).parent.parent

    # Get args
    if len(sys.argv) < 3:
        print("Usage: python session-checkpoint.py <session-id> <description> [files...]")
        print("Example: python session-checkpoint.py 2025-10-25-session-001 'Auth implemented'")
        print("         python session-checkpoint.py 2025-10-25-session-001 'Bug fix' src/auth.py")
        sys.exit(1)

    session_id = sys.argv[1]
    description = sys.argv[2]
    files_to_snapshot = sys.argv[3:] if len(sys.argv) > 3 else None

    print(f"Creating checkpoint for session: {session_id}")
    print(f"Description: {description}")
    if files_to_snapshot:
        print(f"Files to snapshot: {', '.join(files_to_snapshot)}")
    else:
        print("Snapshotting all artifacts...")
    print()

    # Initialize session manager
    session_mgr = SessionManager(project_root)

    try:
        # Create checkpoint
        result = session_mgr.create_checkpoint(
            session_id=session_id,
            description=description,
            files_to_snapshot=files_to_snapshot
        )

        print("[OK] Checkpoint created successfully!")
        print()
        print(f"[SAVE] Checkpoint ID: {result['checkpoint_id']}")
        print(f" Location: {result['checkpoint_path']}")
        print(f" Files snapshotted: {result['files_snapshotted']}")
        print(f" Description: {result['description']}")
        print()
        print("Checkpoint saved! You can restore from this point if needed.")

    except ValueError as e:
        print(f"[ERROR] Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Error creating checkpoint: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
