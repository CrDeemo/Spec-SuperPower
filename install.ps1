Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

Write-Host "=== spec-superpowers Quick Install ===" -ForegroundColor Cyan
Write-Host ""

# 1. OpenSpec CLI (global - it's a CLI tool, like npm/git)
Write-Host "[1/4] Installing OpenSpec CLI..."
if (Get-Command npm -ErrorAction SilentlyContinue) {
    try { npm install -g @fission-ai/openspec@latest }
    catch { Write-Host " Warning: OpenSpec install failed. Please install Node.js first: https://nodejs.org/" -ForegroundColor Yellow }
} else {
    Write-Host " Warning: npm not found. Please install Node.js first: https://nodejs.org/" -ForegroundColor Yellow
}

# 2. Install spec-superpowers skill (project-level)
Write-Host "[2/4] Installing spec-superpowers skill..."
if (Get-Command npx -ErrorAction SilentlyContinue) {
    try { npx skills add CrDeemo/Spec-SuperPower --skill spec-superpowers --agent cursor --yes }
    catch { Write-Host " Warning: Skill install failed. Try manually: npx skills add CrDeemo/Spec-SuperPower --skill spec-superpowers --agent cursor --yes" -ForegroundColor Yellow }
} else {
    Write-Host " Warning: npx not found. Please install Node.js first: https://nodejs.org/" -ForegroundColor Yellow
}

# 3. Install planning-with-files skill (project-level)
Write-Host "[3/4] Installing planning-with-files skill..."
if (Get-Command npx -ErrorAction SilentlyContinue) {
    try { npx skills add OthmanAdi/planning-with-files --agent cursor --yes }
    catch { Write-Host " Warning: planning-with-files install failed. Try manually: npx skills add OthmanAdi/planning-with-files --agent cursor --yes" -ForegroundColor Yellow }
} else {
    Write-Host " Warning: npx not found." -ForegroundColor Yellow
}

# 4. Copy gatekeeper rule
Write-Host "[4/4] Setting up gatekeeper rule..."
$gatekeeperSrc = ".cursor\skills\spec-superpowers\.cursor\00-spec-superpowers.mdc"
if (Test-Path $gatekeeperSrc) {
    New-Item -ItemType Directory -Force -Path ".cursor\rules" | Out-Null
    Copy-Item $gatekeeperSrc ".cursor\rules\" -ErrorAction SilentlyContinue
    Write-Host " Done: Gatekeeper rule installed." -ForegroundColor Green
} else {
    Write-Host " Warning: Skill directory not found, skipping gatekeeper rule." -ForegroundColor Yellow
    Write-Host "   After install, manually copy: .cursor\skills\spec-superpowers\.cursor\00-spec-superpowers.mdc to .cursor\rules\"
}

Write-Host ""
Write-Host " -----------------------------------------"
Write-Host " Remaining manual step:"
Write-Host "  - Install 'Superpowers' from the Cursor plugin marketplace"
Write-Host " -----------------------------------------"
Write-Host ""
Write-Host "=== Install complete. Restart Cursor, then type /spec-superpowers ===" -ForegroundColor Cyan
