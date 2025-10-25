# Vortxx Installation Checklist

**Quick step-by-step for installing SpecMap skills on your Vortxx computer**

---

## 🎯 Goal

Install 6 skill files so you can use `/skill` commands in VS Code with Claude Code.

---

## ✅ Installation Steps

### Before You Start
- [ ] Vortxx computer has Visual Studio Code installed
- [ ] Claude Code extension is installed in VS Code
- [ ] You know where your Vortxx project folder is located

---

### EASIEST METHOD: GitHub Clone

**On your Vortxx computer:**

#### Step 1: Clone SpecMap
```cmd
cd C:\Users\YourName\Projects
git clone https://github.com/bsifflard77/specmap-mcp.git
```
- [ ] Repository cloned successfully

#### Step 2: Go to Vortxx Project
```cmd
cd C:\path\to\vortxx
```
- [ ] In Vortxx project folder

#### Step 3: Create Skills Folder
```cmd
mkdir .claude\skills
```
- [ ] `.claude\skills` folder created

#### Step 4: Copy Skills
```cmd
xcopy C:\Users\YourName\Projects\specmap-mcp\.claude\skills .claude\skills /E /I
```
**Adjust the path to wherever you cloned specmap-mcp!**

- [ ] Files copied successfully

#### Step 5: Verify Files
```cmd
dir .claude\skills
```
**Should see 6 files:**
- [ ] specmap-reviewer.md
- [ ] specmap-planner.md
- [ ] specmap-task-generator.md
- [ ] specmap-qa.md
- [ ] specmap-session-manager.md
- [ ] specmap-charter-helper.md

#### Step 6: Open in VS Code
```cmd
code .
```
- [ ] Vortxx opened in VS Code

#### Step 7: Test Skills
In Claude Code panel, type:
```
/skill specmap-reviewer
```
- [ ] Skill activates successfully

**If yes, YOU'RE DONE!** ✅

---

### ALTERNATIVE: ZIP Transfer Method

**Use this if GitHub doesn't work**

#### Step 1: Get ZIP File

On **this computer**, the ZIP file is at:
```
d:\Monomoy Strategies\Projects\specmap-mcp\specmap-skills-portable.zip
```

- [ ] Copy file to USB/email/cloud storage
- [ ] Transfer to Vortxx computer

#### Step 2: On Vortxx Computer

Navigate to Vortxx folder:
```cmd
cd C:\path\to\vortxx
```
- [ ] In Vortxx folder

Create skills folder:
```cmd
mkdir .claude\skills
```
- [ ] Folder created

#### Step 3: Extract ZIP

- [ ] Right-click `specmap-skills-portable.zip`
- [ ] Extract All → Choose `.claude\skills` as destination
- [ ] Verify 6 `.md` files are in `.claude\skills`

#### Step 4: Open and Test
```cmd
code .
```
- [ ] Vortxx opened in VS Code

Test:
```
/skill specmap-reviewer
```
- [ ] Skill works!

---

## 🧪 Final Verification

Test each skill works:

- [ ] `/skill specmap-reviewer` - Spec review
- [ ] `/skill specmap-planner` - Implementation planning
- [ ] `/skill specmap-task-generator` - TDD tasks
- [ ] `/skill specmap-qa` - Quality validation
- [ ] `/skill specmap-session-manager` - Session management
- [ ] `/skill specmap-charter-helper` - Project setup

---

## 🎯 Real World Test

Try with actual Vortxx work:

```
/skill specmap-reviewer

Review this Vortxx feature specification:
[paste a real spec from your project]
```

- [ ] Claude gives RULEMAP analysis
- [ ] Scores each element
- [ ] Provides specific feedback

**If yes, installation is successful!** 🎊

---

## 🆘 Troubleshooting

**If skills don't work:**

1. **Check files exist:**
   ```cmd
   dir .claude\skills
   ```
   Should show 6 `.md` files

2. **Restart VS Code:**
   Close completely and reopen

3. **Check location:**
   Must be in Vortxx project root folder

4. **Show hidden files:**
   In File Explorer: View → Show hidden items

---

## 📖 Full Documentation

For detailed instructions: [VORTXX-PHASE2-INSTALLATION.md](VORTXX-PHASE2-INSTALLATION.md)

---

**Questions?** Refer to the full installation guide or troubleshooting section.
