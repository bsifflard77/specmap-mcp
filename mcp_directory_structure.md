# SpecMap MCP Server - Directory Structure

## Complete Project Layout

```
specmap-cli/
├── src/specmap/              # Existing SpecMap CLI (keep as-is)
│   ├── __init__.py
│   ├── cli.py
│   ├── specify.py
│   ├── clarify.py
│   ├── plan.py
│   ├── tasks.py
│   ├── config.py
│   ├── structure.py
│   ├── init.py
│   └── agents.py
│
├── templates/                # Existing templates (keep as-is)
│   ├── specifications/
│   ├── planning/
│   └── TRACKING-ID-SYSTEM.md
│
├── mcp-server/               # NEW: MCP Server Package
│   ├── README.md            # Installation & usage guide
│   ├── setup.py             # Package installation
│   ├── install.sh           # Auto-installation script
│   ├── test_mcp.py          # Test suite
│   │
│   ├── src/
│   │   └── specmap_mcp/
│   │       ├── __init__.py
│   │       └── server.py    # Main MCP server (7 tools)
│   │
│   ├── examples/            # NEW: Usage examples
│   │   ├── basic-workflow.md
│   │   ├── claude-code-demo.md
│   │   └── troubleshooting.md
│   │
│   └── tests/               # NEW: Unit tests
│       ├── __init__.py
│       ├── test_init.py
│       ├── test_specify.py
│       └── test_tools.py
│
├── docs/                     # Enhanced documentation
│   ├── README.md
│   ├── getting-started.md
│   ├── mcp-integration.md   # NEW: MCP setup guide
│   ├── claude-code-guide.md # NEW: Claude Code usage
│   └── api-reference.md
│
├── .gitignore
├── LICENSE
└── README.md
```

## File Sizes & Line Counts

### MCP Server Files

| File | Lines | Purpose |
|------|-------|---------|
| `server.py` | ~600 | Main MCP server with 7 tools |
| `setup.py` | ~50 | Package installation |
| `README.md` | ~350 | Installation & usage guide |
| `install.sh` | ~150 | Auto-installation script |
| `test_mcp.py` | ~200 | Test suite |

**Total**: ~1,350 lines of new code

### Tools Implemented

1. **specmap_init** - Initialize projects
2. **specmap_specify** - Create specifications
3. **specmap_clarify** - Run clarifications
4. **specmap_plan** - Generate plans
5. **specmap_tasks** - Create task breakdowns
6. **specmap_status** - Check progress
7. **specmap_validate** - Quality validation

## Installation Steps

### Quick Install (Automated)

```bash
# Navigate to mcp-server directory
cd specmap-cli/mcp-server

# Run installation script
chmod +x install.sh
./install.sh

# Restart Claude Code
```

### Manual Install

```bash
# 1. Install SpecMap CLI (if not already)
cd specmap-cli
pip install -e .

# 2. Install FastMCP
pip install fastmcp

# 3. Install MCP Server
cd mcp-server
pip install -e .

# 4. Configure Claude Code
# Edit: ~/Library/Application Support/ClaudeCode/config.json
# Add the specmap server configuration (see README)

# 5. Restart Claude Code
```

## Usage in Claude Code

Once configured, use naturally:

```
You: "Initialize a SpecMap project called user-dashboard"
Claude: [Uses specmap_init tool]

You: "Create a spec for user authentication"
Claude: [Uses specmap_specify tool]

You: "Generate the implementation plan"
Claude: [Uses specmap_plan tool]
```

## Testing

```bash
# Run test suite
cd mcp-server
python test_mcp.py

# Expected output:
# ✅ All Tests Completed Successfully!
```

## Configuration Files

### Claude Code (`config.json`)

```json
{
  "mcpServers": {
    "specmap": {
      "command": "python3",
      "args": [
        "/full/path/to/specmap-cli/mcp-server/src/specmap_mcp/server.py"
      ],
      "env": {
        "PYTHONPATH": "/full/path/to/specmap-cli/src"
      }
    }
  }
}
```

### Claude Desktop (`claude_desktop_config.json`)

Same configuration as above, different file location:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

## Dependencies

### Python Packages Required

```
fastmcp>=2.0.0     # MCP server framework
specmap>=1.0.0     # Your SpecMap CLI (local)
```

### System Requirements

- Python 3.8+
- Claude Code or Claude Desktop
- Git (for GitHub integration)

## Next Steps

1. **Create the directories:**
   ```bash
   cd specmap-cli
   mkdir -p mcp-server/src/specmap_mcp
   mkdir -p mcp-server/examples
   mkdir -p mcp-server/tests
   ```

2. **Copy the files:**
   - Save `server.py` to `mcp-server/src/specmap_mcp/`
   - Save `setup.py` to `mcp-server/`
   - Save `README.md` to `mcp-server/`
   - Save `install.sh` to `mcp-server/`
   - Save `test_mcp.py` to `mcp-server/`

3. **Create `__init__.py`:**
   ```bash
   touch mcp-server/src/specmap_mcp/__init__.py
   touch mcp-server/tests/__init__.py
   ```

4. **Run installation:**
   ```bash
   cd mcp-server
   ./install.sh
   ```

5. **Test it works:**
   ```bash
   python test_mcp.py
   ```

6. **Restart Claude Code and test!**

## GitHub Repository Structure

When pushing to GitHub:

```
your-username/specmap/
├── specmap-cli/         # Main CLI package
├── mcp-server/          # MCP integration
├── docs/                # Documentation
├── README.md            # Project overview
├── LICENSE              # MIT License
└── .gitignore           # Git exclusions
```

Perfect for open-source distribution!
