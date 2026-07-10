#!/usr/bin/env bash
# uninstall.sh — Remove geo-audit-skill
set -euo pipefail

INSTALL_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills/geo-audit}"

if [ -d "$INSTALL_DIR" ]; then
  echo "Removing $INSTALL_DIR..."
  rm -rf "$INSTALL_DIR"
  echo "✅ geo-audit-skill uninstalled"
else
  echo "geo-audit-skill not found at $INSTALL_DIR"
fi
