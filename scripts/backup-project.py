#!/usr/bin/env python3
"""
Create a full project backup
Backs up all critical project files and folders
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

    print("Creating daily project backup...")
    print()

    # Initialize session manager
    session_mgr = SessionManager(project_root)

    try:
        # Create daily backup
        result = session_mgr.create_daily_backup()

        print("[OK] Backup created successfully!")
        print()
        print(f" Backup Date: {result['backup_date']}")
        print(f" Backup Location: {result['backup_path']}")
        print(f" Items Backed Up: {result['items_backed_up']}")
        print(f" Manifest: {result['manifest']}")
        print()
        print("Backed up:")
        print("  - 00-governance/ (constitution, charter)")
        print("  - 01-specifications/ (all feature specs)")
        print("  - 02-planning/ (implementation plans)")
        print("  - 03-implementation/ (development tracking)")
        print("  - 04-agents/session-summaries/ (session logs)")
        print("  - 04-agents/sessions/archive/ (archived sessions)")
        print("  - TRACKING.md")
        print("  - PROJECT-STATUS.md")
        print()
        print("Your project is safely backed up! [SAVE]")

    except Exception as e:
        print(f"[ERROR] Error creating backup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
