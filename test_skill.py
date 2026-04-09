#!/usr/bin/env python3
"""Validation script for the spec-superpowers skill (~60 checks across 10 categories)."""

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

# Load content once for later categories
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
check("name = 'spec-superpowers'", name_value == "spec-superpowers")

fm_and_desc = fm_text
check("Trigger '/spec-superpowers' in description", "/spec-superpowers" in fm_and_desc)
check("Trigger 'spec first' in description", "spec first" in fm_and_desc)

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
# Category 6 — Key content
# ---------------------------------------------------------------------------
category("Category 6: Key content")

lower_text = skill_text.lower()
check("Contains '/spec-superpowers' command", "/spec-superpowers" in skill_text)
check(
    "Contains complexity triage ('light' or 'triage' or 'complexity')",
    any(w in lower_text for w in ["light", "triage", "complexity"]),
)
check(
    "Contains pipeline phases ('phase' or 'pipeline')",
    any(w in lower_text for w in ["phase", "pipeline"]),
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
    "Two-level complexity mentioned",
    "light" in lower_text and "full" in lower_text,
)
check(
    "Session recovery mentioned",
    "session recovery" in lower_text or "session" in lower_text and "recover" in lower_text,
)
check(
    "Quality gates mentioned (G0 or G1)",
    "g0" in lower_text or "G0" in skill_text or "g1" in lower_text or "G1" in skill_text,
)
check(
    "5-Question or Reboot mentioned",
    "5-question" in lower_text or "reboot" in lower_text,
)
check("Review loop mentioned", "review" in lower_text and "loop" in lower_text)
check("3-Strike mentioned", "3-strike" in lower_text or "3-Strike" in skill_text)
check("Subagent mentioned", "subagent" in lower_text)
check(
    "Finishing / archive mentioned",
    "finishing" in lower_text or "archive" in lower_text,
)
check(
    "systematic-debugging or 3-Strike mentioned",
    "systematic-debugging" in lower_text or "3-strike" in lower_text,
)

# ---------------------------------------------------------------------------
# Category 10 — Dependency skills installed
# ---------------------------------------------------------------------------
category("Category 10: Dependency skills installed")

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
