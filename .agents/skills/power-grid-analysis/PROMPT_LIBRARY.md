# Power Grid Analysis Prompt Library

Use these prompts to trigger the `power-grid-analysis` skill with clear intent.

## How to Use This Library

- Replace placeholders like `<path-to-input.json>` and `<target-file.py>`.
- Keep four details in your prompt: task, data source, expected output, and constraints.
- For best routing, explicitly mention PGM, PGM-DS, and/or PGM-IO when relevant.

## High-Signal Prompts (Best for This Skill)

These are particularly well answered by this skill because they map directly to the skill workflow (conversion -> validation -> calculation -> explanation/debugging).

1. "Build an end-to-end script that converts `<source-format>` data to PGM format, validates it, runs a symmetric power flow, and writes a concise summary report. Use only PGM, PGM-DS, PGM-IO, numpy, pandas, matplotlib, seaborn."
2. "I have `<path-to-input.json>`. Validate the dataset for power flow, list structural errors first, then run engineering plausibility checks and return a table of suspicious-but-valid values."
3. "Create a converter selection decision for these inputs: `<format-description>`. Explain why the chosen PGM-IO path is correct and provide a runnable conversion snippet."
4. "Run a batch power flow on `<dataset-path>` with clear handling for partial failures. Return which scenarios failed, likely causes, and recommended fixes."
5. "Analyze topology from `<dataset-path>` using PGM-DS graph tools only (no external graph libraries). Identify islands, radial/meshed areas, and weakly connected sections."
6. "Debug this abnormal result set from `<results-path>`. Separate input-data issues from solver/configuration issues and propose the minimum change set to retest."
7. "Explain these PGM outputs for an operations audience: `<result-path>`. Include limit violations, loading hotspots, voltage concerns, and a plain-language conclusion."
8. "Compare Newton-Raphson and iterative-current methods for this network `<dataset-path>`. Show assumptions, option changes, and differences in key output metrics."
9. "Design a reusable validation gate for CI that blocks structurally invalid PGM datasets and warns on realism violations using configurable thresholds."
10. "Use `data/PGM_1408/input.json` and reproduce the PV-node behavior investigation from `data/PGM_1408/issue.md`. Provide a diagnosis checklist and a script-level fix strategy."

## Prompt Templates by Task

### 1) Application Build / Workflow Automation

"Create `<target-file.py>` that:
1) loads `<input-path>`,
2) converts/deserializes to PGM-compatible arrays,
3) validates input/update data,
4) runs `<calculation-type>` with `<method/options>`,
5) exports results to `<output-path>` and a short markdown report.
Keep dependencies limited to PGM ecosystem + numpy/pandas/matplotlib/seaborn."

### 2) Conversion and Mapping

"I need to convert `<source-format>` to PGM JSON. Choose the correct PGM-IO converter, show mapping assumptions, and generate a script that logs dropped/altered fields and unit conversions."

"Audit this conversion output `<converted-path>` against source `<source-path>`. Return a mismatch report grouped by criticality (blocking, warning, informational)."

### 3) Validation and Data Quality

"Validate `<dataset-path>` for `<calculation-type>`. Return:
- hard validation failures,
- likely modeling mistakes,
- realism anomalies with confidence labels,
- exact rows/components to fix first."

"Create a validation report function for PGM datasets that outputs JSON + markdown and can be reused in batch pipelines."

### 4) Study Execution (Power Flow / State Estimation / Short Circuit)

"Run `<study-type>` on `<dataset-path>` with justified default options. Then produce a compact KPI table for node voltage, branch loading, and source/generator active-reactive balance."

"Generate a parameter sweep for `<option-name>` over `<range>` and show sensitivity of `<metric>` with a chart and short interpretation."

### 5) Result Evaluation and Explanation

"Given `<results-path>`, produce an engineering summary with:
- top 10 overloaded elements,
- top 10 voltage deviations,
- probable root causes,
- mitigation actions ranked by impact and implementation risk."

"Translate these study results into two outputs: a technical appendix and an operator-facing summary with less jargon."

### 6) Debugging and Failure Triage

"This calculation fails with `<error-message>`. Build a triage flow: data issue vs topology issue vs method/options issue, then produce a smallest-first remediation plan."

"I suspect bad topology after conversion. Use PGM-DS graph checks to find disconnected components, invalid orientations, or suspicious feeder splits. Provide reproducible checks in code."

## Ready-to-Use Prompts for This Repository

1. "Validate `data/PGM_1408/input.json` for power flow and generate a markdown findings report under `data/PGM_1408/validation_report.md`."
2. "Use `data/PGM_1408/pgm_pv_node_error.py` as a baseline. Refactor it into reusable functions for build-input, run-study, and report-anomalies without changing behavior."
3. "Read `data/PGM_1408/sym_output.json` and produce a concise interpretation of voltage profile, branch loading, losses, and reactive power behavior."
4. "Create tests that assert abnormal PV-node behavior is either rejected by validation or flagged in post-run realism checks. Put tests under `tests/`."

## Prompt Quality Upgrades

Weak prompt:

"Run power flow and explain it."

Stronger prompt:

"Run symmetric power flow on `<dataset-path>` using Newton-Raphson. Return: validation findings, solver settings, top violations, and a short operator summary. Use only PGM ecosystem dependencies."

Weak prompt:

"Fix this grid issue."

Stronger prompt:

"Debug `<error-or-symptom>` on `<dataset-path>`. Distinguish conversion errors, structural validation errors, and solver instability. Provide ranked fixes and a minimal reproduction script."

## Checklist for Writing New Prompts

- Name the task type (convert, validate, calculate, explain, debug).
- Include exact input and output locations.
- Specify required deliverable format (code patch, report, table, chart, tests).
- Add constraints (allowed libraries, method choice, performance bounds).
- Ask for assumptions and confidence tags when uncertainty is expected.