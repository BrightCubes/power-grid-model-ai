---
name: pgm-skill-update
description: "Use when: the user explicitly requests to update the pgm-assistant skill references with the latest changes from the power-grid-model package, check for deprecations or new features, or keep the skill in sync with recent releases. This skill is used only when explicitly called."
metadata:
  internal: true
---

# PGM Skill Update Workflow

This skill reviews recent releases across the `power-grid-model` ecosystem and determines whether any changes warrant updates to the reference files in the `pgm-assistant` skill.

## Step 0: Read Current Version Status

Read `.agents/skills/pgm-assistant/SKILL.md` and locate the **Package Version Status** section near the top. Report the currently recorded versions and last-checked date to the user — this is the baseline for deciding which releases to look at.

## Step 1: Fetch All Releases

Fetch the releases pages for all three repositories in parallel:

- **PGM**: `https://github.com/PowerGridModel/power-grid-model/releases`
- **PGM-DS**: `https://github.com/PowerGridModel/power-grid-model-ds/releases`
- **PGM-IO**: `https://github.com/PowerGridModel/power-grid-model-io/releases`

For all three repositories, include all releases newer than the versions recorded in Step 0.

For **every qualifying release across all three repositories**, extract:

1. The **highlights** section of the changelog — the bulleted summary of the most important changes.
2. The **full changelog** — the complete release notes including all PR references with their labels or category headings.

For each PR referenced in any release, inspect its label or the category heading it appears under in the release notes to decide whether to fetch it:

- **Fetch** PRs with labels such as: `feature`, `bug`, `bugfix`, `enhancement`, or any other user-facing change indicator.
- **Skip** PRs with labels such as: `dependencies`, `github actions`, `ci`, `chore`, `refactor`, `improvement`, `documentation`, or any other maintenance or tooling indicator.

(These are example label names; match on intent, not exact strings.)

For each **included** PR, fetch the full PR page (description and all comments) and record the content grouped by PR.

## Step 2: Filter and Present Releases

For **all packages**, discard releases that are **only** one or more of the following:

- CI/CD or GitHub Actions dependency updates
- Lock file or linter dependency bumps
- Pure documentation formatting or terminology fixes with no API impact

Present the filtered releases to the user in three separate sections before continuing. For each package, list every included release with its full changelog and a linked PR reference for each entry:

**PGM**
- `vX.Y.Z` (YYYY-MM-DD)
  - Full changelog text, with each PR rendered as a markdown link: `[#123](https://github.com/PowerGridModel/power-grid-model/pull/123) — one-line summary`

**PGM-DS** — same format

**PGM-IO** — same format

If a package has no qualifying releases, state that clearly in its section.

## Step 3: Read Skill Reference Files

Read all reference files across all three layers before moving to the next step. This gives the full picture of what is already documented.

**PGM** (`.agents/skills/pgm-assistant/references/pgm/`)

**PGM-DS** (`.agents/skills/pgm-assistant/references/pgm-ds/`)

**PGM-IO** (`.agents/skills/pgm-assistant/references/pgm-io/`)

## Step 4: Cross-Reference Against References

For each release in the filtered list, decide whether it could affect any of the reference files read in Step 3. Start by matching each release to its corresponding reference layer (PGM → pgm refs, PGM-DS → pgm-ds refs, PGM-IO → pgm-io refs), but also flag cross-layer impacts where relevant.

**Criteria for "potentially relevant":**

- New component type, attribute, or dataset term
- Changed or removed API (method name, parameter, return shape)
- New error or changed error condition that users would encounter
- New calculation method or option
- New converter, data store, or external format support
- New `Grid` object, graph algorithm, or topology operation
- Behavioral change to an existing component or calculation

**Criteria for "skip":**

- Internal solver improvement with no user-facing API or behavioral change
- Feature already accurately covered in the references
- Feature explicitly marked as incomplete or pending validation in the release notes

If nothing passes for a package, state that clearly for that section and move on.

## Step 5: Analyse Full PR Content for Each Relevant Change

Using the full PR descriptions and comments already collected in Step 1, extract for each relevant PR:

- **Motivation**: why the change was made
- **Exact API impact**: what is added, changed, or removed
- **Constraints or known issues**: anything incomplete, pending, or with caveats
- **Stability**: fully validated and documented upstream, or partial/in-progress?

Discard changes where the PR content reveals the feature is incomplete, not yet validated, or purely internal.

## Step 6: Formulate Concrete Suggestions

Grouped by package (**PGM**, **PGM-DS**, **PGM-IO**), produce a specific edit proposal for each surviving change:

- Which file to edit (with path)
- Approximate location (section heading or line reference)
- Exact text to add or change
- Why it improves the reference

Do **not** suggest:

- Deprecation notices that will need to be removed later
- Features that upstream docs or validators still reject
- Anything already accurately covered by the current reference text

## Step 7: Present to User for Approval

Present each suggestion grouped by package. For each one state:

- The proposed change (file, location, exact text)
- The source (PR number and one-sentence rationale)

Wait for explicit approval before making any edits. "No change needed" is a valid and complete outcome.

## Step 8: Update Version Status

After all approved edits are applied (or if no edits were needed), update the **Package Version Status** section in `.agents/skills/pgm-assistant/SKILL.md` to reflect the versions just reviewed and today's date.

Format:

```
## Package Version Status
Last reviewed: PGM vX.Y.Z · PGM-DS vX.Y.Z · PGM-IO vX.Y.Z (checked YYYY-MM-DD)
```

Only update a package's version entry if it was actually checked in this run. Leave the others unchanged.
