---
name: pgm-skill-update
description: "Use when: the user wants to update the power-grid-analysis skill references with the latest changes from the power-grid-model package, check for deprecations or new features, or keep the skill in sync with recent releases."
---

# PGM Skill Update Workflow

This skill reviews recent `power-grid-model` releases and determines whether any changes warrant updates to the reference files in the `power-grid-analysis` skill.

## Step 0: Clarify Time Window

If the user has not specified a time window, ask:

> "What time window should I look at? (e.g. last 2 weeks, since version X, since date Y)"

Wait for the answer before proceeding.

## Step 1: Fetch Release List

Fetch the releases page for the `power-grid-model` repository:

- URL: `https://github.com/PowerGridModel/power-grid-model/releases`
- Extract: version tag, release date, and one-line summary for each release within the time window.

## Step 2: Filter and Present Relevant Releases

Discard releases that are **only** one or more of the following:
- CI/CD or GitHub Actions dependency updates
- Lock file or linter dependency bumps
- Pure documentation formatting or terminology fixes with no API impact

For everything that remains, **output a short list to the user** showing: version, date, and one-line summary. This gives the user visibility before deeper analysis begins.

## Step 3: Read the Skill Reference Files

Read all `.md` files under `.agents/skills/power-grid-analysis/references/pgm/`:

- `README.md`
- `overview-and-entrypoints.md`
- `data-model-components-and-datasets.md`
- `calculation-recipes.md`
- `batch-validation-serialization.md`
- `errors-and-debugging.md`

Read all files before moving to the next step. This gives you the full picture of what is already documented so you can identify genuine gaps.

## Step 4: Cross-Reference Against References

For each release in the filtered list, decide whether it could affect any of the reference files read in Step 3. Base this on the one-line summary alone — do not fetch PRs yet.

Criteria for "potentially relevant":
- New component type, attribute, or dataset term
- Changed or removed API (method name, parameter, return shape)
- New error or changed error condition that users would encounter
- New calculation method or option
- Behavioral change to an existing component or calculation

Criteria for "skip":
- Internal solver improvement with no user-facing API or behavioral change
- Feature already covered in the references
- Feature explicitly marked as incomplete or pending validation in the summary

Retain only the changes that pass this filter. If nothing passes, state that clearly and stop — no further steps needed.

## Step 5: Fetch Full PR for Each Relevant Change

For each change that passed Step 4, fetch the pull request page in full. Extract:

- **Motivation**: why the change was made
- **Exact API impact**: what is added, changed, or removed
- **Constraints or known issues**: anything incomplete, pending, or with caveats
- **Stability**: is this fully validated and documented upstream, or a partial/in-progress implementation?

Use this information to decide whether a reference file update is warranted. Discard changes where the PR reveals the feature is incomplete, not yet validated, or purely internal.

## Step 6: Formulate Concrete Suggestions

For each surviving change, produce a specific edit proposal:

- Which file to edit (with path)
- Approximate location (section heading or line reference)
- Exact text to add or change
- Why it improves the reference

Do **not** suggest:
- Deprecation notices that will need to be removed later
- Features that the upstream docs or validator still reject
- Anything already accurately covered by the current reference text

## Step 7: Present to User for Approval

Present each suggestion clearly. For each one state:
- The proposed change (file, location, exact text)
- The source (PR number and one-sentence rationale)

Wait for explicit approval before making any edits. "No change needed" is a valid and complete outcome.
