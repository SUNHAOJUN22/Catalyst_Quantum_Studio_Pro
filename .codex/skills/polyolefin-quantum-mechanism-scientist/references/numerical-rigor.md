# Numerical Rigor

## Constants

- `1 Hartree = 627.509474 kcal/mol`
- `1 Hartree = 2625.499638 kJ/mol`
- `1 Hartree = 27.211386245988 eV`
- `R = 0.00198720425864083 kcal mol^-1 K^-1`
- Default `T = 350 K`

Keep one canonical source for constants. Test direct and inverse conversions with tolerances.

## Energy Contracts

- `ΔGbind = G(complex) - ΣG(fragments)`
- `ΔGpoison = G(O→Ti) - G(C=C π-complex)`
- `ΔGπ = G(π-complex) - G(free site + monomer)`
- `ΔG‡ = G(TS) - G(free site + monomer)`
- `ΔG‡complex = G(TS) - G(π-complex)`
- `ΔΔG‡ = ΔG‡candidate - ΔG‡reference`
- `krel = exp[-ΔΔG‡/(RT)]`
- `BDE = ΣG(radical fragments) - G(parent)`

Reject missing, non-finite, or unit-ambiguous values. Do not silently mix electronic energies, enthalpies, and Gibbs energies.

## Stable Computation

- Use the minimum energy as the reference for Boltzmann factors.
- Clamp or log-transform exponential calculations to avoid overflow; disclose the numerical policy.
- Require `T > 0`.
- Keep dimensionless quantities explicit.
- For rates, report whether tunneling, symmetry, standard-state, quasi-harmonic, concentration, and transmission-coefficient corrections are included.

## Comparability

Only compare energies when species use compatible:

- method and basis;
- dispersion and solvation;
- standard state and temperature;
- spin treatment;
- fragment definitions;
- thermal correction protocol.

If compatibility is unknown, return a warning and grade the result C at most.

## TS and Radical Checks

- A minimum: no imaginary frequency.
- A TS: exactly one chemically relevant imaginary frequency.
- Insertion TS: mode follows C-C formation and Ti-C migration; IRC connects reactant and product.
- Radical calculations: validate multiplicity and report `<S^2>` contamination.
- BDE: use consistent parent/fragment methods and properly separated radical fragments.

## Uncertainty

Threshold classifications are decision aids, not physical discontinuities. Report proximity to thresholds and sensitivity to plausible numerical uncertainty, especially around `ΔGpoison = 0` and `+5 kcal/mol`.
