# Independent scientific and prose audit

Astrophysical fluid dynamics · Written Modules 01–12

Signed: Codex — OpenAI | 20 September 2026 | America/Los_Angeles

## Verdict: substantial revision required

Yes, after substantial revision. The twelve written modules contain enough useful derivation and physical material to form a good textbook, but the present manuscript is not ready to be relied on as one. Several central conclusions are mathematically or logically wrong; the most serious errors concern observational bounds, magnetic support, accretion and time-dependent mixing. The prose is frequently grammatical yet unnatural, repetitive and unnecessarily combative. It often explains the manuscript’s production history instead of the physics. A cosmetic copy-edit would leave these problems intact.

## Scope and method

This is an independent report by Codex, not an amendment to Claude’s manuscript or a claim to represent a human publisher. It applies the named science-editor skill to the current local checkout. Findings are examples supported by evidence, not an estimate of the percentage of all sentences or claims that are defective.

Snapshot: Git HEAD f93735fd035d4fd6e01376ad8415b61c54732709, including the working-copy changes already present in module10.html and module12.html. The existing untracked afd-stem-textbook-runbook.html was preserved. Line numbers refer to this local snapshot, not necessarily the current GitHub page. The public repositories were opened for context; the local manuscript is the object of the audit.

All twelve written modules were surveyed: their main narrative, definitions, major results, figures and captions, conclusions, and selected proofs and exercises. High-consequence claims and cross-module inconsistencies were pursued in detail. This is not a fresh derivation of every proposition, a solution of every exercise, a complete numerical reproduction, or certification of every reference. No previous editor’s pass/fail verdict was treated as evidence of correctness.

The domain brief was assembled from README.md, HANDOFF.md, the current modules, and the project’s house-style and notation documents under .ignore/plan. The reader is mathematically mature but new to the subfield; the book uses Gaussian/CGS conventions. Historical memory was used only to orient the inspection; current files determined the findings.

Six primary-source PDFs were downloaded into this audit folder and relevant passages were read. Twelve independent algebraic or numerical checks were saved separately. Local links were checked across the modules. The preservation check found all twelve module files unchanged from the audit baseline. Of 217 original files, 216 retained their hashes; HANDOFF.md changed while the checkout advanced to commit ff289c4c345a3dd83ebfdc7ef9c57384e3534515. These changes were outside Codex’s audit actions. Codex wrote only inside this new audit folder and did not restore or modify the concurrent changes. See integrity-verification.json.

The 40 replacements below are complete proposed paragraphs or result boxes, not a complete patch for every repeated occurrence, table, figure or exercise. No replacement was applied. The 48 prose edits are representative rather than a full copy-edit. The inventory contains about 164,000 whitespace-separated text tokens, including mathematical notation; that is not a count of ordinary English words.

## Ranked content findings

The first six findings block reliance on central conclusions. Major findings teach an incorrect concept, inference or scope. Moderate findings affect precision, consistency or validation. Quotes and locations are taken from the current HTML; each proposed replacement is separate from the original.

### C01 — Blocking: A lower bound is used backwards to reject Bondi accretion

Location: afd/module09.html:749

> That second comparison is what the refutation rests on

The predicted rate exceeds an observational LOWER limit. That satisfies the inequality; it does not violate it. The factor 401 is arithmetically correct and logically irrelevant to the claimed rejection. The source explicitly discusses problems for very LOW accretion rates. The error is repeated in the narrative, verdict and figure interpretation. The conditional upper limits can constrain a model, but the lower limits cannot rescue an upper-limit argument whose assumptions have been relaxed.

Standard affected: Precise statement; valid inference from concrete evidence

Evidence: Marrone et al. (2007), downloaded PDF p. 4, paragraph beginning “Our RM”; independent inequality check.

**Proposed replacement — not applied:**

```html
<div class="keyresult"><b>Check 10 — a conditional constraint on the inward mass flux.</b> The Bondi estimate exceeds the quoted Faraday-rotation upper limits under the magnetic-field assumptions used to obtain them. Those assumptions must accompany the comparison. The lower limits impose a different requirement: the accretion rate must be large enough to produce the observed rotation measure. Our Bondi estimate satisfies those lower limits, so they provide no evidence against it. A claim that the inflow is reduced between the Bondi radius and the inner flow therefore requires an applicable upper limit or another independent constraint.</div>
```

### C02 — Blocking: A viscosity upper bound becomes a fictitious measured interval

Location: afd/module12.html:690

> The classical factor is larger than the measured one

The chapter acknowledges a one-sided bound in the caption, then treats suppression factors of roughly 10–1000 as the endpoints of a measured interval. For the cited Prandtl-number cases, the source constrains effective viscosity to be small: a still smaller value is not excluded by that inequality. Also, a local perpendicular component of a transport tensor is not directly the same quantity as an effective scalar viscosity inferred from cluster fluctuations. Neither the stated 22.8–24.8-decade discrepancy nor the claimed refutation follows. This is the same category of inference error as C01.

Standard affected: Precise statement; evidence interpretation; limits

Evidence: Zhuravleva et al. (2019), downloaded PDF pp. 4–5 and p. 12; independent inequality check.

**Proposed replacement — not applied:**

```html
<div class="keyresult"><b>Check 4 — strong particle magnetisation, with effective transport unresolved.</b> The large value of $\omega_i\tau_i$ places the ions in the strongly magnetised regime. Braginskii's local perpendicular viscosity is correspondingly much smaller than the parallel coefficient. Zhuravleva et al. constrain an effective viscosity from cluster fluctuations; for the cases discussed here, their result is an upper bound on that viscosity, not a lower bound. A coefficient below the bound is not excluded. Moreover, relating a local anisotropic coefficient to the inferred effective viscosity requires a model of field geometry and the motions being measured. The present calculation supplies no such model and therefore does not test, or refute, the classical perpendicular coefficient.</div>
```

### C03 — Blocking: The supernova mixing-width bound substitutes variable acceleration into a constant-acceleration law

Location: afd/module08.html:833

> Putting the second into the first is the whole of this section

The chapter correctly identifies h = α A g t² as a constant-acceleration relation, then inserts an instantaneous g(t). An accumulated displacement cannot generally be obtained this way. Using the Read-type history dependence introduced in Module 7, h = α A [∫√g dt]², and R = C t^m gives h/R = 4αA(1−m)/m when the idealised history begins at zero. This is not αAm(1−m). At m = 1/2 the two differ by a factor 16. A finite onset time changes the result again. This calculation is a counterexample to the asserted bound, not a replacement validated model of a curved, expanding shell. Proposition 9 and its headline refutation need to be withdrawn pending an appropriate model.

Standard affected: Proof; hypotheses; limit case

Evidence: Module 7 Read-integral prescription; independent integration and numerical counterexample in independent-checks.json.

**Proposed replacement — not applied:**

```html
<p>The planar relation $h=\alpha Agt^2$ assumes constant acceleration. The shell acceleration $g(t)=m(1-m)Ct^{m-2}$ is time dependent, so inserting its instantaneous value into that relation does not establish a mixing-width bound. For comparison, applying the history-dependent prescription $h=\alpha A[\int_{t_0}^{t}\sqrt{g(t')}\,dt']^2$ gives</p>
<p>$$\frac{h}{R}=\frac{4\alpha A(1-m)}{m}\left[1-\left(\frac{t_0}{t}\right)^{m/2}\right]^2,\qquad 0\lt m\lt 1.$$</p>
<p>This expression still neglects curvature, expansion effects on the mixing layer and the evolution of its density contrast. It demonstrates why the acceleration history matters; it does not supply a tested supernova-shell law. The observed width cannot be used to reject the planar model through the proposed instantaneous-acceleration bound.</p>
```

### C04 — Blocking: The magnetic critical mass-to-flux interpretation is reversed

Location: afd/module12.html:549

> Below it no field strength is enough; above it the cloud is held

At fixed geometry the subcritical side has relatively more magnetic support; the supercritical side has too much mass per unit flux for magnetic support alone. The later proposition and discussion have the intended direction, so the opening directly contradicts what follows. Even on the subcritical side, “held” needs the qualification that gas can still move along field lines and that non-ideal processes can change the flux-to-mass relation.

Standard affected: Precise statement; limit case

Evidence: Troland & Crutcher (2008), downloaded PDF p. 2 and p. 3; manuscript Proposition 7.

**Proposed replacement — not applied:**

```html
<p>Magnetic support is characterised by a critical mass-to-flux ratio. A cloud below the critical ratio is magnetically subcritical: in the idealised geometry, magnetic stresses can oppose collapse across the field. A cloud above it is supercritical: the field cannot prevent gravitational collapse by itself. Flux freezing preserves the ratio for a material flux tube, whereas processes such as ambipolar diffusion can change it. The numerical critical coefficient depends on the cloud geometry.</p>
```

### C05 — Blocking: The luminosity test compares unlike efficiencies and contradicts the assumed energy model

Location: afd/module09.html:757

> both readings refute the model as stated

The numerator used here is a 2–10 keV luminosity. The standard thin-disc efficiency is bolometric. Dividing the band luminosity by a Bondi supply rate gives a band-specific apparent efficiency referenced to the outer supply, not a measured radiative efficiency of the material reaching the black hole. More fundamentally, adiabatic Bondi accretion does not assume a thin-disc efficiency of 0.1. Radiating little is compatible with radiation being dynamically unimportant. Module 11 §9 carries this invalid comparison forward rather than correcting it.

Standard affected: Precise definition; valid comparison; limits

Evidence: The manuscript’s own luminosity-band definition and model assumptions; dimensional and model-consistency analysis.

**Proposed replacement — not applied:**

```html
<div class="keyresult"><b>Check 11 — a low X-ray luminosity relative to the outer gas supply.</b> The ratio $L_{2-10\,{\rm keV}}/(\dot M_{\rm B}c^2)$ is approximately $4\times10^{-9}$ for the inputs used here. It is an X-ray-band luminosity divided by the rest-mass power associated with the Bondi supply estimate. It is not a bolometric radiative efficiency, and the actual inward mass flux may differ from $\dot M_{\rm B}$. Comparison with a thin-disc efficiency therefore requires both a bolometric luminosity and an estimate of the mass reaching the emitting region. The low band luminosity alone does not refute an adiabatic Bondi model.</div>
```

### C06 — Blocking: Circularisation radius is mistaken for a ballistic stopping radius

Location: afd/module11.html:106

> Inside $R_{\rm circ}$ the gas cannot go

The force-balance radius l²/(GM) is the radius of a circular orbit with that angular momentum. It is not the pericentre of a parcel arriving on a parabolic orbit. For zero orbital energy, solving l²/(2R²)−GM/R=0 gives R_p = l²/(2GM) = R_circ/2. Gas can pass inside R_circ without first losing angular momentum; dissipation of orbital energy permits circularisation. Angular-momentum transport is then needed for sustained inward motion through approximately circular orbits.

Standard affected: Precise definition; proof; counterexample

Evidence: Independent effective-potential calculation in independent-checks.json.

**Proposed replacement — not applied:**

```html
<p>The radius $R_{\rm circ}=\ell^2/(GM)$ is the radius of a circular orbit with specific angular momentum $\ell$. It is not a hard inner limit to ballistic infall: a zero-energy orbit with the same $\ell$ has pericentre $R_{\rm p}=\ell^2/(2GM)$. Gas can circularise near $R_{\rm circ}$ by dissipating orbital energy. Once it forms an approximately Keplerian disc, further inward motion through nearly circular orbits requires angular-momentum transport.</p>
```

### C07 — Major: The Reynolds-number interpretation ignores the density inside the mean free path

Location: afd/module02.html:499

> The density cancels

An explicit factor of ρ cancels when the kinetic viscosity estimate is substituted. Density dependence does not disappear: for a neutral gas λ = 1/(√2 nσ), so Re is proportional to n at fixed speed, temperature, cross-section and system size. For a Coulomb plasma the collision length also depends on density. The formula Re ≈ 3 Ma_th/Kn is useful; its stated physical interpretation is wrong.

Standard affected: Precise statement; physical interpretation

Evidence: Module 1 mean-free-path formula; independent substitution.

**Proposed replacement — not applied:**

```html
<p>The explicit factor of $\rho$ cancels on substituting the kinetic estimate of viscosity, giving $\mathrm{Re}\simeq3\mathrm{Ma}_{\rm th}/\mathrm{Kn}$. The density still enters through $\lambda$. For neutral hard-sphere collisions, $\lambda=(\sqrt{2}n\sigma)^{-1}$, so $\mathrm{Re}\propto n$ when $u$, $L$, $T$ and $\sigma$ are fixed. The formula relates three dimensionless measures of the same gas; it does not make the Reynolds number independent of density.</p>
```

### C08 — Major: The solar-wind collision count uses spatial optical depth instead of collisional age

Location: afd/module01.html:549

> Fewer than one proton in three

The bulk plasma travels outward at U(r), whereas λ is formed from a thermal speed and a relaxation time. The relevant accumulated relaxation measure is ∫dt/τ = ∫dr/[Uτ] = ∫(v_th/U)dr/λ. Omitting v_th/U changes the quantity. Extending a fitted outer-wind power law to r=0 is also unsupported. Finally, a Coulomb deflection time describes accumulated small-angle scattering, not a Poisson count of discrete binary encounters. The claimed fraction of protons with no collision is not established.

Standard affected: Definition; proof; concrete interpretation

Evidence: Verscharen et al., Living Reviews in Solar Physics (2019), equation 133; manuscript collision-time convention.

**Proposed replacement — not applied:**

```html
<p>To estimate cumulative collisional relaxation, follow a plasma element from a specified starting radius $r_0$ to $r_1$. Its collisional age is $A_c=\int_{r_0}^{r_1}dr/[U(r)\tau_c(r)]$. If the convention is $\lambda=v_{\rm th}\tau_c$, this becomes $A_c=\int_{r_0}^{r_1}[v_{\rm th}(r)/U(r)]\;dr/\lambda(r)$. The result depends on the flow and temperature profiles and on the starting radius. Because Coulomb relaxation accumulates many small deflections, $A_c$ should not be interpreted here as a measured fraction of particles that have undergone a discrete collision.</p>
```

### C09 — Major: Solar luminosity does not bound all departures from hydrostatic balance at 10⁻²⁴

Location: afd/module03.html:178

> It is forced by the observed luminosity

The argument assumes a particular slowly evolving contraction with a secular gravitational-energy release. It cannot exclude oscillatory accelerations or convection, whose work need not accumulate in the assumed way. A purely illustrative displacement of 1 m with a 300 s period has acceleration/g ≈ 1.6×10⁻⁶ at the surface, already eighteen orders larger, without implying sustained contraction. This is a logical counterexample, not a claim about a measured solar amplitude. Hydrostatic balance remains an excellent mean-structure approximation; the proposed observational precision does not follow.

Standard affected: Hypotheses; proof; scope

Evidence: Independent counterexample; inspection of the assumptions in §2 and §8.

**Proposed replacement — not applied:**

```html
<p>For a star evolving through approximately hydrostatic states on a timescale $t_{\rm evol}$, a characteristic secular acceleration is $R/t_{\rm evol}^2$. Its ratio to gravity is of order $(t_{\rm dyn}/t_{\rm evol})^2$. Taking a thermal evolution timescale therefore motivates a small secular acceleration. This estimate does not bound oscillatory or convective accelerations and is not a luminosity-derived error bar on hydrostatic balance. We use hydrostatic equilibrium to model the mean stellar structure, while treating motions and their timescales separately.</p>
```

### C10 — Major: An effective equation-of-state parameter is used as a conserved composition variable

Location: afd/module06.html:367

> the table's own, $\mu = \rho k_BT/(P\,m_u)$

The Ledoux proof assumes the parcel retains its composition. The inferred μ_eff = ρkBT/(Pm_u) can vary because of ionisation and non-ideal equation-of-state effects, not only composition. The chapter itself warns at line 371 not to feed the outer gradient into Proposition 3, yet uses it to move the boundary to 0.7306 R and calls the displacement an upper bound without proof. Similarly a measured background ∇ plateau is not by itself a measurement of the thermodynamic derivative ∇ad. This undermines the claimed precision of the solar stability calculation.

Standard affected: Defined terms; consistent hypotheses; valid numerical interpretation

Evidence: Current Table 1, Proposition 3 and its explicit caveat; thermodynamic definition of Γ₁.

**Proposed replacement — not applied:**

```html
<p>The quantity $\mu_{\rm eff}=\rho k_BT/(Pm_u)$ inferred from this table is an equation-of-state diagnostic. Its gradient cannot automatically be identified with a composition gradient carried unchanged by a displaced parcel. A consistent buoyancy calculation uses the model's thermodynamic derivatives; for hydrostatic stratification one may write $N^2=g[(1/\Gamma_1)d\ln P/dr-d\ln\rho/dr]$, with $\Gamma_1$ evaluated for an adiabatic displacement at fixed composition. Alternatively, the Ledoux form requires actual composition variables and the corresponding equation-of-state derivatives. The effective-$\mu$ calculation is illustrative and does not establish a precise shift, or an upper bound on the shift, of the convection-zone boundary.</p>
```

### C11 — Major: The density table confuses a lognormal median with its mode

Location: afd/module10.html:770

> most probable $\rho/\langle\rho\rangle$

The last column is exp(s₀), the median of x=ρ/⟨ρ⟩ and the value corresponding to the mode of s=ln x. The mode of the density PDF p(x) is exp(s₀−σ_s²). The Jacobian p(x)=p_s(ln x)/x matters. For Mach 10 and b=1, the displayed 0.0995 is the median; the density mode is about 0.000985. The simplest repair is to relabel the column, preserve the computed values, and explain the distinction.

Standard affected: Defined terms; proof; numerical interpretation

Evidence: Independent change-of-variables derivation and calculation.

**Proposed replacement — not applied:**

```html
<p>Because $s=\ln x$ is Gaussian with mean $s_0=-\sigma_s^2/2$, the median density ratio is $x_{\rm med}=e^{s_0}$. The density probability distribution is $p_x(x)=p_s(\ln x)/x$, whose maximum occurs at $x_{\rm mode}=e^{s_0-\sigma_s^2}$. The final column below lists the <b>median</b> density ratio, not the mode of the density distribution. At $\mathcal M=10$ and $b=1$, these are approximately $0.0995$ and $0.000985$, respectively.</p>
<p><b>Replacement table heading:</b> median $\rho/\langle\rho\rangle$.</p>
```

### C12 — Major: The simulation-to-observation inequality is reversed

Location: afd/module11.html:649

> the true gap may be smaller than $5$ and cannot be larger

The quoted simulation result is α_sim ≲ 0.02, and the observational range begins around 0.1. For those reported values the ratio is at least 5, and can be larger if α_sim is smaller. It is a separate physical possibility that more complete simulations would increase α. The prose confuses that possibility with the direction of the numerical bound.

Standard affected: Precise statement; inference

Evidence: King, Pringle & Livio (2007), downloaded PDF pp. 4 and 6; independent inequality check.

**Proposed replacement — not applied:**

```html
<p>For the quoted comparison, $\alpha_{\rm obs}\gtrsim0.1$ and $\alpha_{\rm sim}\lesssim0.02$ imply $\alpha_{\rm obs}/\alpha_{\rm sim}\gtrsim5$. Smaller simulated values increase this ratio. The authors also discuss limitations that may cause the simulations to underestimate the physical stress. Addressing those limitations could reduce the discrepancy, but that possibility does not reverse the inequality for the results being compared.</p>
```

### C13 — Major: Plasma beta is conflated with the Alfvén Mach number

Location: afd/module12.html:202

> which is the physical reason §6 has a surface to find

Beta compares thermal and magnetic pressure. An Alfvén surface is defined by the relevant flow speed matching the Alfvén speed, not by beta crossing unity. For the simple speed definitions used here, M_A²=(γβ/2)M_s². At M_A=1 and M_s=10, beta is 0.012 for γ=5/3. A pressure-only census lacking a bulk-flow speed cannot locate the surface. Likewise “the gas drags the field” requires an induction/transport argument, not beta alone.

Standard affected: Defined terms; concrete interpretation

Evidence: Independent substitution of the chapter’s definitions.

**Proposed replacement — not applied:**

```html
<p>The pressure diagram compares thermal and magnetic stresses through $\beta$. It does not locate the Alfvén surface, which depends on the flow speed. With $M_s=U/c_s$ and $M_A=U/v_A$, the definitions give $M_A^2=(\gamma\beta/2)M_s^2$. Thus $M_A=1$ need not occur at $\beta=1$. Section 6 uses the wind speed and magnetic field to examine that separate transition.</p>
```

### C14 — Major: The cited source does not say that L694-2 contains a star

Location: afd/module05.html:534

> Lynds 694-2, which contains a star

Kandori et al. distinguish Barnard 335, with a Class 0 source, from other listed globules without IRAS sources. They classify L694-2 as “star-forming” because it shows inward gas motion. The manuscript silently converts that classification into an embedded-star detection. This finding concerns what the cited paper supports, not a claim that no later observation could change the object’s classification.

Standard affected: Concrete source attribution; precise statement

Evidence: Kandori et al. (2005), downloaded PDF p. 5, §2.1.

**Proposed replacement — not applied:**

```html
<p>Kandori et al. place Lynds 694-2 in their star-forming category because of evidence for inward gas motion. That classification should not be restated as a detection of an embedded star: their discussion distinguishes it from Barnard 335, which has an identified Class 0 source. The quoted Bonnor–Ebert fit can still be compared with the critical dimensionless radius, subject to the equilibrium model's assumptions.</p>
```

### C15 — Major: The foundational kinetic model is called exact, then dismissed

Location: afd/module01.html:146

> Equation (2.1) is exact and unusable

The Boltzmann equation with the stated binary collision closure is already a model, with dilute-gas and molecular-chaos assumptions. It does not retain all particle correlations. “Unusable” also contradicts the book’s later recommendation to solve kinetic equations where fluid closures fail. A capable reader needs to understand what is approximated at each level, not to accept a false exact-model versus usable-model dichotomy.

Standard affected: Precise statement; model hypotheses

Evidence: Current equation and surrounding definitions; MIT OCW 2.57 lecture notes, Boltzmann-equation assumptions.

**Proposed replacement — not applied:**

```html
<p>The Boltzmann equation describes the evolution of the one-particle distribution under a dilute-gas collision model. Its collision term assumes that the incoming particles' velocities are uncorrelated at the level required for this closure. The equation retains much more velocity-space information than a five-field fluid model, so solving it is generally more expensive. A fluid approximation is useful when the moments needed for the problem can be evolved with a justified closure.</p>
```

### C16 — Major: Failure of a collisional closure is overstated as failure of every fluid description

Location: afd/module01.html:355

> No closed fluid description exists

A large Knudsen number invalidates the local collisional Chapman–Enskog argument being used. It does not prove that no useful moment closure exists. The book later discusses magnetised, anisotropic and collisionless cases. Conversely, a small Knudsen number does not by itself justify dropping viscosity: the relevant force ratio is set by Re. Using the book’s relation, Kn=10⁻⁴ and Ma_th=10⁻⁶ gives Re≈0.03, a continuum flow dominated by viscosity.

Standard affected: Hypotheses; rescue or limit case

Evidence: Cross-check with Module 2 Proposition 12 and later magnetic closures; numerical counterexample.

**Proposed replacement — not applied:**

```html
<p>When the collision length is comparable to the macroscopic scale, the local collisional closure used here is no longer controlled. A kinetic treatment or a separately justified moment closure is then needed. Small $\mathrm{Kn}$ supports a continuum approximation, but the inviscid limit requires an additional comparison: $\mathrm{Re}\gg1$ on the scales of interest. Heat transport, time dependence and boundary layers may impose further restrictions.</p>
```

### C17 — Major: Small acoustic amplitude does not prevent shock formation over long propagation distances

Location: afd/module04.html:164

> When the ratio approaches one, the wave steepens into a shock

The local ratio of nonlinear to linear terms estimates the per-period error. Weak nonlinearity can accumulate: a compressive acoustic wave of velocity amplitude δu can steepen over a time of order 1/(kδu), even when δu/c_s≪1. Also, the statement identifies linear theory in general with subsonic motion, although this derivation is specifically a perturbation about a uniform acoustic background.

Standard affected: Hypotheses; limit case

Evidence: Independent timescale argument from the terms displayed in the chapter.

**Proposed replacement — not applied:**

```html
<p>For these acoustic perturbations, the instantaneous ratio of the nonlinear advection term to the linear term is of order $|\mathbf u_1|/c_s$. A small ratio justifies linear evolution over sufficiently short times. Nonlinear steepening can nevertheless accumulate over many periods: for a compressive wave the characteristic steepening time is of order $(k|\mathbf u_1|)^{-1}$. Shock formation therefore does not require the perturbation velocity to first become comparable with the sound speed.</p>
```

### C18 — Major: A standard atmosphere is treated as a universal weather profile

Location: afd/module06.html:126

> It nevertheless convects every afternoon

The International Standard Atmosphere specifies a reference lapse rate, not every afternoon’s actual stratification. Dry convection can arise over a heated surface; moisture is not the only resolution of the comparison. The latent heat quoted is per gram of condensed water, not a fixed heat release per gram of the rising air parcel. The same over-attribution appears in Module 3’s explanation of the difference from the standard lapse rate.

Standard affected: Precise statement; defined quantities; scope

Evidence: Definition of the reference profile; parcel thermodynamics; cross-check with Module 3.

**Proposed replacement — not applied:**

```html
<p>The standard tropospheric lapse rate is smaller than the dry adiabatic lapse rate, so this reference profile is stable to unsaturated adiabatic displacements. An actual daytime boundary layer can have a different profile and may support dry convection above a heated surface. In saturated air, condensation releases latent heat and reduces the parcel's cooling rate; the moist stability criterion can then differ from the dry one. The released heat is the latent heat per unit mass of water multiplied by the amount of water condensed, not a fixed heat input per unit mass of air.</p>
```

### C19 — Major: A conditional Schwarzschild estimate is promoted to a universal solar-mode bound

Location: afd/module06.html:241

> every solar g mode must have a period longer

The 38.8 min estimate uses a maximum N/(2π)=430.06 μHz without the composition term. The same table gives a Ledoux value of 453.84 μHz, corresponding to 36.72 min. Even taking the table at face value, the stronger universal bound does not follow. This does not prove an observed solar mode below 38.8 min; it identifies an inconsistent inference. The general gravity-wave frequency constraint also needs a specified oscillation model.

Standard affected: Hypotheses; consistency; limit case

Evidence: Current Table 1 and §3.1; independent reciprocal-frequency calculation.

**Proposed replacement — not applied:**

```html
<p>In the composition-free approximation used for this estimate, the maximum buoyancy frequency corresponds to a period of about $38.8$ minutes. This is a characteristic lower-period scale for gravity waves within that approximation. It is not a universal lower bound for solar gravity modes: composition changes the buoyancy frequency, as the last column of Table 1 already shows. Quantitative mode periods require a consistent stratification and the stellar oscillation boundary-value problem.</p>
```

### C20 — Major: The interface introduction denies a result already derived in the Jeans chapter

Location: afd/module07.html:119

> a growth rate that depends on the wavelength of the disturbance

Module 5 explicitly derives a wavelength-dependent growth rate. Moreover, wavelength dependence does not automatically select a finite fastest-growing scale: ideal sharp-interface Rayleigh–Taylor growth without regularisation increases towards short wavelengths. The new ingredient is the interface boundary conditions, not the invention of wavelength-dependent stability.

Standard affected: Dependencies; precise statement; limits

Evidence: Module 5 dispersion relation and Module 7 limiting cases.

**Proposed replacement — not applied:**

```html
<p>We now examine perturbations of an interface between two fluids. As in the Jeans calculation, different wavelengths can grow at different rates. The new step is to match the perturbations on the two sides through the interface conditions. A preferred finite wavelength exists only when the relevant stabilising physics or finite interface structure supplies one; the ideal sharp-interface problem need not select such a scale.</p>
```

### C21 — Major: A discontinuity is not necessarily a shock

Location: afd/module08.html:124

> Such a surface is a shock

A contact discontinuity can have a density jump without the mass flux and irreversible compression characteristic of a shock. The definition should distinguish these before introducing Rankine–Hugoniot conditions, which apply more generally to conservation-law discontinuities.

Standard affected: Defined terms; limit case

Evidence: Conservation-law definitions and the later contact-discontinuity discussion.

**Proposed replacement — not applied:**

```html
<p>The inviscid equations can admit discontinuities. A shock is a propagating discontinuity across which matter flows and, for an admissible compressive gas-dynamic shock, entropy increases. A contact discontinuity is different: the normal velocity and pressure are continuous in the ideal gas-dynamic case, while density and temperature may jump. The jump conditions follow from conservation; additional conditions determine which type of discontinuity they describe.</p>
```

### C22 — Major: Velocity-sign symmetry is confused with selecting the physical wind and accretion branches

Location: afd/module09.html:124

> Take the outward branch and it is E. N. Parker's solar wind

For the same closure, reversing a signed velocity preserves the stationary equations, but it does not turn the physical Parker solution into the usual Bondi solution with its outer boundary conditions. In speed magnitude, the transonic wind is subsonic inside and supersonic outside; Bondi accretion has the opposite arrangement. The two pass through the critical point on different slopes. The chapter later describes the topology more carefully, but the opening teaches the wrong shortcut.

Standard affected: Precise statement; boundary conditions

Evidence: Current phase portrait and asymptotic branch descriptions.

**Proposed replacement — not applied:**

```html
<p>Steady spherical winds and accretion flows share the same critical-point structure when the same thermodynamic closure is used. Reversing the sign of a velocity preserves the stationary equations, but the physical solution also depends on its boundary conditions. The transonic wind is subsonic on the inner side of the critical point and supersonic outside it; the usual transonic accretion solution has the reverse arrangement. They follow different branches of the common equation.</p>
```

### C23 — Major: Reaching the sonic line is confused with crossing it smoothly

Location: afd/module09.html:305

> a curve reaches $u = 1$ only when $C = -3$

For C<−3, the level sets reach u=1 at the endpoints bounding the forbidden radial interval. Their derivative is singular there; they do not form a smooth transonic flow. The minimum argument establishes the unique constant for a smooth critical crossing, not the absence of all other intersections with u=1.

Standard affected: Proof; precise statement

Evidence: Independent inspection of u²−2 ln u = 4 ln x+4/x+C and its extrema.

**Proposed replacement — not applied:**

```html
<p>A smooth transonic solution passes through both $u=1$ and $x=1$, which fixes $C=-3$. For $C\lt -3$, branches can reach $u=1$ at other radii, but the differential equation is singular there and the branches do not continue as smooth transonic flows. The distinction is between touching the sonic line at a singular endpoint and crossing it regularly through the critical point.</p>
```

### C24 — Major: Viscous dissipation is described as destruction of energy

Location: afd/module10.html:126

> energy is destroyed at a rate

Viscosity converts resolved kinetic energy into internal energy. The distinction matters in a textbook that previously derived a total-energy equation. The smooth incompressible Euler energy statement also needs that scope: weak solutions and compressible shocks complicate the limiting argument. The anomaly concerns a finite kinetic-energy dissipation rate as viscosity tends to zero.

Standard affected: Defined quantity; hypotheses

Evidence: Cross-check with the book’s energy balance; distinction between kinetic and total energy.

**Proposed replacement — not applied:**

```html
<p>For smooth incompressible Euler flow in a closed or periodic domain, kinetic energy is conserved. At small nonzero viscosity, the flow can transfer kinetic energy to increasingly small scales, where viscosity converts it into heat. The kinetic-energy dissipation rate may remain finite as viscosity tends to zero. This limiting behaviour is called the dissipation anomaly; it does not violate conservation of total energy.</p>
```

### C25 — Major: Rayleigh stability is used to rule out every angular-momentum transport mechanism

Location: afd/module11.html:94

> A stable disc transports no angular momentum

The Rayleigh criterion concerns centrifugal instability under particular inviscid, axisymmetric assumptions. It does not establish the absence of viscous, non-axisymmetric, magnetic or wind-driven transport. Module 12 repeats the overstatement. The useful result is that Keplerian rotation is not centrifugally unstable by this criterion; the transport problem remains to be solved.

Standard affected: Hypotheses; limits

Evidence: Scope of the chapter’s Rayleigh derivation; later stress equations.

**Proposed replacement — not applied:**

```html
<p>Because specific angular momentum increases outward, a Keplerian disc satisfies the Rayleigh criterion for stability to axisymmetric centrifugal disturbances in the inviscid model. This removes one possible source of instability; it does not forbid angular-momentum transport. Viscous stresses, other instabilities, magnetic stresses and outflows require separate analysis. The next sections quantify the stress needed for accretion before examining candidate mechanisms.</p>
```

### C26 — Major: A chosen one-temperature closure is presented as the definition of single-fluid MHD

Location: afd/module12.html:812

> Single-fluid MHD has one temperature by construction

A model with one bulk velocity can still evolve separate electron and ion internal energies. The distinction between a single bulk momentum equation and a one-temperature closure should not be erased. The book is entitled to omit two-temperature physics, but it should explain that this is its modelling choice.

Standard affected: Definition; rescue or limit case

Evidence: Model-variable distinction; current energy-equilibration discussion.

**Proposed replacement — not applied:**

```html
<p>This module uses a one-temperature closure in addition to a single bulk velocity. Those are separate assumptions: a single-fluid momentum description can be coupled to distinct electron and ion energy equations. We do not develop that extension here. Where electron–ion equilibration is slow, the one-temperature closure requires additional justification.</p>
```

### C27 — Major: The dimensionless Jeans-plot caption gives dimensional slope and intercept

Location: afd/module05.html:265

> a straight line of slope $c_s^2$

For y=ω²/(4πGρ₀) and x=(k/k_J)², the dispersion relation is y=x−1. The plotted slope is 1 and the intercept −1. The caption instead quotes the slope and intercept for dimensional ω² against k². This is a direct figure-reading error.

Standard affected: Concrete figure; units

Evidence: Independent nondimensionalisation of equation (3.1).

**Proposed replacement — not applied:**

```html
<p>In the left panel, $y=\omega^2/(4\pi G\rho_0)$ is plotted against $x=(k/k_J)^2$, so the dispersion relation is $y=x-1$. The dimensionless slope is $1$ and the intercept is $-1$. Negative $y$, corresponding to $k\lt k_J$, gives gravitational growth rather than oscillation.</p>
```

### C28 — Major: The Trinity comparison assigns a formal rejection level without the full error model

Location: afd/module08.html:591

> A structured residual is a failed model, not a noisy measurement

A systematic residual can arise from inadequate physics, calibration, correlated measurement error or data processing. The chapter itself acknowledges some of these possibilities nearby. The “REFUTED at 3.8σ” energy verdict divides a discrepancy by a quoted yield uncertainty without establishing the uncertainty of the film-based inference and its model inputs. That is a discrepancy expressed in units of one reported error, not a calibrated total significance.

Standard affected: Evidence grade; limits

Evidence: Current §5 error discussion and stated uncertainty budget; statistical inference.

**Proposed replacement — not applied:**

```html
<p>The residuals show a systematic trend relative to the fitted similarity law. This warrants investigation of both the physical assumptions and the measurement process, including calibration and correlated errors. The inferred energy differs from the comparison yield by about $3.8$ times that yield's quoted uncertainty. Because the uncertainty of the film-based inference and its model inputs has not been included, this ratio should not be reported as a $3.8\sigma$ rejection of the model.</p>
```

### C29 — Major: Mean and median fits are treated as statistical bounds

Location: afd/module02.html:643

> The true answer lies between them

Separate fits to density and speed do not bracket their joint mass flux. The average of their product depends on covariance; even the product of their means is generally not the mean product. A median-product curve is not automatically a lower or upper bound. Conservation is a law of the flow, but testing a steady spherical reduction with ensemble statistics requires the corresponding averages and assumptions.

Standard affected: Defined statistic; evidence interpretation

Evidence: Independent identity for the mean of a product; current fit definitions.

**Proposed replacement — not applied:**

```html
<p>The mean-fit and median-fit constructions give different radial trends. Neither is automatically a bound on the physical mass flux. In particular, $\langle\rho u\rangle=\langle\rho\rangle\langle u\rangle+\operatorname{Cov}(\rho,u)$, so the density–speed covariance is needed to infer the mean flux. The comparison is a consistency check on these fitted summaries, not a proof that the true mass flux lies between them.</p>
```

### C30 — Major: Mean-fit solar-wind values are labelled median fits

Location: afd/module10.html:509

> Venzmer & Bothmer median fits

The cited Table 3 has separate mean and median columns. The values used here—7.57 cm⁻³, 9.67×10⁴ K, 6.05 nT and 435.6 km/s—come from the mean-fit column. Module 9 identifies that choice correctly. The labels in Module 10’s paragraph and table should match both the source and the calculation.

Standard affected: Source fidelity; defined statistic

Evidence: Venzmer & Bothmer (2018), downloaded PDF p. 8, Table 3.

**Proposed replacement — not applied:**

```html
<p>The comparison uses the <b>mean-fit</b> coefficients in Venzmer and Bothmer's Table 3, as does Module 9: $n=7.57 {\rm cm^{-3}}$, $T=9.67\times10^4 {\rm K}$, $B=6.05 {\rm nT}$ and $U=435.6 {\rm km\,s^{-1}}$ at 1 au. The median-fit coefficients describe a different statistical summary and are not the values in this column.</p>
```

### C31 — Major: A scaling fit is said to prove loss of initial-condition dependence

Location: afd/module07.html:499

> a layer still governed by its seed would not be linear in it at all

A linear late-time relation can have a coefficient or offset that still depends on the seed. Demonstrating the functional form therefore does not demonstrate universality or complete loss of initial-condition memory. The later discussion itself distinguishes the fitted coefficients.

Standard affected: Valid inference; limits

Evidence: Logical distinction between functional form and parameter universality; current experiment description.

**Proposed replacement — not applied:**

```html
<p>Late-time linearity against the Read variable supports the proposed functional form over the measured interval. It does not by itself establish independence from the initial perturbation: the slope, offset or onset time may still depend on the seed. That stronger claim requires comparisons showing that the relevant fitted parameters converge across initial conditions.</p>
```

### C32 — Major: Large magnetic Reynolds number is confused with material conductivity

Location: afd/module12.html:250

> a good conductor through its size

System size changes the ratio of advection to diffusion, not the electrical conductivity of the material. Even in the idealised Spitzer regime, density cancellation is approximate because the Coulomb logarithm can change. The useful explanation is that large L can make magnetic diffusion slow on the dynamical timescale.

Standard affected: Defined terms; physical interpretation

Evidence: Definitions of conductivity, magnetic diffusivity and Rm in §2.

**Proposed replacement — not applied:**

```html
<p>Large size can make magnetic diffusion slow relative to advection even when the material conductivity is finite. The relevant ratio is $\mathrm{R_m}=UL/\eta_{\rm m}$, where $\eta_{\rm m}$ is magnetic diffusivity. Increasing $L$ increases $\mathrm{R_m}$ at fixed $U$ and $\eta_{\rm m}$; it does not make the plasma intrinsically more conducting. In the classical fully ionised regime, the leading density dependence of the resistivity largely cancels, although the Coulomb logarithm retains a weaker dependence.</p>
```

### C33 — Major: Gyrophase is called a count of complete gyro-orbits

Location: afd/module12.html:619

> the number of gyro-orbits a proton completes

The chapter correctly defines ωcτ as a phase in radians near the beginning, but later calls it a count of complete orbits. The count is ωcτ/(2π). Also λ/r_g=ωcτ only when the same velocity convention defines both lengths; the chapter’s later collision-time comparison exists precisely because its conventions differ. The huge magnetisation conclusion survives, but the stated meaning of the number does not.

Standard affected: Defined quantity; notation

Evidence: Current Definition 2 and transport-convention comparison; independent 2π conversion.

**Proposed replacement — not applied:**

```html
<p>The dimensionless quantity $\omega_i\tau_i$ is the gyro-phase accumulated in radians during one collision time. The number of complete gyro-orbits is $\omega_i\tau_i/(2\pi)$. A length ratio $\lambda/r_g$ equals $\omega_i\tau_i$ only when $\lambda$ and $r_g$ use compatible velocity and collision-time conventions. Either measure is very large here, establishing strong particle magnetisation.</p>
```

### C34 — Major: Collisionless dynamics is described as unchanging orbits

Location: afd/module01.html:605

> the stellar orbits it has today are the orbits it was born with

Negligible two-body relaxation does not freeze a galaxy’s mean potential or individual trajectories. Collective evolution and time-dependent gravitational fields can change orbital energies and angular momenta without close stellar encounters. The adjacent absolute denial of every fluid description also needs care: collisionless moment equations exist, although their closure is nontrivial.

Standard affected: Precise statement; limit case

Evidence: Distinction between encounter relaxation and evolution in a collective potential.

**Proposed replacement — not applied:**

```html
<p>A very long two-body relaxation time means that discrete stellar encounters make little change over the age of the galaxy. The stars still move in the collective gravitational potential, which can evolve and alter their orbits. Collisionless dynamics therefore removes an important relaxation mechanism; it does not imply that the present orbital structure is identical to the initial one. A kinetic description retains the velocity distribution, while a moment description requires a suitable closure.</p>
```

### C39 — Major: A conditional mass-bias calculation is labelled an observational confirmation

Location: afd/module10.html:715

> Treating this cluster core as static costs about four per cent

The proposition and proof correctly require a radially constant pressure ratio and explicitly discuss the missing derivative. The verdict then states the mass cost as an established property of the cluster. A dispersion and temperature from one annulus do not measure the pressure-ratio gradient or independently measure the mass bias. The caveat about not extending the result to r500 is valuable but does not supply the missing local assumption. This is a failure to carry a correct hypothesis into the headline, not a failure of the displayed theorem.

Standard affected: Hypotheses retained in conclusions; evidence grade

Evidence: Current Proposition 7, its correct proof and the following verdict.

**Proposed replacement — not applied:**

```html
<div class="keyresult"><b>Conditional estimate of hydrostatic mass bias.</b> If the turbulent-to-thermal pressure ratio is constant with radius, the adopted ratio of $4.15$ per cent implies a mass underestimate of $3.98$ per cent. The measurement in one annulus does not establish that radial constancy. In general, $M=(1+\alpha)M_{\rm th}-[r^2P_{\rm th}/(G\rho)]\,d\alpha/dr$, so the bias also depends on the pressure-ratio gradient. The quoted percentage is therefore a conditional calculation, not an independently measured mass bias.</div>
```

### C40 — Major: A partially reused observation is presented as a 25% test of a prediction

Location: afd/module06.html:574

> SURVIVES: the mixing-length velocity law itself

The revised convective flux is built from the observed velocity and temperature contrast. That flux is then fed into the velocity law, whose output is compared with the same observed velocity. This is not a tautological identity—the velocity enters the prediction only to the one-third power—but it is not an independent velocity prediction either. The stated density, correlation and formation-height assumptions further condition the flux estimate. Calling the agreement a model survival to 25% overstates the test.

Standard affected: Independence of concrete evidence; limits

Evidence: Current §7.3 Steps 2–3; dependency tracing of inputs and outputs.

**Proposed replacement — not applied:**

```html
<p>Using the observed velocity and inferred temperature contrast gives a conditional estimate of the convective flux. Substituting that flux into the mixing-length velocity relation returns $0.816\ {\rm km\,s^{-1}}$, compared with the input velocity of $0.65\ {\rm km\,s^{-1}}$. Because the observed velocity contributes to the flux used in this calculation, the comparison is a partial consistency check, not an independent prediction accurate to $25$ per cent. An independent test would require the flux to be determined without reusing the velocity being tested.</p>
```

### C35 — Moderate: The book misstates its own dependency chain

Location: afd/module05.html:115

> Modules 2 to 4 treated gravity as a field imposed from outside

Module 3 already treats self-gravitating hydrostatic spheres through the Lane–Emden equation. Module 5 introduces perturbations of self-gravity, not self-gravity for the first time. A related stale statement in Module 4 says ionising-gas thermodynamics is not developed in the book, although Module 6 develops a Saha-based treatment. These are substantive navigation errors for a learner.

Standard affected: Dependencies; precise statement

Evidence: Direct cross-check of Modules 3, 4, 5 and 6.

**Proposed replacement — not applied:**

```html
<p>Module 3 treated self-gravity in hydrostatic equilibrium. Module 4 studied acoustic perturbations while keeping the gravitational field fixed. We now allow the density perturbation to generate a gravitational perturbation through Poisson's equation and ask when that feedback overcomes pressure support. The distinction is between an equilibrium gravitational field and the evolving field of the disturbance.</p>
```

### C36 — Moderate: The prose overstates its own viscosity table

Location: afd/module02.html:519

> by ten or more orders of magnitude

The first two rows give inverse Reynolds numbers of about 9.8×10⁻¹⁴ and 2.5×10⁻⁶. The second is a suppression by roughly 5.6 orders, not ten or more. Both may support an inviscid large-scale approximation, but the sentence is numerically false and “not an approximation anyone need worry about” erases the scale and boundary-layer qualifications.

Standard affected: Numbers; scope

Evidence: Current table; direct comparison of powers of ten.

**Proposed replacement — not applied:**

```html
<p>For the first two entries, the estimated viscous-to-inertial ratios are about $10^{-13}$ and $2.5\times10^{-6}$ on the adopted macroscopic scales. These values support neglecting viscosity in the corresponding large-scale momentum balances. They do not exclude viscous effects at smaller scales or in boundary layers.</p>
```

### C37 — Moderate: Analytic test cases are treated as an error bound for other polytropic indices

Location: afd/module03.html:437

> therefore trusted to about

Agreement for n=0,1,5 is valuable validation, but it does not establish the same error for n=3/2 or 3. Surface location and derivative extraction can have different numerical behaviour. The quoted accuracy should be demonstrated by convergence or an independent reference solution for the actual cases.

Standard affected: Evidence grade; numerical limits

Evidence: Scope of the reported numerical validation; no fresh integration run claimed.

**Proposed replacement — not applied:**

```html
<p>The analytic cases test the implementation and the surface-location procedure. Their errors do not by themselves bound the errors at $n=3/2$ and $n=3$. For those cases, numerical accuracy should be assessed by reducing the integration step and checking convergence of the first zero, its derivative and the derived mass coefficient. Until that check is supplied, the digits quoted here are computed values rather than an established error bound.</p>
```

### C38 — Moderate: A difference between two reconstructions becomes a universal uncertainty floor

Location: afd/module05.html:693

> no mass statement about this cloud is better than that

The 13.4% discrepancy is evidence that these inputs and modelling choices do not reproduce a unique mass. It is not a statistically calibrated uncertainty and cannot bound every possible mass determination of the cloud. The same precision inflation appears elsewhere when illustrative input values yield many displayed digits.

Standard affected: Evidence grade; scope

Evidence: Difference between model consistency and inferential uncertainty.

**Proposed replacement — not applied:**

```html
<p>The two reconstructions differ by $13.4$ per cent. This is a consistency discrepancy between the adopted inputs and model relations, not a calibrated uncertainty on every mass estimate for the cloud. A mass uncertainty would require an error budget for the measurements, their covariance and the modelling assumptions. We retain both results to show the sensitivity of this reconstruction.</p>
```

## Prose and clarity

### The objection is justified, but “bad grammar” is too narrow.

There are genuine local errors: “The Coulomb force has no range” says the wrong thing; the photospheric “—, against” construction mishandles punctuation; a radius is described as the size “across”; and the list of “all different” powers repeats k². Many other sentences are syntactically legal. Their problems are register, reference, rhythm or meaning. Calling all of them ungrammatical would obscure the work that actually needs doing.

### The dominant voice is a referee delivering verdicts.

“Confirmed”, “refuted”, “the premise is spent” and “what the gap indicts” make the author sound preoccupied with winning an argument. A textbook should distinguish a derivation, a numerical check, a fitted parameter, a consistency comparison and a falsification. Those categories are repeatedly blurred. The reversed-bound examples show that this is more than an aesthetic problem.

### The book repeatedly explains its own manufacture.

The reader encounters “first draft”, “shipped page”, “Gate D”, generators, what was fetched, and debts owed to other modules. Reproducibility and provenance matter, but most of this belongs in an editorial log, source appendix or reproducibility note. The physical argument should survive removal of every sentence about how the chapter was produced.

### The recurring metaphors require an unnecessary translation.

Assumptions are paid for or spent; modules owe and repay; gravity charges and shear pays; discrepancies indict models. An occasional analogy can help. This repeated financial and adversarial vocabulary forces the reader to translate physics into the author’s private idiom. State the mechanism, approximation or comparison directly.

### Prominent claims outrun their own caveats.

“Exactly”, “nothing else”, “every” and “cannot” repeatedly extend conclusions beyond their assumptions. Some subsequent paragraphs provide good qualifications, but a correct caveat does not cure a false opening or result box. Readers reasonably remember the prominent sentence. Its condition belongs in that sentence.

### The rhythm exposes the template.

A setup announces a disagreement; a bold sentence declares a result; a calculation returns a striking ratio; a paragraph confirms or refutes; a final sentence passes a debt to another module. This repetition, alongside stage directions such as “Hold that number”, creates the artificial effect the user noticed. This is a stylistic diagnosis, not an AI-authorship detector or a claim about Claude’s hidden drafting process.

### The skill’s appearance is present; its central judgement is inconsistent.

The science-editor skill requires precise claims, defined terms, proofs, limits and evidence. The manuscript often has their outward forms—proposition boxes, algebra and source quotations—but important inferences still fail. A script can confirm that 8.02×10⁻⁶ divided by 2×10⁻⁸ is 401 without checking whether exceeding a lower bound is a contradiction. That semantic check is the missing editorial work. Conversely, mechanically applying a five-part template to every simple identity can inflate the prose. Not every connective step needs a proposition box.

### Numerical precision is not the same as physical precision.

Many digits can be useful for checking a numerical implementation against an analytic case. They should not be carried uncritically into conclusions based on uncertain astrophysical inputs. The book sometimes makes this distinction well, then abandons it in the next verdict. State separately the numerical error, measurement error and model uncertainty.

### 48 representative line edits

Each edit identifies whether the issue is incorrect English, ambiguity, overstatement or stylistic choice. The revisions preserve mathematical depth while replacing theatrical or administrative language with explanation.

### Module 01

**P01 — module01.html:146**

> The fluid description is the bet that we never need it.

A metaphor replaces the closure argument. Not a grammar error.

**Rewrite:** A fluid model evolves a few moments of the distribution instead of resolving its full velocity dependence. We must determine when those moments admit an adequate closure.

**P02 — module01.html:252**

> The Coulomb force has no range

Wrong idiom for the intended physical meaning.

**Rewrite:** The unscreened Coulomb force has no finite cutoff: two charges interact at every separation.

**P03 — module01.html:248**

> Sixty-six micrometres, in an object

Sentence fragment plus a radius described as a diameter.

**Rewrite:** The mean free path is about 66 micrometres, whereas the solar radius is 6.957 × 10¹⁰ cm. Their ratio measures the separation between microscopic and stellar scales.

**P04 — module01.html:581**

> the magnetic rescue is one-dimensional

The label contradicts the following “two directions out of three”; “rescue” hides the mechanism.

**Rewrite:** Gyromotion restricts motion across a locally uniform field, while particles remain free to stream along it. These two directions therefore require different transport descriptions.

### Module 02

**P05 — module02.html:205**

> There are five, so there are five

Tautological emphasis obscures what is being counted.

**Rewrite:** The five independent collision invariants yield five scalar conservation equations: one for mass, three for momentum and one for energy.

**P06 — module02.html:308**

> the gas at this point is not changing, but a denser parcel has arrived

The spatial and material viewpoints are mixed.

**Rewrite:** The local derivative measures change at a fixed position. The advective term accounts for the change experienced by a moving parcel as it crosses a spatial density gradient.

**P07 — module02.html:487**

> The subscript is not decoration.

Scolding aside; the promised global convention is contradicted later.

**Rewrite:** In this module, μ denotes dynamic viscosity and μₘ denotes mean molecular weight. The global notation table should identify the convention used in later modules.

**P08 — module02.html:519**

> dropping it is not an approximation anyone need worry about

An absolute reassurance suppresses the approximation’s domain.

**Rewrite:** Viscosity is negligible in this large-scale force balance; it may still matter on smaller scales and near boundaries.

### Module 03

**P09 — module03.html:178**

> Note the direction of this argument.

Stage direction delays the actual assumption.

**Rewrite:** This estimate concerns slow secular contraction; it does not bound oscillatory departures from hydrostatic equilibrium.

**P10 — module03.html:630**

> Hold that number.

Unnecessary instruction to the reader.

**Rewrite:** This pressure fraction tests the assumption that gas pressure dominates at the solar centre.

**P11 — module03.html:340**

> The difference is the latent heat released

Overconfident causal compression; the reference atmosphere is not a measured moist adiabat.

**Rewrite:** Latent heat can reduce the cooling rate of a saturated rising parcel. The standard atmospheric lapse rate, however, is a reference profile rather than the result of this parcel calculation alone.

**P12 — module03.html:437**

> The integrator is therefore trusted

Passive declaration of confidence instead of a stated validation limit.

**Rewrite:** The analytic cases support the implementation. The numerical cases still require a convergence check before an error estimate can be assigned.

### Module 04

**P13 — module04.html:127**

> as the $331.45

A stranded numerical value is made the grammatical subject of “tests”; name the measurement.

**Rewrite:** The solar frequency spacing tests the interior sound-speed profile, just as the measured speed of sound in air tests the thermodynamic closure for air.

**P14 — module04.html:184**

> That is the whole of the disagreement between Newton and Laplace

Grand historical verdict adds little and exceeds the specific derivation.

**Rewrite:** The two predictions differ because one uses an isothermal pressure response and the other an adiabatic response.

**P15 — module04.html:164**

> Linear theory is therefore the theory of motions

Definition is broader than the calculation supports.

**Rewrite:** For the acoustic perturbations considered here, linearisation requires a small velocity amplitude relative to the sound speed.

**P16 — module04.html:147**

> the thermodynamics of an ionising gas is not developed in this book

Stale whole-book statement; readers cannot rely on the navigation.

**Rewrite:** We postpone the thermodynamics of partial ionisation to Module 6. Here it identifies one limitation of the constant-γ closure.

### Module 05

**P17 — module05.html:115**

> The gas now makes its own gravitational field

Personification conceals what is new relative to Module 3.

**Rewrite:** The density perturbation now contributes to the gravitational field through Poisson’s equation.

**P18 — module05.html:115**

> the question is when that field wins against the pressure

A contest metaphor substitutes for the growth criterion.

**Rewrite:** We ask when the perturbed gravitational force exceeds the restoring effect of pressure, allowing a density disturbance to grow.

**P19 — module05.html:534**

> which contains a star

A source classification is overtranslated into a physical detection.

**Rewrite:** which the cited study classifies as star-forming because of evidence for inward gas motion

**P20 — module05.html:693**

> no mass statement about this cloud is better than that

Universal claim where a local consistency result is intended.

**Rewrite:** The two reconstructions disagree by 13.4 per cent; this discrepancy should be resolved before either is presented as a precise mass estimate.

### Module 06

**P21 — module06.html:188**

> where the premise is therefore spent

The recurring financial metaphor gives a false binary verdict at Mach 0.427.

**Rewrite:** At this Mach number, pressure equilibration is less well separated from the parcel’s motion, so the approximation requires closer examination.

**P22 — module06.html:512**

> No single mixing length describes both

Ambiguous: a constant length and a constant mixing-length parameter are different claims.

**Rewrite:** The local turnover time varies strongly with depth. This is compatible with a mixing length proportional to the local pressure scale height.

**P23 — module06.html:647**

> The isochoric runaway fires nowhere

Unidiomatic personification.

**Rewrite:** The isochoric instability criterion is not satisfied anywhere in this table.

**P24 — module06.html:754**

> one confirmed and one refuted, from the same source table

Announces a predetermined dramatic structure instead of the physical questions.

**Rewrite:** We compare the two predictions with the same source table, stating the assumptions and uncertainties for each comparison.

### Module 07

**P25 — module07.html:183**

> Their $k$-dependences are all different

Direct contradiction: the displayed list contains k² twice.

**Rewrite:** The contributions scale as k, k² or k³. Their signs and coefficients determine which wavelengths are unstable.

**P26 — module07.html:398**

> Gravity charges by volume and the shear pays by area

Extended financial metaphor is harder to interpret than the dispersion relation.

**Rewrite:** For this interface, the stabilising gravity term is proportional to k, whereas the destabilising shear term is proportional to k². Gravity therefore dominates at sufficiently small k.

**P27 — module07.html:449**

> marginal, and just interesting enough to believe

The author’s appetite for a result replaces an evidential judgement.

**Rewrite:** The predicted growth is about one e-folding over the crossing time. The interface may amplify a disturbance, but this estimate does not establish nonlinear roll-up.

**P28 — module07.html:505**

> Refuted: that the measurement settles the coefficient

Labels a limitation of inference as the refutation of a physical prediction.

**Rewrite:** What the measurement constrains about the mixing coefficient

### Module 08

**P29 — module08.html:124**

> Against every other length in the problem that is zero

A useful approximation is stated as a literal equality.

**Rewrite:** The estimated layer thickness is negligible compared with the macroscopic scales used in this calculation.

**P30 — module08.html:591**

> a failed model, not a noisy measurement

A rhetorical contrast excludes explanations the data have not excluded.

**Rewrite:** The residual trend requires investigation of both model inadequacy and systematic measurement effects.

**P31 — module08.html:608**

> the energy — REFUTED at 3.8σ

Verdict typography outruns the available uncertainty budget.

**Rewrite:** The inferred energy and the comparison yield disagree; the significance requires a fuller uncertainty budget.

**P32 — module08.html:833**

> the whole of this section's theory

Self-advertised brevity conceals an invalid change of assumptions.

**Rewrite:** The following calculation must account for the acceleration history before the planar mixing law can be applied to an expanding shell.

### Module 09

**P33 — module09.html:122**

> This module does the thing neither of them did

Vague “thing” and theatrical comparison with earlier chapters.

**Rewrite:** We solve the steady spherical-flow equations and examine how regular passage through a critical point constrains the solution.

**P34 — module09.html:212**

> more constrained than it has any right to be

Personification adds surprise without explaining the constraint.

**Rewrite:** Regularity at the sonic point restricts the allowed flow profiles.

**P35 — module09.html:156**

> because the module's first draft got it wrong

Draft history belongs in an editorial log, not the conceptual introduction.

**Rewrite:** The steady equations alone do not uniquely select the accretion rate; the transonic solution also requires a physical selection argument.

**P36 — module09.html:433**

> the last column is where the answer lives

Vague personification and an unnecessary promise.

**Rewrite:** The last column compares the predicted speed with the measured value.

### Module 10

**P37 — module10.html:299**

> There is exactly one result in the theory of turbulence that is exact

An unsupported superlative. Other exact balances and relations exist.

**Rewrite:** The four-fifths law is an exact relation derived from the Navier–Stokes equations under specified assumptions; its coefficient is not obtained from dimensional analysis.

**P38 — module10.html:749**

> Supersonic turbulence has nothing else

False exclusive claim; velocity, magnetic and energy statistics still matter.

**Rewrite:** Supersonic turbulence also develops large density fluctuations, whose distribution is important for star formation.

**P39 — module10.html:864**

> Two fits, forty years apart

Elementary chronology error: the cited papers are from 1981 and 1987.

**Rewrite:** Two linewidth–size fits published six years apart

**P40 — module10.html:872**

> did the measurement properly

Dismissive and scientifically uninformative.

**Rewrite:** Solomon and colleagues used a single survey, distance scale and cloud-identification method for their sample of 273 molecular clouds.

### Module 11

**P41 — module11.html:92**

> five decades inside the Bondi radius

The stated radii differ by about 3.29 decades; five decades refers approximately to the horizon.

**Rewrite:** The circularisation radius is about 2,000 times smaller than the quoted Bondi radius.

**P42 — module11.html:106**

> what holds the gas up? to what lets it down?

Cute symmetry blurs orbital support and angular-momentum transport.

**Rewrite:** The question changes from radial infall to the transport of angular momentum through an orbiting disc.

**P43 — module11.html:520**

> the repayment is this paragraph rather than an edit to a shipped page

Production policy is presented as pedagogy; it preserves an erroneous earlier claim.

**Rewrite:** The comparison must use a bolometric luminosity and the mass flux reaching the emitting region before it can be interpreted as a radiative efficiency.

**P44 — module11.html:570**

> the weakest imaginable magnetic field

Hyperbole omits wavelength and non-ideal limits on MRI.

**Rewrite:** In ideal MHD, a sufficiently weak field can destabilise differential rotation when the unstable wavelengths fit within the disc; non-ideal effects can alter this conclusion.

### Module 12

**P45 — module12.html:110**

> this module exists to pay them

The introduction centres a promise ledger rather than the subject.

**Rewrite:** This module develops the magnetic stresses and induction equation, then applies them to waves, gravitational support, transport and disc instability.

**P46 — module12.html:305**

> a draught, not a wind —, against

Broken punctuation around an already overloaded parenthesis; the air-speed analogy distracts.

**Rewrite:** For the adopted 5 G photospheric field, the magnetic pressure is about 1 dyn cm⁻², much smaller than the adopted gas pressure.

**P47 — module12.html:813**

> Gate D placed this return

Internal workflow vocabulary has leaked into the textbook.

**Rewrite:** Pressure anisotropy lies outside the isotropic closure used in this module. We identify the missing physics here but do not derive its instability thresholds.

**P48 — module12.html:819**

> Deriving them here would make a shipped module false

The reason for excluding a topic is an editing constraint, not a learning objective.

**Rewrite:** Oblique MHD shock conditions are beyond this module’s scope. Applying the theory to a magnetised shock would require those conditions in addition to the results derived here.

## Module-by-module assessment

Every written module was surveyed. The strengths below identify useful material; they do not certify every calculation in that module.

### 01 · Why a fluid at all?

A strong opening question is undermined by an “exact” Boltzmann equation, an over-rigid fluid definition, the collision-age inference and the claim of unchanging galactic orbits. Rebuild the hierarchy from kinetic models to moments and closures, identifying what collisions, fields and scale separation each justify.

What to preserve: The neutral and Coulomb mean-free-path mechanisms and the explanation of reciprocal averaging.

Relevant findings: C08, C15, C16, C34.

### 02 · Conservation laws

Keep the moment derivations but rewrite their interpretations. Re retains density dependence through the collision length; separate population fits do not bound the mean mass flux. Clarify scalar/vector equation counting and reconcile the promised μ/μₘ convention across the book.

What to preserve: The integration-by-parts steps and explicit material-derivative chain rule.

Relevant findings: C07, C29, C36.

### 03 · Hydrostatic structure

The luminosity-based precision claim is invalid even though hydrostatic equilibrium is a sound mean-structure approximation. Separate dynamical and secular timescales. Recast the atmospheric reference profile and distinguish analytic numerical checks from error estimates for other indices.

What to preserve: The Lane–Emden development and comparison between simplified polytropes and the real Sun.

Relevant findings: C09, C18 (also applies here), C37.

### 04 · Sound and stellar oscillations

Comparatively close to a coherent teaching chapter, but the small-amplitude argument omits cumulative nonlinear steepening. Historical flourishes, numerical values used as grammatical subjects and stale forward references interrupt the explanation.

What to preserve: The connection between acoustic travel time and stellar frequency spacing.

Relevant findings: C17; C35 and P16 for the ionisation reference.

### 05 · Gravitational instability

Introduce perturbed self-gravity rather than self-gravity for the first time. Repair the dimensionless figure caption, the L694-2 classification and the universal mass-error claim. Distinguish the Jeans infinite-medium setting from finite pressure-confined equilibria before comparing their criteria.

What to preserve: The careful distinction between a fitted/reconstructed contrast and an independent observation.

Relevant findings: C14, C27, C35, C38.

### 06 · Convection and thermal instability

The parcel arguments are useful, but the solar stability conclusions outrun the thermodynamic information supplied. Separate effective equation-of-state parameters from conserved composition, approximate evaluations from precise boundaries, and consistency checks from independent predictions.

What to preserve: The explicit density, correlation and formation-height assumptions in the granulation-flux calculation; carry them into the verdict.

Relevant findings: C10, C18, C19, C40.

### 07 · Interface instabilities

The common dispersion relation is a good organising device. Boundary conditions are the new ingredient, not wavelength-dependent growth itself. Replace the financial metaphors; distinguish scaling form from universal coefficient and wavelength dependence from selection of a finite fastest-growing scale.

What to preserve: The limiting cases and the distinction between a sufficient Richardson-number condition and its converse.

Relevant findings: C20, C31.

### 08 · Shocks and blast waves

Requires scientific repair before polish. Distinguish shocks from contacts, rebuild the Trinity comparison around an error budget, and withdraw the shell mixing-width bound until acceleration history and geometry are handled. Two malformed TeX source fragments also need repair.

What to preserve: Conservation-law jump derivations and the refusal to compare a gas-dynamic prediction with an incompatible magnetic-shock Mach number.

Relevant findings: C03, C21, C28; production notes.

### 09 · Winds and accretion

The critical-point calculations are valuable. The principal observational refutation fails because a lower bound is used backwards; the luminosity comparison adds a separate invalid rejection. Clarify the branch selection and separate outer supply, inner accretion, band luminosity and bolometric efficiency.

What to preserve: The analysis of exponential sensitivity to base temperature and the warning that a factor-of-few mass-loss match is a weak test.

Relevant findings: C01, C05, C22, C23.

### 10 · Turbulence

Replace unsupported absolutes about energy destruction, exact results and density statistics. Correct the lognormal variable transformation. Keep the assumptions of the hydrostatic mass-bias theorem in its result box. Fix the mean/median table label and six-year chronology.

What to preserve: The component-counting discipline and the explicit derivative caveat in the mass-bias proof.

Relevant findings: C11, C24, C30, C39.

### 11 · Accretion discs

Begin with orbital energy and angular momentum as distinct constraints. Circularisation is not a hard ballistic stopping radius. State Rayleigh stability in its limited setting, correct the α inequality, and repair the inherited luminosity comparison.

What to preserve: The distinction between Newtonian and relativistic efficiency values and the development of the stress/transport equations.

Relevant findings: C05 (inherited), C06, C12, C25.

### 12 · Magnetohydrodynamics

Several central interpretations need repair: critical mass-to-flux direction, beta versus Alfvén Mach number, and the viscosity-bound inference. Replace the promise-ledger introduction with magnetic stress, induction and wave speeds. Distinguish particle magnetisation, pressure ratio and bulk-flow response.

What to preserve: The magnetic-pressure/tension decomposition and explicit warnings about applying classical coefficients outside their regimes.

Relevant findings: C02, C04, C13, C26, C32, C33.

## Structure and pedagogy

### Use a physical sequence instead of a production ledger.

Question → assumptions → derivation → interpretation → worked example → limits. Move fetched-source status, previous-draft corrections, gate names, generator details and cross-module debts into supporting notes. Keep reproducibility links without narrating the build process in the explanation.

### Replace the binary verdict system.

Distinguish “derived under these assumptions”, “implementation check”, “fit”, “conditional consistency comparison”, “observational constraint” and “rejected under a stated error model”. A discrepancy does not automatically reject a theory; reproducing an input-derived number does not independently confirm one.

### Keep assumptions in summaries, captions and exercises.

Module 10 shows how a correct conditional theorem can become a false unconditional teaching point. When revisions are authorised, repair every dependent summary, figure caption, accessibility description, table and solution, not just the main paragraph.

### Repair the dependency map.

Module 3 already uses self-gravity; Module 6 develops partial-ionisation thermodynamics. Modules 11 and 12 discuss each other’s drafting order instead of presenting a clean reading order. Planned topics should be visibly labelled as planned, not offered as working links. Promised two-temperature and anisotropic-plasma material should be delivered or explicitly excluded at the relevant first use.

### Distinguish uncertainty from disagreement.

A model-to-model difference is not an uncertainty interval; a lower limit is not a point measurement; a local tensor coefficient is not an observational effective scalar. Identify the measured and derived quantities, the assumptions connecting them and the errors before printing a ratio.

### Use exercises to teach judgement.

Retain substitution exercises but add questions that require a limiting case, a probability-density transformation, the direction of an observational bound, or identification of a missing assumption. These mechanisms catch the actual errors found here. The complete exercise set was not independently solved in this audit.

### Reduce repetition without reducing the mathematics.

The reader can handle full derivations. Cut repeated self-justification: the proposition announces a result, the proof derives it, the paragraph restates it emphatically and the verdict announces it again. Keep a repetition only if it adds a new physical interpretation or example.

### Demonstrations of a more natural opening

#### Module 9

Gas around a gravitating body need not remain in hydrostatic equilibrium. A hot corona can expand as a wind, while gas supplied at large radius can flow inward. We will study both possibilities using steady spherical flow. The geometry simplifies the equations enough that we can trace how pressure, gravity and inertia determine the radial velocity.

The central difficulty occurs where the flow speed equals the sound speed. At that point, a smooth solution requires the numerator of the velocity equation to vanish along with its denominator. We will derive this regularity condition, distinguish the wind and accretion branches, and ask which observational comparisons constrain the idealised solutions.

#### Module 12

A magnetic field changes a conducting fluid in two related ways: it exerts stresses on the gas, and the moving gas changes the field. We begin by deriving the magnetic force and the induction equation. Together with mass, momentum and energy conservation, they define the magnetohydrodynamic model used in this chapter.

Three comparisons will recur. Plasma beta compares thermal with magnetic pressure. The Alfvén Mach number compares the flow speed with an Alfvénic wave speed. The product of gyrofrequency and collision time measures how strongly particles respond to the field between collisions. These quantities answer different questions, so we will keep their roles separate when discussing waves, collapse, transport and disc instability.

## Production checks and audit limits

The local-link check found eight unresolved destinations: seven links to unwritten Modules 13 or 14 and one missing anchor in Module 2. These are current filesystem checks, not an external-link availability survey. No live website was changed.

Module 8’s caption at lines 303–305 splits the intended rho commands into new lines followed by “ho_2” and “ho_1”. At lines 938–939, an intended roman BW subscript is split into a newline followed by “m BW”. These are malformed source fragments, not ordinary line wrapping. The intended first expression is $\rho_2/\rho_1 = \mathcal{M}^2 = \gamma M_1^2$; the second affected token is $R_{\rm BW}$. Both need rendering verification after an authorised repair.

The twelve independent checks test particular audit arguments, not the entire textbook. They cover Reynolds scaling, oscillatory acceleration, buoyancy periods, time-dependent mixing, bound logic, the lognormal mode, ballistic pericentre, the α inequality, beta versus Mach number, radial decades and gyro-orbit counting. No existing generator or build script was run to rewrite textbook outputs.

Rhetorical counts are saved in mechanical-checks.json. They describe extracted text after removing scripts, styles and SVG, and include quoted material. They are not a quality score or an AI-authorship score.

The report uses the manuscript’s optional MathJax CDN for display. Its text, source evidence, copyable replacement HTML and Markdown companion remain available without mathematical rendering.

- module09.html:847 → module13.html
- module09.html:914 → module13.html
- module09.html:915 → module13.html
- module09.html:944 → module13.html
- module10.html:285 → module14.html
- module10.html:918 → module14.html
- module11.html:666 → module13.html
- module12.html:112 → module02.html#boltzmann

## Evidence and source map

PDF page numbers count from one. Files and SHA-256 hashes are retained in the evidence folder. Only the identified passages were independently checked for this report; this is not a complete audit of the cited papers.

- [Marrone et al. (2007): Sgr A* rotation measure](https://arxiv.org/abs/astro-ph/0611791). Local sources/marrone2007.pdf, p. 4. Read the lower-limit paragraph and field-strength caveats. The source says lower limits “may pose problems for very low” accretion-rate models. Used for C01.

- [Zhuravleva et al. (2019): cluster viscosity](https://arxiv.org/abs/1906.06346). Local sources/zhuravleva2019.pdf, p. 5. Read pp. 4–5 and p. 12, including the anisotropic-transport alternative. The key direction is “suppressed by at least a factor”. The constraint is one-sided and depends on the Prandtl number. Used for C02.

- [Kandori et al. (2005): globule structure](https://arxiv.org/abs/astro-ph/0506205). Local sources/kandori2005.pdf, p. 5. Read §2.1. Barnard 335 has a Class 0 source; L694-2 “shows strong evidence of gas inward motion”, the stated classification basis. Used for C14, without making a claim about all later observations.

- [Troland & Crutcher (2008): magnetic fields in cores](https://arxiv.org/abs/0802.2253). Local sources/troland2008.pdf, p. 2. Read pp. 2–3. Subcritical masses satisfy M < MΦ; the opposite side is supercritical. Used for C04.

- [King, Pringle & Livio (2007): disc viscosity](https://arxiv.org/abs/astro-ph/0701803). Local sources/king2007.pdf, p. 6. Read the simulation summary on p. 4 and discussion on p. 6: observational α ≈ 0.1–0.4 versus simulated α ≤ 0.02 in the stated comparison. Used for C12, not as a survey of modern MRI simulations.

- [Venzmer & Bothmer (2018): solar-wind distributions](https://arxiv.org/abs/1711.07534). Local sources/venzheimer2018.pdf, p. 8. Read Table 3 and its separate Median and Mean headers. The values reproduced in Module 10 are from the mean column. Used for C30. The local evidence filename retains the downloader’s spelling.

- [Verscharen et al. (2019), equation 133](https://link.springer.com/article/10.1007/s41116-019-0021-0). The collisional-age definition follows a plasma element, ∫dt/τ = ∫dr/(Uτ). Read on the source page; used for C08.

- [MIT OCW 2.57 lecture notes](https://ocw.mit.edu/courses/2-57-nano-to-macro-transport-processes-spring-2012/2e4ecaa5cf55f03bcefbc8ccce79aed6_MIT2_57S12_lec_notes_2004.pdf). Supporting exposition for the collision-model assumptions in C15, including molecular chaos; not a full audit of the notes.

- [Textbook repository](https://github.com/az9713/astrophysical-fluid-dynamics). Opened for context. The local working-copy files were audited.

- [Writing-skills repository](https://github.com/az9713/writing-skills). Opened for context. The invoked science-editor skill was read from the local SKILL.md.

Editorial method: %USERPROFILE%/.agents/skills/science-editor/SKILL.md. Its role description supplies an editorial stance, not a biographical credential of this report’s author.

## Recommended revision sequence

1. Repair C01–C06 and their dependent conclusions first. These change what the book teaches. Do not retain a wrong conclusion merely because an earlier page has been shipped.
2. Repair the remaining major definitions, assumptions, statistical interpretations and source readings. Recompute affected tables and figures only after the corrected physical statement is settled.
3. Rewrite introductions, transitions and conclusions module by module in a consistent explanatory voice. Use the 48 edits as examples, not as a substitute for a full prose pass.
4. Reconcile notation, dependencies and missing-scope promises. Remove or relocate production-history paragraphs. Run numerical and rendering checks against the corrected content.
5. Finish with an independent read that asks what is assumed, what follows and what is measured. Reopen evidence whenever a conclusion is stronger than its premises. Perform grammar and punctuation cleanup last.

### What already works

The manuscript should not be discarded. Its worked calculations, explicit source tables, efforts to expose assumptions and several careful distinctions between validation and observation form a substantial foundation. Those virtues are applied inconsistently. The next pass should preserve the useful mathematics, make the conclusions obey it, and give the explanation a stable, direct voice.

## Signature and preservation

Signed: Codex — OpenAI. Independent scientific and prose audit, 20 September 2026, America/Los_Angeles. This signature identifies the author of this report and its proposed wording; it does not attribute these passages to Claude. No original manuscript content was edited.

Evidence: original-file-hashes.json, integrity-verification.json, independent-checks.json, mechanical-checks.json, findings.json and sources/source-manifest.json.
