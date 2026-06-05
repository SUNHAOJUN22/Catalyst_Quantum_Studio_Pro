# MCP Interface Rules

## Tool Classes

1. Pure calculation: unit conversion, ΔG, BDE, Boltzmann, kinetics, decisions.
2. Read-only parser: Gaussian, cube, NBO, QTAIM, NCI, GoodVibes.
3. Template generator: Gaussian, formchk, cubegen, Multiwfn, GoodVibes, SLURM.
4. Audit: scientific formula manifest, provenance, external-tool configuration.
5. Report: Chinese report draft with evidence and missing-data boundaries.

## Tool Metadata

Every tool should expose:

- Chinese and English title;
- purpose;
- JSON input/output schema;
- units;
- execution mode;
- `can_execute_external`;
- confirmation requirement;
- evidence output policy;
- safety boundary.

## Response Contract

Return:

- `result`;
- `warnings`;
- `units`;
- `quality`;
- `evidence_grade`;
- `eligible_evidence_grade`;
- `paper_ready`;
- `provenance`;
- `safety_boundary`.

Missing scientific fields are `null`, never fabricated.

## Recommended Tools

- `audit_scientific_formulas`
- `calculate_delta_g_bind`
- `calculate_delta_g_poison`
- `calculate_insert_barrier`
- `calculate_bde_sic`
- `calculate_bde_sio`
- `calculate_bde_roor`
- `calculate_radical_kinetics`
- `parse_gaussian_log`
- `parse_cube`
- `parse_nbo`
- `parse_qtaim`
- `parse_nci`
- `parse_goodvibes`
- `inspect_external_tool_configuration`
- `generate_gaussian_input`
- `generate_cubegen_template`
- `generate_multiwfn_qtaim_template`
- `generate_slurm_script_template`
- `generate_chinese_report`

MCP tools must call typed internal services, not arbitrary shell commands.
