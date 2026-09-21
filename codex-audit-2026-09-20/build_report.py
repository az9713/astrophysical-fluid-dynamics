from pathlib import Path
from bs4 import BeautifulSoup
import json, html, re, hashlib

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent
findings=[]
styles=[]

def locate(m, quote):
    p=ROOT/'afd'/f'module{m:02}.html'
    lines=p.read_bytes().decode('utf8').split('\n')
    for n,line in enumerate(lines,1):
        t=BeautifulSoup(line,'html.parser').get_text(' ',strip=True)
        if quote in t:
            return n,t
    raise ValueError(f'Quote not found M{m}: {quote}')

def finding(m,quote,title,why,replacement,severity='Major',basis='Independent reasoning and current manuscript',standard='Precise statement; hypotheses and limits'):
    line,context=locate(m,quote)
    findings.append(dict(id=f'C{len(findings)+1:02}',module=m,line=line,quote=quote,context=context,title=title,why=why,replacement=replacement,severity=severity,basis=basis,standard=standard))

def style(m,quote,diagnosis,rewrite):
    line,context=locate(m,quote)
    styles.append(dict(id=f'P{len(styles)+1:02}',module=m,line=line,quote=quote,diagnosis=diagnosis,rewrite=rewrite))

# Highest-consequence errors first. All suggested changes remain in this report.
finding(9,r'That second comparison is what the refutation rests on',
'A lower bound is used backwards to reject Bondi accretion',
'The predicted rate exceeds an observational LOWER limit. That satisfies the inequality; it does not violate it. The factor 401 is arithmetically correct and logically irrelevant to the claimed rejection. The source explicitly discusses problems for very LOW accretion rates. The error is repeated in the narrative, verdict and figure interpretation. The conditional upper limits can constrain a model, but the lower limits cannot rescue an upper-limit argument whose assumptions have been relaxed.',
r'''<div class="keyresult"><b>Check 10 — a conditional constraint on the inward mass flux.</b> The Bondi estimate exceeds the quoted Faraday-rotation upper limits under the magnetic-field assumptions used to obtain them. Those assumptions must accompany the comparison. The lower limits impose a different requirement: the accretion rate must be large enough to produce the observed rotation measure. Our Bondi estimate satisfies those lower limits, so they provide no evidence against it. A claim that the inflow is reduced between the Bondi radius and the inner flow therefore requires an applicable upper limit or another independent constraint.</div>''',
'Blocking','Marrone et al. (2007), downloaded PDF p. 4, paragraph beginning “Our RM”; independent inequality check.','Precise statement; valid inference from concrete evidence')

finding(12,r'The classical factor is larger than the measured one',
'A viscosity upper bound becomes a fictitious measured interval',
'The chapter acknowledges a one-sided bound in the caption, then treats suppression factors of roughly 10–1000 as the endpoints of a measured interval. For the cited Prandtl-number cases, the source constrains effective viscosity to be small: a still smaller value is not excluded by that inequality. Also, a local perpendicular component of a transport tensor is not directly the same quantity as an effective scalar viscosity inferred from cluster fluctuations. Neither the stated 22.8–24.8-decade discrepancy nor the claimed refutation follows. This is the same category of inference error as C01.',
r'''<div class="keyresult"><b>Check 4 — strong particle magnetisation, with effective transport unresolved.</b> The large value of $\omega_i\tau_i$ places the ions in the strongly magnetised regime. Braginskii's local perpendicular viscosity is correspondingly much smaller than the parallel coefficient. Zhuravleva et al. constrain an effective viscosity from cluster fluctuations; for the cases discussed here, their result is an upper bound on that viscosity, not a lower bound. A coefficient below the bound is not excluded. Moreover, relating a local anisotropic coefficient to the inferred effective viscosity requires a model of field geometry and the motions being measured. The present calculation supplies no such model and therefore does not test, or refute, the classical perpendicular coefficient.</div>''',
'Blocking','Zhuravleva et al. (2019), downloaded PDF pp. 4–5 and p. 12; independent inequality check.','Precise statement; evidence interpretation; limits')

finding(8,r'Putting the second into the first is the whole of this section',
'The supernova mixing-width bound substitutes variable acceleration into a constant-acceleration law',
'The chapter correctly identifies h = α A g t² as a constant-acceleration relation, then inserts an instantaneous g(t). An accumulated displacement cannot generally be obtained this way. Using the Read-type history dependence introduced in Module 7, h = α A [∫√g dt]², and R = C t^m gives h/R = 4αA(1−m)/m when the idealised history begins at zero. This is not αAm(1−m). At m = 1/2 the two differ by a factor 16. A finite onset time changes the result again. This calculation is a counterexample to the asserted bound, not a replacement validated model of a curved, expanding shell. Proposition 9 and its headline refutation need to be withdrawn pending an appropriate model.',
r'''<p>The planar relation $h=\alpha Agt^2$ assumes constant acceleration. The shell acceleration $g(t)=m(1-m)Ct^{m-2}$ is time dependent, so inserting its instantaneous value into that relation does not establish a mixing-width bound. For comparison, applying the history-dependent prescription $h=\alpha A[\int_{t_0}^{t}\sqrt{g(t')}\,dt']^2$ gives</p>
<p>$$\frac{h}{R}=\frac{4\alpha A(1-m)}{m}\left[1-\left(\frac{t_0}{t}\right)^{m/2}\right]^2,\qquad 0\lt m\lt 1.$$</p>
<p>This expression still neglects curvature, expansion effects on the mixing layer and the evolution of its density contrast. It demonstrates why the acceleration history matters; it does not supply a tested supernova-shell law. The observed width cannot be used to reject the planar model through the proposed instantaneous-acceleration bound.</p>''',
'Blocking','Module 7 Read-integral prescription; independent integration and numerical counterexample in independent-checks.json.','Proof; hypotheses; limit case')

finding(12,r'Below it no field strength is enough; above it the cloud is held',
'The magnetic critical mass-to-flux interpretation is reversed',
'At fixed geometry the subcritical side has relatively more magnetic support; the supercritical side has too much mass per unit flux for magnetic support alone. The later proposition and discussion have the intended direction, so the opening directly contradicts what follows. Even on the subcritical side, “held” needs the qualification that gas can still move along field lines and that non-ideal processes can change the flux-to-mass relation.',
r'''<p>Magnetic support is characterised by a critical mass-to-flux ratio. A cloud below the critical ratio is magnetically subcritical: in the idealised geometry, magnetic stresses can oppose collapse across the field. A cloud above it is supercritical: the field cannot prevent gravitational collapse by itself. Flux freezing preserves the ratio for a material flux tube, whereas processes such as ambipolar diffusion can change it. The numerical critical coefficient depends on the cloud geometry.</p>''',
'Blocking','Troland & Crutcher (2008), downloaded PDF p. 2 and p. 3; manuscript Proposition 7.','Precise statement; limit case')

finding(9,r'both readings refute the model as stated',
'The luminosity test compares unlike efficiencies and contradicts the assumed energy model',
'The numerator used here is a 2–10 keV luminosity. The standard thin-disc efficiency is bolometric. Dividing the band luminosity by a Bondi supply rate gives a band-specific apparent efficiency referenced to the outer supply, not a measured radiative efficiency of the material reaching the black hole. More fundamentally, adiabatic Bondi accretion does not assume a thin-disc efficiency of 0.1. Radiating little is compatible with radiation being dynamically unimportant. Module 11 §9 carries this invalid comparison forward rather than correcting it.',
r'''<div class="keyresult"><b>Check 11 — a low X-ray luminosity relative to the outer gas supply.</b> The ratio $L_{2-10\,{\rm keV}}/(\dot M_{\rm B}c^2)$ is approximately $4\times10^{-9}$ for the inputs used here. It is an X-ray-band luminosity divided by the rest-mass power associated with the Bondi supply estimate. It is not a bolometric radiative efficiency, and the actual inward mass flux may differ from $\dot M_{\rm B}$. Comparison with a thin-disc efficiency therefore requires both a bolometric luminosity and an estimate of the mass reaching the emitting region. The low band luminosity alone does not refute an adiabatic Bondi model.</div>''',
'Blocking','The manuscript’s own luminosity-band definition and model assumptions; dimensional and model-consistency analysis.','Precise definition; valid comparison; limits')

finding(11,r'Inside $R_{\rm circ}$ the gas cannot go',
'Circularisation radius is mistaken for a ballistic stopping radius',
'The force-balance radius l²/(GM) is the radius of a circular orbit with that angular momentum. It is not the pericentre of a parcel arriving on a parabolic orbit. For zero orbital energy, solving l²/(2R²)−GM/R=0 gives R_p = l²/(2GM) = R_circ/2. Gas can pass inside R_circ without first losing angular momentum; dissipation of orbital energy permits circularisation. Angular-momentum transport is then needed for sustained inward motion through approximately circular orbits.',
r'''<p>The radius $R_{\rm circ}=\ell^2/(GM)$ is the radius of a circular orbit with specific angular momentum $\ell$. It is not a hard inner limit to ballistic infall: a zero-energy orbit with the same $\ell$ has pericentre $R_{\rm p}=\ell^2/(2GM)$. Gas can circularise near $R_{\rm circ}$ by dissipating orbital energy. Once it forms an approximately Keplerian disc, further inward motion through nearly circular orbits requires angular-momentum transport.</p>''',
'Blocking','Independent effective-potential calculation in independent-checks.json.','Precise definition; proof; counterexample')

finding(2,r'The density cancels',
'The Reynolds-number interpretation ignores the density inside the mean free path',
'An explicit factor of ρ cancels when the kinetic viscosity estimate is substituted. Density dependence does not disappear: for a neutral gas λ = 1/(√2 nσ), so Re is proportional to n at fixed speed, temperature, cross-section and system size. For a Coulomb plasma the collision length also depends on density. The formula Re ≈ 3 Ma_th/Kn is useful; its stated physical interpretation is wrong.',
r'''<p>The explicit factor of $\rho$ cancels on substituting the kinetic estimate of viscosity, giving $\mathrm{Re}\simeq3\mathrm{Ma}_{\rm th}/\mathrm{Kn}$. The density still enters through $\lambda$. For neutral hard-sphere collisions, $\lambda=(\sqrt{2}n\sigma)^{-1}$, so $\mathrm{Re}\propto n$ when $u$, $L$, $T$ and $\sigma$ are fixed. The formula relates three dimensionless measures of the same gas; it does not make the Reynolds number independent of density.</p>''',
'Major','Module 1 mean-free-path formula; independent substitution.','Precise statement; physical interpretation')

finding(1,r'Fewer than one proton in three',
'The solar-wind collision count uses spatial optical depth instead of collisional age',
'The bulk plasma travels outward at U(r), whereas λ is formed from a thermal speed and a relaxation time. The relevant accumulated relaxation measure is ∫dt/τ = ∫dr/[Uτ] = ∫(v_th/U)dr/λ. Omitting v_th/U changes the quantity. Extending a fitted outer-wind power law to r=0 is also unsupported. Finally, a Coulomb deflection time describes accumulated small-angle scattering, not a Poisson count of discrete binary encounters. The claimed fraction of protons with no collision is not established.',
r'''<p>To estimate cumulative collisional relaxation, follow a plasma element from a specified starting radius $r_0$ to $r_1$. Its collisional age is $A_c=\int_{r_0}^{r_1}dr/[U(r)\tau_c(r)]$. If the convention is $\lambda=v_{\rm th}\tau_c$, this becomes $A_c=\int_{r_0}^{r_1}[v_{\rm th}(r)/U(r)]\;dr/\lambda(r)$. The result depends on the flow and temperature profiles and on the starting radius. Because Coulomb relaxation accumulates many small deflections, $A_c$ should not be interpreted here as a measured fraction of particles that have undergone a discrete collision.</p>''',
'Major','Verscharen et al., Living Reviews in Solar Physics (2019), equation 133; manuscript collision-time convention.','Definition; proof; concrete interpretation')

finding(3,r'It is forced by the observed luminosity',
'Solar luminosity does not bound all departures from hydrostatic balance at 10⁻²⁴',
'The argument assumes a particular slowly evolving contraction with a secular gravitational-energy release. It cannot exclude oscillatory accelerations or convection, whose work need not accumulate in the assumed way. A purely illustrative displacement of 1 m with a 300 s period has acceleration/g ≈ 1.6×10⁻⁶ at the surface, already eighteen orders larger, without implying sustained contraction. This is a logical counterexample, not a claim about a measured solar amplitude. Hydrostatic balance remains an excellent mean-structure approximation; the proposed observational precision does not follow.',
r'''<p>For a star evolving through approximately hydrostatic states on a timescale $t_{\rm evol}$, a characteristic secular acceleration is $R/t_{\rm evol}^2$. Its ratio to gravity is of order $(t_{\rm dyn}/t_{\rm evol})^2$. Taking a thermal evolution timescale therefore motivates a small secular acceleration. This estimate does not bound oscillatory or convective accelerations and is not a luminosity-derived error bar on hydrostatic balance. We use hydrostatic equilibrium to model the mean stellar structure, while treating motions and their timescales separately.</p>''',
'Major','Independent counterexample; inspection of the assumptions in §2 and §8.','Hypotheses; proof; scope')

finding(6,"the table's own, $\\mu = \\rho k_BT/(P\\,m_u)$",
'An effective equation-of-state parameter is used as a conserved composition variable',
'The Ledoux proof assumes the parcel retains its composition. The inferred μ_eff = ρkBT/(Pm_u) can vary because of ionisation and non-ideal equation-of-state effects, not only composition. The chapter itself warns at line 371 not to feed the outer gradient into Proposition 3, yet uses it to move the boundary to 0.7306 R and calls the displacement an upper bound without proof. Similarly a measured background ∇ plateau is not by itself a measurement of the thermodynamic derivative ∇ad. This undermines the claimed precision of the solar stability calculation.',
r'''<p>The quantity $\mu_{\rm eff}=\rho k_BT/(Pm_u)$ inferred from this table is an equation-of-state diagnostic. Its gradient cannot automatically be identified with a composition gradient carried unchanged by a displaced parcel. A consistent buoyancy calculation uses the model's thermodynamic derivatives; for hydrostatic stratification one may write $N^2=g[(1/\Gamma_1)d\ln P/dr-d\ln\rho/dr]$, with $\Gamma_1$ evaluated for an adiabatic displacement at fixed composition. Alternatively, the Ledoux form requires actual composition variables and the corresponding equation-of-state derivatives. The effective-$\mu$ calculation is illustrative and does not establish a precise shift, or an upper bound on the shift, of the convection-zone boundary.</p>''',
'Major','Current Table 1, Proposition 3 and its explicit caveat; thermodynamic definition of Γ₁.','Defined terms; consistent hypotheses; valid numerical interpretation')

finding(10,r'most probable $\rho/\langle\rho\rangle$',
'The density table confuses a lognormal median with its mode',
'The last column is exp(s₀), the median of x=ρ/⟨ρ⟩ and the value corresponding to the mode of s=ln x. The mode of the density PDF p(x) is exp(s₀−σ_s²). The Jacobian p(x)=p_s(ln x)/x matters. For Mach 10 and b=1, the displayed 0.0995 is the median; the density mode is about 0.000985. The simplest repair is to relabel the column, preserve the computed values, and explain the distinction.',
r'''<p>Because $s=\ln x$ is Gaussian with mean $s_0=-\sigma_s^2/2$, the median density ratio is $x_{\rm med}=e^{s_0}$. The density probability distribution is $p_x(x)=p_s(\ln x)/x$, whose maximum occurs at $x_{\rm mode}=e^{s_0-\sigma_s^2}$. The final column below lists the <b>median</b> density ratio, not the mode of the density distribution. At $\mathcal M=10$ and $b=1$, these are approximately $0.0995$ and $0.000985$, respectively.</p>
<p><b>Replacement table heading:</b> median $\rho/\langle\rho\rangle$.</p>''',
'Major','Independent change-of-variables derivation and calculation.','Defined terms; proof; numerical interpretation')

finding(11,r'the true gap may be smaller than $5$ and cannot be larger',
'The simulation-to-observation inequality is reversed',
'The quoted simulation result is α_sim ≲ 0.02, and the observational range begins around 0.1. For those reported values the ratio is at least 5, and can be larger if α_sim is smaller. It is a separate physical possibility that more complete simulations would increase α. The prose confuses that possibility with the direction of the numerical bound.',
r'''<p>For the quoted comparison, $\alpha_{\rm obs}\gtrsim0.1$ and $\alpha_{\rm sim}\lesssim0.02$ imply $\alpha_{\rm obs}/\alpha_{\rm sim}\gtrsim5$. Smaller simulated values increase this ratio. The authors also discuss limitations that may cause the simulations to underestimate the physical stress. Addressing those limitations could reduce the discrepancy, but that possibility does not reverse the inequality for the results being compared.</p>''',
'Major','King, Pringle & Livio (2007), downloaded PDF pp. 4 and 6; independent inequality check.','Precise statement; inference')

finding(12,r'which is the physical reason §6 has a surface to find',
'Plasma beta is conflated with the Alfvén Mach number',
'Beta compares thermal and magnetic pressure. An Alfvén surface is defined by the relevant flow speed matching the Alfvén speed, not by beta crossing unity. For the simple speed definitions used here, M_A²=(γβ/2)M_s². At M_A=1 and M_s=10, beta is 0.012 for γ=5/3. A pressure-only census lacking a bulk-flow speed cannot locate the surface. Likewise “the gas drags the field” requires an induction/transport argument, not beta alone.',
r'''<p>The pressure diagram compares thermal and magnetic stresses through $\beta$. It does not locate the Alfvén surface, which depends on the flow speed. With $M_s=U/c_s$ and $M_A=U/v_A$, the definitions give $M_A^2=(\gamma\beta/2)M_s^2$. Thus $M_A=1$ need not occur at $\beta=1$. Section 6 uses the wind speed and magnetic field to examine that separate transition.</p>''',
'Major','Independent substitution of the chapter’s definitions.','Defined terms; concrete interpretation')

finding(5,r'Lynds 694-2, which contains a star',
'The cited source does not say that L694-2 contains a star',
'Kandori et al. distinguish Barnard 335, with a Class 0 source, from other listed globules without IRAS sources. They classify L694-2 as “star-forming” because it shows inward gas motion. The manuscript silently converts that classification into an embedded-star detection. This finding concerns what the cited paper supports, not a claim that no later observation could change the object’s classification.',
r'''<p>Kandori et al. place Lynds 694-2 in their star-forming category because of evidence for inward gas motion. That classification should not be restated as a detection of an embedded star: their discussion distinguishes it from Barnard 335, which has an identified Class 0 source. The quoted Bonnor–Ebert fit can still be compared with the critical dimensionless radius, subject to the equilibrium model's assumptions.</p>''',
'Major','Kandori et al. (2005), downloaded PDF p. 5, §2.1.','Concrete source attribution; precise statement')

finding(1,r'Equation (2.1) is exact and unusable',
'The foundational kinetic model is called exact, then dismissed',
'The Boltzmann equation with the stated binary collision closure is already a model, with dilute-gas and molecular-chaos assumptions. It does not retain all particle correlations. “Unusable” also contradicts the book’s later recommendation to solve kinetic equations where fluid closures fail. A capable reader needs to understand what is approximated at each level, not to accept a false exact-model versus usable-model dichotomy.',
r'''<p>The Boltzmann equation describes the evolution of the one-particle distribution under a dilute-gas collision model. Its collision term assumes that the incoming particles' velocities are uncorrelated at the level required for this closure. The equation retains much more velocity-space information than a five-field fluid model, so solving it is generally more expensive. A fluid approximation is useful when the moments needed for the problem can be evolved with a justified closure.</p>''',
'Major','Current equation and surrounding definitions; MIT OCW 2.57 lecture notes, Boltzmann-equation assumptions.','Precise statement; model hypotheses')

finding(1,r'No closed fluid description exists',
'Failure of a collisional closure is overstated as failure of every fluid description',
'A large Knudsen number invalidates the local collisional Chapman–Enskog argument being used. It does not prove that no useful moment closure exists. The book later discusses magnetised, anisotropic and collisionless cases. Conversely, a small Knudsen number does not by itself justify dropping viscosity: the relevant force ratio is set by Re. Using the book’s relation, Kn=10⁻⁴ and Ma_th=10⁻⁶ gives Re≈0.03, a continuum flow dominated by viscosity.',
r'''<p>When the collision length is comparable to the macroscopic scale, the local collisional closure used here is no longer controlled. A kinetic treatment or a separately justified moment closure is then needed. Small $\mathrm{Kn}$ supports a continuum approximation, but the inviscid limit requires an additional comparison: $\mathrm{Re}\gg1$ on the scales of interest. Heat transport, time dependence and boundary layers may impose further restrictions.</p>''',
'Major','Cross-check with Module 2 Proposition 12 and later magnetic closures; numerical counterexample.','Hypotheses; rescue or limit case')

finding(4,r'When the ratio approaches one, the wave steepens into a shock',
'Small acoustic amplitude does not prevent shock formation over long propagation distances',
'The local ratio of nonlinear to linear terms estimates the per-period error. Weak nonlinearity can accumulate: a compressive acoustic wave of velocity amplitude δu can steepen over a time of order 1/(kδu), even when δu/c_s≪1. Also, the statement identifies linear theory in general with subsonic motion, although this derivation is specifically a perturbation about a uniform acoustic background.',
r'''<p>For these acoustic perturbations, the instantaneous ratio of the nonlinear advection term to the linear term is of order $|\mathbf u_1|/c_s$. A small ratio justifies linear evolution over sufficiently short times. Nonlinear steepening can nevertheless accumulate over many periods: for a compressive wave the characteristic steepening time is of order $(k|\mathbf u_1|)^{-1}$. Shock formation therefore does not require the perturbation velocity to first become comparable with the sound speed.</p>''',
'Major','Independent timescale argument from the terms displayed in the chapter.','Hypotheses; limit case')

finding(6,r'It nevertheless convects every afternoon',
'A standard atmosphere is treated as a universal weather profile',
'The International Standard Atmosphere specifies a reference lapse rate, not every afternoon’s actual stratification. Dry convection can arise over a heated surface; moisture is not the only resolution of the comparison. The latent heat quoted is per gram of condensed water, not a fixed heat release per gram of the rising air parcel. The same over-attribution appears in Module 3’s explanation of the difference from the standard lapse rate.',
r'''<p>The standard tropospheric lapse rate is smaller than the dry adiabatic lapse rate, so this reference profile is stable to unsaturated adiabatic displacements. An actual daytime boundary layer can have a different profile and may support dry convection above a heated surface. In saturated air, condensation releases latent heat and reduces the parcel's cooling rate; the moist stability criterion can then differ from the dry one. The released heat is the latent heat per unit mass of water multiplied by the amount of water condensed, not a fixed heat input per unit mass of air.</p>''',
'Major','Definition of the reference profile; parcel thermodynamics; cross-check with Module 3.','Precise statement; defined quantities; scope')

finding(6,r'every solar g mode must have a period longer',
'A conditional Schwarzschild estimate is promoted to a universal solar-mode bound',
'The 38.8 min estimate uses a maximum N/(2π)=430.06 μHz without the composition term. The same table gives a Ledoux value of 453.84 μHz, corresponding to 36.72 min. Even taking the table at face value, the stronger universal bound does not follow. This does not prove an observed solar mode below 38.8 min; it identifies an inconsistent inference. The general gravity-wave frequency constraint also needs a specified oscillation model.',
r'''<p>In the composition-free approximation used for this estimate, the maximum buoyancy frequency corresponds to a period of about $38.8$ minutes. This is a characteristic lower-period scale for gravity waves within that approximation. It is not a universal lower bound for solar gravity modes: composition changes the buoyancy frequency, as the last column of Table 1 already shows. Quantitative mode periods require a consistent stratification and the stellar oscillation boundary-value problem.</p>''',
'Major','Current Table 1 and §3.1; independent reciprocal-frequency calculation.','Hypotheses; consistency; limit case')

finding(7,r'a growth rate that depends on the wavelength of the disturbance',
'The interface introduction denies a result already derived in the Jeans chapter',
'Module 5 explicitly derives a wavelength-dependent growth rate. Moreover, wavelength dependence does not automatically select a finite fastest-growing scale: ideal sharp-interface Rayleigh–Taylor growth without regularisation increases towards short wavelengths. The new ingredient is the interface boundary conditions, not the invention of wavelength-dependent stability.',
r'''<p>We now examine perturbations of an interface between two fluids. As in the Jeans calculation, different wavelengths can grow at different rates. The new step is to match the perturbations on the two sides through the interface conditions. A preferred finite wavelength exists only when the relevant stabilising physics or finite interface structure supplies one; the ideal sharp-interface problem need not select such a scale.</p>''',
'Major','Module 5 dispersion relation and Module 7 limiting cases.','Dependencies; precise statement; limits')

finding(8,r'Such a surface is a shock',
'A discontinuity is not necessarily a shock',
'A contact discontinuity can have a density jump without the mass flux and irreversible compression characteristic of a shock. The definition should distinguish these before introducing Rankine–Hugoniot conditions, which apply more generally to conservation-law discontinuities.',
r'''<p>The inviscid equations can admit discontinuities. A shock is a propagating discontinuity across which matter flows and, for an admissible compressive gas-dynamic shock, entropy increases. A contact discontinuity is different: the normal velocity and pressure are continuous in the ideal gas-dynamic case, while density and temperature may jump. The jump conditions follow from conservation; additional conditions determine which type of discontinuity they describe.</p>''',
'Major','Conservation-law definitions and the later contact-discontinuity discussion.','Defined terms; limit case')

finding(9,"Take the outward branch and it is E. N. Parker's solar wind",
'Velocity-sign symmetry is confused with selecting the physical wind and accretion branches',
'For the same closure, reversing a signed velocity preserves the stationary equations, but it does not turn the physical Parker solution into the usual Bondi solution with its outer boundary conditions. In speed magnitude, the transonic wind is subsonic inside and supersonic outside; Bondi accretion has the opposite arrangement. The two pass through the critical point on different slopes. The chapter later describes the topology more carefully, but the opening teaches the wrong shortcut.',
r'''<p>Steady spherical winds and accretion flows share the same critical-point structure when the same thermodynamic closure is used. Reversing the sign of a velocity preserves the stationary equations, but the physical solution also depends on its boundary conditions. The transonic wind is subsonic on the inner side of the critical point and supersonic outside it; the usual transonic accretion solution has the reverse arrangement. They follow different branches of the common equation.</p>''',
'Major','Current phase portrait and asymptotic branch descriptions.','Precise statement; boundary conditions')

finding(9,r'a curve reaches $u = 1$ only when $C = -3$',
'Reaching the sonic line is confused with crossing it smoothly',
'For C<−3, the level sets reach u=1 at the endpoints bounding the forbidden radial interval. Their derivative is singular there; they do not form a smooth transonic flow. The minimum argument establishes the unique constant for a smooth critical crossing, not the absence of all other intersections with u=1.',
r'''<p>A smooth transonic solution passes through both $u=1$ and $x=1$, which fixes $C=-3$. For $C\lt -3$, branches can reach $u=1$ at other radii, but the differential equation is singular there and the branches do not continue as smooth transonic flows. The distinction is between touching the sonic line at a singular endpoint and crossing it regularly through the critical point.</p>''',
'Major','Independent inspection of u²−2 ln u = 4 ln x+4/x+C and its extrema.','Proof; precise statement')

finding(10,r'energy is destroyed at a rate',
'Viscous dissipation is described as destruction of energy',
'Viscosity converts resolved kinetic energy into internal energy. The distinction matters in a textbook that previously derived a total-energy equation. The smooth incompressible Euler energy statement also needs that scope: weak solutions and compressible shocks complicate the limiting argument. The anomaly concerns a finite kinetic-energy dissipation rate as viscosity tends to zero.',
r'''<p>For smooth incompressible Euler flow in a closed or periodic domain, kinetic energy is conserved. At small nonzero viscosity, the flow can transfer kinetic energy to increasingly small scales, where viscosity converts it into heat. The kinetic-energy dissipation rate may remain finite as viscosity tends to zero. This limiting behaviour is called the dissipation anomaly; it does not violate conservation of total energy.</p>''',
'Major','Cross-check with the book’s energy balance; distinction between kinetic and total energy.','Defined quantity; hypotheses')

finding(11,r'A stable disc transports no angular momentum',
'Rayleigh stability is used to rule out every angular-momentum transport mechanism',
'The Rayleigh criterion concerns centrifugal instability under particular inviscid, axisymmetric assumptions. It does not establish the absence of viscous, non-axisymmetric, magnetic or wind-driven transport. Module 12 repeats the overstatement. The useful result is that Keplerian rotation is not centrifugally unstable by this criterion; the transport problem remains to be solved.',
r'''<p>Because specific angular momentum increases outward, a Keplerian disc satisfies the Rayleigh criterion for stability to axisymmetric centrifugal disturbances in the inviscid model. This removes one possible source of instability; it does not forbid angular-momentum transport. Viscous stresses, other instabilities, magnetic stresses and outflows require separate analysis. The next sections quantify the stress needed for accretion before examining candidate mechanisms.</p>''',
'Major','Scope of the chapter’s Rayleigh derivation; later stress equations.','Hypotheses; limits')

finding(12,r'Single-fluid MHD has one temperature by construction',
'A chosen one-temperature closure is presented as the definition of single-fluid MHD',
'A model with one bulk velocity can still evolve separate electron and ion internal energies. The distinction between a single bulk momentum equation and a one-temperature closure should not be erased. The book is entitled to omit two-temperature physics, but it should explain that this is its modelling choice.',
r'''<p>This module uses a one-temperature closure in addition to a single bulk velocity. Those are separate assumptions: a single-fluid momentum description can be coupled to distinct electron and ion energy equations. We do not develop that extension here. Where electron–ion equilibration is slow, the one-temperature closure requires additional justification.</p>''',
'Major','Model-variable distinction; current energy-equilibration discussion.','Definition; rescue or limit case')

finding(5,r'a straight line of slope $c_s^2$',
'The dimensionless Jeans-plot caption gives dimensional slope and intercept',
'For y=ω²/(4πGρ₀) and x=(k/k_J)², the dispersion relation is y=x−1. The plotted slope is 1 and the intercept −1. The caption instead quotes the slope and intercept for dimensional ω² against k². This is a direct figure-reading error.',
r'''<p>In the left panel, $y=\omega^2/(4\pi G\rho_0)$ is plotted against $x=(k/k_J)^2$, so the dispersion relation is $y=x-1$. The dimensionless slope is $1$ and the intercept is $-1$. Negative $y$, corresponding to $k\lt k_J$, gives gravitational growth rather than oscillation.</p>''',
'Major','Independent nondimensionalisation of equation (3.1).','Concrete figure; units')

finding(8,r'A structured residual is a failed model, not a noisy measurement',
'The Trinity comparison assigns a formal rejection level without the full error model',
'A systematic residual can arise from inadequate physics, calibration, correlated measurement error or data processing. The chapter itself acknowledges some of these possibilities nearby. The “REFUTED at 3.8σ” energy verdict divides a discrepancy by a quoted yield uncertainty without establishing the uncertainty of the film-based inference and its model inputs. That is a discrepancy expressed in units of one reported error, not a calibrated total significance.',
r'''<p>The residuals show a systematic trend relative to the fitted similarity law. This warrants investigation of both the physical assumptions and the measurement process, including calibration and correlated errors. The inferred energy differs from the comparison yield by about $3.8$ times that yield's quoted uncertainty. Because the uncertainty of the film-based inference and its model inputs has not been included, this ratio should not be reported as a $3.8\sigma$ rejection of the model.</p>''',
'Major','Current §5 error discussion and stated uncertainty budget; statistical inference.','Evidence grade; limits')

finding(2,r'The true answer lies between them',
'Mean and median fits are treated as statistical bounds',
'Separate fits to density and speed do not bracket their joint mass flux. The average of their product depends on covariance; even the product of their means is generally not the mean product. A median-product curve is not automatically a lower or upper bound. Conservation is a law of the flow, but testing a steady spherical reduction with ensemble statistics requires the corresponding averages and assumptions.',
r'''<p>The mean-fit and median-fit constructions give different radial trends. Neither is automatically a bound on the physical mass flux. In particular, $\langle\rho u\rangle=\langle\rho\rangle\langle u\rangle+\operatorname{Cov}(\rho,u)$, so the density–speed covariance is needed to infer the mean flux. The comparison is a consistency check on these fitted summaries, not a proof that the true mass flux lies between them.</p>''',
'Major','Independent identity for the mean of a product; current fit definitions.','Defined statistic; evidence interpretation')

finding(10,r'Venzmer & Bothmer median fits',
'Mean-fit solar-wind values are labelled median fits',
'The cited Table 3 has separate mean and median columns. The values used here—7.57 cm⁻³, 9.67×10⁴ K, 6.05 nT and 435.6 km/s—come from the mean-fit column. Module 9 identifies that choice correctly. The labels in Module 10’s paragraph and table should match both the source and the calculation.',
r'''<p>The comparison uses the <b>mean-fit</b> coefficients in Venzmer and Bothmer's Table 3, as does Module 9: $n=7.57 {\rm cm^{-3}}$, $T=9.67\times10^4 {\rm K}$, $B=6.05 {\rm nT}$ and $U=435.6 {\rm km\,s^{-1}}$ at 1 au. The median-fit coefficients describe a different statistical summary and are not the values in this column.</p>''',
'Major','Venzmer & Bothmer (2018), downloaded PDF p. 8, Table 3.','Source fidelity; defined statistic')

finding(7,r'a layer still governed by its seed would not be linear in it at all',
'A scaling fit is said to prove loss of initial-condition dependence',
'A linear late-time relation can have a coefficient or offset that still depends on the seed. Demonstrating the functional form therefore does not demonstrate universality or complete loss of initial-condition memory. The later discussion itself distinguishes the fitted coefficients.',
r'''<p>Late-time linearity against the Read variable supports the proposed functional form over the measured interval. It does not by itself establish independence from the initial perturbation: the slope, offset or onset time may still depend on the seed. That stronger claim requires comparisons showing that the relevant fitted parameters converge across initial conditions.</p>''',
'Major','Logical distinction between functional form and parameter universality; current experiment description.','Valid inference; limits')

finding(12,r'a good conductor through its size',
'Large magnetic Reynolds number is confused with material conductivity',
'System size changes the ratio of advection to diffusion, not the electrical conductivity of the material. Even in the idealised Spitzer regime, density cancellation is approximate because the Coulomb logarithm can change. The useful explanation is that large L can make magnetic diffusion slow on the dynamical timescale.',
r'''<p>Large size can make magnetic diffusion slow relative to advection even when the material conductivity is finite. The relevant ratio is $\mathrm{R_m}=UL/\eta_{\rm m}$, where $\eta_{\rm m}$ is magnetic diffusivity. Increasing $L$ increases $\mathrm{R_m}$ at fixed $U$ and $\eta_{\rm m}$; it does not make the plasma intrinsically more conducting. In the classical fully ionised regime, the leading density dependence of the resistivity largely cancels, although the Coulomb logarithm retains a weaker dependence.</p>''',
'Major','Definitions of conductivity, magnetic diffusivity and Rm in §2.','Defined terms; physical interpretation')

finding(12,r'the number of gyro-orbits a proton completes',
'Gyrophase is called a count of complete gyro-orbits',
'The chapter correctly defines ωcτ as a phase in radians near the beginning, but later calls it a count of complete orbits. The count is ωcτ/(2π). Also λ/r_g=ωcτ only when the same velocity convention defines both lengths; the chapter’s later collision-time comparison exists precisely because its conventions differ. The huge magnetisation conclusion survives, but the stated meaning of the number does not.',
r'''<p>The dimensionless quantity $\omega_i\tau_i$ is the gyro-phase accumulated in radians during one collision time. The number of complete gyro-orbits is $\omega_i\tau_i/(2\pi)$. A length ratio $\lambda/r_g$ equals $\omega_i\tau_i$ only when $\lambda$ and $r_g$ use compatible velocity and collision-time conventions. Either measure is very large here, establishing strong particle magnetisation.</p>''',
'Major','Current Definition 2 and transport-convention comparison; independent 2π conversion.','Defined quantity; notation')

finding(1,r'the stellar orbits it has today are the orbits it was born with',
'Collisionless dynamics is described as unchanging orbits',
'Negligible two-body relaxation does not freeze a galaxy’s mean potential or individual trajectories. Collective evolution and time-dependent gravitational fields can change orbital energies and angular momenta without close stellar encounters. The adjacent absolute denial of every fluid description also needs care: collisionless moment equations exist, although their closure is nontrivial.',
r'''<p>A very long two-body relaxation time means that discrete stellar encounters make little change over the age of the galaxy. The stars still move in the collective gravitational potential, which can evolve and alter their orbits. Collisionless dynamics therefore removes an important relaxation mechanism; it does not imply that the present orbital structure is identical to the initial one. A kinetic description retains the velocity distribution, while a moment description requires a suitable closure.</p>''',
'Major','Distinction between encounter relaxation and evolution in a collective potential.','Precise statement; limit case')

finding(5,r'Modules 2 to 4 treated gravity as a field imposed from outside',
'The book misstates its own dependency chain',
'Module 3 already treats self-gravitating hydrostatic spheres through the Lane–Emden equation. Module 5 introduces perturbations of self-gravity, not self-gravity for the first time. A related stale statement in Module 4 says ionising-gas thermodynamics is not developed in the book, although Module 6 develops a Saha-based treatment. These are substantive navigation errors for a learner.',
r'''<p>Module 3 treated self-gravity in hydrostatic equilibrium. Module 4 studied acoustic perturbations while keeping the gravitational field fixed. We now allow the density perturbation to generate a gravitational perturbation through Poisson's equation and ask when that feedback overcomes pressure support. The distinction is between an equilibrium gravitational field and the evolving field of the disturbance.</p>''',
'Moderate','Direct cross-check of Modules 3, 4, 5 and 6.','Dependencies; precise statement')

finding(2,r'by ten or more orders of magnitude',
'The prose overstates its own viscosity table',
'The first two rows give inverse Reynolds numbers of about 9.8×10⁻¹⁴ and 2.5×10⁻⁶. The second is a suppression by roughly 5.6 orders, not ten or more. Both may support an inviscid large-scale approximation, but the sentence is numerically false and “not an approximation anyone need worry about” erases the scale and boundary-layer qualifications.',
r'''<p>For the first two entries, the estimated viscous-to-inertial ratios are about $10^{-13}$ and $2.5\times10^{-6}$ on the adopted macroscopic scales. These values support neglecting viscosity in the corresponding large-scale momentum balances. They do not exclude viscous effects at smaller scales or in boundary layers.</p>''',
'Moderate','Current table; direct comparison of powers of ten.','Numbers; scope')

finding(3,r'therefore trusted to about',
'Analytic test cases are treated as an error bound for other polytropic indices',
'Agreement for n=0,1,5 is valuable validation, but it does not establish the same error for n=3/2 or 3. Surface location and derivative extraction can have different numerical behaviour. The quoted accuracy should be demonstrated by convergence or an independent reference solution for the actual cases.',
r'''<p>The analytic cases test the implementation and the surface-location procedure. Their errors do not by themselves bound the errors at $n=3/2$ and $n=3$. For those cases, numerical accuracy should be assessed by reducing the integration step and checking convergence of the first zero, its derivative and the derived mass coefficient. Until that check is supplied, the digits quoted here are computed values rather than an established error bound.</p>''',
'Moderate','Scope of the reported numerical validation; no fresh integration run claimed.','Evidence grade; numerical limits')

finding(5,r'no mass statement about this cloud is better than that',
'A difference between two reconstructions becomes a universal uncertainty floor',
'The 13.4% discrepancy is evidence that these inputs and modelling choices do not reproduce a unique mass. It is not a statistically calibrated uncertainty and cannot bound every possible mass determination of the cloud. The same precision inflation appears elsewhere when illustrative input values yield many displayed digits.',
r'''<p>The two reconstructions differ by $13.4$ per cent. This is a consistency discrepancy between the adopted inputs and model relations, not a calibrated uncertainty on every mass estimate for the cloud. A mass uncertainty would require an error budget for the measurements, their covariance and the modelling assumptions. We retain both results to show the sensitivity of this reconstruction.</p>''',
'Moderate','Difference between model consistency and inferential uncertainty.','Evidence grade; scope')

# Four representative prose edits per module, including real errors and editorial choices.
style(1,r'The fluid description is the bet that we never need it.','A metaphor replaces the closure argument. Not a grammar error.','A fluid model evolves a few moments of the distribution instead of resolving its full velocity dependence. We must determine when those moments admit an adequate closure.')
style(1,r'The Coulomb force has no range','Wrong idiom for the intended physical meaning.','The unscreened Coulomb force has no finite cutoff: two charges interact at every separation.')
style(1,r'Sixty-six micrometres, in an object','Sentence fragment plus a radius described as a diameter.','The mean free path is about 66 micrometres, whereas the solar radius is 6.957 × 10¹⁰ cm. Their ratio measures the separation between microscopic and stellar scales.')
style(1,r'the magnetic rescue is one-dimensional','The label contradicts the following “two directions out of three”; “rescue” hides the mechanism.','Gyromotion restricts motion across a locally uniform field, while particles remain free to stream along it. These two directions therefore require different transport descriptions.')

style(2,r'There are five, so there are five','Tautological emphasis obscures what is being counted.','The five independent collision invariants yield five scalar conservation equations: one for mass, three for momentum and one for energy.')
style(2,r'the gas at this point is not changing, but a denser parcel has arrived','The spatial and material viewpoints are mixed.','The local derivative measures change at a fixed position. The advective term accounts for the change experienced by a moving parcel as it crosses a spatial density gradient.')
style(2,r'The subscript is not decoration.','Scolding aside; the promised global convention is contradicted later.','In this module, μ denotes dynamic viscosity and μₘ denotes mean molecular weight. The global notation table should identify the convention used in later modules.')
style(2,r'dropping it is not an approximation anyone need worry about','An absolute reassurance suppresses the approximation’s domain.','Viscosity is negligible in this large-scale force balance; it may still matter on smaller scales and near boundaries.')

style(3,r'Note the direction of this argument.','Stage direction delays the actual assumption.','This estimate concerns slow secular contraction; it does not bound oscillatory departures from hydrostatic equilibrium.')
style(3,r'Hold that number.','Unnecessary instruction to the reader.','This pressure fraction tests the assumption that gas pressure dominates at the solar centre.')
style(3,r'The difference is the latent heat released','Overconfident causal compression; the reference atmosphere is not a measured moist adiabat.','Latent heat can reduce the cooling rate of a saturated rising parcel. The standard atmospheric lapse rate, however, is a reference profile rather than the result of this parcel calculation alone.')
style(3,r'The integrator is therefore trusted','Passive declaration of confidence instead of a stated validation limit.','The analytic cases support the implementation. The numerical cases still require a convergence check before an error estimate can be assigned.')

style(4,r'as the $331.45','A stranded numerical value is made the grammatical subject of “tests”; name the measurement.','The solar frequency spacing tests the interior sound-speed profile, just as the measured speed of sound in air tests the thermodynamic closure for air.')
style(4,r'That is the whole of the disagreement between Newton and Laplace','Grand historical verdict adds little and exceeds the specific derivation.','The two predictions differ because one uses an isothermal pressure response and the other an adiabatic response.')
style(4,r'Linear theory is therefore the theory of motions','Definition is broader than the calculation supports.','For the acoustic perturbations considered here, linearisation requires a small velocity amplitude relative to the sound speed.')
style(4,r'the thermodynamics of an ionising gas is not developed in this book','Stale whole-book statement; readers cannot rely on the navigation.','We postpone the thermodynamics of partial ionisation to Module 6. Here it identifies one limitation of the constant-γ closure.')

style(5,r'The gas now makes its own gravitational field','Personification conceals what is new relative to Module 3.','The density perturbation now contributes to the gravitational field through Poisson’s equation.')
style(5,r'the question is when that field wins against the pressure','A contest metaphor substitutes for the growth criterion.','We ask when the perturbed gravitational force exceeds the restoring effect of pressure, allowing a density disturbance to grow.')
style(5,r'which contains a star','A source classification is overtranslated into a physical detection.','which the cited study classifies as star-forming because of evidence for inward gas motion')
style(5,r'no mass statement about this cloud is better than that','Universal claim where a local consistency result is intended.','The two reconstructions disagree by 13.4 per cent; this discrepancy should be resolved before either is presented as a precise mass estimate.')

style(6,r'where the premise is therefore spent','The recurring financial metaphor gives a false binary verdict at Mach 0.427.','At this Mach number, pressure equilibration is less well separated from the parcel’s motion, so the approximation requires closer examination.')
style(6,r'No single mixing length describes both','Ambiguous: a constant length and a constant mixing-length parameter are different claims.','The local turnover time varies strongly with depth. This is compatible with a mixing length proportional to the local pressure scale height.')
style(6,r'The isochoric runaway fires nowhere','Unidiomatic personification.','The isochoric instability criterion is not satisfied anywhere in this table.')
style(6,r'one confirmed and one refuted, from the same source table','Announces a predetermined dramatic structure instead of the physical questions.','We compare the two predictions with the same source table, stating the assumptions and uncertainties for each comparison.')

style(7,r'Their $k$-dependences are all different','Direct contradiction: the displayed list contains k² twice.','The contributions scale as k, k² or k³. Their signs and coefficients determine which wavelengths are unstable.')
style(7,r'Gravity charges by volume and the shear pays by area','Extended financial metaphor is harder to interpret than the dispersion relation.','For this interface, the stabilising gravity term is proportional to k, whereas the destabilising shear term is proportional to k². Gravity therefore dominates at sufficiently small k.')
style(7,r'marginal, and just interesting enough to believe','The author’s appetite for a result replaces an evidential judgement.','The predicted growth is about one e-folding over the crossing time. The interface may amplify a disturbance, but this estimate does not establish nonlinear roll-up.')
style(7,r'Refuted: that the measurement settles the coefficient','Labels a limitation of inference as the refutation of a physical prediction.','What the measurement constrains about the mixing coefficient')

style(8,r'Against every other length in the problem that is zero','A useful approximation is stated as a literal equality.','The estimated layer thickness is negligible compared with the macroscopic scales used in this calculation.')
style(8,r'a failed model, not a noisy measurement','A rhetorical contrast excludes explanations the data have not excluded.','The residual trend requires investigation of both model inadequacy and systematic measurement effects.')
style(8,r'the energy — REFUTED at 3.8σ','Verdict typography outruns the available uncertainty budget.','The inferred energy and the comparison yield disagree; the significance requires a fuller uncertainty budget.')
style(8,"the whole of this section's theory",'Self-advertised brevity conceals an invalid change of assumptions.','The following calculation must account for the acceleration history before the planar mixing law can be applied to an expanding shell.')

style(9,r'This module does the thing neither of them did','Vague “thing” and theatrical comparison with earlier chapters.','We solve the steady spherical-flow equations and examine how regular passage through a critical point constrains the solution.')
style(9,r'more constrained than it has any right to be','Personification adds surprise without explaining the constraint.','Regularity at the sonic point restricts the allowed flow profiles.')
style(9,"because the module's first draft got it wrong",'Draft history belongs in an editorial log, not the conceptual introduction.','The steady equations alone do not uniquely select the accretion rate; the transonic solution also requires a physical selection argument.')
style(9,r'the last column is where the answer lives','Vague personification and an unnecessary promise.','The last column compares the predicted speed with the measured value.')

style(10,r'There is exactly one result in the theory of turbulence that is exact','An unsupported superlative. Other exact balances and relations exist.','The four-fifths law is an exact relation derived from the Navier–Stokes equations under specified assumptions; its coefficient is not obtained from dimensional analysis.')
style(10,r'Supersonic turbulence has nothing else','False exclusive claim; velocity, magnetic and energy statistics still matter.','Supersonic turbulence also develops large density fluctuations, whose distribution is important for star formation.')
style(10,r'Two fits, forty years apart','Elementary chronology error: the cited papers are from 1981 and 1987.','Two linewidth–size fits published six years apart')
style(10,r'did the measurement properly','Dismissive and scientifically uninformative.','Solomon and colleagues used a single survey, distance scale and cloud-identification method for their sample of 273 molecular clouds.')

style(11,r'five decades inside the Bondi radius','The stated radii differ by about 3.29 decades; five decades refers approximately to the horizon.','The circularisation radius is about 2,000 times smaller than the quoted Bondi radius.')
style(11,r'what holds the gas up? to what lets it down?','Cute symmetry blurs orbital support and angular-momentum transport.','The question changes from radial infall to the transport of angular momentum through an orbiting disc.')
style(11,r'the repayment is this paragraph rather than an edit to a shipped page','Production policy is presented as pedagogy; it preserves an erroneous earlier claim.','The comparison must use a bolometric luminosity and the mass flux reaching the emitting region before it can be interpreted as a radiative efficiency.')
style(11,r'the weakest imaginable magnetic field','Hyperbole omits wavelength and non-ideal limits on MRI.','In ideal MHD, a sufficiently weak field can destabilise differential rotation when the unstable wavelengths fit within the disc; non-ideal effects can alter this conclusion.')

style(12,r'this module exists to pay them','The introduction centres a promise ledger rather than the subject.','This module develops the magnetic stresses and induction equation, then applies them to waves, gravitational support, transport and disc instability.')
style(12,r'a draught, not a wind —, against','Broken punctuation around an already overloaded parenthesis; the air-speed analogy distracts.','For the adopted 5 G photospheric field, the magnetic pressure is about 1 dyn cm⁻², much smaller than the adopted gas pressure.')
style(12,r'Gate D placed this return','Internal workflow vocabulary has leaked into the textbook.','Pressure anisotropy lies outside the isotropic closure used in this module. We identify the missing physics here but do not derive its instability thresholds.')
style(12,r'Deriving them here would make a shipped module false','The reason for excluding a topic is an editing constraint, not a learning objective.','Oblique MHD shock conditions are beyond this module’s scope. Applying the theory to a magnetised shock would require those conditions in addition to the results derived here.')

finding(10,'Treating this cluster core as static costs about four per cent',
'A conditional mass-bias calculation is labelled an observational confirmation',
'The proposition and proof correctly require a radially constant pressure ratio and explicitly discuss the missing derivative. The verdict then states the mass cost as an established property of the cluster. A dispersion and temperature from one annulus do not measure the pressure-ratio gradient or independently measure the mass bias. The caveat about not extending the result to r500 is valuable but does not supply the missing local assumption. This is a failure to carry a correct hypothesis into the headline, not a failure of the displayed theorem.',
r'''<div class="keyresult"><b>Conditional estimate of hydrostatic mass bias.</b> If the turbulent-to-thermal pressure ratio is constant with radius, the adopted ratio of $4.15$ per cent implies a mass underestimate of $3.98$ per cent. The measurement in one annulus does not establish that radial constancy. In general, $M=(1+\alpha)M_{\rm th}-[r^2P_{\rm th}/(G\rho)]\,d\alpha/dr$, so the bias also depends on the pressure-ratio gradient. The quoted percentage is therefore a conditional calculation, not an independently measured mass bias.</div>''',
'Major','Current Proposition 7, its correct proof and the following verdict.','Hypotheses retained in conclusions; evidence grade')

finding(6,'SURVIVES: the mixing-length velocity law itself',
'A partially reused observation is presented as a 25% test of a prediction',
'The revised convective flux is built from the observed velocity and temperature contrast. That flux is then fed into the velocity law, whose output is compared with the same observed velocity. This is not a tautological identity—the velocity enters the prediction only to the one-third power—but it is not an independent velocity prediction either. The stated density, correlation and formation-height assumptions further condition the flux estimate. Calling the agreement a model survival to 25% overstates the test.',
r'''<p>Using the observed velocity and inferred temperature contrast gives a conditional estimate of the convective flux. Substituting that flux into the mixing-length velocity relation returns $0.816\ {\rm km\,s^{-1}}$, compared with the input velocity of $0.65\ {\rm km\,s^{-1}}$. Because the observed velocity contributes to the flux used in this calculation, the comparison is a partial consistency check, not an independent prediction accurate to $25$ per cent. An independent test would require the flux to be determined without reusing the velocity being tested.</p>''',
'Major','Current §7.3 Steps 2–3; dependency tracing of inputs and outputs.','Independence of concrete evidence; limits')

(OUT/'findings.json').write_text(json.dumps({'content':findings,'prose':styles},ensure_ascii=False,indent=2),encoding='utf8')
print(f'Located {len(findings)} content findings and {len(styles)} prose edits against the original HTML.')
