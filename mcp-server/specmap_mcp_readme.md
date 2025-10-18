# SpecMap MCP Server

Model Context Protocol (MCP) server for integrating SpecMap with Claude Code.

## Overview

This MCP server exposes SpecMap's specification-driven development workflow to Claude Code, enabling natural language interactions with your SpecMap projects:

- **Initialize projects** with RULEMAP structure
- **Create specifications** following the 7-element framework
- **Run clarifications** to resolve ambiguities
- **Generate plans** with technical decisions
- **Break down tasks** with TDD workflow
- **Track progress** across features

## Installation

### Prerequisites

1. **Python 3.8+** installed
2. **SpecMap CLI** installed:
   ```bash
   cd specmap-cli
   pip install -e .
   ```
3. **Claude Code** installed (or Claude Desktop)
4. **FastMCP** library:
   ```bash
   pip install fastmcp
   ```

### Install MCP Server

#### Option 1: Development Installation (Recommended)

```bash
# Navigate to mcp-server directory
cd specmap-cli/mcp-server

# Install in development mode
pip install -e .

# Verify installation
specmap-mcp --help
```

#### Option 2: Direct Python Execution

```bash
# Make server executable
chmod +x src/specmap_mcp/server.py

# Test it works
python3 src/specmap_mcp/server.py
```

## Configuration

### For Claude Code

1. **Find your configuration file:**
   - **macOS**: `~/Library/Application Support/ClaudeCode/config.json`
   - **Linux**: `~/.config/ClaudeCode/config.json`
   - **Windows**: `%APPDATA%\ClaudeCode\config.json`

2. **Add the SpecMap server:**

```json
{
  "mcpServers": {
    "specmap": {
      "command": "python3",
      "args": [
        "/absolute/path/to/specmap-cli/mcp-server/src/specmap_mcp/server.py"
      ],
      "env": {
        "PYTHONPATH": "/absolute/path/to/specmap-cli/src"
      }
    }
  }
}
```

**Important**: Replace `/absolute/path/to/` with your actual path!

3. **Restart Claude Code**

4. **Verify it's working:**
   - Type `/mcp` in Claude Code
   - You should see `specmap: connected`

### For Claude Desktop

Same configuration file location, but named `claude_desktop_config.json`:

**macOS/Linux**:
```bash
# Edit config
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows**:
```bash
# Edit config
notepad %APPDATA%\Claude\claude_desktop_config.json
```

Add the same MCP server configuration as above.

## Usage

Once configured, you can use SpecMap naturally in Claude Code:

### Initialize a Project

```
You: "Initialize a new SpecMap project called 'user-dashboard' for a web app"

Claude: [Uses specmap_init]
✅ Project 'user-dashboard' initialized successfully!
📁 Created 34 folders
📄 Generated 5 core documents
🤖 Agent: claude
📍 Location: ./user-dashboard
```

### Create a Specification

```
You: "Create a specification for user authentication with OAuth support"

Claude: [Uses specmap_specify]
✅ Specification created: 001-user-authentication
📝 Location: 01-specifications/features/001-user-authentication
🔢 Tracking IDs generated:
   requirements: 7 items
   questions: 3 items
   acceptance: 5 items
```

### Run Clarification

```
You: "Run clarification on that feature"

Claude: [Uses specmap_clarify]
❓ Feature: 001-user-authentication
📊 RULEMAP Score: 6.5/10.0
⚠️ Threshold: NOT MET (need ≥8.0)
❓ Questions: 3 need clarification
```

### Generate Implementation Plan

```
You: "Generate the implementation plan"

Claude: [Uses specmap_plan]
✅ Implementation plan generated: 001-user-authentication
📋 Technical Decisions: 5
🎯 Milestones: 3
⏱️  Estimated Duration: 14 days
```

### Break Down into Tasks

```
You: "Break it down into tasks"

Claude: [Uses specmap_tasks]
✅ Task breakdown generated: 001-user-authentication
📋 Total Tasks: 23
🔄 Parallel Groups: 4
⏱️  Estimated Duration: 14 days
📊 Breakdown by phase:
   Phase 0 (Setup): 3 tasks
   Phase 1 (TDD Red): 5 tasks
   Phase 2 (TDD Green): 7 tasks
   ...
```

### Check Project Status

```
You: "What's the status of this project?"

Claude: [Uses specmap_status]
📊 Project Status: user-dashboard
📁 Type: web-app
🤖 Agent: claude
📝 Features: 3 total

Workflow Progress:
   ✅ Specified: 3
   📋 Planned: 2
   🔨 Tasks Created: 1
```

## Available Tools

The MCP server exposes these tools to Claude Code:

| Tool | Description |
|------|-------------|
| `specmap_init` | Initialize new project with RULEMAP structure |
| `specmap_specify` | Create RULEMAP-enhanced specification |
| `specmap_clarify` | Run clarification process and RULEMAP scoring |
| `specmap_plan` | Generate implementation plan with decisions |
| `specmap_tasks` | Create TDD task breakdown |
| `specmap_status` | Get project progress overview |
| `specmap_validate` | Validate against quality standards |

## Troubleshooting

### "Connection failed" in Claude Code

**Check:**
1. Path to `server.py` is absolute (not relative)
2. `PYTHONPATH` includes `specmap-cli/src`
3. SpecMap CLI is installed: `pip list | grep specmap`
4. FastMCP is installed: `pip list | grep fastmcp`

**Test manually:**
```bash
python3 /path/to/server.py
# Should start without errors
# Press Ctrl+C to exit
```

### "Import error" when running

**Fix:**
```bash
# Make sure both are installed
cd specmap-cli
pip install -e .

# Install FastMCP
pip install fastmcp

# Test imports
python3 -c "from specmap.init import ProjectInitializer; print('OK')"
python3 -c "from fastmcp import FastMCP; print('OK')"
```

### Server shows "connected" but tools don't work

**Debug:**
1. Check Claude Code logs (if available)
2. Test a simple tool manually in Python:
   ```python
   from specmap_mcp.server import specmap_status
   import asyncio
   result = asyncio.run(specmap_status(".", False))
   print(result)
   ```

### "Not a SpecMap project" error

Make sure you're in a directory initialized with `specmap_init`. The MCP server needs:
- `.specmap/` folder to exist
- Valid project structure

## Development

### Running Tests

```bash
cd mcp-server
pytest tests/
```

### Adding New Tools

1. Add function to `src/specmap_mcp/server.py`
2. Decorate with `@server.tool()`
3. Add type hints and docstring
4. Restart Claude Code to load changes

### Debugging

Enable debug logging:

```json
{
  "mcpServers": {
    "specmap": {
      "command": "python3",
      "args": ["-u", "/path/to/server.py"],
      "env": {
        "PYTHONPATH": "/path/to/src",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new tools
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- **Issues**: https://github.com/your-username/specmap/issues
- **Documentation**: https://github.com/your-username/specmap/tree/main/docs
- **SpecMap CLI Docs**: See main README in `specmap-cli/`

---

**SpecMap System** - AI-powered specification-driven development with RULEMAP quality
