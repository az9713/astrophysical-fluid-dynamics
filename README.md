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
| 2 | **Continuity, Euler, Navier–Stokes, energy** — moments of the Boltzmann equation, the closure gap, the Lagrangian against the Eulerian derivative | ready |
| 3 | **Hydrostatic equilibrium** — scale height, polytropes, the Lane–Emden equation; the solar convection zone confirmed as an n = 3/2 polytrope to 1.8%, a standard solar model's convection-zone base refuted at 29σ by helioseismology | ready |
| 4 | **Sound waves and linear perturbation theory** — the wave equation, Newton against Laplace, the acoustic cutoff, the large separation; Laplace agrees with the measured speed of sound in air to 0.04%, an isothermal Sun refuted by a bound 3.25% below the measured solar large separation | ready |

### Instability

| # | Module | Status |
|---|---|---|
| 5 | **Jeans instability** — gravity against pressure, the Jeans mass, the Jeans swindle repaired by an expanding background and by the Bonnor–Ebert sphere; the Jeans criterion at mean density calls every isothermal sphere stable while Barnard 68 sits 2.25σ on the unstable Bonnor–Ebert branch, its outer density slope 3.24 against the 2.5176 ceiling of every isothermal sphere | ready |
| 6 | **Convection and thermal instability** — Schwarzschild, Ledoux and Field criteria, the collapse of ∇_ad in an ionisation zone, mixing-length theory and the two-phase interstellar medium; mixing-length theory over-drives the solar photosphere by a factor 76 in flux and survives to 25% on the measured flux, and the predicted two-phase pressure window contains the measured median of 89 sight lines while the same measurement refutes a static medium, 29% of the cold gas below a floor that allows 0% | ready |
| 7 | **Rayleigh–Taylor and Kelvin–Helmholtz** — one dispersion relation with four terms, the capillary and gravitational cutoffs at opposite ends of the spectrum, the non-linear mixing law and the Richardson number; a laser experiment at the National Ignition Facility confirms h = α_B A g t² and refutes its own abstract's claim to have settled α_B, which leaves an astrophysical mixing width uncertain by a factor 2, while Kelvin–Helmholtz vortices on a coronal mass ejection yield no confirmation but do bound the field along the wavevector at 0.0675 gauss for equal fields on both sides, 0.0954 gauss for a one-sided field. The Rayleigh–Taylor half had no astronomical check of its own; Module 8 supplies one at Tycho, and it refutes the transfer | ready |

### Shocks and flows

| # | Module | Status |
|---|---|---|
| 8 | **Shocks and the Sedov–Taylor blast wave** — the Rankine–Hugoniot conditions as Module 2 integrated across a discontinuity, the compression ceiling (γ+1)/(γ−1), the entropy jump that forbids rarefaction shocks, the isothermal shock that has no ceiling at all, and the Sedov–Taylor similarity solution. Taylor's own twenty-five Trinity photographs confirm the 2/5 exponent to within 2.4 per cent over a factor 620 in time and refute, through the residuals of the same fit, the model that produced it — a 7.3σ trend — while the recovered energy falls 3.8σ short of the modern radiochemical yield. Voyager 2 confirms the ceiling of 4 at Neptune's bow shock and refutes the single-fluid closure at the termination shock, 10⁵ K observed against 10⁶ K predicted. And Module 7's mixing law, carried to Tycho, is short by a factor 11 with the Atwood number and the expansion index both already at their ceilings | ready |
| 9 | **Bondi accretion and the Parker wind** — one critical-point calculation with the velocity sign reversed, so that Bondi's accretion and Parker's wind are the same solution of the same equation. A static corona in a 1/r potential has a floor pressure at infinity, 2.4×10⁸ times the interstellar value, so it cannot be static. Eleven checks, of which seven refute: the isothermal wind fails three ways, the single-polytrope repair places its critical point at 1.020 R_☉ below its own 1.03 R_☉ base, and steady Euler with the measured pressure gradient still under-predicts the observed acceleration by a factor 2.98. At Sgr A* the Bondi rate exceeds Marrone et al.'s upper limit by 40 — 4 if the field is 3 per cent of equipartition — and their field-independent lower limits by at least 401, while the X-ray efficiency is 4×10⁻⁹ against a thin disc's 0.1. Bondi's own Summary proves only λ ≤ λ_c, so what the data refute is the physics assumed and never the algebra | **ready** |
| 10 | **Turbulence** — Kolmogorov 1941 from two units and no fitting, the dissipation scale and the Re³ cost of resolving it, the 4/5 law, and the steeper supersonic **exponent** of the interstellar medium; the spectrum is an inference through δv ∝ ℓ^h ⇒ E(k) ∝ k^−(1+2h) and is measured nowhere here. Four checks, of which two refute. The terrestrial constant C_K = 0.53 ± 0.055 holds across more than 100 flows and 4.60 decades in Reynolds number. The anchor is Podesta et al.'s solar wind at 1 au: the mean magnetic exponent confirms 5/3 to 0.70 per cent (t = −0.41 on 3 dof, p = 0.71) while the velocity exponent is refuted interval by interval, 3.8 to 8.3 half-widths below and all on one side. Hitomi's Perseus dispersion prices Module 3's "static" idealisation at 3.98 per cent of the mass, 7.66 if the large-scale shear doubles it. Solomon et al.'s 273 clouds give a size–linewidth exponent 0.50 ± 0.05, which lies 3.33 systematic envelopes from Kolmogorov's 1/3 and exactly on Burgers' 1/2. And the intracluster medium's collisional Reynolds number is 0.90 at Kn = 0.375, a formula outside its own domain, so the magnetised bound Re⊥ ≥ 4.68×10¹² is what the observed cascade runs on | **ready** |

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
afd/module01.html     module 1 (module02.html to module06.html likewise)
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

Each module has the same four scripts, with `m02_` in place of `m01_` and so on.
Every numbers script prints a PUNCHLINE line for each comparison against a
published value.

Module 1's anchor result is a first-principles Coulomb mean free path of 22.5 kpc
against Sarazin (1988)'s published 23 kpc, a ratio of 0.978.

Module 2's anchor is sharper, because it tests an exact conservation law
rather than a coefficient. Steady spherically symmetric continuity requires
that the radial exponents of solar wind density and speed, n ∝ r^−α and
v ∝ r^+β, satisfy α − β = 2 exactly. Venzmer & Bothmer (2018) fitted the two
exponents independently to Helios data, with no continuity constraint imposed
on the fitting; their mean fits give 1.961 and their median fits 2.035,
bracketing the prediction with a midpoint of 1.998. The same table breaks the
adiabatic energy equation, whose predicted temperature exponent of −1.340 sits
19.6 standard deviations from the measured −0.792 — the wind is heated as it
expands.

Module 3 tests closures, not the hydrostatic equation itself, because the
standard solar model it reads (BS2005-AGS,OP) was built by solving that
equation. The convection zone gives an effective polytropic index of 1.527
against the 3/2 fixed in advance by adiabatic convection, a ratio of 1.018.
Eddington's n = 3 predicts a central condensation of 54.18 against the
tabulated 106.88. The model's convection-zone base, 0.7280 R, lies 29.4
standard deviations from the helioseismic (0.7133 ± 0.0005) R of Basu & Antia
(2004): the solar abundance problem.

## Sources checked against so far

- Sarazin (1988), §5.4 — intracluster Coulomb mean free path, the Coulomb
  logarithm, and the ion–electron equilibration ratios.
- Randall et al. (2008), ApJ 679, 1173 — the dark matter self-interaction limit.
- "Bimodal distribution of the solar wind at 1 AU", A&A (2020) — solar wind
  proton density and temperature at 1 AU.
- Binney & Tremaine (2008), eq. 1.38 — the two-body relaxation time.
- Maxwell (1867), Phil. Trans. 157, 49 — viscosity independent of density.
- Venzmer & Bothmer (2018), A&A 611, A36 — radial power-law fits to Helios 1 and
  2 solar wind data over 0.29–0.98 AU: density, speed and temperature exponents.
- Verscharen, Bale & Velli (2021), MNRAS 506, 4993 — solar wind mass flux at 1 AU.
- Bahcall, Serenelli & Basu (2005), ApJ 621, L85 — the tabulated standard solar
  model BS2005-AGS,OP and its convection-zone base.
- Basu & Antia (2004), ApJ 606, L85 — the helioseismic convection-zone base.
- Chandrasekhar (1939), ch. IV, Table 4 — polytrope constants for n = 3.
- ISO 2533:1975 / US Standard Atmosphere 1976 — the standard atmosphere.

## Licence

Not yet chosen.
