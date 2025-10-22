# Folder Management Guide

**SpecMap CLI** - Comprehensive folder organization for sessions and documents

---

## Overview

The SpecMap folder management system provides:

- **Hierarchical Session Organization**: Automatic date-based folder structure
- **Document Categories**: Clear guidelines for where documents belong
- **CLI Tools**: Easy-to-use commands for folder operations
- **Migration Support**: Tools to reorganize existing files

---

## Session Summary Organization

### Hierarchical Structure

Session summaries are organized in a date-based hierarchy:

```
session-summaries/
├── YYYY/                      # Year folders
│   ├── MM-MonthName/         # Month folders
│   │   ├── DD-DayName/       # Day folders
│   │   │   ├── session-01.md # First session of the day
│   │   │   ├── session-02.md # Second session
│   │   │   └── ...
│   │   └── ...
│   └── ...
├── README.md                  # Session system documentation
└── TEMPLATE.md               # Session template file
```

### Example Structure

```
session-summaries/
├── 2025/
│   ├── 10-October/
│   │   ├── 18-Friday/
│   │   │   ├── session-01.md
│   │   │   └── session-02.md
│   │   ├── 19-Saturday/
│   │   │   └── session-01.md
│   │   └── 22-Tuesday/
│   │       ├── session-01.md
│   │       ├── session-02.md
│   │       └── session-03.md
│   └── 11-November/
│       └── 01-Friday/
│           └── session-01.md
├── README.md
└── TEMPLATE.md
```

### Benefits

1. **Clear Organization**: Sessions grouped by date hierarchy
2. **Easy Navigation**: Find sessions by year, month, or day
3. **Multiple Sessions**: Support for multiple sessions per day
4. **Scalability**: Works for long-term projects
5. **Backward Compatible**: Legacy flat files can be migrated

---

## CLI Commands

### Session Management

#### Create New Session

```bash
# Create session for today
specmap folder session create

# Create session for specific date
specmap folder session create --date 2025-10-18

# Create and open in editor
specmap folder session create --open
```

**Output**:
- Creates folder structure automatically
- Copies template and fills in date
- Returns path to new session file

#### List Sessions

```bash
# List all sessions (latest 20)
specmap folder session list

# Filter by year
specmap folder session list --year 2025

# Filter by year and month
specmap folder session list --year 2025 --month 10

# Show more sessions
specmap folder session list --limit 50
```

**Output**:
- Table with date, path, size, and modification time
- Sorted by date (newest first)
- Filterable by year/month

#### Migrate Legacy Sessions

```bash
# Preview migration (dry run)
specmap folder session migrate --dry-run

# Perform migration
specmap folder session migrate
```

**What it does**:
- Finds flat session files (YYYY-MM-DD.md format)
- Moves them to hierarchical structure
- Preserves all content
- Renames to session-01.md format

---

### Document Category Management

#### List Categories

```bash
specmap folder categories
```

**Shows**:
- All 8 document categories
- Path for each category
- Purpose and description
- Subdirectories available

**Categories**:

1. **Specifications** (`01-specifications/`)
   - Feature specs, requirements, RULEMAP docs
   - Subdirs: features, archives, templates

2. **Planning** (`02-planning/`)
   - Implementation plans, task breakdowns
   - Subdirs: features, sprints, roadmaps

3. **Implementation** (`03-implementation/`)
   - Development tracking, code reviews
   - Subdirs: features, milestones, reviews

4. **Agents** (`04-agents/`)
   - Agent configs, session summaries, performance
   - Subdirs: session-summaries, agent-configurations, agent-performance, handoffs

5. **Quality** (`05-quality-assurance/`)
   - Validation reports, test results, scoring
   - Subdirs: constitution-validation, rulemap-scoring, validation-reports, user-feedback

6. **Documentation** (`06-documentation/`)
   - User guides, technical docs, API specs
   - Subdirs: user-guides, technical-docs, api-specifications, deployment-guides

7. **Tracking** (`07-project-tracking/`)
   - Progress tracking, metrics, reports
   - Subdirs: weekly-reports, monthly-reports, metrics, retrospectives

8. **Deliverables** (`08-deliverables/`)
   - Final outputs, releases, presentations
   - Subdirs: releases, presentations, final-reports, handover-documents

#### Validate Structure

```bash
specmap folder validate
```

**Shows**:
- Table of all expected folders
- Status (exists or missing)
- Summary of validation results

#### Create Missing Folders

```bash
specmap folder create-all
```

**Creates**:
- All 8 document category folders
- All subdirectories for each category
- Session summaries root folder

#### View Statistics

```bash
specmap folder stats
```

**Shows**:
- Total files and folders
- Total size (human-readable)
- Session count
- Per-category breakdown (files, folders, size)

#### Display Guide

```bash
# View guide in terminal
specmap folder guide

# Save guide to file
specmap folder guide --save
```

**Creates**: `FOLDER-GUIDE.md` with complete organization reference

---

## Document Placement Guidelines

### Where to Put Documents

| Document Type | Category | Subdirectory | Example |
|--------------|----------|--------------|---------|
| Feature specs | Specifications | features | `01-specifications/features/001-auth/spec.md` |
| Requirements | Specifications | features | `01-specifications/features/001-auth/requirements.md` |
| Implementation plans | Planning | features | `02-planning/features/001-auth/plan.md` |
| Sprint plans | Planning | sprints | `02-planning/sprints/sprint-01.md` |
| Roadmaps | Planning | roadmaps | `02-planning/roadmaps/2025-q4.md` |
| Dev tracking | Implementation | features | `03-implementation/features/001-auth/progress.md` |
| Code reviews | Implementation | reviews | `03-implementation/reviews/review-001.md` |
| Session summaries | Agents | session-summaries | `04-agents/session-summaries/YYYY/MM-Month/DD-Day/session-01.md` |
| Agent configs | Agents | agent-configurations | `04-agents/agent-configurations/claude/config.yaml` |
| Test results | Quality | validation-reports | `05-quality-assurance/validation-reports/test-001.md` |
| RULEMAP scores | Quality | rulemap-scoring | `05-quality-assurance/rulemap-scoring/feature-001.md` |
| User guides | Documentation | user-guides | `06-documentation/user-guides/getting-started.md` |
| API docs | Documentation | api-specifications | `06-documentation/api-specifications/api-v1.md` |
| Weekly reports | Tracking | weekly-reports | `07-project-tracking/weekly-reports/2025-week-42.md` |
| Metrics | Tracking | metrics | `07-project-tracking/metrics/velocity.md` |
| Releases | Deliverables | releases | `08-deliverables/releases/v1.0.0/` |
| Presentations | Deliverables | presentations | `08-deliverables/presentations/demo-day.pdf` |

---

## Usage Patterns

### Daily Development Workflow

**Morning**:
```bash
# Create new session for today
specmap folder session create --open

# Validate folder structure
specmap folder validate
```

**During Development**:
- Document work in session file
- Place documents in appropriate categories
- Use feature folders for organization

**End of Day**:
- Complete session summary
- Run `specmap folder stats` to see progress
- Commit session and documents

### Weekly Review

```bash
# List week's sessions
specmap folder session list --year 2025 --month 10

# View statistics
specmap folder stats

# Generate weekly report
# (place in 07-project-tracking/weekly-reports/)
```

### Monthly Cleanup

```bash
# Validate structure
specmap folder validate

# Create any missing folders
specmap folder create-all

# Review statistics
specmap folder stats
```

---

## Migration Guide

### Migrating Legacy Sessions

If you have session files in flat format (`session-summaries/YYYY-MM-DD.md`):

**Step 1: Preview Migration**
```bash
specmap folder session migrate --dry-run
```

This shows what will be migrated without moving files.

**Step 2: Backup (Optional)**
```bash
cp -r session-summaries session-summaries-backup
```

**Step 3: Perform Migration**
```bash
specmap folder session migrate
```

**Step 4: Verify**
```bash
specmap folder session list
```

### Results

- Flat files moved to hierarchical structure
- Renamed to `session-01.md` format
- Original modification times preserved
- README.md and TEMPLATE.md unchanged

---

## Python API

### Using FolderManager Programmatically

```python
from pathlib import Path
from specmap.folders import FolderManager

# Initialize
project_path = Path('/path/to/project')
manager = FolderManager(project_path)

# Create session file
session_file = manager.create_session_file()
print(f"Created: {session_file}")

# List sessions
sessions = manager.list_sessions(year=2025, month=10)
for session in sessions:
    print(f"{session['date']}: {session['path']}")

# Get document location
spec_path = manager.get_document_location('specifications', 'features')
print(f"Place specs in: {spec_path}")

# Validate structure
validation = manager.validate_folder_structure()
missing = [k for k, v in validation.items() if not v]
if missing:
    print(f"Missing folders: {missing}")

# Get statistics
stats = manager.get_folder_stats()
print(f"Total files: {stats['total_files']}")
print(f"Total size: {stats['total_size_bytes']} bytes")
```

---

## Best Practices

### Session Organization

1. **One Session Per Work Period**: Create new session for each distinct work session
2. **Complete Summaries**: Fill in all RULEMAP sections before ending session
3. **Regular Commits**: Commit sessions to version control
4. **Consistent Naming**: Use auto-generated names (session-01.md, etc.)

### Document Organization

1. **Follow Categories**: Use the 8 standard categories
2. **Use Subdirectories**: Leverage subdirs for better organization
3. **Feature Folders**: Group related docs by feature ID
4. **Clear Names**: Use descriptive, consistent file names

### Maintenance

1. **Weekly Validation**: Run `specmap folder validate` weekly
2. **Monthly Stats**: Review folder statistics monthly
3. **Archive Old Content**: Move completed work to archives
4. **Backup Important Docs**: Keep backups of critical files

---

## Troubleshooting

### Sessions Not Found

**Problem**: `specmap folder session list` shows no sessions

**Solution**:
1. Check if `session-summaries/` exists
2. Run `specmap folder validate`
3. Create new session: `specmap folder session create`

### Migration Errors

**Problem**: Migration fails or skips files

**Solution**:
1. Check file naming (must be YYYY-MM-DD.md)
2. Ensure write permissions
3. Check for existing files in destination
4. Run with `--dry-run` first

### Missing Folders

**Problem**: Validation shows missing folders

**Solution**:
```bash
specmap folder create-all
```

### Permission Errors

**Problem**: Cannot create folders or files

**Solution**:
1. Check file system permissions
2. Ensure you're in the project directory
3. Run with appropriate user permissions

---

## Advanced Usage

### Custom Session Templates

You can customize `session-summaries/TEMPLATE.md` to change the default session structure. All new sessions will use your template.

### Automated Session Creation

Add to your shell profile:

```bash
# .bashrc or .zshrc
alias work-start='specmap folder session create --open'
```

### CI/CD Integration

Validate folder structure in CI:

```yaml
# .github/workflows/validate.yml
- name: Validate Folder Structure
  run: |
    specmap folder validate
    specmap folder stats
```

---

## Reference

### File Naming Conventions

- **Sessions**: `session-01.md`, `session-02.md`, etc.
- **Features**: `001-feature-name`, `002-feature-name`, etc.
- **Dates**: `YYYY-MM-DD` format
- **Reports**: `YYYY-week-NN.md` or `YYYY-month-NN.md`

### Folder Naming Conventions

- **Date folders**: `YYYY/MM-MonthName/DD-DayName/`
- **Category folders**: `NN-category-name/`
- **Feature folders**: `features/NNN-feature-name/`

### Environment Variables

- `EDITOR`: Editor used by `--open` flag (default: nano)

---

## FAQ

**Q: Can I change the session-summaries location?**
A: Currently, it's fixed at `session-summaries/`. Future versions may support custom paths.

**Q: What happens to README.md and TEMPLATE.md?**
A: They stay in the root `session-summaries/` directory and are never migrated.

**Q: Can I have sessions outside the hierarchy?**
A: Yes, but `specmap folder session list` won't find them. Use the hierarchy for best results.

**Q: How do I delete old sessions?**
A: Manually delete the day folder or individual session files. No CLI command for deletion (by design).

**Q: Can I reorganize the 8 categories?**
A: The 8-phase structure is part of SpecMap's methodology. Customization would require code changes.

---

## Related Documentation

- [README.md](../README.md) - Main project documentation
- [TRACKING.md](../TRACKING.md) - Project tracking
- [Session Summaries README](../session-summaries/README.md) - Session documentation
- [SKILLS.md](SKILLS.md) - Skills system

---

**Version**: 1.0.0
**Last Updated**: 2025-10-22
**Status**: Active
