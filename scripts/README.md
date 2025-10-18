# SpecMap CLI - Helper Scripts

Automation scripts for managing SpecMap development workflow.

## Available Scripts

### Session Management

#### `new-session.py`
Create a new session summary from template.

**Usage**:
```bash
# Create session for today
python scripts/new-session.py

# Create session for specific date
python scripts/new-session.py 2025-10-19
```

**What it does**:
1. Copies `TEMPLATE.md` to `session-summaries/YYYY-MM-DD.md`
2. Replaces `[DATE]` placeholders
3. Provides next steps guidance

#### `update-tracking.py`
Update TRACKING.md with latest session information.

**Usage**:
```bash
python scripts/update-tracking.py
```

**What it does**:
1. Finds most recent session summary
2. Extracts key metrics (RULEMAP score, completion, features, etc.)
3. Adds entry to TRACKING.md Update Log section
4. Preserves existing tracking information

**Extracted Metrics**:
- RULEMAP Score
- Focus area
- Status
- Features delivered
- Lines of code
- Tests written
- Completion percentage

### Future Scripts (Planned)

#### `finalize-session.py`
Calculate metrics and finalize session summary.

#### `weekly-summary.py`
Generate weekly summary from daily sessions.

#### `monthly-summary.py`
Aggregate monthly progress and trends.

#### `check-quality.py`
Validate RULEMAP scores and quality gates.

## Workflow

### Daily Workflow

**Morning**:
```bash
# Start new session
python scripts/new-session.py

# Open session file and start tracking work
code session-summaries/$(date +%Y-%m-%d).md
```

**During Day**:
- Fill in accomplishments as you work
- Document decisions and rationale
- Note challenges and solutions
- Track time on tasks

**End of Day**:
```bash
# Complete session summary (manually)
# - Fill in RULEMAP analysis
# - Calculate metrics
# - Complete retrospective
# - Calculate RULEMAP score

# Update tracking
python scripts/update-tracking.py

# Review tracking
cat TRACKING.md
```

### Example Session Flow

```bash
# 1. Morning: Start session
$ python scripts/new-session.py
✅ Created session summary: session-summaries/2025-10-19.md

📝 Next steps:
   1. Open: session-summaries/2025-10-19.md
   2. Fill in session details as you work
   3. Complete RULEMAP analysis at end of day
   4. Update TRACKING.md with session results

# 2. During day: Work and document
# (Edit session file throughout the day)

# 3. End of day: Complete and update
$ python scripts/update-tracking.py
📊 Updating TRACKING.md with latest session...
📅 Latest session: 2025-10-19.md

📋 Extracted Information:
   Date: 2025-10-19
   Focus: Integration Testing
   RULEMAP Score: 8.5/10
   Completion: 85%
   Features: 3

✅ Updated TRACKING.md with session 2025-10-19
   Review: TRACKING.md
```

## Script Requirements

### Python Version
- Python 3.11 or higher

### Dependencies
- Standard library only (no external dependencies)
- Pathlib for file operations
- Regex for parsing

### File Structure Required
```
project-root/
├── scripts/
│   ├── new-session.py
│   ├── update-tracking.py
│   └── README.md
├── session-summaries/
│   ├── TEMPLATE.md
│   └── YYYY-MM-DD.md
└── TRACKING.md
```

## Error Handling

### Common Errors

**Session file already exists**:
```
⚠️  Session file already exists: session-summaries/2025-10-19.md
Overwrite? (y/N):
```
- Choose 'y' to overwrite or 'N' to cancel

**Template not found**:
```
❌ Template not found: session-summaries/TEMPLATE.md
```
- Ensure TEMPLATE.md exists in session-summaries/

**TRACKING.md not found**:
```
❌ TRACKING.md not found
```
- Ensure TRACKING.md exists in project root

**Update Log section missing**:
```
⚠️  Update Log section not found in TRACKING.md
```
- Ensure TRACKING.md has "## Update Log" section

## Customization

### Modify Template
Edit `session-summaries/TEMPLATE.md` to customize session structure.

### Add Custom Metrics
Modify `update-tracking.py` to extract additional metrics:

```python
def parse_session_summary(session_path: Path) -> dict:
    # Add custom extraction
    info['custom_metric'] = extract_value(content, r'pattern')
    return info
```

### Change Update Format
Modify `update_tracking_file()` to change how tracking is updated:

```python
new_entry = f"""
### {session_info['date']}
- Custom format here
"""
```

## Best Practices

### Session Management
1. **Start fresh each day** - Create new session file each morning
2. **Document as you go** - Don't wait until end of day
3. **Be honest** - Accurate metrics help improve velocity
4. **Complete RULEMAP** - Don't skip sections
5. **Update tracking** - Keep project-level view current

### Tracking Updates
1. **Run at end of day** - When session is complete
2. **Review before commit** - Validate extracted metrics
3. **Keep history** - Never delete update log entries
4. **Track trends** - Use data for improvement

### Code Quality
1. **Follow PEP 8** - Python style guide
2. **Add error handling** - Graceful failures
3. **Document changes** - Update this README
4. **Test scripts** - Verify they work
5. **Keep simple** - Don't over-engineer

## Contributing

When adding new scripts:

1. **Follow naming convention**: `verb-noun.py`
2. **Add usage documentation** here
3. **Include error handling**
4. **Use argparse for arguments**
5. **Add helpful output messages**
6. **Test thoroughly**

### Script Template

```python
#!/usr/bin/env python3
"""
Brief description of what the script does
"""

import sys
from pathlib import Path


def main():
    """Main entry point"""
    print("✅ Script executed successfully")
    sys.exit(0)


if __name__ == "__main__":
    main()
```

## Troubleshooting

### Script Won't Run

**Permission denied**:
```bash
chmod +x scripts/new-session.py
```

**Python not found**:
```bash
# Use python3 explicitly
python3 scripts/new-session.py
```

### Parsing Errors

**Metrics not extracted**:
- Check session summary follows template format
- Verify RULEMAP score format: "X.X/10"
- Ensure completion format: "X%"

**Update fails**:
- Verify TRACKING.md has Update Log section
- Check file permissions
- Review script output for specific error

## Integration with SpecMap

These scripts integrate with SpecMap methodology:

- **RULEMAP Compliance**: Sessions use RULEMAP structure
- **Constitution Alignment**: Quality gates enforced
- **Tracking Integration**: Maintains project-level view
- **Documentation Standards**: Comprehensive, searchable history

## Roadmap

### Near Term
- [x] Session creation script
- [x] Tracking update script
- [ ] Session finalization script
- [ ] Quality check script

### Future
- [ ] Weekly summary generation
- [ ] Monthly reports
- [ ] Metrics visualization
- [ ] GitHub integration
- [ ] Slack notifications
- [ ] AI-assisted summary generation

## Support

For issues with scripts:
1. Check this README
2. Review script comments
3. Check session-summaries/README.md
4. Review TRACKING.md format
5. Create GitHub issue

---

**Scripts Version**: 1.0
**Last Updated**: 2025-10-18
**Maintained By**: Development Team
