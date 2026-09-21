from pathlib import Path
from bs4 import BeautifulSoup


PATH = Path(__file__).parent / "textbook-edition-20-rule" / "module12.html"


def replace_inner(tag, html):
    fragment = BeautifulSoup(html, "html.parser")
    tag.clear()
    for child in list(fragment.contents):
        tag.append(child)


soup = BeautifulSoup(PATH.read_text(encoding="utf-8"), "html.parser")

# Headings form part of the exposition. They should name the physics directly.
headings = {
    "magnetised": "1. When is a fluid magnetised?",
    "speeds": "1.1 Thermal-speed conventions",
    "induction": "2. The induction equation and magnetic flux freezing",
    "lorentz": "3. Magnetic pressure and tension",
    "waves": "4. Magnetohydrodynamic wave speeds",
    "m7bound": "4.1 The magnetic bound from Module 7",
    "spiral": "5. The Parker spiral",
    "check1": "5.1 Comparison with Helios measurements",
    "sensitivity": "5.2 Sensitivity to modelling choices",
    "alfvenradius": "6. Locating the Alfvén surface",
    "check2": "6.1 An observational bracket on the Alfvén radius",
    "support": "7. Magnetic support against gravitational collapse",
    "check3": "7.1 Critical mass-to-flux ratios",
    "transport": "8. Transport across a magnetic field",
    "twotimes": "8.1 Two measures of particle magnetisation",
    "check4": "8.2 What strong magnetisation does and does not imply",
    "mri": "9. The magnetorotational instability",
    "balance": "10. Anisotropy and critical balance",
    "limits": "11. Scope and limitations of single-fluid MHD",
    "anisotropy": "11.1 Pressure anisotropy in weakly collisional plasmas",
}
for ident, title in headings.items():
    node = soup.find(id=ident)
    if node is None:
        raise RuntimeError(f"missing heading #{ident}")
    node.string = title

blocks = []
stop = False
for node in soup.find_all(["h2", "h3", "p", "li", "figcaption"]):
    if node.name == "h2" and node.get("id") in {"problems", "notation", "sources"}:
        stop = True
    if stop:
        break
    if node.name in {"h2", "h3"}:
        continue
    if node.find_parent("nav") or node.find_parent("header"):
        continue
    if node.get_text(" ", strip=True):
        blocks.append(node)

# The indices below refer to complete prose blocks in the teaching body. Each
# replacement was written and reviewed in the context of its surrounding section.
R = {
    1: r"Magnetohydrodynamics extends ordinary fluid dynamics by adding the Lorentz force and an equation for magnetic-field evolution. The resulting theory describes Alfvén waves, magnetic support, anisotropic transport, the Parker spiral, and the magnetorotational instability.",
    16: r"Magnetic fields have already entered several physical arguments in this book. They confine weakly collisional plasmas, modify the stability of interfaces and clouds, and make transport direction-dependent. We now treat the field as a dynamical variable. Magnetohydrodynamics, or MHD, couples the fluid equations of Module 2 to Maxwell’s equations.",
    17: r"This coupling introduces two equations. The momentum equation acquires the Lorentz force, while Faraday’s law and Ohm’s law determine the evolution of $\mathbf B$. The kinetic derivation in Module 2 §4 remains applicable because $\nabla_{\mathbf v}\!\cdot\mathbf a=0$ for the Lorentz acceleration $\mathbf a=(q/mc)\,\mathbf v\times\mathbf B$. We can therefore retain the same moment hierarchy and add the electromagnetic terms explicitly.",
    18: r"The word <em>magnetised</em> refers to two different physical comparisons. The plasma beta $\beta$ compares gas pressure with magnetic pressure, so it measures the field’s dynamical importance. The product $\omega_{\rm c}\tau$ compares the gyrofrequency with the collision rate. It measures whether a particle executes appreciable gyromotion between collisions. Either condition may hold without the other.",
    19: r"Plasma beta provides a convenient environmental census because it does not require an assumed mean particle mass. Computing the Alfvén speed does require that assumption. The table lists both quantities and verifies $v_{\rm A}^2/c_s^2=2/(\gamma\beta)$. Agreement with this identity checks that the pressure, density, composition, and sound-speed conventions are mutually consistent.",
    20: r"We adopt a photospheric field strength of $5$ G as an order-of-magnitude value for the quiet Sun. It should not be interpreted as a measured global mean. The NASA Sun Fact Sheet gives $1$–$2$ G near the poles and about $25$ G in the bright network. It reports roughly $200$ G in plages and fields as large as $3000$ G in sunspots. Photospheric field strength therefore depends strongly on location and magnetic activity.",
    21: r"The other entries are representative field strengths for the environments considered earlier in the book. The $10$ G coronal value comes from the active-region example in Module 7. The solar-wind and intracluster values are the $5$ nT and $1\,\mu$G references used in Modules 1 and 10. For the molecular cloud we adopt $10\,\mu$G. Troland and Crutcher (2008) instead find a mean $|\mathbf B|=16.4\,\mu$G for their denser sample. A factor-of-two change in these illustrative values does not alter the regime classifications below.",
    22: r"The pressure diagram compares thermal and magnetic stresses through $\beta$; it does not locate the Alfvén surface. That transition also depends on the flow speed. Define the sonic and Alfvénic Mach numbers by $M_s=U/c_s$ and $M_A=U/v_A$. The definitions then give $M_A^2=(\gamma\beta/2)M_s^2$. Consequently, $M_A=1$ need not coincide with $\beta=1$. Section 6 includes the wind speed when locating the transition.",
    23: r"Plasma beta is a pressure ratio rather than a direct measure of field strength. The adopted corona and molecular cloud have the same $\beta$, although their fields differ by six orders of magnitude. Four census environments lie far from equipartition, $\beta=1$. The solar wind changes from sub-Alfvénic to super-Alfvénic as it expands, a transition examined in §6.",
    24: r"Thermal speed is not unique until its component convention is specified. A one-dimensional speed, a perpendicular rms speed, and a three-dimensional rms speed differ by fixed numerical factors. The table defines each convention before it is used. These definitions also explain the factor $\sqrt{3/2}$ that appears in §8.1.",
    25: r"The perpendicular, three-dimensional rms, and mean thermal speeds occur in the ratio $1:1.2247:1.1284$. Each serves a different calculation, so they must not be interchanged. The sound speed $c_s$ and Alfvén speed $v_{\rm A}$ are bulk wave speeds rather than particle thermal speeds. Their relation in equation (1.2) follows directly from the definitions and is independent of the component convention.",
    26: r"Maxwell’s equations determine the magnetic field, while the fluid equations determine the motion of the gas. Ohm’s law couples these systems by relating the electric field to the flow and current. Substitution into Faraday’s law produces an induction equation with two competing processes: advection of magnetic flux and resistive diffusion.",
    27: r"Their relative importance is measured by the magnetic Reynolds number $\mathrm{R_m}=UL/\eta_{\rm m}$, where $U$ and $L$ are characteristic flow scales and $\eta_{\rm m}$ is the magnetic diffusivity. A large system can have $\mathrm{R_m}\gg1$ even when its conductivity is finite. Increasing $L$ slows diffusion relative to advection; it does not change the material conductivity. In a classical, fully ionised plasma, the leading density dependence of the resistivity cancels, leaving only the weaker density dependence contained in the Coulomb logarithm.",
    28: r"Proposition 4 states the flux-freezing theorem associated with Alfvén (1942). The derivation given here is self-contained: when resistive diffusion is negligible, a material surface conserves its magnetic flux. The original paper is cited for historical attribution rather than as a missing step in the argument.",
    29: r"The plasma current couples the magnetic field to the fluid through the Lorentz force. Rewriting that force separates two effects. Spatial variation in $B^2/8\pi$ acts as a magnetic-pressure gradient, while curvature of the field lines produces magnetic tension. Pressure pushes across the field; tension acts along the local direction of a curved field line.",
    30: r"The final column equals $1/\beta$ by definition, but displaying it permits a direct pressure comparison. With the adopted photospheric field $B=5$ G, the magnetic pressure is approximately $1\ \mathrm{dyn\,cm^{-2}}$. It is therefore much smaller than the adopted gas pressure in that row.",
    31: r"Module 4 derived sound waves for a gas whose only restoring force was pressure. A magnetic field adds both magnetic pressure and field-line tension. These additional restoring forces split the compressive response into fast and slow magnetosonic modes and introduce the transverse Alfvén mode.",
    32: r"All tabulated speeds are in km s$^{-1}$. In the photosphere, $v_{\rm A}$ is about three hundred times smaller than $c_s$. Magnetic corrections to the acoustic wave speed are therefore only a few parts per million for the adopted parameters. This scale separation justifies the hydrodynamic approximation used for the photospheric example in Module 4.",
    33: r"""Module 7 §9.5 asks whether a magnetic field can suppress the observed Kelvin–Helmholtz growth. For equal fields on both sides of the interface, Proposition 6 gives the condition
$$ B\cos\theta \;\lt\; \Delta U\sqrt{\frac{2\pi\rho_h\rho_l}{\rho_h+\rho_l}} . \tag{4.2}$$
Here $\theta$ is the angle between the field and the perturbation wavevector. If the field exists on only one side, $2\pi$ is replaced by $4\pi$. We recompute the bound from the dispersion relation rather than importing the numerical result from Module 7.""",
    34: r"The recalculation reproduces the magnetic bound obtained in Module 7 and checks consistency between the two modules. It is not an experimental validation because both values follow from the same theoretical relation. A laboratory test would instead compare the dispersion relation with controlled measurements of Alfvénic or MHD interface modes; such data are outside the present source set.",
    35: r"The Parker spiral follows from solar rotation and radial wind expansion. Under ideal MHD, a field line remains tied to its rotating photospheric footpoint while the wind carries the outer portion away from the Sun. The radial and azimuthal motions therefore wind the field into a spiral. Once the solar rotation rate and wind speed are specified, the idealised geometry has no additional fitting parameter.",
    36: r"""The spiral changes the radial dependence of the total field. Define $x\equiv\Omega(r-r_0)\sin\theta/v$. Then
$$ |\mathbf B| = B_r\sqrt{1+x^2}, \qquad \frac{\mathrm{d}\ln|\mathbf B|}{\mathrm{d}\ln r} = -2 + \frac{x^2}{1+x^2}\left(\frac{r}{r-r_0} - \frac{\mathrm{d}\ln v}{\mathrm{d}\ln r}\right). \tag{5.2}$$
Close to the Sun, $x\ll1$, the field is nearly radial, and $|\mathbf B|\propto r^{-2}$. Farther out, $x\gg1$, the azimuthal component dominates and the index approaches $-1$. A spacecraft sampling the transition measures an intermediate exponent, as shown in Fig. 2.""",
    37: r"Left: four equatorial field lines extend from the source surface at $2.5\,R_\odot$ to 1 au. At 1 au, the highlighted line makes an angle of $44.20^\circ$ with the radial direction for the mean fitted wind speed. Right: the total field across the Helios interval, $0.29$–$0.98$ au. Equation (5.2) gives a best-fitting exponent of $-1.7751$ over this finite range. Venzmer and Bothmer measure $-1.5460$, with year-to-year scatter $0.110$ and formal fit error $0.018$. The mean-fit difference is $2.08$ times the year-to-year scatter; the median-fit difference is $0.92$ times its scatter. Both comparisons favour a wound field over the unwound $r^{-2}$ reference, although the ideal Parker model does not reproduce the measured exponent exactly.",
    38: r"Venzmer and Bothmer (2018) fit power laws $x(r)=d\,r^e$ to Helios 1 and 2 observations from $0.29$ to $0.98$ au. They report distinct mean and median fits, each with its own coefficients and uncertainties. The calculations below retain those pairings so that no coefficient from one fit is combined with another.",
    39: r"The density profile provides an independent consistency check. For a steady spherical wind, mass conservation gives $\rho\propto r^{-2-\alpha_v}$, where $\alpha_v$ is the measured velocity exponent. The predicted density indices are $-2.0580$ for the median fit and $-2.0490$ for the mean fit. The corresponding measurements are $-2.093\pm0.046$ and $-2.010\pm0.038$. Their differences are $0.49$ and $0.54$ times the reported year-to-year scatter. The Helios data therefore recover the expected density scaling while showing that the magnetic field decreases more slowly than $r^{-2}$.",
    40: r"The largest exponent shift produced by the modelling choices in the table is $0.0194$. This is $5.7$ times smaller than the observed year-to-year scatter of $0.110$. The comparison with the Helios exponent is therefore insensitive to these particular choices, although it remains sensitive to departures from the ideal Parker assumptions.",
    41: r"Close to the Sun, the wind is sub-Alfvénic: $v\lt v_{\rm A}$. Alfvénic disturbances can then propagate upstream against the outflow. Farther out, $v\gt v_{\rm A}$, and the wind carries all such disturbances away from the Sun. The Alfvén surface is the locus $v=v_{\rm A}$ separating these causal regimes.",
    42: r"Wind speed and radial Alfvén speed from equation (6.1), plotted against heliocentric distance for the mean fits and a proton plasma. Their crossing defines the model Alfvén radius. The shaded band covers eight variants: mean or median fits, constant or power-law wind speed, and either pure protons or 4 per cent helium. These variants give $15.76$–$19.35\,R_\odot$. The published estimate $12.080\pm0.236\,R_\odot$ is shown as a point. The Parker Solar Probe value $19.8\,R_\odot$ is shown as a lower bound rather than a direct measurement of the crossing.",
    43: r"All eight model variants place the crossing between $15.76$ and $19.35\,R_\odot$. The dominant uncertainty comes from extrapolating a wind-speed fit measured over $0.29$–$0.98$ au inward to roughly $0.08$ au. Replacing the power-law speed with a constant value changes $r_{\rm A}$ by $6.9$ per cent. A realistic accelerating inner wind would lower the inferred crossing radius, moving it toward the estimate of Verscharen, Bale, and Velli.",
    44: r"A magnetic field can oppose gravitational contraction across its field lines. The relevant measure is the mass per unit magnetic flux, $M/\Phi$. A cloud with a ratio below the critical value is <em>subcritical</em>; magnetic stresses can support it in the idealised geometry. A supercritical cloud exceeds that value, so its field cannot prevent collapse by itself. Ideal flux freezing conserves $M/\Phi$ for a material flux tube. Non-ideal processes, including ambipolar diffusion, can change it. The numerical critical coefficient depends on the assumed cloud geometry.",
    45: r"Consider the fiducial cloud used in the census: radius $R=5$ pc, total number density $n_{\rm tot}=100\ \mathrm{cm^{-3}}$, mean molecular weight $\mu=2.33$, and field strength $B=10\ \mu$G. Applying the spherical and sheet-like critical coefficients gives the two estimates below.",
    46: r"The cloud mass is $2.993\times10^{3}\,M_\odot$. Both geometries classify the cloud as supercritical, so the adopted field cannot support it against gravity. Their numerical answers differ by the coefficient ratio $1.2657$, which measures the geometric dependence of the idealised threshold.",
    47: r"""Troland and Crutcher (2008) observed 34 dark-cloud cores for approximately $500$ hours using Arecibo OH Zeeman measurements. They express the mass-to-flux ratio as
$$ \lambda = 7.6\times10^{-21}\,\frac{N({\rm H_2})}{B_{\rm los}}, \qquad N \text{ in cm}^{-2},\quad B_{\rm los}\text{ in }\mu\text{G}. \tag{7.3}$$
Their critical value follows Nakano and Nakamura and uses the same coefficient as equation (7.2). This agreement checks the normalization. Interpreting an individual cloud still requires care because Zeeman observations measure the line-of-sight field rather than the full three-dimensional field.""",
    48: r"Transport in the intracluster medium is strongly direction-dependent. Classical isotropic viscosity would make the Reynolds number too small to explain the observed turbulent fluctuations. Unrestricted classical conduction would also redistribute heat rapidly. A magnetic field suppresses motion across its direction while permitting much faster transport along it. Braginskii’s coefficients describe this local anisotropy, whereas astronomical observations constrain an effective coefficient averaged over tangled fields and large spatial scales.",
    49: r"""For a hydrogen plasma, Braginskii’s equations (2.12) and (2.13) give the electron thermal conductivities
$$ \kappa_\parallel = 3.16\,\frac{n_{\rm e}T_{\rm e}\tau_{\rm e}}{m_{\rm e}}, \qquad \kappa_\perp = 4.66\,\frac{n_{\rm e}T_{\rm e}}{m_{\rm e}\omega_{\rm e}^2\tau_{\rm e}}, \qquad \frac{\kappa_\perp}{\kappa_\parallel} = \frac{4.66}{3.16}\frac{1}{(\omega_{\rm e}\tau_{\rm e})^2}. \tag{8.2}$$
The parallel coefficient grows with the collision time because particles travel farther between collisions. The perpendicular coefficient decreases with collision time because well-resolved gyromotion confines particles more effectively. Braginskii’s ion-viscosity coefficients have the same qualitative structure; Module 10 §6.2 uses $\eta_0^{\rm B}=0.96\,n_iT_i\tau_i$ and $\eta_1^{\rm B}=(3/10)n_iT_i/(\omega_i^2\tau_i)$.""",
    50: r"Two common collision-time conventions give slightly different numerical ion magnetisations. One computes $\omega_i\tau_i$ directly from Braginskii’s collision time. The other divides a Spitzer mean free path by a gyroradius. Both describe the same strongly magnetised plasma, but they use different thermal-speed conventions and slightly different Coulomb logarithms.",
    51: r"""Their ratio is
$$ \frac{\lambda/r_g}{\omega_i\tau_i^{\rm B}} = \sqrt{\tfrac32}\,\frac{\ln\Lambda_{\rm e}({\rm derived})}{\ln\Lambda({\rm census})} = 1.224745\times\frac{37.081}{37.8}=1.2015. \tag{8.3}$$
The exact factor $\sqrt{3/2}$ comes from counting velocity components. A Spitzer mean free path uses the three-dimensional rms speed $\sqrt{3k_{\rm B}T/m}$. The gyroradius uses the perpendicular rms speed $\sqrt{2k_{\rm B}T/m}$. The remaining factor, $37.081/37.8$, reflects the two adopted Coulomb logarithms. It changes the ratio by only $1.9$ per cent and does not indicate an inconsistency between the modules.""",
    52: r"The final row checks the collision-time normalization. Braginskii’s ion and electron collision times obey $\tau_i/\tau_{\rm e}=\sqrt{2m_{\rm p}/m_{\rm e}}$. The normalized value must therefore equal unity; any departure would signal that one convention had changed without the other.",
    53: r"The large value of $\omega_i\tau_i$ establishes that individual ions are strongly magnetised. It does not determine the effective transport coefficient of a tangled, weakly collisional cluster plasma. That coefficient also depends on field-line geometry, pressure-anisotropy instabilities, and the relation between local stresses and coarse-grained motion. These effects must be modelled before Braginskii’s local tensor can be compared with the observed fluctuation spectrum.",
    54: r"Differentially rotating discs require a mechanism that transports angular momentum outward. The magnetorotational instability, or MRI, provides such a mechanism when a weak magnetic field couples neighbouring fluid elements. We analyse the instability locally, taking the background shear as given. The global disc structure and the $\alpha$ prescription are developed in Module 11.",
    55: r"A Keplerian disc has $\Omega\propto R^{-3/2}$ and specific angular momentum $\ell=\Omega R^2\propto R^{1/2}$. Because $\ell$ increases outward, the Rayleigh criterion predicts hydrodynamic stability. An outwardly displaced ring carries too little angular momentum for its new orbit and returns inward. A weak magnetic field changes this response by coupling displaced rings through magnetic tension. The coupling destabilises the differential rotation and permits outward angular-momentum transport.",
    56: r"Growth rate from equation (9.1) for Keplerian shear, $q=3/2$. The unstable root reaches $\gamma=0.75\,\Omega$ at $kv_{\rm A}=\sqrt{15}\,\Omega/4$. Growth ends at $kv_{\rm A}=\sqrt3\,\Omega$, which imposes a minimum unstable wavelength. The dotted lines correspond to wavelengths equal to one scale height in the two worked discs. Both fall inside the unstable interval, so each disc can contain an MRI mode. A sufficiently strong field moves this scale beyond the upper wavenumber boundary and stabilises the local mode.",
    57: r"Module 10 finds a solar-wind magnetic spectrum close to $k^{-5/3}$. A hydrodynamic Kolmogorov argument alone cannot explain this exponent in a magnetised plasma because the cascade is anisotropic. Critical-balance theory supplies a separate argument for a $-5/3$ spectrum perpendicular to the local magnetic field while predicting a different scaling parallel to it.",
    58: r"""The anisotropy relation must include the outer scale $L$:
$$ k_\parallel \approx k_\perp^{2/3}L^{-1/3}. $$
The factor $L^{-1/3}$ restores dimensional consistency. Writing only $k_\parallel\sim k_\perp^{2/3}$ would equate quantities with different physical dimensions and would therefore be incomplete.""",
    59: r"Single-fluid MHD is a controlled idealisation rather than a universal plasma theory. The table below lists each assumption, the phenomenon it excludes, and the later treatment that relaxes it when one is available. Assumptions without a later remedy are identified explicitly.",
    60: r"A magnetic field constrains charged-particle motion across the field but not along it. A magnetised collisionless plasma therefore need not possess a single scalar pressure. Instead it can have distinct components $p_\parallel$ and $p_\perp$. Collisions tend to equalise them, but that relaxation is slow in a weakly collisional plasma. The Chew–Goldberger–Low, or double-adiabatic, theory retains these two pressures. Solar-wind observations routinely measure the resulting anisotropy. When the anisotropy becomes large, firehose and mirror instabilities scatter particles and limit further departure from isotropy.",
    61: r"The single-fluid equations derived in this module assume an isotropic scalar pressure. They consequently exclude the firehose and mirror instabilities and cannot predict their regulation of transport. Describing those effects requires either kinetic theory or a fluid closure that evolves the parallel and perpendicular pressures separately.",
}

if len(blocks) < max(R):
    raise RuntimeError(f"expected at least {max(R)} teaching blocks, found {len(blocks)}")
for number, html in R.items():
    replace_inner(blocks[number - 1], html)

PATH.write_text(str(soup), encoding="utf-8")
print(f"rewrote {len(R)} teaching blocks and {len(headings)} headings in {PATH.name}")
