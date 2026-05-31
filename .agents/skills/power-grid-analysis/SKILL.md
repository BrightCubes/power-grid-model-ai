---
name: power-grid-analysis
description: "Use when: working on any power-grid-model ecosystem task, including app building, data conversion, validation, calculations, result explanation, and debugging."
---

# Power Grid Model Ecosystem Operations

This skill is for operations across the full `power-grid-model` ecosystem. The repositories are tools; the user request defines the task.

Prompt starters are available in `PROMPT_LIBRARY.md`.

## Ecosystem Tool Roles
- `power-grid-model` (PGM): core calculations and validation APIs.
- `power-grid-model-ds` (PGM-DS): application-layer grid objects, graph/topology operations, mutations, and visualizer workflows.
- `power-grid-model-io` (PGM-IO): conversion between external formats and PGM-compatible datasets.

## Dependency Rules

| Constraint Category | Rule Details |
| --- | --- |
| **Reference Documents** | Start with `references/README.md`, then route to task guides in `references/tasks` and layer guides in `references/pgm`, `references/pgm-ds`, `references/pgm-io`. `REFERENCES.md` is kept as a backward-compatible landing page. |
| **Allowed Libraries** | You are strictly constrained to `power-grid-model` (PGM), `power-grid-model-ds` (PGM-DS), `power-grid-model-io` (PGM-IO), `numpy`, `pandas`, `matplotlib`, and `seaborn`. |
| **Preference** | Prefer `numpy` over `pandas` where straightforward. |
| **Graph & Visualization** | Strictly utilize any graph and network consistency logic from `power-grid-model-ds` (which exposes a `Grid` dataclass, graph algorithms, and grid visualizer tools). Do not use outside graph dependencies like networkx directly. |
| **Less Popular Libraries** | If you need any library outside the permitted list, ask the user for confirmation first. |
| **Ask Questions** | When requirements are unclear at any step, pause and ask the user for clarification. |

Use the following task-first workflow.

## Step 1: Classify the Task
Classify the user request into one or more of the following tasks:
- Build or extend an application/workflow on top of PGM.
- Convert/bridge datasets between formats or tools.
- Validate input/update data before calculations.
- Run studies (power flow, state estimation, short circuit).
- Evaluate and explain calculation outputs.
- Debug failures or inconsistent results.

If the request is ambiguous, ask clarifying questions first.

## Step 2: Deserialize and Normalize Data
Ensure the input/update data is in a PGM-compatible form.
- If data is in PGM JSON format, use `power-grid-model-io` converter flows.
- If data is external (Vision, Pandapower, tabular), convert with the correct PGM-IO converter.
- If deserialization or conversion fails, provide precise errors and corrective actions.

Primary references:
- `references/pgm-io/overview-and-converter-selection.md`
- `references/pgm-io/pgm-json-and-data-stores.md`

## Step 3: Execute the Task Playbook
Route to the relevant reference set:

- **Application build/extension**:
	- `references/tasks/application-build-and-automation.md`
	- `references/pgm-ds/pgm-interface-workflow.md`
- **Data validation**:
	- `references/tasks/conversion-validation.md`
	- `references/tasks/data-validation.md`
	- `references/tasks/engineering-plausibility-and-realism.md`
	- `references/tasks/validation-rules.yml`
	- `references/pgm/batch-validation-serialization.md`
- **Calculation run patterns**:
	- `references/pgm/calculation-recipes.md`
	- `references/pgm/overview-and-entrypoints.md`
- **Result evaluation and explanation**:
	- `references/tasks/result-evaluation-and-explanation.md`
	- `references/tasks/engineering-plausibility-and-realism.md`
- **Debugging/troubleshooting**:
	- `references/pgm/errors-and-debugging.md`
	- `references/pgm-ds/graph-and-topology-recipes.md`

When tasks overlap, prioritize references in the order of conversion, validation, calculation, and then debugging.

## Step 4: Return Outputs for the Active Task
Always return task-appropriate outputs:
- Code/script changes for implementation tasks.
- Validation findings and rejected records for validation tasks.
- Calculated datasets and method assumptions for study tasks.
- Clear diagnostics and fix options for debugging tasks.
- Summaries/charts and interpretation for result-explanation tasks.

## Completion Criteria
- [ ] The user request was classified into the correct PGM task(s).
- [ ] Data was deserialized/converted and validated where required.
- [ ] Appropriate ecosystem layers (PGM/PGM-DS/PGM-IO) were used for the task.
- [ ] Deliverables were provided in a task-appropriate form (code, diagnostics, or explanation).
- [ ] Verified that no unauthorized external dependencies were used.
