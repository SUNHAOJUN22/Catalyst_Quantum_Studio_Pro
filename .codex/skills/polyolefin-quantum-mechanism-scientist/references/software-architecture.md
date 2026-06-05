# Software Architecture

Use this architecture for research software unless the existing project already has a clear equivalent.

## Recommended Layers

```text
scientific_core/
  units.py
  energies.py
  kinetics.py
  decisions.py
  descriptors.py
  validation_manifest.py

parsers/
  gaussian.py
  cube.py
  nbo.py
  qtaim.py
  nci.py
  goodvibes.py

api/
  molecules.py
  gaussian.py
  analysis.py
  cubes.py
  experimental.py
  reports.py

frontend/components/
frontend/components/layout/
frontend/components/data/
frontend/components/workflows/
frontend/components/viewers/
frontend/components/charts/
frontend/hooks/
frontend/lib/
```

## Responsibilities

- `scientific_core`: constants, formulas, kinetic models, BDE, decision rules, and pure functions.
- `validation_manifest`: machine-readable constants, formulas, numerical policies, evidence rules, and paper-readiness boundaries.
- `parsers`: read-only file/text parsers returning normalized JSON with units, warnings, quality, and provenance.
- `api`: validation, persistence, orchestration, and Chinese error messages.
- `frontend/components/layout`: topbar, grouped sidebar, page header, detail panel.
- `frontend/components/data`: resource table, evidence badge, source-quality badge, provenance panel, empty state.
- `frontend/components/workflows`: Gaussian workspace, report workspace, literature knowledge view, molecule resource view.
- `reports`: Chinese report sections, missing-data statements, mock warnings, evidence-grade explanations.
- `tests`: scientific formulas, parser fixtures, API boundaries, UI smoke, security boundaries.

## Parser Contract

Parser output should include:

- `quality`: complete, partial, failed, readable, encoded-garbled, scanned-needs-ocr, or project equivalent.
- `warnings`: Chinese warnings.
- `units`: explicit units per field.
- `provenance`: file name/path, parser version, source type.
- `evidence_grade`, `eligible_evidence_grade`, and `paper_ready`.
- Missing fields as `null`, never fabricated.

## Safety Contract

Do not execute external chemistry programs by default. Generate command templates only when clearly labeled “not executed”.
