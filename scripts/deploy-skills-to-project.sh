#!/bin/bash
# SpecMap Skills Deployment Script
# Automatically creates all SpecMap skills in your project

echo "======================================================"
echo "  SpecMap Skills Deployment"
echo "======================================================"
echo ""

# Get target project directory
if [ -z "$1" ]; then
    echo "Usage: ./deploy-skills-to-project.sh /path/to/your/project"
    echo ""
    echo "Example:"
    echo "  ./deploy-skills-to-project.sh /home/user/vortxx"
    echo ""
    exit 1
fi

PROJECT_DIR="$1"

# Verify project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Error: Directory not found: $PROJECT_DIR"
    exit 1
fi

echo "📁 Target project: $PROJECT_DIR"
echo ""

# Create skills directory
SKILLS_DIR="$PROJECT_DIR/.claude/skills"
mkdir -p "$SKILLS_DIR"

echo "✅ Created skills directory: $SKILLS_DIR"
echo ""
echo "📝 Creating skill files..."
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCE_SKILLS_DIR="$SCRIPT_DIR/../.claude/skills"

# Check if source skills exist
if [ -d "$SOURCE_SKILLS_DIR" ]; then
    echo "📋 Copying skills from: $SOURCE_SKILLS_DIR"
    cp -r "$SOURCE_SKILLS_DIR"/* "$SKILLS_DIR/"
    echo "✅ Skills copied successfully!"
else
    echo "⚠️  Source skills directory not found. Creating skills from templates..."

    # If we can't find the source, point to the repository
    echo ""
    echo "To get the skills, either:"
    echo "1. Clone the SpecMap repository:"
    echo "   git clone https://github.com/bsifflard77/specmap-mcp.git"
    echo "   cd specmap-mcp"
    echo "   cp -r .claude/skills/* $SKILLS_DIR/"
    echo ""
    echo "2. Or copy the skills folder manually from the SpecMap repository"
    exit 1
fi

echo ""
echo "======================================================"
echo "  ✅ Deployment Complete!"
echo "======================================================"
echo ""
echo "Skills installed in: $SKILLS_DIR"
echo ""
echo "Installed skills:"
ls -1 "$SKILLS_DIR" | grep "\.md$"
echo ""
echo "Next steps:"
echo "1. Open your project in Claude Code Desktop"
echo "2. Try: /skill specmap-reviewer"
echo "3. See docs/VORTXX-DEPLOYMENT-PLAN.md for usage guide"
echo ""
