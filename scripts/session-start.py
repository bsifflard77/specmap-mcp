#!/usr/bin/env python3
"""
Start a new SpecMap development session
Creates organized workspace and initializes tracking
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from specmap.sessions import SessionManager


def main():
    """Main entry point"""

    # Get project root (assuming script is in scripts/)
    project_root = Path(__file__).parent.parent

    # Get focus from args
    if len(sys.argv) < 2:
        print("Usage: python session-start.py <focus> [agent]")
        print("Example: python session-start.py 'authentication feature' claude")
        sys.exit(1)

    focus = sys.argv[1]
    agent = sys.argv[2] if len(sys.argv) > 2 else "claude"

    print(f"Starting new session...")
    print(f"  Focus: {focus}")
    print(f"  Agent: {agent}")
    print()

    # Initialize session manager
    session_mgr = SessionManager(project_root)

    try:
        # Start session
        result = session_mgr.start_session(focus, agent)

        print("[OK] Session started successfully!")
        print()
        print(f"Session ID: {result['session_id']}")
        print(f"Workspace: {result['session_path']}")
        print(f"Metadata: {result['metadata_file']}")
        print()
        print("Session workspace structure:")
        print("  artifacts/  - Files created during session")
        print("  notes/      - Session notes and scratch work")
        print("  decisions/  - Technical decisions documented")
        print("  snapshots/  - Incremental checkpoints")
        print()
        print("Next steps:")
        print("  1. Save all session work to the workspace")
        print("  2. Create checkpoints: python scripts/session-checkpoint.py <session-id> <description>")
        print("  3. End session: python scripts/session-end.py <session-id>")
        print()
        print(f"Happy coding!")

    except Exception as e:
        print(f"[ERROR] Error starting session: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
