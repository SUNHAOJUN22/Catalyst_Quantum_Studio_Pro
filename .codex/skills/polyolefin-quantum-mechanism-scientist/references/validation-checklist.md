# Validation Checklist

Run commands from `<PROJECT_ROOT>`.

## Documentation Only

- Run mojibake audit if Chinese text changed.
- Check report/README/CHANGELOG consistency.

## Frontend

- `npm run audit:mojibake` if available.
- `npm --prefix frontend run typecheck`
- `npm --prefix frontend run lint`
- `npm --prefix frontend run build`
- UI smoke or browser inspection for visible layout changes.

## Backend API

- Backend unit tests if available.
- API smoke tests if available.
- Validate Chinese error messages and no unhandled 500s.

## Parsers

- Unit tests with complete, partial, and failed fixtures.
- Check normalized JSON fields, units, warnings, and provenance.
- Confirm missing data is `null`, not fabricated.

## Scientific Formulas

- `python <SKILL_PATH>/scripts/scientific_formula_audit.py --project <PROJECT_ROOT>`
- Unit conversion tests.
- Delta-G formula tests.
- krel temperature tests.
- BDE tests.
- Decision-boundary tests.

## Scientific Software Connectors

- `python <SKILL_PATH>/scripts/check_external_tools.py --project <PROJECT_ROOT>`
- Confirm path inspection does not execute a version command.
- Confirm shell metacharacters are rejected for real execution.
- Confirm MCP tools report `can_execute_external=false` unless an isolated runner is explicitly implemented.

## Full Release

Run the project’s own quality gate if present. Otherwise run the Skill script:

```bash
python <SKILL_PATH>/scripts/run_quality_gate.py --project <PROJECT_ROOT>
```

## Final Response

State commands run, pass/fail/skip status, and remaining risk.
