# OpenSpec Workflow

This file describes how spec-superpowers invokes OpenSpec for specification authoring (Phase 1). OpenSpec is the fixed spec mode — there is no dual-mode switching.

## Spec Artifact Location

All spec artifacts are stored in the `openspec/` directory at the project root. This is the standard OpenSpec output location.

## Full Mode Flow

Full mode is used for new features, refactors, and multi-file changes.

```
/opsx:explore  →  /opsx:propose  →  User Confirmation
   │                   │                    │
   ▼                   ▼                    ▼
 Ideation &       Create change        User must say
 investigation    proposal + gen       "confirmed" /
                  spec artifacts       "approved" /
                  into openspec/       "looks good"
```

1. **Explore** — Invoke `/opsx:explore` to investigate the problem space, gather context, and brainstorm approaches.
2. **Propose** — Invoke `/opsx:propose` to create a concrete change proposal and generate spec artifacts into `openspec/`.
3. **Confirm** — Present the spec to the user and wait for explicit confirmation.

## Light Mode Flow

Light mode is used for single-file bugfixes, config changes, and typos.

```
/opsx:propose  →  User Confirmation
      │                  │
      ▼                  ▼
  One-step           Explicit
  proposal +         user approval
  spec artifacts     required
```

1. **Propose** — Invoke `/opsx:propose` directly (skip explore).
2. **Confirm** — Present the spec to the user and wait for explicit confirmation.

## Spec Confirmation Protocol

The user must explicitly approve the spec before Gate G1 can pass. Acceptable confirmations include:

- "confirmed"
- "approved"
- "looks good"
- "lgtm"
- Or any equivalent affirmative statement

Ambiguous responses (e.g., "maybe", "I guess") do **not** count. If the response is unclear, ask the user to confirm explicitly.

## Brainstorming Review Loop

After the spec is written and before requesting user confirmation, dispatch a quality review:

```
Spec written → dispatch spec-document-reviewer subagent → review result
    ├─ Pass → present spec to user for confirmation
    └─ Fail → revise spec based on feedback → re-review
               (max 3 rounds)
               └─ Still failing after 3 rounds → escalate to user
```

The reviewer subagent evaluates the spec for completeness, clarity, and feasibility. This uses the `brainstorming` skill from Superpowers.

## Gate G1 Clearance

Gate G1 passes when **both** conditions are met:

1. The brainstorming review loop has passed (reviewer subagent approved)
2. The user has explicitly confirmed the spec

If the user requests changes, revise the spec, re-run the review loop, and resubmit for confirmation.

## Important: Loose Coupling

This workflow references only OpenSpec's stable interface:

- **Commands**: `/opsx:explore`, `/opsx:propose`, `/opsx:verify`
- **Directory convention**: `openspec/`

Do NOT inline CLI parameters, internal config file formats, or any implementation details of OpenSpec itself. If OpenSpec's internal behavior changes, this workflow remains valid as long as the command names and directory convention are preserved.
