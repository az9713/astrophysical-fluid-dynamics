# Delta scientific and prose audit

*Astrophysical Fluid Dynamics* · Modules 13–14, with a focused all-module pass

Signed: **Codex — OpenAI** | 22 September 2026 | America/Los_Angeles

## Verdict: not yet teachable

Modules 13 and 14 contain substantial useful material, including explicit assumptions, reproducible numerical runs, source lists, worked exercises and several careful derivations. They are not yet reliable textbook chapters. Module 13 overstates a photospheric diffusion estimate as a refutation and applies Thomson scattering outside its stated domain. Module 14 makes a false norm-independent claim about SPH convergence and presents a representation-dependent grid estimate as a bound on every numerical scheme.

The prose has not yet met the twenty-rule standard. It remains dense, self-conscious and editorial. Much of it describes drafts, gates, plans, debts, checks and shipped pages. The reader is repeatedly asked to follow the history of manuscript production rather than the physical argument.

### Module verdicts

| Module | Verdict | Reason |
|---|---|---|
| 13 — Radiation hydrodynamics | **Not yet teachable** | The central photospheric verdict exceeds the validity of its diffusion closure; the Eddington discussion needs spectral and composition qualifications. |
| 14 — Numerical methods | **Not yet teachable** | The SPH convergence verdict is false without a norm, and the universal resolution bound is overclaimed. |
| 1–12 focused follow-up | **Substantial revision still required** | The new rubric confirms pervasive long-sentence load, production narration and unresolved evidence labels. This was a focused pass, not a second complete scientific audit. |

## Scope and method

The deep audit covers the scientific narrative, major claims, equations, numerical checks, figures, captions, conclusions and selected exercises of Modules 13 and 14. The all-module follow-up applies checks that became explicit in the twenty-rule rubric: sentence load, production narration, evidence-verdict language, evidence taxonomy, duplicate anchors and local links. It does not replace the full Modules 1–12 audit dated 20 September 2026.

The module files were not edited. Baseline SHA-256 hashes were recorded for all fourteen modules. The original problem-check programs were rerun: Module 13 passed 83 checks and Module 14 passed 80. Module 14's full numerical generator also completed with all assertions passing. Passing the supplied assertions establishes internal reproducibility; it does not validate the interpretation of every result.

Independent calculations tested the claims most likely to change a conclusion. They recomputed the photospheric optical-depth scales, the Klein–Nishina correction, SPH pressure errors in two norms and the reported Sedov shock-position errors. Full machine-readable results accompany this report.

## Executive findings

- **Two blocking findings:** the Module 13 boundary-layer diffusion verdict and the Module 14 norm-free SPH non-convergence verdict.
- **Seven module-level major findings:** Thomson-limit scope, inherited Sgr A* interpretation, composition scope, post-hoc validation, a universal grid bound, finite-resolution shock position, and misuse of formal order.
- **Two book-wide major findings:** unresolved evidence labels and failure of the twenty-rule prose standard.
- **No structural HTML failures:** no duplicate IDs and no broken local module links were found.
- **Originals preserved:** the final integrity file compares all fourteen original module hashes with the baseline.

## Ranked findings

### M13-C01 — Blocking: A boundary-layer diffusion estimate is presented as a refutation of adiabatic oscillations

**Location:** afd/module13.html:399

**Rubric:** Rules 9, 10, 12 and 14; scientific claim standard 1–4

> CHECK 3 — the adiabatic assumption is REFUTED at the photosphere

Equation (4.4) was derived after imposing the optically thick diffusion closure. The module itself says that this law fails at a stellar surface. The check nevertheless evaluates it at Rosseland optical depth 2/3. The local mean free path is 84.16 km and the acoustic wavelength is 2615 km, so the wavelength spans about 31 local optical depths; however, the outward boundary is only 2/3 optical depth away. A local diffusion estimate can show that heat leakage is plausibly important, but it does not solve the non-adiabatic transfer problem with the photospheric boundary condition. Values of 0.34–0.45 therefore show that the adiabatic limit is not well controlled under this estimate. They do not refute the complete adiabatic oscillation model.

**Proposed replacement — not applied:**

```html
<div class="keyresult"><b>CHECK 3 — radiative leakage may be important near the photosphere.</b> Using the local ATLAS9 opacity and density in the diffusion estimate gives $\omega\chi/c_{\rm s}^2=0.4468$ at $T=5772$ K and $0.3445$ at $\tau_{\rm R}=2/3$. Neither value is much smaller than unity, so the adiabatic approximation is not asymptotically controlled in these layers. This calculation is only an estimate: radiative diffusion assumes an optically thick, nearly isotropic field, whereas the outward optical depth at the photosphere is $2/3$. A quantitative damping rate requires a non-adiabatic oscillation calculation coupled to radiative transfer and the surface boundary condition.</div>
```

### M13-C02 — Major: The Thomson opacity is treated as a frequency-independent floor for every spectrum

**Location:** afd/module13.html:493

**Rubric:** Rules 9, 10 and 12; scientific limits and rescue cases

> For electron scattering, sigma_T does not depend on frequency ... whatever the spectrum

The statement is valid only in the Thomson limit, $h\nu\ll m_ec^2$, for free non-relativistic electrons. At higher photon energies the Klein–Nishina cross-section falls below the Thomson value. Direct evaluation gives 0.963, 0.741 and 0.431 times $\sigma_T$ at 10, 100 and 511 keV. Electron scattering therefore is not a spectrum-independent opacity floor for arbitrary radiation fields. The missing restriction matters in a chapter that applies the Eddington limit to compact objects.

**Proposed replacement — not applied:**

```html
<p>For fully ionised gas illuminated by photons with $h\nu\ll m_ec^2$, scattering is in the Thomson regime and $\sigma_T$ is effectively independent of frequency. In that limit, and when other opacities are negligible, $\kappa_{\rm F}=\kappa_{\rm es}=\sigma_T(1+X)/(2m_p)$. At X-ray and gamma-ray energies the Klein–Nishina cross-section decreases with photon energy, so the flux-mean scattering opacity and the corresponding Eddington luminosity depend on the spectrum.</p>
```

### M13-C03 — Major: Module 13 repeats an invalid Sgr A* refutation from Module 9

**Location:** afd/module13.html:563

**Rubric:** Rules 10, 14 and 18; evidence interpretation

> That refutation is Module 9's and is cited, not re-checked

The earlier audit showed that Module 9 divides a 2–10 keV luminosity by the rest-mass power of the outer Bondi supply and calls the result a radiative efficiency. This compares a band luminosity with a supply rate at another radius and then compares the ratio with a bolometric thin-disc efficiency. Module 13 reproduces the arithmetic and imports the invalid inference. A cross-reference does not insulate a new chapter from a known error in the referenced chapter.

**Proposed replacement — not applied:**

```html
<p>Sagittarius A* has a 2–10 keV luminosity of $3.70\times10^{-12}L_{\rm Edd}$ in the inputs used by Module 9, while its Bondi supply estimate is $8.405\times10^{-5}\dot M_{\rm Edd}$. Their ratio is $4.40\times10^{-9}$. This is a band-limited luminosity divided by the rest-mass power associated with an outer supply estimate; it is not a measured bolometric efficiency of gas reaching the black hole. Interpreting the ratio requires a bolometric correction and a model for mass loss between the Bondi radius and the emitting flow.</p>
```

### M13-C04 — Major: A solar abundance is presented as the appropriate composition for black-hole accretion

**Location:** afd/module13.html:516

**Rubric:** Rules 1, 10 and 12; precise statement and defined scope

> X = 0.7261 ... is the apt value for gas a black hole accretes

The initial solar hydrogen fraction is appropriate for protosolar gas, not for black-hole accretion in general. Accreted gas can be metal poor, enriched, hydrogen deficient, partially ionised, pair loaded or drawn from a stellar companion. The useful result is the parametric dependence $L_{\rm Edd}\propto2/(1+X)$ in the fully ionised Thomson limit. The worked solar-composition value should remain an example, not a default physical claim.

**Proposed replacement — not applied:**

```html
<p>The pure-hydrogen formula corresponds to $X=1$. For fully ionised gas in the Thomson regime, composition enters through $\kappa_{\rm es}=\sigma_T(1+X)/(2m_p)$, so $L_{\rm Edd}\propto2/(1+X)$. The value $X=0.7261$ is the initial hydrogen fraction in the cited solar model and provides one worked example. It is not a universal composition for black-hole accretion; the appropriate $X$ must be chosen for the gas being modelled.</p>
```

### M13-C05 — Major: A post-hoc tolerance is used to label an opacity comparison confirmed

**Location:** afd/module13.html:322

**Rubric:** Rules 10, 11 and 14; evidence standard

> CONFIRMED as a column mean ... The tolerance ... was computed after the 1.1482 was known

The text candidly states that the acceptance band was selected after the result was known. That prevents the band from functioning as a validation criterion. The comparison can still be reported: the inferred and ATLAS9 column means differ by factors 1.016 and 1.148, and the discrepancy traces mainly to the borrowed pressure. The word confirmed overstates what the calculation establishes.

**Proposed replacement — not applied:**

```html
<div class="keyresult"><b>CHECK 2 — comparison with an ATLAS9 column mean.</b> Equation (6.1) gives $\bar\kappa_{\rm R}=0.15231\ \mathrm{cm^2\,g^{-1}}$. The ATLAS9 column mean is 0.15470 at the layer where $T=5772$ K and 0.17487 at $\tau_{\rm R}=2/3$, giving ratios of 1.0157 and 1.1482. This agreement is descriptive because no acceptance tolerance was specified before the comparison. Read as a local opacity, equation (6.1) is low by factors 2.36–2.92; it is a column mean and should not be used as a local coefficient.</div>
```

### M14-C01 — Blocking: A maximum-norm result is generalized into non-convergence

**Location:** afd/module14.html:633

**Rubric:** Rules 10, 12 and 14; numerical convergence standard

> Standard SPH REFUTED as convergent there; the repair CONFIRMED

The module reports only the largest pressure error in a fixed neighbourhood of the contact. That error stays near 9%, which is evidence against uniform or maximum-norm convergence over the sampled resolutions. It does not establish non-convergence in other norms. Reintegrating the saved particle states gives relative $L_1$ errors of 0.05108, 0.02412 and 0.01289 at 200, 400 and 800 particles per unit length. Standard SPH therefore converges in this $L_1$ measure over the same runs. Artificial conductivity reduces the maximum error, but three resolutions do not establish a general asymptotic theorem for the repaired method.

**Proposed replacement — not applied:**

```html
<div class="keyresult"><b>CHECK 4 — pressure error at an SPH contact.</b> For standard SPH, the maximum relative pressure error within 0.05 of the contact is 0.0893, 0.0938 and 0.0942 at 200, 400 and 800 particles per unit length. These runs show no maximum-norm convergence over this resolution range. The corresponding volume-weighted relative $L_1$ errors are 0.0511, 0.0241 and 0.0129, so the integrated error does decrease. With Price's artificial conductivity, the maximum error falls to 0.0371, 0.0310 and 0.0216. The added conductivity improves this test, but the conclusion must specify the norm and the sampled resolutions.</div>
```

### M14-C02 — Major: A one-cell scaling estimate is called a bound for any numerical scheme

**Location:** afd/module14.html:655

**Rubric:** Rules 9, 10 and 12; assumptions and limits

> A bound for any scheme. No scheme can represent a structure narrower than one cell

The estimate assumes one characteristic degree of freedom per cell, a local grid scale $L/N$, Kolmogorov scaling, and the weak requirement that the dissipation scale occupy one cell. High-order finite-volume, discontinuous-Galerkin, spectral, interface-tracking and subcell methods do not fit the literal claim. Moreover, one cell across a dissipative structure is normally not an accuracy criterion. The $N^{4/3}$ relation is a useful dimensional scaling for a particular representation, not a universal theorem.

**Proposed replacement — not applied:**

```html
<p><b>A grid-scale estimate.</b> Suppose a local discretisation has one characteristic spatial scale $\Delta x=L/N$ and requires the Kolmogorov scale $\eta$ to be no smaller than $\Delta x$. Then $L/\eta=\mathrm{Re}^{3/4}$ gives the necessary estimate $\mathrm{Re}\lesssim N^{4/3}$. It yields $1.032\times10^4$ for $N=1024$ and $6.554\times10^4$ for $N=4096$. This is not a universal accuracy bound: practical calculations need several effective degrees of freedom across the smallest relevant structure, and the number depends on the method and error criterion.</p>
```

### M14-C03 — Major: Conservation is said to fix the finite-resolution shock position

**Location:** afd/module14.html:569

**Rubric:** Rules 10, 12 and 14; numerical validation

> the position of the shock is fixed by conservation of energy and mass

The measured half-height locations are 1.02764, 1.01365 and 1.00663 rather than the exact radius 1. Conservation gives the correct integral constraints and is essential for convergence to the weak solution, but it does not uniquely fix a numerical shock position at finite resolution. The data demonstrate first-order convergence of the chosen position estimator. They do not confirm an exact position.

**Proposed replacement — not applied:**

```html
<div class="keyresult"><b>CHECK 3 — convergence in the Sedov test.</b> The half-height estimate of the shock radius is 1.02764, 1.01365 and 1.00663 on 100, 200 and 400 cells. Its absolute error approximately halves when the resolution doubles, consistent with first-order convergence toward the exact radius 1. The peak density remains below the exact jump value because the shock is spread over several cells. Conservative updating preserves the integral balances that select the correct weak solution, but it does not make the finite-resolution shock position exact.</div>
```

### M14-C04 — Major: The formal order of a scheme is said to be refuted by a discontinuous solution

**Location:** afd/module14.html:505

**Rubric:** Rules 10 and 14; defined terms

> the formal order REFUTED

Formal order is defined for a specified scheme, regularity class and norm. A contact discontinuity violates the smoothness assumptions behind the usual first-order truncation estimate and can reduce global convergence. The experiment illustrates that distinction; it does not refute the scheme's formal order. The module's own contact-width derivation is useful once the verdict is corrected.

**Proposed replacement — not applied:**

```html
<div class="keyresult"><b>CHECK 2(b) — convergence is limited by the contact.</b> From $N=100$ to 6400, the density $L_1$ error falls with measured orders 1.013 at the shock, 0.511 at the contact, 0.752 in the fan and 0.646 overall. Equation (5.1) predicts the contact's $\Delta x^{1/2}$ scaling without a fitted parameter. The result does not contradict the method's formal first-order accuracy for smooth solutions. It shows that a discontinuity can control the global error and reduce the observed convergence rate in this norm.</div>
```

### BOOK-C01 — Major: Simulation and model outputs are still labelled as measurements in older modules

**Location:** afd/module01.html–afd/module14.html

**Rubric:** Rules 8, 10, 12 and 18; source and evidence standard

> Examples include module12.html:683, module08.html:878 and module05.html:703

Module 14's census correctly exposes an unresolved book-wide taxonomy problem. Examples include the Zhuravleva simulation comparison in Module 12, the Wang–Chevalier simulation width in Module 8, ATLAS9 outputs in Module 5, BS05 model quantities in Modules 3 and 6, and a simulation-derived velocity in Module 7. Listing the errors in Module 14 does not repair the original pages. Each occurrence should say measured, simulated, model-derived or inferred according to its provenance.

**Proposed replacement — not applied:**

```html
<p>Use <b>measured</b> only for quantities directly constrained by observations or experiments. Use <b>model-derived</b> for atmosphere and stellar-structure tables, <b>simulation output</b> for numerical hydrodynamics, and <b>inferred by comparison with simulations</b> when an observation is interpreted through a simulation. State the inference chain beside the number.</p>
```

### BOOK-P01 — Major: The twenty-rule prose standard is not yet satisfied

**Location:** afd/module01.html–afd/module14.html

**Rubric:** Rules 1–8 and 13–19

> The mechanical screen found 782 sentences above 35 words

The screen found 782 sentences longer than 35 words across the fourteen modules. Module 13 contains 60 and Module 14 contains 39. Length alone is not a quality verdict, but inspection confirms repeated clause chains, production history, courtroom labels, source-audit narration and paragraphs that carry several independent ideas. These features produce the same mechanical, non-human textbook voice identified in the first audit.

**Proposed replacement — not applied:**

```html
<p>Rewrite the narrative paragraph by paragraph. Give each paragraph one physical idea, place assumptions beside the result they restrict, and reserve source disputes for notes. Replace CONFIRMED and REFUTED with the measured quantity, its uncertainty or error norm, and the inference that follows. Remove references to drafts, gates, plans, shipped pages, editors and debts from the teaching narrative.</p>
```

## Independent numerical checks

### Module 13: photospheric locality

At the ATLAS9 $\tau_R=2/3$ point, the local photon mean free path is 84.155 km. The acoustic wavelength used by the module is 2615.2 km, giving an optical depth of 31.08 across one wavelength if the local opacity is held fixed. This supports using diffusion as a local scale estimate within the material. It does not remove the free-surface problem: the outward optical depth from the evaluation point is only 2/3. The report therefore does not say the numerical estimate is useless; it says its advertised refutation is too strong.

### Module 13: energy dependence of electron scattering

The integrated Klein–Nishina formula gives the following total cross-sections per free electron:

| Photon energy | $\sigma_{KN}/\sigma_T$ |
|---:|---:|
| 10 keV | 0.96276 |
| 100 keV | 0.74070 |
| 511 keV | 0.43073 |

The Thomson value is the low-energy limit, not a spectrum-independent floor.

### Module 14: SPH convergence depends on the norm

The independent calculation used the module's saved particle states and the same contact neighbourhood. It integrated the pressure error over particle volumes.

| Particles per unit length | Maximum relative error | Volume-weighted relative $L_1$ error |
|---:|---:|---:|
| 200 | 0.08927 | 0.05108 |
| 400 | 0.09381 | 0.02412 |
| 800 | 0.09424 | 0.01289 |

The maximum error does not fall, while the integrated error falls by nearly a factor of two per doubling. Both statements can be true because the pressure blip becomes narrower. A convergence claim must name the norm.

### Module 14: Sedov location

The reported half-height radii differ from the exact radius by 0.02764, 0.01365 and 0.00663. The error nearly halves at each doubling, which is evidence for first-order convergence of that estimator. It is not evidence that conservation makes the finite-resolution position exact.

## Twenty-rule compliance

| Rule | Modules 13–14 | Evidence |
|---:|---|---|
| 1 | Fail | Academic content is obscured by mechanical, editorial prose. |
| 2 | Fail | Several paragraphs carry derivation, provenance, verdict and cross-module commentary at once. |
| 3 | Fail | Module 13 has 60 sentences above 35 words; Module 14 has 39. |
| 4 | Fail | Long semicolon, parenthesis and comma chains are common. |
| 5 | Fail | CONFIRMED, REFUTED, debts and punchline rhetoric recur. |
| 6 | Partial | Personification is less common than in earlier modules, but debt and repayment metaphors remain. |
| 7 | Fail | Drafts, gates, plans, editors, readers and shipped pages appear in the narrative. |
| 8 | Fail | Source criticism and editorial provenance interrupt physical exposition. |
| 9 | Mostly pass | Notation tables are strong, but some assumptions are supplied after conclusions. |
| 10 | Fail | Implementation checks, approximations and validation claims are repeatedly conflated. |
| 11 | Partial | Some uncertainties are well named; other qualifications are rhetorical or post hoc. |
| 12 | Fail | The Thomson and diffusion qualifications are not placed beside the claims they restrict. |
| 13 | Fail | Announcements such as check, finding, verdict and what is refuted recur. |
| 14 | Fail | The most serious scientific errors are framed as CONFIRMED or REFUTED. |
| 15 | Fail | Transitions often follow the production plan or old-module debts. |
| 16 | Partial | Paragraphs are generally bounded, but several are much too dense. |
| 17 | Fail | Read aloud, many paragraphs sound like an audit log rather than a textbook. |
| 18 | Partial | Cross-links are extensive, but Module 13 inherits a known Module 9 error. |
| 19 | Fail | Grammatically valid but unnatural sentences were retained in large numbers. |
| 20 | Pass | This audit did not modify any original module HTML. |

## Representative prose rewrites

These examples address voice and structure in addition to the scientific replacements above. They are proposals only.

### Module 13, line 98

**Current:** “Photons carry momentum, and a fluid that is lit from inside feels it. This module derives the Eddington limit that five shipped pages have been quoting, prices the composition hidden in its proton mass, and evaluates the one computation the book deferred by name.”

**Rewrite:**

> Radiation transports momentum as well as energy. This chapter derives the radiative force, the diffusion limit and the Eddington luminosity. It then examines how opacity and composition change those results in stellar atmospheres and accreting systems.

### Module 13, line 208

**Current:** The paragraph explains what a “step-1 generator” wrote and what “Gate D” required.

**Rewrite:**

> The factor $1/3$ follows from the angular average in the diffusion closure. It is the radiative analogue of the factor in kinetic-theory transport coefficients. Consequently, photons with speed $c$ and mean free path $\lambda_{ph}$ have diffusion coefficient $D=c\lambda_{ph}/3$.

### Module 13, line 313

**Rewrite:**

> Module 6 gives the photospheric pressure, density and scale height at optical depth $\tau=2/3$, but it does not state an opacity. Hydrostatic balance converts the pressure into a column mass. The condition $\tau=2/3$ then determines the column-averaged Rosseland opacity, which can be compared with an atmosphere model.

### Module 14, line 147

**Rewrite:**

> Consider constant-speed advection, $\partial_tu+a\partial_xu=0$, with $a>0$. Its exact solution is $u(x,t)=u_0(x-at)$. The upwind method takes the interface flux from the upstream cell, whereas FTCS averages the two adjacent states. Their amplification factors show why satisfying the Courant condition is necessary but not sufficient for stability.

### Module 14, line 213

**Rewrite:**

> An explicit compressible solver is limited by the signal speed $|u|+c_s$, not by the flow speed alone. Its step count therefore exceeds the incompressible estimate by $1+1/M$, where $M=U/c_s$. The correction is 35.0 for the subsonic wind-tunnel example and 1.092 for the supersonic cloud. Module 10's work estimate is consequently a lower bound for an explicit compressible calculation.

### Module 14, line 425

The present paragraph is 79 words in its longest sentence and develops several ideas at once. It should become a short sequence: first identify the contact as an upwind advection problem; then derive the variance; then invoke the Gaussian limit with its conditions; finally derive the $L_1$ error. The derivation is worth retaining, but its current packaging makes it unnecessarily difficult to follow.

## Focused all-module prose screen

The sentence parser strips HTML and mathematics before splitting punctuation. It is approximate: abbreviations and displayed expressions can produce false splits. It is a triage instrument, not a prose score.

| Module | Sentences | 15–25 words | 36–50 words | Over 50 | Total over 35 |
|---|---:|---:|---:|---:|---:|
| module01.html | 350 | 86 | 37 | 11 | 48 |
| module02.html | 299 | 96 | 27 | 7 | 34 |
| module03.html | 324 | 108 | 18 | 3 | 21 |
| module04.html | 320 | 81 | 23 | 2 | 25 |
| module05.html | 440 | 124 | 26 | 12 | 38 |
| module06.html | 501 | 110 | 57 | 31 | 88 |
| module07.html | 397 | 77 | 42 | 28 | 70 |
| module08.html | 558 | 141 | 66 | 26 | 92 |
| module09.html | 532 | 122 | 60 | 40 | 100 |
| module10.html | 543 | 137 | 61 | 18 | 79 |
| module11.html | 254 | 69 | 20 | 7 | 27 |
| module12.html | 414 | 105 | 43 | 18 | 61 |
| module13.html | 319 | 79 | 42 | 18 | 60 |
| module14.html | 351 | 55 | 27 | 12 | 39 |


Total sentences above 35 words: **782**. The highest counts occur in Modules 9 (100), 8 (92), 6 (88) and 10 (79). This result confirms that the prose problem is book-wide. A mechanical split is not enough; each paragraph needs a human editorial pass that restores argument, emphasis and rhythm.

## Evidence taxonomy in Modules 1–12

Module 14's census identifies genuine unresolved labels in older chapters. The following should be corrected when a revised edition is authorised:

- Module 12 lines 683, 690, 692 and 955: the Zhuravleva constraint depends on comparison with direct numerical simulations; it is not a direct viscosity measurement.
- Module 8 lines 878, 883 and 939: the quoted Tycho width is simulation-derived, although the table calls the widths observed.
- Module 1 lines 607 and 690: the Randall constraint is inferred through simulations, not directly observed.
- Module 5 lines 703, 709, 744 and 747: ATLAS9 quantities are atmosphere-model outputs.
- Module 6 lines 216, 342, 345 and 426: the BS05 slope is model-derived.
- Module 3 lines 182 and 630: values from a standard solar model should be labelled as model values.
- Module 7 line 516: the extracted coefficient uses a simulation velocity.
- Module 11 lines 211, 583 and 600: the claimed measured range $\alpha=0.1$–0.4 requires a verified primary-source chain.

## What should be retained

Module 13's derivation of the column-mean opacity from $m=P/g$ is clear and physically useful once the post-hoc verdict is removed. Its distinction between local and column-mean opacity is essential. The definition of flux-mean opacity is also the right starting point for the Eddington force balance.

Module 14's conservative finite-volume update, CFL necessity-versus-stability distinction, exact Sod solution and region-by-region error decomposition form a strong numerical-methods spine. The contact-width calculation is especially valuable when split into readable stages. The Jeans-resolution section clearly distinguishes an empirical criterion from a derived density scaling. The limitations table is unusually candid and should survive after production-history language is removed.

## Source evidence map

| Finding | Evidence read | What it establishes |
|---|---|---|
| M13-C01 | Module 13's own Proposition 4 and surface discussion; independent optical-depth calculation | Diffusion assumes an optically thick nearly isotropic field; the evaluation point has only 2/3 outward optical depth. |
| M13-C02 | CERN Geant4 Physics Reference Manual, citing Klein & Nishina (1929) | Compton scattering depends on photon energy; Thomson scattering is a low-energy limit. |
| M13-C03 | Existing signed audit of Module 9; Module 13's reproduced inputs | The arithmetic is reproducible, but the band-luminosity interpretation is invalid. |
| M13-C04 | Bahcall, Serenelli & Basu (2005), Table 1 | $X=0.7261$ is a solar-model initial abundance, not a universal accretion composition. |
| M14-C01 | Price (2008); independent integration of the saved SPH states | Artificial conductivity addresses the pressure blip; convergence still requires a named norm. |
| M14-C04 | Banks, Aslam & Rider (2008) | Captured linearly degenerate waves can converge sublinearly; this does not refute formal order for smooth solutions. |

Primary links: [Price 2008](https://arxiv.org/abs/0709.2772), [Banks, Aslam & Rider 2008](https://www.osti.gov/servlets/purl/945128), [CERN Geant4 Compton reference](https://geant4.web.cern.ch/documentation/dev/prm_html/PhysicsReferenceManual/electromagnetic/gamma_incident/compton/compton.html), [Bahcall, Serenelli & Basu 2005](https://arxiv.org/abs/astro-ph/0412440).

## Production and preservation checks

- Duplicate HTML IDs: **0**.
- Broken local links among module and index pages: **0**.
- Module 13 problem checker: **83 checks, 0 failures**.
- Module 14 problem checker: **80 checks passed**.
- Module 14 full generator: **all assertions passed**.
- Original module edits made by Codex: **none**.

The HTML passed structural parsing, signature, finding-ID, duplicate-anchor and rubric-completeness checks. The in-app browser's security policy blocked opening this new local `file:` URL, so this delta report does not claim a fresh visual desktop/mobile rendering check. The earlier report's visual check cannot substitute for this file.

The audit artifacts contain the baseline hashes, independent calculations, fresh-run logs, mechanical screen and final integrity comparison. The unrelated untracked file `afd-stem-textbook-runbook.html` was left untouched and is not part of the audit commit.

## Recommended revision order

1. Correct M13-C01 and M14-C01 before using the chapters for instruction.
2. Repair the other major scientific qualifications and remove the inherited Sgr A* verdict.
3. Replace verdict rhetoric with quantities, assumptions, norms and limits.
4. Move source disputes, production history and the evidence census into editorial appendices or provenance notes.
5. Perform a paragraph-level human rewrite under all twenty rules, then rerun numerical and rendering checks.
6. Apply the evidence taxonomy to Modules 1–12 in the separate revised edition only.

## Signature

This report is independent work by **Codex — OpenAI**. It is not part of the Claude-authored textbook text and does not modify any original module.

Signed: **Codex — OpenAI**

Date: **22 September 2026**

Place: **America/Los_Angeles**

## Appendix A — Full governing rubric

### Codex textbook audit rubric

This rubric governs the independent scientific and editorial audit of the *Astrophysical Fluid Dynamics* modules. It combines the twenty-rule prose standard with checks for scientific correctness, evidence, derivations, pedagogy, notation, and production quality.

The audit must not modify existing module files. Findings, evidence, proposed replacements, and any later rewritten edition belong inside the `codex-audit-2026-09-20` folder.

## A. Twenty-rule prose standard

1. Write in clear, natural academic English suitable for advanced undergraduate or beginning graduate readers.
2. Give each paragraph one identifiable idea. State it, explain it, and identify its physical consequence.
3. Prefer sentences of 15–25 words. Split sentences longer than about 35 words unless their structure is exceptionally clear.
4. Do not combine independent claims using comma chains, semicolons, parentheses, or repeated dashes.
5. Remove synthetic rhetoric, dramatic verdicts, slogans, fake suspense, and self-conscious commentary.
6. Avoid personification such as “the answer lives here,” “the theory pays a debt,” or “the premise is spent.”
7. Keep the writing and production process out of the textbook narrative.
8. Separate physical exposition from source criticism and editorial provenance.
9. Define every symbol before use and state assumptions before drawing conclusions.
10. Distinguish derivations, approximations, empirical comparisons, interpretations, and conjectures.
11. Use cautious language only for a specific, identifiable uncertainty.
12. Place each qualification immediately beside the claim it restricts.
13. Remove repetitive announcements such as “this is the result” or “this is the point.”
14. Avoid casual claims that evidence “confirms” or “refutes” a theory. Present the comparison and justified inference.
15. Base transitions on the scientific argument rather than the module-production process.
16. Keep paragraphs reasonably short without creating choppy sequences of one-sentence paragraphs.
17. Apply a read-aloud test and rewrite prose that sounds bureaucratic, mechanical, theatrical, or unnatural.
18. Check adjacent modules for consistent terminology, notation, assumptions, and scientific conclusions.
19. Retain an existing sentence only if it already meets the textbook standard, not merely because it is grammatical.
20. Do not modify the existing module files. Any revised edition must be placed in a separate folder.

## B. Scientific claim standard

Every substantive claim must satisfy five requirements:

1. **Precise statement.** State exactly what is claimed and under which conditions.
2. **Defined terms.** Define every variable, technical term, convention, and reference frame before use.
3. **Visible mechanism.** Derive the result in the smallest setting that reveals why it is true.
4. **Limits and rescue cases.** State where the result fails and what added physics modifies or restores it.
5. **Concrete connection.** Connect the claim to a calculation, observation, simulation, figure, or primary source.

The audit also checks algebra, calculus, signs, factors, units, dimensions, substitutions, initial and boundary conditions, constitutive assumptions, closure relations, limiting cases, internal consistency, inequality directions, statistics, and consistency among equations, prose, tables, figures, captions, examples, exercises, and conclusions.

## C. Sources and evidence

- Read the primary source behind each important citation and verify the cited passage.
- Check numerical values against the source’s definitions, tables, and units.
- Distinguish measurements, model outputs, fitted parameters, reconstructed quantities, and assumptions.
- Flag citations that support only a weaker claim or cannot be verified.
- Do not repair citations from memory.
- Check whether the module’s calculations or later evidence contradict its interpretation.
- Preserve a source map connecting major findings to their evidence.

## D. Derivations, calculations, and exercises

- Reproduce important derivations independently and inspect intermediate steps.
- Test dimensions, signs, simple limits, and selected numerical examples.
- Check whether displayed numerical precision is justified.
- Confirm that exercises are solvable from the preceding text and verify worked solutions where supplied.
- Distinguish a code implementation check from independent scientific validation.

## E. Pedagogy and structure

- Open with a clear physical question and motivate concepts before formalism.
- Supply a nearby worked example for each major new concept.
- Keep dependencies backward-pointing or prove required material in place.
- Move coherently from assumptions through derivation to interpretation.
- Use scientifically motivated transitions.
- Close by stating what the reader can now calculate or understand.
- Arrange exercises in increasing difficulty and make them self-contained.
- Require every figure to add information and every caption to stand alone.
- Judge whether a quantitatively trained reader new to the subfield can learn from the module without hidden prerequisites.

## F. Notation and cross-module consistency

- Introduce each symbol before use and keep its meaning stable.
- Follow standard field conventions unless alternatives are explained.
- Distinguish vectors, tensors, scalars, averages, perturbations, and dimensionless quantities.
- Keep indices, subscripts, signs, coordinates, and normalizations consistent.
- Verify cross-references and prerequisite claims against adjacent modules.
- Flag silent reversals or overstatements of conclusions established elsewhere.

## G. Figures, tables, HTML, and production quality

- Validate HTML and MathJax delimiters.
- Detect malformed equations, duplicate anchors, and broken internal links.
- Preserve figures, tables, scripts, navigation, and accessibility text.
- Check figure labels, units, legends, captions, and table definitions.
- Check desktop and mobile rendering for overflow and JavaScript errors.
- Record original module hashes before the audit and verify them afterward.

## H. Required audit deliverable

The signed report must contain:

1. A module-level verdict: **acceptable**, **acceptable after revision**, or **not yet teachable**.
2. Findings ranked as **blocking**, **major**, or **minor**.
3. Exact `file:line` locations and quoted source text.
4. The violated rubric item and an explanation of the defect.
5. Full proposed replacement text rather than vague editing instructions.
6. Representative prose rewrites.
7. Structural and pedagogical recommendations.
8. Independent numerical checks.
9. A primary-source evidence map.
10. Specific passages that already work and should be retained.
11. A preservation record showing that original modules were not changed.
12. A Codex signature distinguishing this audit from the original Claude-authored material.

Signed: **Codex — OpenAI**
Rubric recorded: 22 September 2026, America/Los_Angeles
