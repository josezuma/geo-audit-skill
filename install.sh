#!/usr/bin/env bash
# install.sh — One-command install for geo-audit-skill
set -euo pipefail

REPO="josezuma/geo-audit-skill"
INSTALL_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills/geo-audit}"
VENV_DIR="$INSTALL_DIR/.venv"

echo "📦 Installing geo-audit-skill..."

# Clone or update
if [ -d "$INSTALL_DIR" ]; then
  echo "  Updating existing install at $INSTALL_DIR"
  cd "$INSTALL_DIR" && git pull
else
  echo "  Cloning to $INSTALL_DIR"
  git clone "https://github.com/$REPO.git" "$INSTALL_DIR"
fi

# Create venv
echo "  Setting up Python virtual environment..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
pip install -q requests beautifulsoup4

echo ""
echo "✅ geo-audit-skill installed!"
echo ""
echo "Quick start:"
echo "  cd $INSTALL_DIR"
echo "  source .venv/bin/activate"
echo "  python scripts/audit.py https://yoursite.com"
echo ""
echo "Or use as a Claude Code skill:"
echo "  claude code --skill $INSTALL_DIR"
