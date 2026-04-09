#!/bin/bash
set -e

echo "=== spec-superpowers Quick Install ==="
echo ""

# 1. OpenSpec CLI
echo "[1/3] Installing OpenSpec CLI..."
if command -v npm >/dev/null 2>&1; then
  npm install -g @fission-ai/openspec@latest || echo " ⚠ OpenSpec install failed. Please install Node.js first: https://nodejs.org/"
else
  echo " ⚠ npm not found. Please install Node.js first: https://nodejs.org/"
fi

# 2. Install this Skill
echo "[2/3] Installing spec-superpowers Skill..."
if command -v npx >/dev/null 2>&1; then
  npx skills add CrDeemo/spec-superpowers --skill spec-superpowers --agent cursor --global --yes || echo " ⚠ Skill install failed. Try manually: npx skills add CrDeemo/spec-superpowers"
else
  echo " ⚠ npx not found. Please install Node.js first: https://nodejs.org/"
fi

# 3. Dependency prompts
echo "[3/3] Dependency check..."
echo ""
echo " Please ensure these Cursor Skills are installed:"
echo " ─────────────────────────────────────"
echo " Required:"
echo "  • using-superpowers (with sub-skills)"
echo "  • planning-with-files"
echo " ─────────────────────────────────────"
echo ""
echo " Optional: copy gatekeeper rule"
echo " cp .cursor/00-spec-superpowers.mdc <your-project>/.cursor/rules/"
echo ""
echo "=== Install complete. Restart Cursor, then type /spec-superpowers ==="
