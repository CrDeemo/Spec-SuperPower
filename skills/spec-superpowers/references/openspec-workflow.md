# OpenSpec Workflow

How spec-superpowers invokes brainstorming (Superpowers) + OpenSpec for specification (Step 3) and archiving (Step 6).

## Applicability

| Mode | Brainstorming (Step 1) | OpenSpec (Step 3) | Archive (Step 6) |
|------|----------------------|-------------------|-------------------|
| **Quick** | Brief confirmation (2-3 sentences) | **Skipped** — inline spec only | Clear `_active.txt` only |
| **Light** | **Full** (never shortened) | propose + validate + confirm | `openspec archive` + copy-swap |
| **Full** | **Full** | propose + validate + confirm | `openspec archive` + copy-swap |

## Spec Artifact Location

All artifacts in `openspec/` at project root. Each task maps to one OpenSpec change:

```
openspec/changes/
  feat-user-auth/       ← task "feat-user-auth"
  fix-login-bug/        ← task "fix-login-bug"
```

Task name from `.spec-tasks/_active.txt` = change name. Managed natively by OpenSpec.

## Specification Flow (Light and Full)

```
brainstorming design approved → /opsx:propose → openspec validate → User Confirmation
```

1. **Brainstorm** — Invoke the `brainstorming` skill (Superpowers). Explore context, ask clarifying questions one at a time, propose 2-3 approaches with trade-offs, present recommended design, wait for user approval. Output: design document. Brainstorming is identical for Light and Full — understanding the user is never abbreviated.
2. **Propose** — `/opsx:propose` to formalize the approved design into an OpenSpec change proposal + spec artifacts in `openspec/`
3. **Validate** — `openspec validate --change <name>` for structural completeness. Fix errors first.
4. **Confirm** — Present final spec to user, wait for explicit confirmation

## Spec Confirmation Protocol

User must explicitly approve. Acceptable: "confirmed", "approved", "looks good", "lgtm", or equivalent affirmative. Ambiguous responses ("maybe", "I guess") do not count — ask again.

## Brainstorming Review Loop

After spec is written and validated, before user confirmation:

```
Spec written → openspec validate → dispatch spec-document-reviewer subagent
    ├─ Pass → present to user for confirmation
    └─ Fail → revise → re-validate → re-review (max 3 rounds → escalate to user)
```

Reviewer evaluates completeness, clarity, and feasibility against the brainstorming design document.

## Gate G1 Clearance

All three required:
1. Brainstorming design document approved by user
2. `openspec validate --change <name>` passes
3. User explicitly confirmed final spec

On user change request: revise → re-validate → re-review → resubmit for confirmation.

## Step 6: Archive

After G3 passes:

```
openspec archive <change-name>
```

Merges change delta into main specs. Then: copy root planning files to `.spec-tasks/<task>/` → clean root files + `_active.txt`.

Quick mode: no OpenSpec archive — just clear `_active.txt`.

## Loose Coupling

References only stable interfaces: `brainstorming` skill (Superpowers), `/opsx:propose`, `/opsx:verify`, and `openspec/` directory convention. No internal CLI parameters or config formats.
