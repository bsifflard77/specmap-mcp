#!/usr/bin/env python3
"""
Create a new session summary from template
"""

import sys
from pathlib import Path
from datetime import datetime
import shutil


def create_new_session(date_str=None):
    """Create a new session summary file from template"""

    # Get project root (assuming script is in scripts/)
    project_root = Path(__file__).parent.parent

    # Determine date
    if date_str:
        session_date = date_str
    else:
        session_date = datetime.now().strftime("%Y-%m-%d")

    # Paths
    template_path = project_root / "session-summaries" / "TEMPLATE.md"
    session_path = project_root / "session-summaries" / f"{session_date}.md"

    # Check if session already exists
    if session_path.exists():
        print(f"WARNING: Session file already exists: {session_path}")
        response = input("Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("CANCELLED")
            return False

    # Check template exists
    if not template_path.exists():
        print(f"ERROR: Template not found: {template_path}")
        return False

    # Copy template
    try:
        shutil.copy(template_path, session_path)

        # Replace [DATE] placeholder
        content = session_path.read_text(encoding='utf-8')
        content = content.replace('[DATE]', session_date)
        session_path.write_text(content, encoding='utf-8')

        print(f"SUCCESS: Created session summary: {session_path}")
        print(f"\nNext steps:")
        print(f"   1. Open: {session_path}")
        print(f"   2. Fill in session details as you work")
        print(f"   3. Complete RULEMAP analysis at end of day")
        print(f"   4. Update TRACKING.md with session results")

        return True

    except Exception as e:
        print(f"ERROR: Error creating session: {e}")
        return False


def main():
    """Main entry point"""

    # Get date from args if provided
    date_str = sys.argv[1] if len(sys.argv) > 1 else None

    if date_str:
        print(f"Creating session for: {date_str}")
    else:
        print(f"Creating session for today")

    success = create_new_session(date_str)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
