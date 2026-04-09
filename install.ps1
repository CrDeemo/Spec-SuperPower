Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

Write-Host "=== spec-superpowers Quick Install ===" -ForegroundColor Cyan
Write-Host ""

# 1. OpenSpec CLI (global - it's a CLI tool, like npm/git)
Write-Host "[1/5] Installing OpenSpec CLI..."
if (Get-Command npm -ErrorAction SilentlyContinue) {
    try { npm install -g @fission-ai/openspec@latest }
    catch { Write-Host " Warning: OpenSpec install failed. Please install Node.js first: https://nodejs.org/" -ForegroundColor Yellow }
} else {
    Write-Host " Warning: npm not found. Please install Node.js first: https://nodejs.org/" -ForegroundColor Yellow
}

# 2. Install spec-superpowers skill (project-level)
Write-Host "[2/5] Installing spec-superpowers skill..."
if (Get-Command npx -ErrorAction SilentlyContinue) {
    try { npx skills add CrDeemo/Spec-SuperPower --skill spec-superpowers --agent cursor --yes }
    catch { Write-Host " Warning: Skill install failed. Try manually: npx skills add CrDeemo/Spec-SuperPower --skill spec-superpowers --agent cursor --yes" -ForegroundColor Yellow }
} else {
    Write-Host " Warning: npx not found. Please install Node.js first: https://nodejs.org/" -ForegroundColor Yellow
}

# 3. Install planning-with-files skill (project-level)
Write-Host "[3/5] Installing planning-with-files skill..."
if (Get-Command npx -ErrorAction SilentlyContinue) {
    try { npx skills add OthmanAdi/planning-with-files --agent cursor --yes }
    catch { Write-Host " Warning: planning-with-files install failed. Try manually: npx skills add OthmanAdi/planning-with-files --agent cursor --yes" -ForegroundColor Yellow }
} else {
    Write-Host " Warning: npx not found." -ForegroundColor Yellow
}

# 4. Copy gatekeeper rule
Write-Host "[4/5] Setting up gatekeeper rule..."
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

# 5. Append recommended .gitignore entries
Write-Host "[5/5] Updating .gitignore..."
$gitignoreMarker = "# spec-superpowers workflow artifacts"
$gitignoreBlock = @"

# spec-superpowers workflow artifacts
.spec-tasks/
task_plan.md
findings.md
progress.md

# Superpowers artifacts
.superpowers/
docs/superpowers/
"@

if (Test-Path ".gitignore") {
    $content = Get-Content ".gitignore" -Raw -ErrorAction SilentlyContinue
    if ($content -and $content.Contains($gitignoreMarker)) {
        Write-Host " Done: .gitignore already configured." -ForegroundColor Green
    } else {
        Add-Content -Path ".gitignore" -Value $gitignoreBlock
        Write-Host " Done: .gitignore updated." -ForegroundColor Green
    }
} else {
    Set-Content -Path ".gitignore" -Value $gitignoreBlock.TrimStart()
    Write-Host " Done: .gitignore created." -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Install complete. Restart Cursor, then type /spec-superpowers ===" -ForegroundColor Cyan
