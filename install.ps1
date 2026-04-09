Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

Write-Host "=== spec-superpowers Quick Install ===" -ForegroundColor Cyan
Write-Host ""

# 1. OpenSpec CLI
Write-Host "[1/3] Installing OpenSpec CLI..."
if (Get-Command npm -ErrorAction SilentlyContinue) {
    try { npm install -g @fission-ai/openspec@latest }
    catch { Write-Host " ⚠ OpenSpec install failed. Please install Node.js first: https://nodejs.org/" -ForegroundColor Yellow }
} else {
    Write-Host " ⚠ npm not found. Please install Node.js first: https://nodejs.org/" -ForegroundColor Yellow
}

# 2. Install this Skill
Write-Host "[2/3] Installing spec-superpowers Skill..."
if (Get-Command npx -ErrorAction SilentlyContinue) {
    try { npx skills add CrDeemo/spec-superpowers --skill spec-superpowers --agent cursor --global --yes }
    catch { Write-Host " ⚠ Skill install failed. Try manually: npx skills add CrDeemo/spec-superpowers" -ForegroundColor Yellow }
} else {
    Write-Host " ⚠ npx not found. Please install Node.js first: https://nodejs.org/" -ForegroundColor Yellow
}

# 3. Dependency prompts
Write-Host "[3/3] Dependency check..."
Write-Host ""
Write-Host " Please ensure these Cursor Skills are installed:"
Write-Host " ─────────────────────────────────────"
Write-Host " Required:"
Write-Host "  • using-superpowers (with sub-skills)"
Write-Host "  • planning-with-files"
Write-Host " ─────────────────────────────────────"
Write-Host ""
Write-Host " Optional: copy gatekeeper rule"
Write-Host " Copy-Item .cursor\00-spec-superpowers.mdc <your-project>\.cursor\rules\"
Write-Host ""
Write-Host "=== Install complete. Restart Cursor, then type /spec-superpowers ===" -ForegroundColor Cyan
