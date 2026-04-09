# OpenSpec Workflow

This file describes how spec-superpowers invokes OpenSpec for specification authoring (Phase 1) and archiving (Phase 4). OpenSpec is the fixed spec mode — there is no dual-mode switching.

## Spec Artifact Location

All spec artifacts are stored in the `openspec/` directory at the project root. This is the standard OpenSpec output location.

### Multi-Change Support

OpenSpec natively supports multiple changes via `openspec/changes/<name>/`. Each task workspace in spec-superpowers maps to one OpenSpec change:

```
openspec/
  changes/
    feat-user-auth/       ← task "feat-user-auth"
    fix-login-bug/        ← task "fix-login-bug"
```

The task name from `.spec-tasks/_active.txt` is used as the change name. This is managed natively by OpenSpec — spec-superpowers does not move or copy these directories.

## Full Mode Flow

Full mode is used for new features, refactors, and multi-file changes.

```
/opsx:explore  →  /opsx:propose  →  openspec validate  →  User Confirmation
   │                   │                    │                     │
   ▼                   ▼                    ▼                     ▼
 Ideation &       Create change        Check spec            User must say
 investigation    proposal + gen       structural             "confirmed" /
                  spec artifacts       completeness           "approved" /
                  into openspec/                              "looks good"
```

1. **Explore** — Invoke `/opsx:explore` to investigate the problem space, gather context, and brainstorm approaches.
2. **Propose** — Invoke `/opsx:propose` to create a concrete change proposal and generate spec artifacts into `openspec/`.
3. **Validate** — Run `openspec validate --change <name>` to check structural completeness. Fix any errors before proceeding.
4. **Confirm** — Present the spec to the user and wait for explicit confirmation.

## Light Mode Flow

Light mode is used for single-file bugfixes, config changes, and typos.

```
/opsx:propose  →  openspec validate  →  User Confirmation
      │                  │                     │
      ▼                  ▼                     ▼
  One-step           Check spec            Explicit
  proposal +         structural            user approval
  spec artifacts     completeness          required
```

1. **Propose** — Invoke `/opsx:propose` directly (skip explore).
2. **Validate** — Run `openspec validate --change <name>`. Fix errors if any.
3. **Confirm** — Present the spec to the user and wait for explicit confirmation.

## Spec Confirmation Protocol

The user must explicitly approve the spec before Gate G1 can pass. Acceptable confirmations include:

- "confirmed"
- "approved"
- "looks good"
- "lgtm"
- Or any equivalent affirmative statement

Ambiguous responses (e.g., "maybe", "I guess") do **not** count. If the response is unclear, ask the user to confirm explicitly.

## Brainstorming Review Loop

After the spec is written and validated, before requesting user confirmation, dispatch a quality review:

```
Spec written → openspec validate → dispatch spec-document-reviewer subagent → review result
    ├─ Pass → present spec to user for confirmation
    └─ Fail → revise spec based on feedback → re-validate → re-review
               (max 3 rounds)
               └─ Still failing after 3 rounds → escalate to user
```

The reviewer subagent evaluates the spec for completeness, clarity, and feasibility. This uses the `brainstorming` skill from Superpowers.

## Gate G1 Clearance

Gate G1 passes when **all three** conditions are met:

1. `openspec validate --change <name>` passes with no errors
2. The brainstorming review loop has passed (reviewer subagent approved)
3. The user has explicitly confirmed the spec

If the user requests changes, revise the spec, re-run validate + review loop, and resubmit for confirmation.

## Phase 4: Archive with OpenSpec

After implementation is complete and G3 passes, Phase 4 includes archiving the OpenSpec change:

```
openspec archive <change-name>
```

This merges the change delta into the main specs. After archiving:
1. The change in `openspec/changes/<name>/` is merged into the main spec
2. Root planning files are copied back to `.spec-tasks/<task>/` for history
3. Root planning files and `_active.txt` are cleaned up

## Important: Loose Coupling

This workflow references only OpenSpec's stable interface:

- **Commands**: `/opsx:explore`, `/opsx:propose`, `/opsx:verify`
- **Directory convention**: `openspec/`

Do NOT inline CLI parameters, internal config file formats, or any implementation details of OpenSpec itself. If OpenSpec's internal behavior changes, this workflow remains valid as long as the command names and directory convention are preserved.
