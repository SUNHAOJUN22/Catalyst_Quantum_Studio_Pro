# Scientific Framework

## Four-Axis Model

1. Monomer axis: DCS, MCSOMe, DMOS, Si-O, Si-C, Si-Cl, Si-OMe, C=C.
2. Catalyst axis: Ziegler-Natta active site, Ti, MgCl2, TEA/AlEt3/AlEt2Cl, internal donor.
3. Radical axis: RO-OR, RO radicals, PP radicals, EPC radicals, coagent, O2.
4. Microphase axis: iPP crystal, PP amorphous phase, EPC-rich phase, PP/EPC interface.

Separate polymerization-stage chemistry from post-treatment chemistry:

- Polymerization: C=C coordination, Ti active site, TEA interaction, O→Ti poisoning.
- Post-treatment: Si-Cl/Si-OMe hydrolysis, Si-O-Si condensation, peroxide radicals, PP beta-scission, grafting, crosslinking.

## Constants

- `1 Hartree = 627.509474 kcal/mol`
- `1 Hartree = 2625.499638 kJ/mol`
- `1 Hartree = 27.211386245988 eV`
- `R = 0.00198720425864083 kcal mol^-1 K^-1`
- Default `T = 350 K`

## Core Formulas

- `ΔGbind = G(complex) - ΣG(fragments)`
- `ΔGpoison = G(O→Ti complex) - G(C=C π-complex)`
- `ΔGπ = G(π-complex) - G(free active site + monomer)`
- `ΔG‡insert = G(insertion TS) - G(free active site + monomer)`
- `ΔG‡complex = G(insertion TS) - G(π-complex)`
- `ΔΔG‡ = ΔG‡candidate - ΔG‡reference`
- `krel = exp[-ΔΔG‡ / RT]`
- `BDE(Si-C) = G(R•) + G(•Si fragment) - G(R-Si)`
- `BDE(Si-O) = G(R•) + G(•O-Si fragment) - G(R-O-Si)`
- `BDE(RO-OR) = G(2RO•) - G(RO-OR)`
- `R_scission = kβ[PP•]`
- `R_branch = krec[PP•]^2 + kg[PP•][M] + kc[PP•][coagent]`
- `S_LCB = R_branch / (R_branch + R_scission + R_oxidation)`

## Decision Rules

- Ti poisoning: `ΔGpoison > +5`, productive C=C insertion favored; `0 <= ΔGpoison <= +5`, coordination competition; `ΔGpoison < 0`, poisoning risk.
- Si-O weakening: longer Si-O, lower WBI, and redshifted Si-O vibration imply Lewis-acid weakening.
- Si-C risk: low BDE or low radical-near-SiC scission barrier implies linker failure risk.
- PP degradation: lower Mw, higher MFR, and low gel imply beta-scission-dominated degradation.
- Effective LCB: SAOS low-frequency enhancement, strain hardening, and low-to-medium gel imply long-chain branching or mild crosslinking.
- Oxidation risk: higher carbonyl index and dielectric loss imply oxidative carbonyl side reactions.

## Evidence Grades

- A: Real computation with method/basis, convergence, frequency/TS/IRC checks where relevant, provenance, and scientific review.
- B: Real experimental data with sample, process, and measurement conditions.
- C: Read-only parser output pending full review, literature clue, or user input not reproduced in the current system.
- D: Mock/example data or hypothesis only.

Parser success alone does not assign A. Store both the current grade and the highest eligible grade after validation.

## Experimental Mapping

- GPC/MFR: Mw decrease plus MFR increase means degradation.
- Gel fraction: low means non-gelled or LCB; medium means mild crosslinking; high means over-gel.
- SAOS/extensional rheology: low-frequency storage modulus enhancement and strain hardening support LCB.
- FTIR: carbonyl index tracks oxidation; Si-O-Si and Si-OH track hydrolysis/condensation.
- NMR: 29Si and 13C track silane and olefin sequence environments.
- DSC/XRD: crystallinity and phase effects.
- TEM/SEM/AFM: EPC domains and interface stabilization.
- Dielectric/space charge: carbonyl traps and electrical risk.
