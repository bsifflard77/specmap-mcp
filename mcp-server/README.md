# SpecMap MCP Server

This MCP server integrates SpecMap with Claude Code.

## Already Installed!

This installer has already set everything up for you.

## Usage in Claude Code

Just talk naturally:

"Initialize a SpecMap project called my-project"
"Create a specification for user authentication"
"Generate the implementation plan"

## Troubleshooting

If you see "specmap: failed" in Claude Code:

1. Check config: %APPDATA%\ClaudeCode\config.json (Windows)
2. Verify paths are absolute (not relative)
3. Restart Claude Code

## Manual Testing

```bash
cd mcp-server
python test_mcp.py
```
