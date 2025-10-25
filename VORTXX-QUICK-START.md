# Vortxx SpecMap Quick Start

**Get SpecMap skills working with Vortxx in 2 phases**

---

## 🚀 Phase 1: START NOW (From Any Computer - 5 minutes)

### What You Need
- Web browser
- Claude Pro account

### Steps

1. **Go to [claude.ai](https://claude.ai)**

2. **Create Project**
   - Click "Projects" → "+ New Project"
   - Name: "Vortxx Development"

3. **Add Custom Instructions**
   - Click Project Settings → Custom Instructions
   - **Copy/paste this:** [See VORTXX-DEPLOYMENT-PLAN.md → Phase 1 → Step 2]

4. **Start Using**
   ```
   Review this Vortxx feature spec using RULEMAP:
   [paste your spec]
   ```

**You're done!** Now you can get SpecMap guidance from any computer.

---

## 💪 Phase 2: FULL POWER (When at Vortxx Computer - 10 minutes)

### What You Need
- Claude Code Desktop on Vortxx computer
- SpecMap skills files (transferred from here)

### Transfer Options

**Option A: GitHub** (Easiest)
```bash
# On Vortxx computer
git clone https://github.com/bsifflard77/specmap-mcp.git
cd /path/to/vortxx
cp -r ../specmap-mcp/.claude/skills .claude/
```

**Option B: Use Portable ZIP**
1. From this computer: Get `specmap-skills-portable.zip`
2. Transfer via USB/Dropbox/Email
3. On Vortxx: Extract to `vortxx/.claude/skills/`

**Option C: Use Deployment Script**
```bash
# On Vortxx computer
cd /path/to/specmap-mcp
./scripts/deploy-skills-to-project.sh /path/to/vortxx
```

### Verify

Open Vortxx in Claude Code Desktop:
```
/skill specmap-reviewer
```

If it works, you're done!

---

## 📋 What You Get

### 6 Skills
1. **specmap-reviewer** - Spec quality review
2. **specmap-planner** - Implementation planning
3. **specmap-task-generator** - TDD task breakdown
4. **specmap-qa** - Quality validation
5. **specmap-session-manager** - Auto file organization
6. **specmap-charter-helper** - Project setup

### Usage Examples

**Review Specification:**
```
/skill specmap-reviewer
Review this auth spec...
```

**Generate Plan:**
```
/skill specmap-planner
Create implementation plan for payment integration
```

**Generate Tasks:**
```
/skill specmap-task-generator
Break down OAuth integration into TDD tasks
```

**Start Session:**
```
/skill specmap-session-manager
Let's work on the Vortxx dashboard feature
```

---

## 📦 Files Included

```
specmap-skills-portable.zip     # Skills ready to extract
scripts/deploy-skills-to-project.sh   # Auto deployment (Linux/Mac)
scripts/deploy-skills-to-project.bat  # Auto deployment (Windows)
docs/VORTXX-DEPLOYMENT-PLAN.md  # Full deployment guide
docs/SPECMAP-DEPLOYMENT-GUIDE.md # General deployment guide
```

---

## 🆘 Troubleshooting

**Skills not showing in Claude Code?**
- Check: `.claude/skills/*.md` files exist
- Try: Restart Claude Code Desktop
- Verify: Files have `.md` extension

**Custom Instructions not working in browser?**
- Make sure you're in the Project (not general chat)
- Try explicitly: "Review this using RULEMAP"

---

## 📚 Full Documentation

- **Vortxx Plan**: [docs/VORTXX-DEPLOYMENT-PLAN.md](docs/VORTXX-DEPLOYMENT-PLAN.md)
- **General Guide**: [docs/SPECMAP-DEPLOYMENT-GUIDE.md](docs/SPECMAP-DEPLOYMENT-GUIDE.md)
- **Session Management**: [docs/SESSION-MANAGEMENT.md](docs/SESSION-MANAGEMENT.md)
- **Skills Guide**: [docs/SKILLS.md](docs/SKILLS.md)

---

**Ready? Start with Phase 1 right now! Takes 5 minutes.**
