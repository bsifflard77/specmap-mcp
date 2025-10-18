# GitHub Setup Guide

This guide will help you push the SpecMap CLI project to GitHub.

---

## Quick Summary

✅ **Git initialized**: Repository created locally
✅ **Initial commit**: 58 files, 20,698+ lines committed
✅ **Ready to push**: All files staged and committed

**Next Step**: Create GitHub repository and push

---

## Option 1: Using GitHub Web Interface (Recommended)

### Step 1: Create Repository on GitHub

1. Go to [github.com](https://github.com) and sign in
2. Click the **"+"** icon in top-right corner
3. Select **"New repository"**

### Step 2: Configure Repository

**Repository Settings:**
- **Owner**: Your GitHub username or organization
- **Repository name**: `specmap-cli` (or your preferred name)
- **Description**: "AI-powered specification-driven development system with RULEMAP framework"
- **Visibility**:
  - ✅ **Public** (if you want to share)
  - ⚪ **Private** (if you want to keep it private)
- **Initialize**:
  - ❌ **DO NOT** check "Add a README file"
  - ❌ **DO NOT** check "Add .gitignore"
  - ❌ **DO NOT** choose a license
  - (We already have these files!)

Click **"Create repository"**

### Step 3: Push to GitHub

After creating the repository, GitHub will show you instructions. Use these commands:

```bash
cd "d:\Monomoy Strategies\Projects\specmap-cli"

# Add GitHub as remote (replace YOUR-USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/specmap-cli.git

# Rename branch to main (GitHub's default)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Example (replace with your username):**
```bash
git remote add origin https://github.com/monomoystrategies/specmap-cli.git
git branch -M main
git push -u origin main
```

You'll be prompted for your GitHub credentials:
- **Username**: Your GitHub username
- **Password**: Use a **Personal Access Token** (not your password)

---

## Option 2: Using GitHub CLI (If Installed)

If you install [GitHub CLI](https://cli.github.com/), you can create and push in one command:

```bash
# Install GitHub CLI first from https://cli.github.com/

# Authenticate
gh auth login

# Create repo and push
gh repo create specmap-cli --public --source=. --remote=origin --push
```

---

## Creating a Personal Access Token

GitHub requires a Personal Access Token for command-line access.

### Steps:

1. Go to **GitHub.com** → Click your profile picture → **Settings**
2. Scroll down to **Developer settings** (bottom of left sidebar)
3. Click **Personal access tokens** → **Tokens (classic)**
4. Click **Generate new token** → **Generate new token (classic)**
5. **Note**: "SpecMap CLI Access"
6. **Expiration**: Choose duration (90 days recommended)
7. **Select scopes**:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (if you'll use GitHub Actions)
8. Click **Generate token**
9. **COPY THE TOKEN** - you won't see it again!

Use this token as your password when pushing.

---

## Verifying the Push

After pushing, verify on GitHub:

1. Go to `https://github.com/YOUR-USERNAME/specmap-cli`
2. You should see:
   - ✅ 58 files
   - ✅ README.md displayed
   - ✅ All directories (src/, mcp-server/, docs/, etc.)
   - ✅ Commit message visible

---

## Current Repository Status

**Local Repository:**
```
Branch: master (will be renamed to main)
Commits: 1 (initial commit)
Files: 58
Lines: 20,698+
Size: ~500KB
```

**Commit Summary:**
```
Initial commit: SpecMap CLI v1.0.0-beta

Complete AI-powered specification-driven development system.
- 20+ CLI commands
- 12 MCP tools
- 5 Claude Code skills
- Comprehensive documentation
- Tracking system
```

---

## After Pushing to GitHub

### Update README Badge (Optional)

Add a GitHub badge to your README:

```markdown
[![GitHub](https://img.shields.io/github/license/YOUR-USERNAME/specmap-cli)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/YOUR-USERNAME/specmap-cli)](https://github.com/YOUR-USERNAME/specmap-cli/stargazers)
```

### Set Up GitHub Pages (Optional)

To host documentation:

1. Go to repository **Settings**
2. Scroll to **Pages** section
3. **Source**: Deploy from a branch
4. **Branch**: main, /docs folder
5. Click **Save**

### Enable Issues and Discussions

1. Go to repository **Settings**
2. Check **Issues** (for bug reports and features)
3. Check **Discussions** (for Q&A and community)

### Add Topics

Add topics to help people discover your project:
1. Click ⚙️ next to "About" on main repo page
2. Add topics:
   - `ai`
   - `claude-code`
   - `specification-driven-development`
   - `rulemap`
   - `mcp-server`
   - `python`
   - `cli-tool`

---

## Cloning on Another Computer

Once pushed to GitHub, clone on any computer:

```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/specmap-cli.git
cd specmap-cli

# Install dependencies
pip install -e .

# Start using
python -m specmap --help
```

---

## Common Issues

### Issue: "Support for password authentication was removed"

**Solution**: Use a Personal Access Token instead of password (see above)

### Issue: "fatal: remote origin already exists"

**Solution**:
```bash
git remote remove origin
git remote add origin https://github.com/YOUR-USERNAME/specmap-cli.git
```

### Issue: "Updates were rejected because the remote contains work"

**Solution**: This shouldn't happen with a new repo. If it does:
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Issue: Authentication failed

**Solution**:
1. Verify your username is correct
2. Generate a new Personal Access Token
3. Use the token as your password

---

## Keeping Local and Remote in Sync

### Pull latest changes:
```bash
git pull origin main
```

### Push new changes:
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

### Check status:
```bash
git status
git log --oneline -5
```

---

## Recommended .github Folder Structure

After pushing, consider adding GitHub-specific files:

```bash
.github/
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   └── feature_request.md
├── workflows/
│   └── tests.yml           # GitHub Actions for CI/CD
├── CONTRIBUTING.md
└── PULL_REQUEST_TEMPLATE.md
```

We can create these in a future session!

---

## Security Considerations

### What's Committed:
- ✅ Source code
- ✅ Documentation
- ✅ Configuration templates
- ✅ Session summaries (valuable history)

### What's Ignored (.gitignore):
- ✅ Virtual environments
- ✅ Python cache files
- ✅ IDE settings
- ✅ Temporary files
- ✅ Local configuration
- ✅ Test projects in src/

### Sensitive Data Check:
Run before pushing:
```bash
# Check for potential secrets
git log --all --full-history --source --find-object="password"
git log --all --full-history --source --find-object="api_key"
git log --all --full-history --source --find-object="secret"
```

Our commit looks clean! ✅

---

## Next Steps After GitHub Setup

1. **Share the repository**
   - Add collaborators if needed
   - Share URL with team members

2. **Set up CI/CD** (future)
   - GitHub Actions for testing
   - Automated quality checks
   - Release automation

3. **Enable Dependabot** (recommended)
   - Security updates
   - Dependency updates
   - Automated PRs

4. **Create releases** (when ready)
   - Tag versions: `v1.0.0-beta`
   - Create release notes
   - Upload distribution packages

---

## Repository URL Format

Your repository will be available at:
```
https://github.com/YOUR-USERNAME/specmap-cli
```

**Clone URL (HTTPS)**:
```
https://github.com/YOUR-USERNAME/specmap-cli.git
```

**Clone URL (SSH)** (if you set up SSH keys):
```
git@github.com:YOUR-USERNAME/specmap-cli.git
```

---

## Quick Reference Commands

```bash
# Check current status
git status

# View commit history
git log --oneline -10

# View remote
git remote -v

# Create and push new branch
git checkout -b feature-name
git push -u origin feature-name

# Pull latest changes
git pull origin main

# View differences
git diff

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes) - CAREFUL!
git reset --hard HEAD~1
```

---

## Support

If you encounter issues:
1. Check GitHub's [authentication documentation](https://docs.github.com/en/authentication)
2. Review GitHub's [quickstart guide](https://docs.github.com/en/get-started/quickstart)
3. Search [GitHub Community](https://github.community/)

---

**Ready to push!** Follow Option 1 above to get your code on GitHub.

Good luck! 🚀
