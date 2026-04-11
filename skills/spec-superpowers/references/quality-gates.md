# Quality Gates

Four hard gates govern the pipeline. Nothing proceeds until all checks pass.

## Gate G0 — Session Recovery

Applies to Light and Full modes only. Quick mode skips session recovery.

| Field | Value |
|-------|-------|
| **Position** | After session recovery check |
| **Pass** | 5-Question Reboot Test consistent + Code Reality Check acknowledged + no unresolved contradictions |
| **Fail** | Re-read planning files, re-test. Still inconsistent → ask user to resolve. |

Consistency checks: checked tasks ↔ progress.md, next task is logical continuation, goal ↔ spec, findings ↔ code state, no orphaned progress.

Code Reality Check: verify `git diff` matches task completion status. Warnings require user acknowledgment before proceeding. Details: [references/planning-workflow.md](planning-workflow.md)

---

## Gate G1 — Specification → Planning

| Field | Value |
|-------|-------|
| **Position** | Step 3 → Step 4 |
| **Pass** | Brainstorming design approved + `openspec validate` passed + user confirmed final spec |
| **Fail** | Fix validation → revise spec → resubmit for confirmation |

Three conditions (all required):
1. Brainstorming design document approved by user (via `brainstorming` skill)
2. `openspec validate --change <name>` passes
3. User said "confirmed" / "approved" / "looks good" / "lgtm" for the final spec (ambiguous ≠ confirmed)

Failure path: brainstorming design rejected → iterate with user. Validate fails → fix structural issues. User requests changes → revise → re-validate. 3 rounds still failing → escalate to user.

---

## Quick Mode Gates

Quick mode uses two lightweight gates instead of the full G0-G3 pipeline.

### Gate G1-Quick — Inline Spec Confirmation

| Field | Value |
|-------|-------|
| **Position** | Before implementation |
| **Pass** | AI stated what + why + scope in 2-3 sentences, user explicitly confirmed |
| **Fail** | Clarify scope → re-state → re-confirm. If task grows beyond Quick criteria → suggest upgrade to Light/Full. |

No OpenSpec artifacts, no brainstorming skill. The inline spec lives only in the chat conversation.

### Gate G3-Quick — Implementation Done

| Field | Value |
|-------|-------|
| **Position** | After implementation |
| **Pass** | Tests pass (if applicable) + single-round code review (AI self-review or `requesting-code-review`) |
| **Fail** | Fix → re-review. 2 failures → suggest upgrading to Light mode for more structure. |

No progress.md evidence required. No two-stage review. No `verification-before-completion` skill mandatory (recommended but optional).

---

## Gate G2 — Planning → Implementation

| Field | Value |
|-------|-------|
| **Position** | Step 4 → Step 5 |
| **Pass** | Files ready + every task annotated + writing-plans review loop passed |
| **Fail** | Fill plan gaps → re-review |

Required files: Full = task_plan.md + findings.md + progress.md. Light = task_plan.md + progress.md.
Every task needs: file paths + acceptance criteria + test strategy.
Plan-document-reviewer subagent must approve (max 3 rounds).

---

## Gate G3 — Implementation → Archive

| Field | Value |
|-------|-------|
| **Position** | Step 5 → Step 6 |
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
Step complete → dispatch reviewer subagent → result
    ├─ Pass → gate clears
    └─ Fail → fix → re-review (max 3 rounds → escalate to user)
```

| Gate | Reviewer | Skill |
|------|----------|-------|
| G1 | brainstorming design review | `brainstorming` (Superpowers) |
| G2 | plan-document-reviewer | `writing-plans` |
| G3 | code-reviewer (two-stage) | `requesting-code-review` |

---

## 3-Strike Error Escalation (Step 5)

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

### Quick → Light/Full (Upgrade)

AI suggests upgrade when:
- Task touches more than one file
- New API surface or exported interface emerges
- Implementation reveals unexpected complexity

Action: Stop current work. Create task workspace in `.spec-tasks/`. Begin at Step 1 (full brainstorming) if not already done, or Step 3 (OpenSpec formalize) if brainstorming is complete. Inline spec from chat serves as starting context — no rework.

### Light → Full (Upgrade)

| Current Step | Action |
|--------------|--------|
| Step 3 | Re-run validate at G1 (brainstorming already full — no change needed). |
| Step 4 | Generate `findings.md`. G2 requires all three files. |
| Step 5 | Full review criteria for remaining work. |

Prior artifacts preserved — no rework. AI suggests upgrade when task exceeds Light criteria (more files than expected, new API surface, architecture implications).

### Full → Light (Downgrade)

| Current Step | Action |
|--------------|--------|
| Step 3 | No change (brainstorming already complete). |
| Step 4 | Stop updating `findings.md`. G2 drops requirement. |
| Step 5 | Light review criteria for remaining work. |

Existing artifacts kept but no longer required for gates. AI suggests downgrade when task is simpler than assessed or user requests simplification.
