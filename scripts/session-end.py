#!/usr/bin/env python3
"""
End a SpecMap development session
Archives session and creates backup
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
    if len(sys.argv) < 2:
        print("Usage: python session-end.py <session-id> [rulemap-score]")
        print("Example: python session-end.py 2025-10-25-session-001 8.5")
        sys.exit(1)

    session_id = sys.argv[1]
    rulemap_score = float(sys.argv[2]) if len(sys.argv) > 2 else None

    print(f"Ending session: {session_id}")
    if rulemap_score:
        print(f"RULEMAP Score: {rulemap_score}/10")
    print()

    # Initialize session manager
    session_mgr = SessionManager(project_root)

    # Get session metadata before ending
    try:
        metadata = session_mgr.get_session_metadata(session_id)
        if not metadata:
            print(f"[ERROR] Session not found: {session_id}")
            print()
            print("Active sessions:")
            active = session_mgr.list_active_sessions()
            if active:
                for s in active:
                    print(f"  - {s['id']}: {s['focus']}")
            else:
                print("  No active sessions")
            sys.exit(1)

        print(f"Session Details:")
        print(f"  Focus: {metadata['session']['focus']}")
        print(f"  Agent: {metadata['session']['agent']}")
        print(f"  Started: {metadata['session']['start_time']}")
        print(f"  Files Created: {metadata['metrics']['files_created']}")
        print(f"  Files Modified: {metadata['metrics']['files_modified']}")
        print(f"  Checkpoints: {metadata['metrics']['checkpoints']}")
        print()

    except Exception as e:
        print(f"[WARN]  Warning: Could not load session metadata: {e}")
        print("Continuing with session end...")
        print()

    # Prompt for RULEMAP score if not provided
    if rulemap_score is None:
        try:
            score_input = input("Enter RULEMAP score for this session (0-10, or skip): ")
            if score_input.strip():
                rulemap_score = float(score_input)
        except (ValueError, KeyboardInterrupt):
            print("No RULEMAP score provided")

    print("Finalizing session...")

    try:
        # End session
        result = session_mgr.end_session(
            session_id=session_id,
            rulemap_score=rulemap_score,
            create_backup=True
        )

        print()
        print("[OK] Session ended successfully!")
        print()
        print(f" Session Summary:")
        print(f"  Session ID: {result['session_id']}")
        print(f"  Duration: {result['duration_minutes']} minutes")
        print(f"  Files Created: {result['files_created']}")
        print(f"  Files Modified: {result['files_modified']}")
        print(f"  Checkpoints: {result['checkpoints']}")
        print()
        print(f" Archived to: {result['archive_path']}")
        if result['backup_path']:
            print(f"[SAVE] Backup: {result['backup_path']}")
        print()
        print("Session complete! All work is saved and backed up. 🎉")

    except ValueError as e:
        print(f"[ERROR] Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Error ending session: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
