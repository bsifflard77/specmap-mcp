#!/usr/bin/env python3
"""
Update TRACKING.md with latest session information
Extracts key metrics from latest session summary and updates tracking
"""

import sys
import re
from pathlib import Path
from datetime import datetime


def parse_session_summary(session_path: Path) -> dict:
    """Parse a session summary and extract key information"""

    if not session_path.exists():
        return None

    content = session_path.read_text(encoding='utf-8')

    # Extract key information using regex
    info = {
        'date': session_path.stem,
        'focus': extract_value(content, r'\*\*Focus\*\*:\s*(.+)'),
        'status': extract_value(content, r'\*\*Status\*\*:\s*(.+)'),
        'rulemap_score': extract_value(content, r'Overall RULEMAP Score:\s*\*\*\s*(\d+\.?\d*)/10'),
        'completion': extract_value(content, r'\*\*Completion\*\*:\s*(\d+)%'),
        'features_delivered': count_checked_items(content, 'Major Features Delivered'),
        'tests_written': extract_value(content, r'Tests Written:\s*(\d+)'),
        'lines_of_code': extract_value(content, r'Lines of Code:\s*(\d+\+?)'),
    }

    return info


def extract_value(content: str, pattern: str) -> str:
    """Extract a value using regex pattern"""
    match = re.search(pattern, content)
    return match.group(1) if match else 'N/A'


def count_checked_items(content: str, section: str) -> int:
    """Count checked items in a section"""
    # Find section
    section_match = re.search(f'### {section}.*?(?=###|\\Z)', content, re.DOTALL)
    if not section_match:
        return 0

    section_content = section_match.group(0)
    # Count [x] or [X] items
    return len(re.findall(r'- \[x\]', section_content, re.IGNORECASE))


def get_latest_session(project_root: Path) -> Path:
    """Get the most recent session file"""
    summaries_dir = project_root / "session-summaries"

    if not summaries_dir.exists():
        return None

    # Find all session files (YYYY-MM-DD.md format)
    session_files = sorted(summaries_dir.glob("20*.md"), reverse=True)

    return session_files[0] if session_files else None


def update_tracking_file(project_root: Path, session_info: dict):
    """Update TRACKING.md with session information"""

    tracking_path = project_root / "TRACKING.md"

    if not tracking_path.exists():
        print(f"ERROR: TRACKING.md not found: {tracking_path}")
        return False

    content = tracking_path.read_text(encoding='utf-8')

    # Find the Update Log section
    update_log_pattern = r'(## Update Log.*?)(\n## |\\Z)'
    match = re.search(update_log_pattern, content, re.DOTALL)

    if not match:
        print("WARNING: Update Log section not found in TRACKING.md")
        return False

    # Create new log entry
    new_entry = f"""
### {session_info['date']}
- RULEMAP Score: {session_info['rulemap_score']}/10
- Focus: {session_info['focus']}
- Status: {session_info['status']}
- Features Delivered: {session_info['features_delivered']}
- Lines of Code: {session_info['lines_of_code']}
- Tests Written: {session_info['tests_written']}
- Completion: {session_info['completion']}%
"""

    # Insert new entry at the beginning of Update Log
    update_log_section = match.group(1)
    updated_section = update_log_section + new_entry

    # Replace in content
    new_content = content.replace(match.group(1), updated_section)

    # Write back
    tracking_path.write_text(new_content, encoding='utf-8')

    print(f"SUCCESS: Updated TRACKING.md with session {session_info['date']}")
    return True


def main():
    """Main entry point"""

    # Get project root
    project_root = Path(__file__).parent.parent

    print("Updating TRACKING.md with latest session...")

    # Get latest session
    latest_session = get_latest_session(project_root)

    if not latest_session:
        print("ERROR: No session summaries found")
        sys.exit(1)

    print(f"Latest session: {latest_session.name}")

    # Parse session
    session_info = parse_session_summary(latest_session)

    if not session_info:
        print("ERROR: Failed to parse session summary")
        sys.exit(1)

    # Display extracted info
    print(f"\nExtracted Information:")
    print(f"   Date: {session_info['date']}")
    print(f"   Focus: {session_info['focus']}")
    print(f"   RULEMAP Score: {session_info['rulemap_score']}/10")
    print(f"   Completion: {session_info['completion']}%")
    print(f"   Features: {session_info['features_delivered']}")

    # Update tracking
    success = update_tracking_file(project_root, session_info)

    if success:
        print(f"\nSUCCESS: Tracking updated successfully!")
        print(f"   Review: {project_root / 'TRACKING.md'}")
    else:
        print(f"\nERROR: Failed to update tracking")
        sys.exit(1)


if __name__ == "__main__":
    main()
