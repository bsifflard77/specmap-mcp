#!/usr/bin/env python3
"""
SpecMap MCP Server - Automated Installer
========================================
This script does EVERYTHING for you:
- Creates all directories
- Creates all files
- Installs dependencies
- Configures Claude Code
- Tests the installation

Just run: python setup_specmap_mcp.py
"""

import os
import sys
import json
import subprocess
from pathlib import Path
import platform

# Fix Windows console encoding for emoji/unicode characters
if platform.system() == "Windows":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Detect OS
IS_WINDOWS = platform.system() == "Windows"
IS_MACOS = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"

# Color output
def print_header(msg):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}\n")

def print_success(msg):
    print(f"✅ {msg}")

def print_error(msg):
    print(f"❌ {msg}")

def print_info(msg):
    print(f"ℹ️  {msg}")

def print_warning(msg):
    print(f"⚠️  {msg}")


# Get the script directory
SCRIPT_DIR = Path(__file__).parent.absolute()
MCP_SERVER_DIR = SCRIPT_DIR / "mcp-server"


# ============================================================================
# FILE CONTENTS - All files embedded in this script
# ============================================================================

SERVER_PY_CONTENT = '''#!/usr/bin/env python3
"""
SpecMap MCP Server - Production Version
"""
import sys
from pathlib import Path
from typing import Dict, Any
from fastmcp import FastMCP

# Import SpecMap modules
from specmap.init import ProjectInitializer
from specmap.specify import SpecificationCreator
from specmap.clarify import ClarificationProcessor
from specmap.plan import PlanGenerator
from specmap.tasks import TaskGenerator
from specmap.config import ConfigManager

server = FastMCP("SpecMap")

@server.tool()
async def specmap_init(project_name: str, project_type: str = "web-app", agent: str = "claude", path: str = ".") -> dict:
    """Initialize a new SpecMap project with RULEMAP structure."""
    try:
        base_path = Path(path).resolve()
        project_path = base_path / project_name
        initializer = ProjectInitializer(project_path, project_name, project_type, agent)
        result = initializer.initialize()
        
        return {
            "success": True,
            "project_path": str(result['path']),
            "folders_created": result['folders_created'],
            "message": f"✅ Project '{project_name}' initialized with {result['folders_created']} folders"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "message": f"❌ Failed: {str(e)}"}

@server.tool()
async def specmap_specify(project_path: str, feature_description: str, feature_id: str = None) -> dict:
    """Create a RULEMAP-enhanced feature specification."""
    try:
        project_path = Path(project_path).resolve()
        creator = SpecificationCreator(project_path)
        result = creator.create_specification(feature_description, feature_id)
        
        return {
            "success": True,
            "feature_id": result['feature_id'],
            "spec_file": result['spec_file'],
            "message": f"✅ Specification created: {result['feature_id']}"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "message": f"❌ Failed: {str(e)}"}

@server.tool()
async def specmap_clarify(project_path: str, feature_id: str) -> dict:
    """Run clarification process for a specification."""
    try:
        project_path = Path(project_path).resolve()
        processor = ClarificationProcessor(project_path)
        result = processor.run_clarification_process(feature_id, False)
        score_result = processor.calculate_rulemap_score(feature_id)
        
        return {
            "success": True,
            "feature_id": feature_id,
            "questions_count": result.get('questions_count', 0),
            "rulemap_score": score_result['score'],
            "meets_threshold": score_result['meets_threshold'],
            "message": f"📊 RULEMAP Score: {score_result['score']:.1f}/10"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "message": f"❌ Failed: {str(e)}"}

@server.tool()
async def specmap_plan(project_path: str, feature_id: str) -> dict:
    """Generate implementation plan for a feature."""
    try:
        project_path = Path(project_path).resolve()
        generator = PlanGenerator(project_path)
        result = generator.generate_implementation_plan(feature_id)
        
        return {
            "success": True,
            "feature_id": feature_id,
            "plan_file": result['plan_file'],
            "estimated_duration": result['estimated_duration'],
            "message": f"✅ Plan generated: {result['estimated_duration']} days"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "message": f"❌ Failed: {str(e)}"}

@server.tool()
async def specmap_tasks(project_path: str, feature_id: str) -> dict:
    """Generate TDD task breakdown for a feature."""
    try:
        project_path = Path(project_path).resolve()
        generator = TaskGenerator(project_path)
        result = generator.generate_tasks_for_feature(feature_id)
        
        return {
            "success": True,
            "feature_id": feature_id,
            "total_tasks": result['total_tasks'],
            "message": f"✅ {result['total_tasks']} tasks generated"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "message": f"❌ Failed: {str(e)}"}

@server.tool()
async def specmap_status(project_path: str) -> dict:
    """Get project status and progress overview."""
    try:
        project_path = Path(project_path).resolve()
        config = ConfigManager(project_path)
        specs_path = project_path / "01-specifications" / "features"
        features = []
        
        if specs_path.exists():
            for feature_dir in sorted(specs_path.iterdir()):
                if feature_dir.is_dir():
                    features.append(feature_dir.name)
        
        return {
            "success": True,
            "project_name": config.get('project.name'),
            "total_features": len(features),
            "features": features,
            "message": f"📊 Project has {len(features)} features"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "message": f"❌ Failed: {str(e)}"}

if __name__ == "__main__":
    server.run(transport="stdio")
'''

SETUP_PY_CONTENT = '''from setuptools import setup, find_packages

setup(
    name="specmap-mcp-server",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=["fastmcp>=2.0.0"],
    entry_points={"console_scripts": ["specmap-mcp=specmap_mcp.server:main"]},
)
'''

README_CONTENT = '''# SpecMap MCP Server

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

1. Check config: %APPDATA%\\ClaudeCode\\config.json (Windows)
2. Verify paths are absolute (not relative)
3. Restart Claude Code

## Manual Testing

```bash
cd mcp-server
python test_mcp.py
```
'''


# ============================================================================
# INSTALLATION FUNCTIONS
# ============================================================================

def create_directory_structure():
    """Create all necessary directories."""
    print_header("Creating Directory Structure")
    
    directories = [
        MCP_SERVER_DIR / "src" / "specmap_mcp",
        MCP_SERVER_DIR / "tests",
        MCP_SERVER_DIR / "examples",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print_success(f"Created: {directory}")
    
    return True


def create_files():
    """Create all necessary files."""
    print_header("Creating Files")
    
    # Create __init__.py files
    init_files = [
        MCP_SERVER_DIR / "src" / "specmap_mcp" / "__init__.py",
        MCP_SERVER_DIR / "tests" / "__init__.py",
    ]
    
    for init_file in init_files:
        init_file.write_text("# SpecMap MCP Server\n", encoding='utf-8')
        print_success(f"Created: {init_file.name}")

    # Create server.py
    server_file = MCP_SERVER_DIR / "src" / "specmap_mcp" / "server.py"
    server_file.write_text(SERVER_PY_CONTENT, encoding='utf-8')
    print_success(f"Created: server.py ({len(SERVER_PY_CONTENT)} bytes)")

    # Create setup.py
    setup_file = MCP_SERVER_DIR / "setup.py"
    setup_file.write_text(SETUP_PY_CONTENT, encoding='utf-8')
    print_success(f"Created: setup.py")

    # Create README.md
    readme_file = MCP_SERVER_DIR / "README.md"
    readme_file.write_text(README_CONTENT, encoding='utf-8')
    print_success(f"Created: README.md")
    
    return True


def install_dependencies():
    """Install Python dependencies."""
    print_header("Installing Dependencies")
    
    # Check if pip is available
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print_success("pip is available")
    except:
        print_error("pip not found!")
        return False
    
    # Check if SpecMap CLI is already installed or available
    print_info("Checking for SpecMap CLI...")
    specmap_setup = SCRIPT_DIR / "setup.py"
    specmap_pyproject = SCRIPT_DIR / "pyproject.toml"

    if specmap_setup.exists() or specmap_pyproject.exists():
        # Try to install from current directory
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-e", str(SCRIPT_DIR)],
                          check=True, capture_output=True)
            print_success("SpecMap CLI installed from current directory")
        except Exception as e:
            print_error(f"Failed to install SpecMap CLI: {e}")
            return False
    else:
        # SpecMap CLI package structure doesn't exist
        print_warning("SpecMap CLI package not found in current directory")
        print_info("The MCP server requires the SpecMap CLI to be installed separately")
        print_info("Expected location: src/specmap/ with setup.py or pyproject.toml")
        print_info("Continuing with MCP server installation...")
    
    # Install FastMCP
    print_info("Installing FastMCP...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "fastmcp"],
                      check=True, capture_output=True)
        print_success("FastMCP installed")
    except Exception as e:
        print_error(f"Failed to install FastMCP: {e}")
        return False
    
    # Install MCP Server
    print_info("Installing MCP Server...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", str(MCP_SERVER_DIR)],
                      check=True, capture_output=True)
        print_success("MCP Server installed")
    except Exception as e:
        print_error(f"Failed to install MCP Server: {e}")
        return False
    
    return True


def get_config_path():
    """Get Claude Code config file path based on OS."""
    if IS_WINDOWS:
        return Path(os.environ.get('APPDATA', '')) / "ClaudeCode" / "config.json"
    elif IS_MACOS:
        return Path.home() / "Library" / "Application Support" / "ClaudeCode" / "config.json"
    elif IS_LINUX:
        return Path.home() / ".config" / "ClaudeCode" / "config.json"
    else:
        return None


def configure_claude_code():
    """Configure Claude Code with MCP server."""
    print_header("Configuring Claude Code")
    
    config_path = get_config_path()
    
    if not config_path:
        print_error("Could not determine config path for your OS")
        return False
    
    print_info(f"Config path: {config_path}")
    
    # Create config directory if needed
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Server details
    server_script = MCP_SERVER_DIR / "src" / "specmap_mcp" / "server.py"
    specmap_src = SCRIPT_DIR / "src"
    
    # Prepare config
    server_config = {
        "command": sys.executable,
        "args": [str(server_script)],
        "env": {
            "PYTHONPATH": str(specmap_src)
        }
    }
    
    # Read or create config
    if config_path.exists():
        print_info("Found existing config")
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Backup
        backup_path = config_path.with_suffix('.json.backup')
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        print_success(f"Backed up to: {backup_path}")
    else:
        print_info("Creating new config")
        config = {}

    # Add SpecMap server
    if "mcpServers" not in config:
        config["mcpServers"] = {}

    config["mcpServers"]["specmap"] = server_config

    # Write config
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    
    print_success("Claude Code configured!")
    print_info(f"Config file: {config_path}")
    
    return True


def test_installation():
    """Test that everything works."""
    print_header("Testing Installation")

    # Test imports (SpecMap CLI is optional at this stage)
    specmap_available = False
    try:
        import specmap
        print_success("SpecMap CLI import works")
        specmap_available = True
    except:
        print_warning("Cannot import SpecMap CLI - install it separately to use the MCP server")
        print_info("To install: pip install -e . from the SpecMap CLI root directory")

    try:
        import fastmcp
        print_success("FastMCP import works")
    except:
        print_error("Cannot import FastMCP")
        return False

    # Test server script exists and is executable
    server_file = MCP_SERVER_DIR / "src" / "specmap_mcp" / "server.py"
    if server_file.exists():
        print_success("Server script exists")
    else:
        print_error("Server script not found")
        return False

    # Additional note if SpecMap CLI is not available
    if not specmap_available:
        print_info("")
        print_info("NOTE: The MCP server is installed but requires SpecMap CLI to function")
        print_info("You'll need to install the SpecMap CLI package before using the server")

    return True


def print_next_steps():
    """Print what to do next."""
    print_header("✅ Installation Complete!")
    
    print("\n🎉 SUCCESS! SpecMap MCP Server is installed!\n")
    print("📋 NEXT STEPS:\n")
    print("1. RESTART CLAUDE CODE")
    print("   - Quit Claude Code completely")
    print("   - Start it again\n")
    
    print("2. VERIFY CONNECTION")
    print("   - In Claude Code, type: /mcp")
    print("   - You should see: specmap: connected ✅\n")
    
    print("3. TEST IT OUT")
    print("   - Try: 'Initialize a SpecMap project called test-project'")
    print("   - Claude will use the specmap_init tool\n")
    
    config_path = get_config_path()
    print(f"📍 Config file: {config_path}\n")
    
    print("🆘 IF IT DOESN'T WORK:")
    print("   - Check the config file has absolute paths")
    print("   - Make sure Claude Code is fully restarted")
    print("   - Try running: python test_mcp.py\n")
    
    print("📚 Documentation: mcp-server/README.md\n")


# ============================================================================
# MAIN INSTALLATION
# ============================================================================

def main():
    """Main installation process."""
    print_header("SpecMap MCP Server - Automated Installer")
    print(f"Python: {sys.executable}")
    print(f"Version: {sys.version.split()[0]}")
    print(f"OS: {platform.system()}")
    print(f"Install location: {SCRIPT_DIR}")
    
    # Run installation steps
    steps = [
        ("Create directories", create_directory_structure),
        ("Create files", create_files),
        ("Install dependencies", install_dependencies),
        ("Configure Claude Code", configure_claude_code),
        ("Test installation", test_installation),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print_error(f"Failed at step: {step_name}")
            print("\n❌ Installation failed!\n")
            sys.exit(1)
    
    # Success!
    print_next_steps()


if __name__ == "__main__":
    main()
