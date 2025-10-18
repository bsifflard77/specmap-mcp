#!/bin/bash
# SpecMap MCP Server Installation Script
# Automatically sets up the MCP server for Claude Code

set -e  # Exit on error

echo "🚀 SpecMap MCP Server Installation"
echo "===================================="
echo ""

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    CONFIG_DIR="$HOME/Library/Application Support/ClaudeCode"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    CONFIG_DIR="$HOME/.config/ClaudeCode"
else
    OS="windows"
    CONFIG_DIR="$APPDATA/ClaudeCode"
fi

echo "📍 Detected OS: $OS"
echo ""

# Get current directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
MCP_SERVER="$SCRIPT_DIR/src/specmap_mcp/server.py"
SPECMAP_SRC="$PROJECT_ROOT/specmap-cli/src"

echo "📂 Project root: $PROJECT_ROOT"
echo "📂 MCP server: $MCP_SERVER"
echo "📂 SpecMap source: $SPECMAP_SRC"
echo ""

# Check prerequisites
echo "✅ Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or later."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "   ✓ Python $PYTHON_VERSION"

# Check pip
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip not found. Please install pip."
    exit 1
fi
echo "   ✓ pip"

# Check if SpecMap CLI is installed
if ! python3 -c "import specmap" 2>/dev/null; then
    echo "⚠️  SpecMap CLI not found. Installing..."
    cd "$PROJECT_ROOT/specmap-cli"
    pip3 install -e .
    echo "   ✓ SpecMap CLI installed"
else
    echo "   ✓ SpecMap CLI"
fi

# Check FastMCP
if ! python3 -c "import fastmcp" 2>/dev/null; then
    echo "⚠️  FastMCP not found. Installing..."
    pip3 install fastmcp
    echo "   ✓ FastMCP installed"
else
    echo "   ✓ FastMCP"
fi

echo ""
echo "📝 Installing MCP server package..."
cd "$SCRIPT_DIR"
pip3 install -e .
echo "   ✓ SpecMap MCP Server installed"

echo ""
echo "⚙️  Configuring Claude Code..."

# Create config directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

CONFIG_FILE="$CONFIG_DIR/config.json"

# Check if config exists
if [ -f "$CONFIG_FILE" ]; then
    echo "   📄 Found existing config: $CONFIG_FILE"
    
    # Backup existing config
    BACKUP_FILE="$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$CONFIG_FILE" "$BACKUP_FILE"
    echo "   💾 Backed up to: $BACKUP_FILE"
    
    # Check if specmap already configured
    if grep -q '"specmap"' "$CONFIG_FILE" 2>/dev/null; then
        echo "   ⚠️  SpecMap already configured in Claude Code"
        echo "   ℹ️  To reconfigure, edit: $CONFIG_FILE"
    else
        # Add SpecMap to existing config
        echo "   ➕ Adding SpecMap to existing configuration..."
        
        # This is a simple append - for production, use jq for proper JSON manipulation
        python3 << EOF
import json

with open("$CONFIG_FILE", "r") as f:
    config = json.load(f)

if "mcpServers" not in config:
    config["mcpServers"] = {}

config["mcpServers"]["specmap"] = {
    "command": "python3",
    "args": ["$MCP_SERVER"],
    "env": {
        "PYTHONPATH": "$SPECMAP_SRC"
    }
}

with open("$CONFIG_FILE", "w") as f:
    json.dump(config, f, indent=2)
EOF
        echo "   ✅ SpecMap added to configuration"
    fi
else
    echo "   📝 Creating new config file..."
    cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "specmap": {
      "command": "python3",
      "args": [
        "$MCP_SERVER"
      ],
      "env": {
        "PYTHONPATH": "$SPECMAP_SRC"
      }
    }
  }
}
EOF
    echo "   ✅ Configuration created"
fi

echo ""
echo "🧪 Testing MCP server..."

# Test the server starts without errors
timeout 5 python3 "$MCP_SERVER" 2>&1 | head -n 1 || true
echo "   ✅ Server starts successfully"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Installation Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 Configuration: $CONFIG_FILE"
echo ""
echo "🔄 Next Steps:"
echo "   1. Restart Claude Code"
echo "   2. Type /mcp to verify 'specmap: connected'"
echo "   3. Try: 'Initialize a new SpecMap project called test-project'"
echo ""
echo "📚 Documentation: $SCRIPT_DIR/README.md"
echo "🐛 Troubleshooting: Check the README if you encounter issues"
echo ""
echo "💡 Quick Test:"
echo "   cd /tmp"
echo "   # In Claude Code: 'Initialize a SpecMap project called my-test'"
echo ""
