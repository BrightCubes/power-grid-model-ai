<!--
SPDX-FileCopyrightText: Contributors to the Power Grid Model project <powergridmodel@lfenergy.org>

SPDX-License-Identifier: MPL-2.0
-->

# Power Grid Model Skills

A collection of agent skills for working with the [power-grid-model](https://github.com/PowerGridModel/power-grid-model) (PGM) Python ecosystem.

## Skills

### power-grid-analysis

A **pair-programming** skill that assists grid operators with the full PGM workflow: loading and converting grid data, running power flow and other studies, validating results, and explaining findings — all using the `power-grid-model`, `power-grid-model-ds`, and `power-grid-model-io` libraries.

Defined in [.agents/skills/power-grid-analysis/SKILL.md](.agents/skills/power-grid-analysis/SKILL.md). It covers:

- **Data ingestion** — deserializing PGM JSON and converting from external formats (Vision, Pandapower, tabular)
- **Validation** — input data validation and engineering plausibility checks
- **Calculations** — power flow, state estimation, and short-circuit studies
- **Result evaluation** — interpreting and explaining calculation outputs
- **Debugging** — diagnosing failures and inconsistent results

Reference documentation for the skill lives in [.agents/skills/power-grid-analysis/references/](.agents/skills/power-grid-analysis/references/).

### pgm-issue-analysis

A **dedicated issue-debugging** skill for investigating errors and unexpected results in PGM. Defined in [.agents/skills/pgm-issues/SKILL.md](.agents/skills/pgm-issues/SKILL.md). You can use the skill to an initial investigation into an issue or error you get when working with PGM. This skill is especially usefull when encountering a **SparseMatrixError** or **IterationDiverge Error**. The skill create a **Minimal Reproducible Case** which helps in understanding what the root cause of the problem is.
It follows a structured five-step investigation workflow:

1. **Reproduce** — run the user's data as-is and confirm the exact error
2. **Understand the data** — build a structural picture of the network (voltage levels, topology, transformer connections)
3. **Validate** — run PGM's built-in validation plus cross-component consistency and physical plausibility checks
4. **Minimal reproducible example** — reduce the dataset to the fewest components that still trigger the failure
5. **Diagnose** — classify the root cause as a user data bug or a potential PGM bug

The skill produces a `report.ipynb` Jupyter notebook with its findings. Each investigation step is also saved as a numbered Python script (`step1_reproduce.py`, etc.) for full traceability.

## Installation

Skills are installed using [`npx skills`](https://skills.sh), a package manager for agent skills. See [skills.sh](https://skills.sh) for more information. 
To install the skills into your coding agent:

```bash
# Install both Skills
npx skills install https://github.com/PowerGridModel/power-grid-model-ai

## Development

To install requirements run:

```bash
uv sync
```

### Installing the skill-creator

The eval loop requires the `skill-creator` skill. How to install it depends on your agent:

**Claude Code** — run `/plugins` and install from the official plugins repository, or install directly with:

```bash
/plugins install https://github.com/anthropics/claude-plugins-official/blob/main/plugins/skill-creator/skills/skill-creator/SKILL.md
```

**Other agents** — download the [skill-creator directory](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator/skills/skill-creator) and place it in your agent's skills directory (e.g. `.agents/skills/skill-creator`).

### Running skill evaluations

Skill development follows an iterative eval loop managed by the `skill-creator` agent skill. To start, open this repository in an agent that has `skill-creator` available and use a prompt like:

> "Run the evaluations for the power-grid-analysis skill at `.agents/skills/power-grid-analysis`"

The agent will take it from there:

1. **Run evals** — the agent runs test cases with and without the skill and saves results under `.agents/skills/power-grid-analysis-workspace/iteration-N/`.
2. **Review results** — the agent opens a viewer where you leave feedback on each test case.
3. **Iterate** — based on your feedback, the agent improves the skill and reruns the evals.
4. **Optimize triggering** — once the skill content is stable, the agent can optimize the description so the skill triggers reliably.

Test cases are stored in [.agents/skills/power-grid-analysis/evals/evals.json](.agents/skills/power-grid-analysis/evals/evals.json).
