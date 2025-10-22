"""
Folder management module for SpecMap
Handles session summary organization and document hierarchy
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import shutil
import calendar


class FolderManager:
    """Manages folder structure for sessions and documents"""

    # Document hierarchy definitions
    DOCUMENT_CATEGORIES = {
        'specifications': {
            'path': '01-specifications',
            'description': 'Feature specs, requirements, RULEMAP docs',
            'subdirs': ['features', 'archives', 'templates']
        },
        'planning': {
            'path': '02-planning',
            'description': 'Implementation plans, task breakdowns',
            'subdirs': ['features', 'sprints', 'roadmaps']
        },
        'implementation': {
            'path': '03-implementation',
            'description': 'Development tracking, code reviews',
            'subdirs': ['features', 'milestones', 'reviews']
        },
        'agents': {
            'path': '04-agents',
            'description': 'Agent configs, session summaries, performance',
            'subdirs': ['session-summaries', 'agent-configurations', 'agent-performance', 'handoffs']
        },
        'quality': {
            'path': '05-quality-assurance',
            'description': 'Validation reports, test results, scoring',
            'subdirs': ['constitution-validation', 'rulemap-scoring', 'validation-reports', 'user-feedback']
        },
        'documentation': {
            'path': '06-documentation',
            'description': 'User guides, technical docs, API specs',
            'subdirs': ['user-guides', 'technical-docs', 'api-specifications', 'deployment-guides']
        },
        'tracking': {
            'path': '07-project-tracking',
            'description': 'Progress tracking, metrics, reports',
            'subdirs': ['weekly-reports', 'monthly-reports', 'metrics', 'retrospectives']
        },
        'deliverables': {
            'path': '08-deliverables',
            'description': 'Final outputs, releases, presentations',
            'subdirs': ['releases', 'presentations', 'final-reports', 'handover-documents']
        }
    }

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.session_summaries_root = self.project_path / "session-summaries"

    def create_session_folder(self, date: Optional[datetime] = None) -> Path:
        """
        Create hierarchical folder for session summaries
        Format: session-summaries/YYYY/MM-MonthName/DD-DayName/

        Args:
            date: Date for the session (default: today)

        Returns:
            Path to the created session folder
        """
        if date is None:
            date = datetime.now()

        # Build hierarchical path
        year = date.strftime("%Y")
        month_num = date.strftime("%m")
        month_name = date.strftime("%B")  # Full month name
        day_num = date.strftime("%d")
        day_name = date.strftime("%A")  # Full day name

        # Create path: YYYY/MM-Month/DD-Day/
        session_path = (
            self.session_summaries_root /
            year /
            f"{month_num}-{month_name}" /
            f"{day_num}-{day_name}"
        )

        # Create the folder
        session_path.mkdir(parents=True, exist_ok=True)

        return session_path

    def get_session_folder(self, date: Optional[datetime] = None) -> Path:
        """Get the session folder path for a given date"""
        if date is None:
            date = datetime.now()

        year = date.strftime("%Y")
        month_num = date.strftime("%m")
        month_name = date.strftime("%B")
        day_num = date.strftime("%d")
        day_name = date.strftime("%A")

        session_path = (
            self.session_summaries_root /
            year /
            f"{month_num}-{month_name}" /
            f"{day_num}-{day_name}"
        )

        return session_path

    def create_session_file(self, date: Optional[datetime] = None,
                          session_number: Optional[int] = None) -> Path:
        """
        Create a new session summary file in the appropriate folder

        Args:
            date: Date for the session (default: today)
            session_number: Session number for the day (auto-increment if None)

        Returns:
            Path to the created session file
        """
        if date is None:
            date = datetime.now()

        session_folder = self.create_session_folder(date)

        # Determine session number if not provided
        if session_number is None:
            existing_sessions = list(session_folder.glob("session-*.md"))
            session_number = len(existing_sessions) + 1

        # Create filename: session-01.md, session-02.md, etc.
        filename = f"session-{session_number:02d}.md"
        session_file = session_folder / filename

        # Copy template if available
        template_path = self.session_summaries_root / "TEMPLATE.md"
        if template_path.exists() and not session_file.exists():
            shutil.copy(template_path, session_file)

            # Update the template with date info
            content = session_file.read_text(encoding='utf-8')
            content = content.replace('[DATE]', date.strftime("%Y-%m-%d"))
            session_file.write_text(content, encoding='utf-8')

        return session_file

    def list_sessions(self, year: Optional[int] = None,
                     month: Optional[int] = None) -> List[Dict[str, any]]:
        """
        List all session summaries, optionally filtered by year/month

        Returns:
            List of session info dictionaries
        """
        sessions = []

        if year:
            year_path = self.session_summaries_root / str(year)
            if not year_path.exists():
                return []

            if month:
                # Search specific month
                month_dirs = [d for d in year_path.iterdir()
                            if d.is_dir() and d.name.startswith(f"{month:02d}-")]
                search_dirs = month_dirs
            else:
                # Search all months in year
                search_dirs = [d for d in year_path.iterdir() if d.is_dir()]
        else:
            # Search all years
            year_dirs = [d for d in self.session_summaries_root.iterdir()
                        if d.is_dir() and d.name.isdigit()]
            search_dirs = []
            for year_dir in year_dirs:
                search_dirs.extend([d for d in year_dir.iterdir() if d.is_dir()])

        # Collect all session files
        for month_dir in search_dirs:
            for day_dir in month_dir.iterdir():
                if not day_dir.is_dir():
                    continue

                for session_file in day_dir.glob("session-*.md"):
                    sessions.append({
                        'path': session_file,
                        'relative_path': session_file.relative_to(self.session_summaries_root),
                        'date': self._parse_date_from_path(session_file),
                        'size': session_file.stat().st_size,
                        'modified': datetime.fromtimestamp(session_file.stat().st_mtime)
                    })

        # Sort by date
        sessions.sort(key=lambda x: x['date'], reverse=True)

        return sessions

    def _parse_date_from_path(self, session_path: Path) -> datetime:
        """Extract date from session path"""
        try:
            parts = session_path.relative_to(self.session_summaries_root).parts
            if len(parts) >= 3:
                year = int(parts[0])
                month = int(parts[1].split('-')[0])
                day = int(parts[2].split('-')[0])
                return datetime(year, month, day)
        except (ValueError, IndexError):
            pass

        # Fallback to file modification time
        return datetime.fromtimestamp(session_path.stat().st_mtime)

    def migrate_legacy_sessions(self) -> Dict[str, int]:
        """
        Migrate flat session files to hierarchical structure
        Looks for YYYY-MM-DD.md files in session-summaries root

        Returns:
            Dictionary with migration statistics
        """
        stats = {'migrated': 0, 'skipped': 0, 'errors': 0}

        # Find legacy session files (YYYY-MM-DD.md format)
        for file in self.session_summaries_root.glob("*.md"):
            # Skip special files
            if file.name in ['README.md', 'TEMPLATE.md']:
                stats['skipped'] += 1
                continue

            # Try to parse date from filename
            try:
                # Expected format: YYYY-MM-DD.md
                date_str = file.stem  # Remove .md extension
                date = datetime.strptime(date_str, "%Y-%m-%d")

                # Create new location
                new_folder = self.create_session_folder(date)
                new_path = new_folder / "session-01.md"

                # Move file if not already there
                if not new_path.exists():
                    shutil.move(str(file), str(new_path))
                    stats['migrated'] += 1
                else:
                    stats['skipped'] += 1

            except (ValueError, OSError) as e:
                stats['errors'] += 1
                print(f"Error migrating {file.name}: {e}")

        return stats

    def create_document_structure(self, category: str) -> Path:
        """
        Create complete folder structure for a document category

        Args:
            category: One of the DOCUMENT_CATEGORIES keys

        Returns:
            Path to the category root
        """
        if category not in self.DOCUMENT_CATEGORIES:
            raise ValueError(f"Unknown category: {category}. "
                           f"Valid: {', '.join(self.DOCUMENT_CATEGORIES.keys())}")

        cat_info = self.DOCUMENT_CATEGORIES[category]
        cat_path = self.project_path / cat_info['path']

        # Create main category folder
        cat_path.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        for subdir in cat_info['subdirs']:
            (cat_path / subdir).mkdir(parents=True, exist_ok=True)

        return cat_path

    def get_document_location(self, category: str,
                            document_type: Optional[str] = None) -> Path:
        """
        Get the appropriate location for a document

        Args:
            category: Document category (e.g., 'specifications')
            document_type: Optional subdirectory (e.g., 'features')

        Returns:
            Path where the document should be stored
        """
        if category not in self.DOCUMENT_CATEGORIES:
            raise ValueError(f"Unknown category: {category}")

        cat_info = self.DOCUMENT_CATEGORIES[category]
        base_path = self.project_path / cat_info['path']

        if document_type:
            if document_type not in cat_info['subdirs']:
                raise ValueError(f"Unknown document type '{document_type}' "
                               f"for category '{category}'. "
                               f"Valid: {', '.join(cat_info['subdirs'])}")
            return base_path / document_type

        return base_path

    def list_document_categories(self) -> Dict[str, Dict]:
        """Get information about all document categories"""
        return self.DOCUMENT_CATEGORIES.copy()

    def validate_folder_structure(self) -> Dict[str, bool]:
        """
        Validate that all expected folders exist

        Returns:
            Dictionary mapping folder paths to existence status
        """
        validation = {}

        # Check document categories
        for category, info in self.DOCUMENT_CATEGORIES.items():
            base_path = self.project_path / info['path']
            validation[info['path']] = base_path.exists()

            for subdir in info['subdirs']:
                full_path = base_path / subdir
                validation[f"{info['path']}/{subdir}"] = full_path.exists()

        # Check session summaries root
        validation['session-summaries'] = self.session_summaries_root.exists()

        return validation

    def create_all_folders(self) -> List[Path]:
        """
        Create complete folder structure for all categories

        Returns:
            List of created folder paths
        """
        created = []

        # Create session summaries root
        self.session_summaries_root.mkdir(parents=True, exist_ok=True)
        created.append(self.session_summaries_root)

        # Create all document categories
        for category in self.DOCUMENT_CATEGORIES.keys():
            cat_path = self.create_document_structure(category)
            created.append(cat_path)

        return created

    def get_folder_stats(self) -> Dict[str, any]:
        """
        Get statistics about folder usage

        Returns:
            Dictionary with folder statistics
        """
        stats = {
            'total_folders': 0,
            'total_files': 0,
            'total_size_bytes': 0,
            'sessions_count': 0,
            'categories': {}
        }

        # Count sessions
        sessions = self.list_sessions()
        stats['sessions_count'] = len(sessions)
        stats['total_files'] += len(sessions)
        stats['total_size_bytes'] += sum(s['size'] for s in sessions)

        # Count files in each category
        for category, info in self.DOCUMENT_CATEGORIES.items():
            cat_path = self.project_path / info['path']
            if cat_path.exists():
                files = list(cat_path.rglob('*'))
                file_count = sum(1 for f in files if f.is_file())
                folder_count = sum(1 for f in files if f.is_dir())
                size = sum(f.stat().st_size for f in files if f.is_file())

                stats['categories'][category] = {
                    'files': file_count,
                    'folders': folder_count,
                    'size_bytes': size
                }

                stats['total_files'] += file_count
                stats['total_folders'] += folder_count
                stats['total_size_bytes'] += size

        return stats


def format_size(size_bytes: int) -> str:
    """Format byte size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def get_folder_guide() -> str:
    """Get a formatted guide for folder organization"""
    guide = """
# SpecMap Folder Organization Guide

## Session Summaries

**Location**: `session-summaries/YYYY/MM-MonthName/DD-DayName/`

**Structure**:
```
session-summaries/
├── 2025/
│   ├── 10-October/
│   │   ├── 18-Friday/
│   │   │   ├── session-01.md
│   │   │   └── session-02.md
│   │   └── 19-Saturday/
│   │       └── session-01.md
│   └── 11-November/
│       └── 01-Friday/
│           └── session-01.md
├── README.md
└── TEMPLATE.md
```

**Usage**:
- Multiple sessions per day are numbered: session-01.md, session-02.md, etc.
- Use `specmap folder session create` to create new session files
- Use `specmap folder session list` to view all sessions

## Document Categories

"""

    fm = FolderManager(Path.cwd())
    for category, info in fm.list_document_categories().items():
        guide += f"\n### {category.title()}\n"
        guide += f"**Location**: `{info['path']}/`\n\n"
        guide += f"**Purpose**: {info['description']}\n\n"
        guide += f"**Subdirectories**:\n"
        for subdir in info['subdirs']:
            guide += f"- `{subdir}/`\n"
        guide += "\n"

    return guide
