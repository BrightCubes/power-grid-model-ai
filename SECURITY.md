# Security Policy

## Scope

This repository ships **agent skills**: markdown instruction files for AI coding agents working with the [power-grid-model](https://github.com/PowerGridModel/power-grid-model) ecosystem. It contains no runtime code of its own — the agent that executes these skills is your own, running with your permissions on your machine. The security considerations below follow from that trust model.

Security issues in the underlying libraries (`power-grid-model`, `power-grid-model-ds`, `power-grid-model-io`) are covered by the [Power Grid Model security policy](https://github.com/PowerGridModel/.github/blob/main/SECURITY.md).

## Reporting a vulnerability

- **Issues in the skill content of this repository** (e.g. a skill instructing an agent to do something unsafe): report them privately via GitHub's [Private Vulnerability Reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability) on this repository. Please do not open a public issue for security-sensitive findings.
- **Issues in the PGM libraries themselves**: report them upstream following the [Power Grid Model security policy](https://github.com/PowerGridModel/power-grid-model?tab=security-ov-file).

## Guidelines for using the skills safely

Skills are instructions your agent will follow. Treat installing a skill with the same care as installing a dependency:

- **Verify the source.** Install the skills only from this repository's URL and review the skill content (`.agents/skills/`) before use. A modified or spoofed skill can steer your agent in unintended ways (see [OWASP LLM03: Supply Chain](https://genai.owasp.org/llm-top-10/)).
- **Run generated code in an isolated environment.** The skills direct your agent to write and execute Python against your grid data. Use a project-scoped virtual environment or the sandbox your agent provides, and review generated code before running it outside that environment.
- **Treat grid data as sensitive.** Real network datasets are critical-infrastructure information. Before providing them to a cloud-hosted agent, check that this complies with your organization's data handling policy (see [OWASP LLM02: Sensitive Information Disclosure](https://genai.owasp.org/llm-top-10/)).
- **Keep approval checkpoints intact.** The skills include steps where the agent must ask for confirmation before acting. Do not instruct your agent to skip these, and be cautious with agent permission modes that auto-approve actions (see [OWASP LLM06: Excessive Agency](https://genai.owasp.org/llm-top-10/)).
- **Stay within the allowed library list.** The `pgm-assistant` skill constrains the agent to a fixed set of established libraries and requires your confirmation for anything else. This limits the dependency surface of generated code — treat requests to go outside the list with appropriate scrutiny.

For more information on best practices for working with agentic systems, see the [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) from the [OWASP Gen AI Security Project](https://genai.owasp.org/).

## References

- [Power Grid Model security policy](https://github.com/PowerGridModel/power-grid-model?tab=security-ov-file)
- [OWASP Gen AI Security Project](https://genai.owasp.org/)
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)
- [OWASP Top 10 for Agentic Applications for 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
