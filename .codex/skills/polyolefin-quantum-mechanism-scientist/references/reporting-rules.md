# Scientific Reporting Rules

## Required Provenance Block

For each result state:

- source file or record;
- source type;
- method/basis/dispersion/solvation where applicable;
- temperature and standard state;
- unit;
- parser version and quality;
- evidence grade;
- mock status;
- paper readiness;
- missing validations.

## Claim Language

- A/B evidence: may support a scoped conclusion after checking consistency and uncertainty.
- C evidence: write “当前线索支持……，仍需当前体系复现或完整计算核验。”
- D evidence: write “示例数据或机制假说，不能作为真实科学结论。”
- Missing data: write “当前数据不足，不能形成可靠结论。”

Do not call a candidate “optimal” from a weighted score alone. Report the weighting, missing dimensions, and sensitivity.

## Minimum Falsification Block

Every mechanism claim includes:

1. Supporting observations.
2. A condition that would refute it.
3. Smallest calculation that discriminates the alternatives.
4. Smallest experiment that discriminates the alternatives.
5. Software/API/parser test needed to preserve the rule.

## Recommended Chapters

- Research question and mechanism axes.
- Data sources and evidence grades.
- Methods and numerical contracts.
- Si-O/Si-C intrinsic descriptors.
- TEA and Ti coordination competition.
- Insertion free-energy profile.
- Hydrolysis/condensation.
- Peroxide radical competition.
- Experiment-computation closure.
- Falsifiable conclusions, limitations, and next tasks.
