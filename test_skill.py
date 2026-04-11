#!/usr/bin/env python3
"""Validation script for the spec-superpowers skill (~70 checks across 12 categories)."""

import os
import re
import sys
from pathlib import Path

SKILL_DIR = Path(os.environ.get("SKILL_DIR", "skills/spec-superpowers"))
SKILLS_ROOT = Path(
    os.environ.get("SKILLS_ROOT", os.path.expanduser("~/.cursor/skills"))
)

passed = 0
failed = 0
current_category = ""


def category(name: str) -> None:
    global current_category
    current_category = name
    print(f"\n{name}")


def check(description: str, condition: bool) -> None:
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS: {description}")
    else:
        failed += 1
        print(f"  FAIL: {description}")


# ---------------------------------------------------------------------------
# Category 1 — File existence
# ---------------------------------------------------------------------------
category("Category 1: File existence")

skill_md = SKILL_DIR / "SKILL.md"
check("SKILL.md exists", skill_md.is_file())

skill_text = skill_md.read_text(encoding="utf-8") if skill_md.is_file() else ""

# ---------------------------------------------------------------------------
# Category 2 — YAML frontmatter
# ---------------------------------------------------------------------------
category("Category 2: YAML frontmatter")

fm_match = re.match(r"^---\n(.*?)\n---", skill_text, re.DOTALL)
check("Frontmatter present", fm_match is not None)

fm_text = fm_match.group(1) if fm_match else ""

check("'name:' field present", "name:" in fm_text)
check("'description:' field present", "description:" in fm_text)

name_match = re.search(r"^name:\s*(.+)", fm_text, re.MULTILINE)
name_value = name_match.group(1).strip() if name_match else ""
check("name = 'ssp'", name_value == "ssp")

check("Trigger '/ssp' in description", "/ssp" in fm_text)
check("Trigger 'spec first' in description", "spec first" in fm_text)

forbidden_fields = ["version:", "license:", "author:", "compatibility:"]
for field in forbidden_fields:
    check(f"No forbidden field '{field}'", field not in fm_text)

# ---------------------------------------------------------------------------
# Category 3 — references/ directory
# ---------------------------------------------------------------------------
category("Category 3: references/ directory")

refs_dir = SKILL_DIR / "references"
check("references/ directory exists", refs_dir.is_dir())

ref_files = [
    "openspec-workflow.md",
    "planning-workflow.md",
    "quality-gates.md",
    "integration-guide.md",
]
for rf in ref_files:
    rp = refs_dir / rf
    check(f"{rf} exists", rp.is_file())
    check(f"{rf} > 100 bytes", rp.is_file() and rp.stat().st_size > 100)

# ---------------------------------------------------------------------------
# Category 4 — assets/ directory
# ---------------------------------------------------------------------------
category("Category 4: assets/ directory")

constitution = SKILL_DIR / "assets" / "templates" / "constitution.md"
check("assets/templates/constitution.md exists", constitution.is_file())

# ---------------------------------------------------------------------------
# Category 5 — Internal links
# ---------------------------------------------------------------------------
category("Category 5: Internal links")

link_pattern = re.compile(r"\]\(((?:references|assets)/[^)]+)\)")
links_found = link_pattern.findall(skill_text)
check("At least one internal link found", len(links_found) > 0)
for link in links_found:
    target = SKILL_DIR / link
    check(f"Link resolves: {link}", target.is_file())

# ---------------------------------------------------------------------------
# Category 6 — Key content (commands + structure)
# ---------------------------------------------------------------------------
category("Category 6: Key content")

lower_text = skill_text.lower()
check("Contains '/ssp' command", "/ssp" in skill_text)
check("Contains '/ssp:design' command", "/ssp:design" in skill_text)
check("Contains '/ssp:plan' command", "/ssp:plan" in skill_text)
check("Contains '/ssp:impl' command", "/ssp:impl" in skill_text)
check(
    "Contains complexity triage ('light' or 'triage' or 'complexity')",
    any(w in lower_text for w in ["light", "triage", "complexity"]),
)
check(
    "Contains step-based structure ('step 1' or 'step 2')",
    "step 1" in lower_text or "step 2" in lower_text,
)

# ---------------------------------------------------------------------------
# Category 7 — Line limit
# ---------------------------------------------------------------------------
category("Category 7: Line limit")

line_count = len(skill_text.splitlines()) if skill_text else 0
check(f"SKILL.md <= 120 lines (actual: {line_count})", line_count <= 120)

# ---------------------------------------------------------------------------
# Category 8 — No redundant concepts
# ---------------------------------------------------------------------------
category("Category 8: No redundant concepts")

redundant = ["TDD-First", "RED-GREEN-REFACTOR", "Clean Code", "SOLID", "DRY", "KISS"]
for concept in redundant:
    check(f"Does not contain '{concept}'", concept not in skill_text)

# ---------------------------------------------------------------------------
# Category 9 — Core features
# ---------------------------------------------------------------------------
category("Category 9: Core features")

check(
    "Three-level complexity (Quick/Light/Full)",
    "quick" in lower_text and "light" in lower_text and "full" in lower_text,
)
check(
    "Dialogue-first principle mentioned",
    "dialogue" in lower_text or "brainstorming" in lower_text,
)
check(
    "Brainstorming NEVER shortened for Light",
    "never" in lower_text and ("shortened" in lower_text or "abbreviated" in lower_text),
)
check(
    "Session recovery mentioned",
    "session recovery" in lower_text or ("session" in lower_text and "recover" in lower_text),
)
check(
    "Quality gates mentioned (G1 or Gate)",
    "g1" in lower_text or "gate" in lower_text,
)
check(
    "5-Question or Reboot mentioned",
    "5-question" in lower_text or "reboot" in lower_text,
)
check("Review loop mentioned", "review" in lower_text and "loop" in lower_text)
check("3-Strike mentioned", "3-strike" in lower_text or "3-Strike" in skill_text)
check("Subagent mentioned", "subagent" in lower_text)
check(
    "Archive mentioned",
    "archive" in lower_text,
)
check(
    "Post-dialogue complexity (triage after brainstorming)",
    "post-dialogue" in lower_text or "after brainstorming" in lower_text,
)

# ---------------------------------------------------------------------------
# Category 10 — Task Workspace
# ---------------------------------------------------------------------------
category("Category 10: Task Workspace")

check(
    "SKILL.md mentions .spec-tasks or task workspace",
    ".spec-tasks" in skill_text or "task workspace" in lower_text or "task router" in lower_text,
)
check(
    "SKILL.md mentions _active.txt",
    "_active.txt" in skill_text,
)
check(
    "SKILL.md mentions copy-swap",
    "copy-swap" in lower_text or ("copy" in lower_text and "swap" in lower_text),
)
check(
    "SKILL.md mentions /ssp:switch command",
    "/ssp:switch" in skill_text,
)

planning_wf = refs_dir / "planning-workflow.md"
planning_text = planning_wf.read_text(encoding="utf-8") if planning_wf.is_file() else ""
planning_lower = planning_text.lower()

check(
    "planning-workflow.md mentions copy-swap protocol",
    "copy-swap" in planning_lower,
)
check(
    "planning-workflow.md mentions hook system",
    "hook" in planning_lower,
)
check(
    "planning-workflow.md mentions writing-plans vs planning-with-files responsibilities",
    "author" in planning_lower and "runtime" in planning_lower,
)

# ---------------------------------------------------------------------------
# Category 11 — OpenSpec validate/archive + complexity adjustment
# ---------------------------------------------------------------------------
category("Category 11: validate/archive/complexity adjustment")

check(
    "SKILL.md mentions openspec validate",
    "openspec validate" in lower_text or "validate" in lower_text,
)
check(
    "SKILL.md mentions complexity adjustment",
    ("light" in lower_text and "full" in lower_text)
    and ("upgrade" in lower_text or "downgrade" in lower_text or "adjustment" in lower_text),
)

openspec_wf = refs_dir / "openspec-workflow.md"
openspec_text = openspec_wf.read_text(encoding="utf-8") if openspec_wf.is_file() else ""
openspec_lower = openspec_text.lower()

check(
    "openspec-workflow.md mentions openspec validate",
    "openspec validate" in openspec_lower,
)
check(
    "openspec-workflow.md mentions openspec archive",
    "openspec archive" in openspec_lower,
)
check(
    "openspec-workflow.md mentions Quick mode skips OpenSpec",
    "quick" in openspec_lower and "skip" in openspec_lower,
)
check(
    "openspec-workflow.md mentions brainstorming never shortened",
    "never" in openspec_lower and ("shortened" in openspec_lower or "abbreviated" in openspec_lower),
)

quality_gates = refs_dir / "quality-gates.md"
qg_text = quality_gates.read_text(encoding="utf-8") if quality_gates.is_file() else ""
qg_lower = qg_text.lower()

check(
    "quality-gates.md mentions openspec validate in G1",
    "openspec validate" in qg_lower,
)
check(
    "quality-gates.md mentions complexity adjustment transitions",
    ("light" in qg_lower and "full" in qg_lower)
    and ("upgrade" in qg_lower or "downgrade" in qg_lower or "adjustment" in qg_lower),
)

# ---------------------------------------------------------------------------
# Category 12 — Dependency skills installed (expected to fail locally)
# ---------------------------------------------------------------------------
category("Category 12: Dependency skills installed")

dep_skills = [
    "using-superpowers",
    "planning-with-files",
    "brainstorming",
    "writing-plans",
    "test-driven-development",
    "verification-before-completion",
    "systematic-debugging",
]
for skill_name in dep_skills:
    skill_path = SKILLS_ROOT / skill_name / "SKILL.md"
    check(f"{skill_name} installed at SKILLS_ROOT", skill_path.is_file())

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("\n========================================")
print(f"Results: {passed} passed, {failed} failed")
sys.exit(0 if failed == 0 else 1)
