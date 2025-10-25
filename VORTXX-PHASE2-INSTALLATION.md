# Vortxx Phase 2 Installation Guide

**Installing SpecMap Skills Locally in Visual Studio with Claude Code**

---

## 🎯 What You're Installing

You're adding **6 SpecMap skill files** to your Vortxx project so Claude Code can use them with `/skill` commands.

**Result:** Claude Code will have expert capabilities for:
- Specification review (RULEMAP)
- Implementation planning
- TDD task generation
- Quality validation
- Session management
- Project setup

---

## 📋 Prerequisites

**On your Vortxx computer, you need:**
- ✅ Visual Studio Code installed
- ✅ Claude Code extension installed in VS Code
- ✅ Vortxx project accessible
- ✅ Access to transfer the skills files

---

## 🚀 Installation Methods

Choose ONE method based on what's easiest for you:

### Method 1: GitHub Clone (Easiest)
### Method 2: Portable ZIP Transfer
### Method 3: Manual File Copy

---

## Method 1: GitHub Clone (Recommended)

**Best if:** Vortxx computer has internet and git

### Step 1: Clone SpecMap Repository

On your Vortxx computer, open a terminal/command prompt:

**Windows (Command Prompt or PowerShell):**
```cmd
cd C:\Users\YourName\Projects
git clone https://github.com/bsifflard77/specmap-mcp.git
```

**Or navigate to where you want it:**
```cmd
cd path\to\where\you\want\specmap
git clone https://github.com/bsifflard77/specmap-mcp.git
```

### Step 2: Navigate to Your Vortxx Project

```cmd
cd C:\path\to\vortxx
```

### Step 3: Create Skills Folder

```cmd
mkdir .claude
mkdir .claude\skills
```

**Or in one command:**
```cmd
mkdir .claude\skills
```

### Step 4: Copy Skills to Vortxx

```cmd
xcopy C:\Users\YourName\Projects\specmap-mcp\.claude\skills .claude\skills /E /I
```

**Adjust the path** to wherever you cloned specmap-mcp!

### Step 5: Verify Files Copied

```cmd
dir .claude\skills
```

**You should see 6 files:**
- specmap-reviewer.md
- specmap-planner.md
- specmap-task-generator.md
- specmap-qa.md
- specmap-session-manager.md
- specmap-charter-helper.md

### Step 6: Open Vortxx in VS Code

```cmd
code .
```

**Or:** In VS Code: File → Open Folder → Select Vortxx folder

### Step 7: Test in Claude Code

In Claude Code (within VS Code), type:
```
/skill specmap-reviewer
```

**If it activates, you're done!** ✅

---

## Method 2: Portable ZIP Transfer

**Best if:** You want to transfer via USB, email, or cloud storage

### Step 1: Get the ZIP File

**On this computer** (where specmap-mcp is):

The ZIP file is already created at:
```
d:\Monomoy Strategies\Projects\specmap-mcp\specmap-skills-portable.zip
```

**Transfer this file to your Vortxx computer via:**
- USB drive
- Email to yourself
- Dropbox/Google Drive/OneDrive
- Network share

### Step 2: On Vortxx Computer - Extract ZIP

1. **Copy `specmap-skills-portable.zip` to your Vortxx computer**

2. **Navigate to Vortxx project folder in File Explorer**
   ```
   C:\path\to\vortxx
   ```

3. **Create `.claude\skills` folder:**
   - Right-click in Vortxx folder
   - New → Folder
   - Name it: `.claude`
   - Inside `.claude`, create folder: `skills`

4. **Extract ZIP contents:**
   - Right-click `specmap-skills-portable.zip`
   - Extract All
   - Choose destination: `C:\path\to\vortxx\.claude\skills`

### Step 3: Verify Files

Open `.claude\skills` folder - you should see 6 `.md` files

### Step 4: Open in VS Code

```cmd
cd C:\path\to\vortxx
code .
```

### Step 5: Test in Claude Code

```
/skill specmap-reviewer
```

---

## Method 3: Manual File Copy

**Best if:** Both computers are on the same network or you can access files remotely

### Step 1: Locate Skills on This Computer

Skills are located at:
```
d:\Monomoy Strategies\Projects\specmap-mcp\.claude\skills\
```

Contains 6 files:
- specmap-reviewer.md
- specmap-planner.md
- specmap-task-generator.md
- specmap-qa.md
- specmap-session-manager.md
- specmap-charter-helper.md

### Step 2: Transfer to Vortxx Computer

**Options:**
- Network file sharing (if same network)
- Remote desktop and copy/paste
- Cloud storage (OneDrive, Dropbox, Google Drive)
- USB drive

### Step 3: On Vortxx - Create Folder Structure

```cmd
cd C:\path\to\vortxx
mkdir .claude\skills
```

### Step 4: Copy Files

Copy all 6 `.md` files into:
```
C:\path\to\vortxx\.claude\skills\
```

### Step 5: Open and Test

```cmd
code .
```

Then in Claude Code:
```
/skill specmap-reviewer
```

---

## 📁 Expected Folder Structure

After installation, your Vortxx project should look like:

```
vortxx/
├── .claude/                  ← NEW FOLDER
│   └── skills/              ← NEW FOLDER
│       ├── specmap-reviewer.md
│       ├── specmap-planner.md
│       ├── specmap-task-generator.md
│       ├── specmap-qa.md
│       ├── specmap-session-manager.md
│       └── specmap-charter-helper.md
├── src/                     ← Your existing Vortxx code
├── tests/
├── package.json
└── ... (rest of your project)
```

**Important:** The `.claude` folder is hidden by default on Windows. You might need to show hidden files to see it in File Explorer.

---

## ✅ Verification Checklist

After installation, verify everything works:

### 1. Files Exist
```cmd
cd C:\path\to\vortxx
dir .claude\skills
```
**Should show 6 .md files**

### 2. VS Code Opens Project
```cmd
code .
```
**Should open Vortxx in VS Code**

### 3. Claude Code Extension Active
- Look for Claude Code icon in VS Code sidebar
- Or open Claude Code panel

### 4. Skills Activate
In Claude Code, test each skill:

```
/skill specmap-reviewer
```
**Should activate and Claude should acknowledge**

```
/skill specmap-planner
```
**Should activate**

```
/skill specmap-session-manager
```
**Should activate**

### 5. Actual Use Test

Try a real task:
```
/skill specmap-reviewer

Review this Vortxx authentication spec:
[paste an actual spec from your project]
```

**Should give RULEMAP analysis just like in the browser!**

---

## 🎯 Using Skills in VS Code with Claude Code

### Basic Usage

**Activate a skill:**
```
/skill specmap-reviewer
```

**Then give it work:**
```
Review this specification:
[paste or describe spec]
```

**Deactivate:**
```
/skill off
```

**Or activate a different skill:**
```
/skill specmap-planner
```

### Typical Workflow

**1. Review Specification:**
```
/skill specmap-reviewer
Please review the authentication spec in docs/auth-spec.md
```

**2. Generate Plan:**
```
/skill specmap-planner
Create an implementation plan for the authentication feature described in docs/auth-spec.md
```

**3. Generate Tasks:**
```
/skill specmap-task-generator
Break down the authentication implementation into TDD tasks
```

**4. Start Development Session:**
```
/skill specmap-session-manager
Let's work on implementing the Vortxx authentication feature
```

**5. Quality Check:**
```
/skill specmap-qa
Review the authentication implementation for quality
```

---

## 🔧 Troubleshooting

### Issue: Skills Don't Show Up

**Problem:** `/skill specmap-reviewer` doesn't work

**Solutions:**

1. **Check files exist:**
   ```cmd
   dir .claude\skills
   ```
   Should show 6 `.md` files

2. **Check file extensions:**
   - Files MUST end in `.md`
   - Not `.md.txt` or anything else

3. **Check folder location:**
   - Must be `.claude\skills` in PROJECT ROOT
   - Not in a subfolder

4. **Restart VS Code:**
   - Close VS Code completely
   - Reopen: `code .` from Vortxx folder

5. **Check Claude Code extension:**
   - Make sure Claude Code extension is installed
   - Check it's enabled for this workspace

6. **Check file format:**
   - Open one of the `.md` files
   - Should have YAML frontmatter at top:
     ```yaml
     ---
     name: specmap-reviewer
     description: ...
     ---
     ```

### Issue: Hidden Folder Not Visible

**Problem:** Can't see `.claude` folder in File Explorer

**Solution:**

1. In File Explorer, click **View** tab
2. Check **Hidden items** checkbox
3. Now `.claude` folder should be visible

**Or create via command line:**
```cmd
cd C:\path\to\vortxx
mkdir .claude\skills
```

### Issue: Permission Denied

**Problem:** Can't create `.claude` folder

**Solutions:**

1. **Run as Administrator:**
   - Right-click Command Prompt
   - "Run as administrator"
   - Try again

2. **Check folder permissions:**
   - Right-click Vortxx folder
   - Properties → Security
   - Make sure you have write permissions

3. **Different location:**
   - Try creating in a folder where you definitely have permissions
   - Test there first

### Issue: Skills Work But Give Errors

**Problem:** Skill activates but doesn't work correctly

**Solutions:**

1. **Check file contents:**
   - Open the `.md` file
   - Make sure it has the full skill content
   - Not empty or corrupted

2. **Re-copy files:**
   - Delete `.claude\skills` folder
   - Copy again from source

3. **Check Claude Code version:**
   - Update Claude Code extension to latest version

---

## 📱 Optional: Add Session Management

If you want automatic file organization and backups (optional but recommended):

### Step 1: Copy Session Scripts

**On Vortxx computer:**

```cmd
cd C:\path\to\vortxx
mkdir scripts
```

**Copy these files from specmap-mcp:**
- `scripts/session-start.py`
- `scripts/session-checkpoint.py`
- `scripts/session-end.py`
- `scripts/backup-project.py`
- `scripts/restore-session.py`

```cmd
xcopy C:\path\to\specmap-mcp\scripts\session-*.py scripts\ /Y
xcopy C:\path\to\specmap-mcp\scripts\backup-project.py scripts\ /Y
xcopy C:\path\to\specmap-mcp\scripts\restore-session.py scripts\ /Y
```

### Step 2: Copy Session Module

```cmd
mkdir vortxx\utils
copy C:\path\to\specmap-mcp\src\specmap\sessions.py vortxx\utils\sessions.py
```

**Adjust paths** based on your Vortxx project structure!

### Step 3: Install Dependencies

```cmd
pip install pyyaml
```

### Step 4: Use Session Manager Skill

```
/skill specmap-session-manager
Let's work on the Vortxx payment integration
```

Claude will automatically:
- Create organized session workspace
- Track all files
- Create checkpoints
- End session with backup

**This is optional** - skills work fine without session management!

---

## 🎊 Success Confirmation

You'll know it's working when:

✅ `/skill specmap-reviewer` activates the skill
✅ Claude gives RULEMAP analysis like in the browser
✅ You can switch between skills with `/skill` commands
✅ All 6 skills are available

---

## 📚 Quick Reference

### Available Skills

| Skill | Command | Use For |
|-------|---------|---------|
| Spec Review | `/skill specmap-reviewer` | RULEMAP analysis of specifications |
| Planning | `/skill specmap-planner` | Implementation plans |
| Tasks | `/skill specmap-task-generator` | TDD task breakdown |
| QA | `/skill specmap-qa` | Quality validation |
| Sessions | `/skill specmap-session-manager` | Auto file organization |
| Charter | `/skill specmap-charter-helper` | Project setup |

### Common Commands

```bash
# Navigate to Vortxx
cd C:\path\to\vortxx

# Open in VS Code
code .

# Check skills installed
dir .claude\skills

# Test skill
/skill specmap-reviewer
```

---

## 🆘 Need Help?

**If you get stuck:**

1. **Check the files:**
   ```cmd
   dir .claude\skills
   ```
   Should show 6 .md files

2. **Check the location:**
   Must be in project root, not a subfolder

3. **Restart VS Code:**
   Close completely and reopen

4. **Verify Claude Code extension:**
   Make sure it's installed and enabled

**Still stuck?** Let me know what error you're seeing!

---

## 📖 Related Documentation

- **Full deployment guide:** [SPECMAP-DEPLOYMENT-GUIDE.md](docs/SPECMAP-DEPLOYMENT-GUIDE.md)
- **Vortxx plan:** [VORTXX-DEPLOYMENT-PLAN.md](docs/VORTXX-DEPLOYMENT-PLAN.md)
- **Quick start:** [VORTXX-QUICK-START.md](VORTXX-QUICK-START.md)
- **Session management:** [SESSION-MANAGEMENT.md](docs/SESSION-MANAGEMENT.md)

---

**Ready to install? Start with Method 1 (GitHub Clone) - it's the easiest!**
