# SpecMap MCP Setup - Bug Review and Fixes

**Review Date**: 2025-10-23
**Reviewer**: Claude (AI Assistant)
**Status**: Critical Issues Found - Requires Fixes

---

## Executive Summary

The MCP server setup has **5 critical issues** that will prevent successful installation and use with Claude Code:

1. **Duplicate/Inconsistent Server Files** - Two different implementations
2. **Missing Dependencies** - fastmcp not installed
3. **Test File Mismatch** - References non-existent function
4. **Incomplete Main Server** - Missing documented tools
5. **Installation Script Issues** - Inconsistent file generation

**Overall Risk**: 🔴 HIGH - MCP server will fail to load in Claude Code

---

## Critical Issues

### Issue #1: Duplicate Server Implementations

**Severity**: 🔴 CRITICAL

**Location**:
- `/mcp-server/src/specmap_mcp/server.py` (194 lines, 6 tools + 6 skill tools = 12 tools)
- `/mcp-server/src/specmap_mcp/specmap_mcp_server.py` (780 lines, 7 tools including `specmap_validate`)

**Problem**:
The repository has TWO different server implementations:

1. **server.py** (Active - entry point):
   - Has 6 workflow tools: init, specify, clarify, plan, tasks, status
   - Has 6 skill management tools
   - ✅ Has skill tools (create_claude_skill, install_specmap_skill_template, etc.)
   - ❌ **MISSING** `specmap_validate` tool
   - ❌ Less detailed docstrings
   - ❌ No traceback in error responses

2. **specmap_mcp_server.py** (Alternate - unused):
   - Has 7 workflow tools: init, specify, clarify, plan, tasks, status, **validate**
   - ✅ Has comprehensive docstrings with examples
   - ✅ Has traceback in error responses
   - ❌ **MISSING** all 6 skill management tools
   - ❌ Not used as entry point

**Impact**:
- Test suite will fail (imports specmap_validate that doesn't exist in active server)
- README documents specmap_validate but it's not available
- Skill management tools work but validate tool doesn't
- Confusion about which file is authoritative

**Fix Required**:
Merge both implementations into single, complete server.py with ALL 13 tools.

---

### Issue #2: Missing Python Dependencies

**Severity**: 🔴 CRITICAL

**Problem**:
```bash
$ python3 -c "import fastmcp"
ModuleNotFoundError: No module named 'fastmcp'
```

The `fastmcp` package is required but not installed.

**Impact**:
- MCP server cannot start
- Claude Code will show "specmap: failed"
- All MCP tools unavailable

**Current Setup**:
- `mcp-server/setup.py` declares dependency: `install_requires=["fastmcp>=2.0.0"]`
- BUT the package is not installed in the environment

**Fix Required**:
```bash
pip install fastmcp
# OR
cd mcp-server && pip install -e .
```

---

### Issue #3: Test File Import Error

**Severity**: 🔴 HIGH

**Location**: `/mcp-server/specmap_mcp_test.py:24`

**Problem**:
```python
from specmap_mcp.server import (
    ...
    specmap_validate  # ❌ This function doesn't exist in server.py
)
```

The test file tries to import `specmap_validate` which only exists in the alternate `specmap_mcp_server.py`, not in the active `server.py`.

**Impact**:
- Test suite cannot run
- `python mcp-server/specmap_mcp_test.py` will crash immediately
- Cannot verify MCP server is working

**Fix Required**:
Either:
1. Remove `specmap_validate` import from test OR
2. Add `specmap_validate` function to server.py

---

### Issue #4: Server Missing Documented Tools

**Severity**: 🟡 MEDIUM

**Problem**:
The README (`mcp-server/specmap_mcp_readme.md:211`) documents a `specmap_validate` tool:

```markdown
| Tool | Description |
|------|-------------|
| `specmap_validate` | Validate against quality standards |
```

BUT this tool doesn't exist in the active `server.py` file.

**Impact**:
- Users reading docs will try to use a tool that doesn't exist
- Documentation is misleading
- Feature gap - no validation tool available

**Fix Required**:
Add `specmap_validate` tool to server.py OR remove from documentation.

---

### Issue #5: Installer Generates Incomplete Server

**Severity**: 🟡 MEDIUM

**Location**: `/specmap_mcp_installer.py:61-196`

**Problem**:
The installer script (`specmap_mcp_installer.py`) has embedded server code that it writes:

```python
SERVER_PY_CONTENT = '''...
# Only has 6 basic tools
# Missing specmap_validate
# Missing skill management tools
...'''
```

This embedded code is **outdated** compared to the actual server files.

**Impact**:
- If someone runs the installer, it will **overwrite** the complete server.py with an incomplete version
- Loss of functionality (skills tools, validate tool)
- Confusion about which version is correct

**Fix Required**:
Update installer to generate complete server OR remove code generation from installer.

---

## Additional Issues

### Issue #6: Configuration Path Inconsistencies

**Severity**: 🟡 MEDIUM

**Problem**:
Different docs reference different config paths for Claude Code:

1. README.md says: `~/Library/Application Support/Claude/claude_desktop_config.json`
2. specmap_mcp_readme.md says: `~/Library/Application Support/ClaudeCode/config.json`

**Correct Paths**:
- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Claude Code**: Different, likely `~/.config/ClaudeCode/` or similar

**Impact**: Users will edit wrong config file

---

### Issue #7: Setup.py Python Version Mismatch

**Severity**: 🟢 LOW

**Problem**:
- Main `setup.py` requires: `python_requires=">=3.11"`
- MCP `setup.py` requires: `python_requires=">=3.8"`

**Impact**: Inconsistent requirements, may cause compatibility issues

---

## Required Fixes - Action Plan

### Fix #1: Create Unified Server (Priority: CRITICAL)

Merge both server files into one complete implementation:

```python
# server.py should have:
# - All 6 workflow tools (init, specify, clarify, plan, tasks, status)
# - All 6 skill tools (create, install, install_all, list, get_templates, delete)
# - The validate tool
# Total: 13 tools
```

### Fix #2: Install Dependencies (Priority: CRITICAL)

```bash
# Install fastmcp
pip install "fastmcp>=2.0.0"

# Install MCP server package
cd mcp-server
pip install -e .

# Verify
python -c "from fastmcp import FastMCP; print('OK')"
```

### Fix #3: Fix Test File (Priority: HIGH)

Options:
1. Remove `specmap_validate` from test imports (if not implementing)
2. Add proper conditional import
3. Implement `specmap_validate` in server.py

### Fix #4: Update Documentation (Priority: MEDIUM)

- Clarify which tools are available
- Fix config file paths for different Claude versions
- Update installer embedded code OR remove it
- Add warning about two server files

### Fix #5: Standardize Python Requirements (Priority: LOW)

Align both setup.py files to same Python version requirement.

---

## Testing Checklist

After fixes are applied, verify:

- [ ] `pip install -e .` works without errors
- [ ] `python -c "from fastmcp import FastMCP; print('OK')"` succeeds
- [ ] `python -c "from specmap_mcp.server import server; print('OK')"` succeeds
- [ ] `python mcp-server/src/specmap_mcp/server.py` starts without errors (Ctrl+C to stop)
- [ ] All 13 tools are defined in server.py
- [ ] Test file imports work: `python -c "from specmap_mcp.server import specmap_status; print('OK')"`
- [ ] Claude Code config is correct format
- [ ] MCP server shows "connected" in Claude Code (`/mcp` command)

---

## Recommended Server Structure

The final `server.py` should have this structure:

```python
#!/usr/bin/env python3
from fastmcp import FastMCP
from specmap import *  # all imports

server = FastMCP("SpecMap")

# Workflow Tools (6)
@server.tool()
async def specmap_init(...): ...

@server.tool()
async def specmap_specify(...): ...

@server.tool()
async def specmap_clarify(...): ...

@server.tool()
async def specmap_plan(...): ...

@server.tool()
async def specmap_tasks(...): ...

@server.tool()
async def specmap_status(...): ...

# Validation Tool (1)
@server.tool()
async def specmap_validate(...): ...

# Skill Management Tools (6)
@server.tool()
async def create_claude_skill(...): ...

@server.tool()
async def install_specmap_skill_template(...): ...

@server.tool()
async def install_all_specmap_skills(...): ...

@server.tool()
async def list_claude_skills(...): ...

@server.tool()
async def get_skill_templates(...): ...

@server.tool()
async def delete_claude_skill(...): ...

# Entry point
if __name__ == "__main__":
    server.run(transport="stdio")
```

Total: 13 tools

---

## Files That Need Updates

1. ✅ `/mcp-server/src/specmap_mcp/server.py` - Add validate tool
2. ✅ `/mcp-server/specmap_mcp_test.py` - Fix imports or add conditional
3. ✅ `/specmap_mcp_installer.py` - Update or remove embedded server code
4. ✅ `/mcp-server/specmap_mcp_readme.md` - Clarify config paths
5. ✅ `/README.md` - Update MCP server documentation
6. ⚠️ `/mcp-server/src/specmap_mcp/specmap_mcp_server.py` - Consider merging or removing

---

## Impact Assessment

**If not fixed**:
- ❌ MCP server won't start (missing fastmcp)
- ❌ Test suite won't run (import errors)
- ❌ Users can't access validate tool (missing)
- ❌ Installer will break working server (overwrites)
- ❌ Documentation misleading (wrong paths)

**After fixes**:
- ✅ Complete MCP server with all 13 tools
- ✅ Tests pass
- ✅ Documentation accurate
- ✅ Clean installation process
- ✅ Ready for production use with Claude Code

---

## Next Steps

1. **Immediate**: Install fastmcp dependency
2. **High Priority**: Merge server implementations
3. **High Priority**: Fix test file imports
4. **Medium Priority**: Update documentation
5. **Low Priority**: Standardize Python versions

---

## Conclusion

The SpecMap MCP setup has **critical issues** that prevent it from working with Claude Code, but all issues are **fixable**. The primary problems are:

1. Missing dependency (fastmcp)
2. Incomplete/inconsistent server implementations
3. Test file references non-existent functions

**Estimated fix time**: 2-3 hours for complete resolution

**Priority**: 🔴 HIGH - Required before MCP server can be used

