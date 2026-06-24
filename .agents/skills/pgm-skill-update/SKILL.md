---
# SPDX-FileCopyrightText: Contributors to the Power Grid Model AI project <info@brightcubes.nl>
#
# SPDX-License-Identifier: MPL-2.0

name: pgm-skill-update
description: "Use when: the user explicitly requests to update the pgm-assistant skill references with the latest changes from the power-grid-model package, check for deprecations or new features, or keep the skill in sync with recent releases. This skill is used only when explicitly called."
metadata:
  internal: true
---

# PGM Skill Update Workflow

This skill reviews recent releases across the `power-grid-model` ecosystem and determines whether any changes warrant updates to the reference files in the `pgm-assistant` skill.

## Step 0: Read Current Version Status

Read `.agents/skills/pgm-assistant/SKILL.md` and locate the **Package Version Status** section near the top. Report the currently recorded versions and last-checked date to the user — this is the baseline for deciding which releases to look at.

## Step 1: Clarify Scope

If the user has not specified a scope, ask:

> "Which packages should I check, and over what range?
>
> - **PGM (main)**: what is the target minor/major version to check up to? (default: latest)
> - **PGM-DS and PGM-IO**: what time window? (default: last 2 weeks)"

Wait for the answer before proceeding.

## Step 2: Fetch PGM Releases (Minor/Major Only)

Fetch the releases page:

- URL: `https://github.com/PowerGridModel/power-grid-model/releases`

Include **only minor or major version releases** (e.g. `1.14.0`, `2.0.0`) that are newer than the version recorded in Step 0. Skip all patch releases (e.g. `1.13.1`, `1.13.2`).

For each qualifying release, extract two things:

1. The **highlights** section of the changelog — the bulleted summary of the most important changes. This is the primary focus.
2. The **full changelog** — the remainder of the release notes covering smaller changes not mentioned in the highlights.

## Step 3: Fetch PGM-DS Releases

Fetch the releases page:

- URL: `https://github.com/PowerGridModel/power-grid-model-ds/releases`

Include **all releases** within the agreed time window. Extract: version tag, release date, and one-line summary for each.

## Step 4: Fetch PGM-IO Releases

Fetch the releases page:

- URL: `https://github.com/PowerGridModel/power-grid-model-io/releases`

Include **all releases** within the agreed time window. Extract: version tag, release date, and one-line summary for each.

## Step 5: Filter and Present Releases

For **all packages**, discard releases that are **only** one or more of the following:

- CI/CD or GitHub Actions dependency updates
- Lock file or linter dependency bumps
- Pure documentation formatting or terminology fixes with no API impact

Present the filtered releases to the user in three separate sections before continuing:

**PGM** — version · date · one-line summary
**PGM-DS** — version · date · one-line summary
**PGM-IO** — version · date · one-line summary

If a package has no qualifying releases, state that clearly in its section.

## Step 6: Read Skill Reference Files

Read all reference files across all three layers before moving to the next step. This gives the full picture of what is already documented.

**PGM** (`.agents/skills/pgm-assistant/references/pgm/`)

**PGM-DS** (`.agents/skills/pgm-assistant/references/pgm-ds/`)

**PGM-IO** (`.agents/skills/pgm-assistant/references/pgm-io/`)

## Step 7: Cross-Reference Against References

For each release in the filtered list, decide whether it could affect any of the reference files read in Step 6. Start by matching each release to its corresponding reference layer (PGM → pgm refs, PGM-DS → pgm-ds refs, PGM-IO → pgm-io refs), but also flag cross-layer impacts where relevant.

For PGM releases, evaluate highlights first; then check the full changelog for smaller changes that may still affect a reference.

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

## Step 8: Fetch Full PR for Each Relevant Change

For each change that passed Step 7, fetch the pull request page in full. Extract:

- **Motivation**: why the change was made
- **Exact API impact**: what is added, changed, or removed
- **Constraints or known issues**: anything incomplete, pending, or with caveats
- **Stability**: fully validated and documented upstream, or partial/in-progress?

Discard changes where the PR reveals the feature is incomplete, not yet validated, or purely internal.

## Step 9: Formulate Concrete Suggestions

Grouped by package (**PGM**, **PGM-DS**, **PGM-IO**), produce a specific edit proposal for each surviving change:

- Which file to edit (with path)
- Approximate location (section heading or line reference)
- Exact text to add or change
- Why it improves the reference

Do **not** suggest:

- Deprecation notices that will need to be removed later
- Features that upstream docs or validators still reject
- Anything already accurately covered by the current reference text

## Step 10: Present to User for Approval

Present each suggestion grouped by package. For each one state:

- The proposed change (file, location, exact text)
- The source (PR number and one-sentence rationale)

Wait for explicit approval before making any edits. "No change needed" is a valid and complete outcome.

## Step 11: Update Version Status

After all approved edits are applied (or if no edits were needed), update the **Package Version Status** section in `.agents/skills/pgm-assistant/SKILL.md` to reflect the versions just reviewed and today's date.

Format:

```
## Package Version Status
Last reviewed: PGM vX.Y.Z · PGM-DS vX.Y.Z · PGM-IO vX.Y.Z (checked YYYY-MM-DD)
```

Only update a package's version entry if it was actually checked in this run. Leave the others unchanged.
