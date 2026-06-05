---
name: polyolefin-quantum-mechanism-scientist
description: A reusable professional research-software skill for Si-O/Si-C functional alpha-olefin chemistry, Ziegler-Natta/TEA/Ti-poisoning mechanisms, Gaussian/cube/NBO/QTAIM/NCI/GoodVibes read-only parsers, guarded scientific-software connectors and MCP tools, peroxide-driven PP beta-scission/LCB/crosslinking models, Chinese scientific UI/reporting, evidence grading, numerical validation, mojibake audits, and release quality gates. Use when Codex builds, tests, audits, or integrates a polyolefin quantum-mechanism research platform.
---

# Polyolefin Quantum Mechanism Scientist

Resolve the current repository as `<PROJECT_ROOT>`. Never assume a private path.

## Operating Protocol

1. Inspect the project and active changes before editing; use `rg` and preserve user work.
2. Separate pure scientific formulas, parsers, API orchestration, persistence, UI, and reports.
3. Keep parsers read-only. Treat generated Gaussian/Multiwfn/cubegen/SLURM text as templates, not results.
4. Keep units, temperature, charge, multiplicity, method, basis, provenance, evidence grade, and mock status explicit.
5. Do not promote parser success to paper-ready evidence without convergence, frequency/TS/IRC, and source review.
6. For every mechanism claim, provide a falsification condition and the smallest useful calculation, experiment, and software test.
7. Use Chinese as the primary product language for Chinese research software; keep English as secondary terminology.
8. Run scope-appropriate tests and update existing reports when behavior changes.

## Required References

- Read `references/scientific-framework.md` for the four-axis mechanism, formulas, decisions, and evidence grades.
- Read `references/numerical-rigor.md` before changing constants, rates, BDE, Boltzmann weighting, uncertainty, or thresholds.
- Read `references/simulation-connectors.md` before integrating Gaussian, formchk, cubegen, Multiwfn, GoodVibes, RDKit, SLURM, or queues.
- Read `references/mcp-tools.md` before adding MCP tools/resources/prompts.
- Read `references/software-architecture.md` for service boundaries and normalized parser contracts.
- Read `references/ui-ux-rules.md` for Google Workspace-style scientific UI.
- Read `references/reporting-rules.md` before generating scientific conclusions or reports.
- Read `references/validation-checklist.md` before final verification.

## Evidence Boundary

- **A**: Real computation with method/basis, convergence, frequency or TS/IRC checks, and provenance verified.
- **B**: Real experiment with sample, process, measurement conditions, and provenance.
- **C**: Read-only parsed output pending full review, literature evidence, or user input not reproduced.
- **D**: Mock/example data, failed parse, task template, or mechanism hypothesis.

Always output evidence grade, source, reliability, paper readiness, and missing validation. C/D evidence cannot become an A/B conclusion.

## Connector Safety

Default to `template_only`, `parse_only`, or `dry_run`.

Do not:

- Execute Gaussian, formchk, cubegen, Multiwfn, GoodVibes, SLURM, uploaded files, or user-derived shell text.
- Pass command templates containing shell metacharacters to an executor.
- Access paths outside the declared project/work directory.

Real execution is allowed only when the host project explicitly implements an isolated runner with an executable allowlist, argument arrays, resolved-path containment, resource limits, explicit user confirmation, audit logs, and disabled-by-default configuration. A normal API route must never directly invoke the chemistry software.

## Reusable Scripts

- `scripts/scientific_formula_audit.py --project <PROJECT_ROOT>`: verify constants, formulas, finite behavior, and optional project imports.
- `scripts/check_external_tools.py --project <PROJECT_ROOT>`: inspect configured paths and environment variables without executing tools.
- `scripts/mojibake_audit.py --project <PROJECT_ROOT> --fail-on-active`: detect Chinese mojibake while preserving scientific symbols.
- `scripts/run_quality_gate.py --project <PROJECT_ROOT> [--quick]`: run available project gates with PASS/FAIL/SKIP output.

## Final Response

State changed files, scientific behavior, validation commands, pass/fail/skip results, evidence boundaries, and remaining risks.
