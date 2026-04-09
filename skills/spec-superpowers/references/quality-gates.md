# Quality Gates

Four hard gates govern the pipeline. Nothing proceeds until all checks pass.

## Gate G0 — Session Recovery

| Field | Value |
|-------|-------|
| **Position** | After Phase 0 |
| **Pass** | 5-Question Reboot Test consistent + no context contradictions |
| **Fail** | Re-read planning files, re-test. Still inconsistent → ask user to resolve. |

Consistency checks: checked tasks ↔ progress.md, next task is logical continuation, goal ↔ spec, findings ↔ code state, no orphaned progress.

---

## Gate G1 — Specification → Planning

| Field | Value |
|-------|-------|
| **Position** | Phase 1 → Phase 2 |
| **Pass** | Brainstorming design approved + `openspec validate` passed + user confirmed final spec |
| **Fail** | Fix validation → revise spec → resubmit for confirmation |

Three conditions (all required):
1. Brainstorming design document approved by user (via `brainstorming` skill)
2. `openspec validate --change <name>` passes
3. User said "confirmed" / "approved" / "looks good" / "lgtm" for the final spec (ambiguous ≠ confirmed)

Failure path: brainstorming design rejected → iterate with user. Validate fails → fix structural issues. User requests changes → revise → re-validate. 3 rounds still failing → escalate to user.

---

## Gate G2 — Planning → Implementation

| Field | Value |
|-------|-------|
| **Position** | Phase 2 → Phase 3 |
| **Pass** | Files ready + every task annotated + writing-plans review loop passed |
| **Fail** | Fill plan gaps → re-review |

Required files: Full = task_plan.md + findings.md + progress.md. Light = task_plan.md + progress.md.
Every task needs: file paths + acceptance criteria + test strategy.
Plan-document-reviewer subagent must approve (max 3 rounds).

---

## Gate G3 — Implementation → Archive

| Field | Value |
|-------|-------|
| **Position** | Phase 3 → Phase 4 |
| **Pass** | All tests pass + two-stage review passed + evidence in progress.md |
| **Fail** | 3-Strike escalation protocol |

Two-stage review:
1. Spec conformance — does implementation match the spec?
2. Code quality — meets quality standards?

Evidence written via `verification-before-completion` skill.

---

## Review Loop Mechanism

All gates with reviews follow:

```
Phase complete → dispatch reviewer subagent → result
    ├─ Pass → gate clears
    └─ Fail → fix → re-review (max 3 rounds → escalate to user)
```

| Gate | Reviewer | Skill |
|------|----------|-------|
| G1 | brainstorming design review | `brainstorming` (Superpowers) |
| G2 | plan-document-reviewer | `writing-plans` |
| G3 | code-reviewer (two-stage) | `requesting-code-review` |

---

## 3-Strike Error Escalation (Phase 3)

```
Error → Strike 1: standard fix
      → Strike 2: check spec alignment (compare code vs openspec/ artifacts)
      → Strike 3: trigger systematic-debugging
                    → still unresolved → challenge architecture → escalate to user
```

Each strike logged in `progress.md`.

---

## Complexity Adjustment Protocol

AI monitors complexity fit throughout the workflow and proactively suggests adjustments. No dedicated commands — AI triggers these based on context.

### Light → Full (Upgrade)

| Current Phase | Action |
|---------------|--------|
| Phase 1 | Add full brainstorming (deep exploration). Re-run validate at G1. |
| Phase 2 | Generate `findings.md`. G2 requires all three files. |
| Phase 3 | Full review criteria for remaining work. |

Prior artifacts preserved — no rework. AI suggests upgrade when task exceeds Light criteria (more files than expected, new API surface, architecture implications).

### Full → Light (Downgrade)

| Current Phase | Action |
|---------------|--------|
| Phase 1 | Skip deep brainstorming exploration. |
| Phase 2 | Stop updating `findings.md`. G2 drops requirement. |
| Phase 3 | Light review criteria for remaining work. |

Existing artifacts kept but no longer required for gates. AI suggests downgrade when task is simpler than assessed or user requests simplification.
