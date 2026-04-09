# spec-superpowers

A Cursor Agent Skill that orchestrates **OpenSpec** + **planning-with-files** + **Superpowers** into a unified spec-driven development workflow. Loosely coupled — uninstalling does not affect independent modules.

## Install

```bash
# Interactive
npx skills add CrDeemo/spec-superpowers

# Non-interactive (CI / new project)
npx skills add CrDeemo/spec-superpowers --skill spec-superpowers --agent cursor --global --yes
```

## Dependency Skills

| Dependency | Install |
|---|---|
| **using-superpowers** | Cursor plugin marketplace (Superpowers) |
| **planning-with-files** | `npx skills add OthmanAdi/planning-with-files` |
| **OpenSpec CLI** | `npm install -g @fission-ai/openspec` |

All three must be installed for the full workflow. Each works independently.

## Usage

| Command | Effect |
|---|---|
| `/spec-superpowers` | Smart full workflow (auto complexity) |
| `/spec-superpowers spec` | OpenSpec specification phase only |
| `/spec-superpowers plan` | planning-with-files planning phase only |
| `/spec-superpowers impl` | Superpowers implementation phase only |
| `/spec-superpowers reset` | Reset complexity choice and state |

## How It Works

```
User describes task
    │
    ▼
Complexity Triage (Light / Full)
    │
    ▼
Phase 1 — Specification (OpenSpec)
    │── Gate G1: user confirmed spec
    ▼
Phase 2 — Planning (planning-with-files)
    │── Gate G2: plan files ready
    ▼
Phase 3 — Implementation (Superpowers)
    │── Gate G3: tests pass + review passed
    ▼
Phase 4 — Archive & finish
```

## Architecture

- **Thin orchestration layer** — SKILL.md describes "who to call, what to expect", never inlines module internals
- **Loose coupling** — references stable interfaces only; zero path coupling; orchestration is purely descriptive
- **Hard quality gates** — four gates (G0–G3) with review loops (max 3 rounds) before any phase transition
- **Always-on gatekeeper** — `.cursor/00-spec-superpowers.mdc` blocks coding without a confirmed spec

## Project Structure

```
spec-superpowers/
├── skills/
│   └── spec-superpowers/
│       ├── SKILL.md
│       ├── references/
│       │   ├── openspec-workflow.md
│       │   ├── planning-workflow.md
│       │   ├── quality-gates.md
│       │   └── integration-guide.md
│       └── assets/
│           └── templates/
│               └── constitution.md
├── .cursor/
│   └── 00-spec-superpowers.mdc
├── install.sh
├── install.ps1
├── test_skill.py
└── README.md
```

## Uninstall

```bash
npx skills remove spec-superpowers
```

Removing spec-superpowers only removes the orchestration layer. OpenSpec, planning-with-files, and Superpowers continue to work independently.

---

Built by CrDeemo · 2026
