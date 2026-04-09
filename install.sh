#!/bin/bash
set -e

echo "=== spec-superpowers Quick Install ==="
echo ""

# 1. OpenSpec CLI (global — it's a CLI tool, like npm/git)
echo "[1/4] Installing OpenSpec CLI..."
if command -v npm >/dev/null 2>&1; then
  npm install -g @fission-ai/openspec@latest || echo " ⚠ OpenSpec install failed. Please install Node.js first: https://nodejs.org/"
else
  echo " ⚠ npm not found. Please install Node.js first: https://nodejs.org/"
fi

# 2. Install spec-superpowers skill (project-level)
echo "[2/4] Installing spec-superpowers skill..."
if command -v npx >/dev/null 2>&1; then
  npx skills add CrDeemo/Spec-SuperPower --skill spec-superpowers --agent cursor --yes || echo " ⚠ Skill install failed. Try manually: npx skills add CrDeemo/Spec-SuperPower --skill spec-superpowers --agent cursor --yes"
else
  echo " ⚠ npx not found. Please install Node.js first: https://nodejs.org/"
fi

# 3. Install planning-with-files skill (project-level)
echo "[3/4] Installing planning-with-files skill..."
if command -v npx >/dev/null 2>&1; then
  npx skills add OthmanAdi/planning-with-files --agent cursor --yes || echo " ⚠ planning-with-files install failed. Try manually: npx skills add OthmanAdi/planning-with-files --agent cursor --yes"
else
  echo " ⚠ npx not found."
fi

# 4. Copy gatekeeper rule
echo "[4/4] Setting up gatekeeper rule..."
if [ -d ".cursor/skills/spec-superpowers/.cursor" ]; then
  mkdir -p .cursor/rules
  cp .cursor/skills/spec-superpowers/.cursor/00-spec-superpowers.mdc .cursor/rules/ 2>/dev/null && \
    echo " ✓ Gatekeeper rule installed." || \
    echo " ⚠ Could not copy gatekeeper rule. You can copy it manually later."
else
  echo " ⚠ Skill directory not found, skipping gatekeeper rule."
  echo "   After install, manually copy: .cursor/skills/spec-superpowers/.cursor/00-spec-superpowers.mdc → .cursor/rules/"
fi

echo ""
echo " ─────────────────────────────────────"
echo " Remaining manual step:"
echo "  • Install 'Superpowers' from the Cursor plugin marketplace"
echo " ─────────────────────────────────────"
echo ""
echo "=== Install complete. Restart Cursor, then type /spec-superpowers ==="
