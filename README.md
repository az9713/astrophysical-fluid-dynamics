# Astrophysical Fluid Dynamics

A rigorous HTML textbook on astrophysical fluid dynamics. The level is final-year
undergraduate to first-year graduate. Derivations are shown in full.

**Read it live:** https://az9713.github.io/astrophysical-fluid-dynamics/

Each module has the same three-part shape:

1. Derive the terrestrial result.
2. Change the regime to the astrophysical one.
3. Check the answer against a measured astronomical number.

Every number in the prose and in the problem solutions comes from a script in
`afd/figs/`. A number used as an input carries a provenance note that says how far
it is trusted. A number compared against a published result carries a box that
names the source and gives the ratio.

## Contents

### Foundations

| # | Module | Status |
|---|---|---|
| 1 | **Why a Fluid at All?** — mean free path, the Coulomb logarithm, the Knudsen number, and the systems where the continuum picture fails | ready |
| 2 | Continuity, Euler, Navier–Stokes, energy — moments of the Boltzmann equation; Lagrangian against Eulerian derivative | planned |
| 3 | Hydrostatic equilibrium — scale height, polytropes, the Lane–Emden equation | planned |
| 4 | Sound waves and linear perturbation theory — the method every later instability reuses | planned |

### Instability

| # | Module | Status |
|---|---|---|
| 5 | Jeans instability — gravity against pressure; the Jeans mass; the Jeans swindle stated openly, then repaired | planned |
| 6 | Convection and thermal instability — Schwarzschild and Field criteria; the multiphase interstellar medium | planned |
| 7 | Rayleigh–Taylor and Kelvin–Helmholtz — supernova ejecta fingers; shredded clouds | planned |

### Shocks and flows

| # | Module | Status |
|---|---|---|
| 8 | Shocks and the Sedov–Taylor blast wave — Rankine–Hugoniot jump conditions; the strong-shock limit | planned |
| 9 | Bondi accretion and the Parker wind — one critical-point calculation, the velocity sign reversed | planned |
| 10 | Turbulence — Kolmogorov in the laboratory; the steeper supersonic spectrum of the interstellar medium | planned |

### Where the field gets hard

| # | Module | Status |
|---|---|---|
| 11 | Accretion discs — angular momentum transport and the Shakura–Sunyaev prescription | planned |
| 12 | Magnetohydrodynamics — flux freezing, magnetic pressure and tension, Alfvén waves, the magnetorotational instability | planned |
| 13 | Radiation hydrodynamics — the Eddington limit; radiation pressure; optically thick and thin regimes | planned |
| 14 | Numerics — grid against smoothed-particle hydrodynamics; the Courant condition | planned |

Modules 1–10 form a closed arc. Modules 11–14 are the advanced tier.

## Layout

```
index.html            redirect to the contents page
afd/index.html        contents
afd/module01.html     module 1
afd/_template_dark.html   the page scaffold
afd/figs/             one numbers script, one figure script, one problem
                      check per module, plus the generated SVGs
afd/figs/splice.py    inserts a generated SVG into its <!--FIG_NAME--> slot
```

## Conventions

- **Units:** CGS-Gaussian throughout (cm, g, s, erg, K, esu, gauss).
- **Numbering:** `Definition N`, `Proposition N`, equations tagged `(S.E)` with
  `S` the section number. Every proposition carries an adjacent proof.
- **Figures** are cited in prose as "Fig. N", never as "the figure below".
- **Every module ends with** a "what it captures / what it misses" section that
  names each idealisation and the module that repays it, then a notation table,
  then a sources list naming every published value compared against.
- The palette is dark: background `#0f172a`, card `#1e293b`, text `#e2e8f0`,
  accents `#fb923c` and `#2dd4bf`.

## Rebuilding the figures and the numbers

Python 3 with NumPy is the only requirement.

```bash
cd afd/figs
python m01_numbers.py          # prints every number the prose quotes
python m01_build_figs.py       # writes m01_fig_*.svg
python splice.py ../module01.html
python m01_problems_check.py   # verifies every problem-set answer
```

`m01_numbers.py` prints a PUNCHLINE line for each comparison against a published
value. Module 1's anchor result is a first-principles Coulomb mean free path of
22.5 kpc against Sarazin (1988)'s published 23 kpc, a ratio of 0.978.

## Sources checked against so far

- Sarazin (1988), §5.4 — intracluster Coulomb mean free path, the Coulomb
  logarithm, and the ion–electron equilibration ratios.
- Randall et al. (2008), ApJ 679, 1173 — the dark matter self-interaction limit.
- "Bimodal distribution of the solar wind at 1 AU", A&A (2020) — solar wind
  proton density and temperature at 1 AU.
- Binney & Tremaine (2008), eq. 1.38 — the two-body relaxation time.
- Maxwell (1867), Phil. Trans. 157, 49 — viscosity independent of density.

## Licence

Not yet chosen.
