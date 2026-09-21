from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent / "textbook-edition-20-rule"


def norm(text):
    return " ".join(text.split())


def apply(number, replacements):
    path = ROOT / f"module{number:02d}.html"
    html = path.read_text(encoding="utf-8")
    for prefix, replacement in replacements:
        soup = BeautifulSoup(html, "html.parser")
        matches = [str(t) for t in soup.find_all(["p", "li", "div", "span", "td", "h2", "h3"])
                   if norm(t.get_text(" ", strip=True)).startswith(prefix)]
        if len(matches) != 1 or matches[0] not in html:
            raise RuntimeError((number, prefix, len(matches)))
        html = html.replace(matches[0], replacement, 1)
    path.write_text(html, encoding="utf-8")
    print(f"module {number:02d}: rewrote {len(replacements)} blocks")


apply(6, [
    (
        "Definition 3 (the mixing length).",
        '<div class="def"><b>Definition 3 (mixing length).</b> A convecting parcel is assumed to retain its identity while rising a distance $\\ell$. It then mixes with its surroundings and transfers its excess heat. Mixing-length theory writes $$\\ell=\\alpha H,\\qquad H=\\frac{P}{\\rho g},\\tag{6.1}$$ where $\\alpha$ is dimensionless and of order unity. This module uses $\\alpha=2.0$. Here $\\alpha$ denotes only the mixing-length parameter; the length scale in Module 5 uses the same symbol in a different context.</div>',
    ),
    (
        "Three premises are spent here",
        '<span class="warn"><b>Three assumptions fail near the photosphere.</b> First, the calculation assigns the entire flux to convection, although radiation carries $98.7$ per cent there. This makes $\\nabla-\\nabla_{\\rm ad}=0.6079$ and $v_c=3.451\\ \\mathrm{km\\,s^{-1}}$ overestimates with respect to the flux split alone. Second, an optically thin parcel radiates while it travels, violating the adiabatic-parcel assumption. That effect requires a larger gradient for a given convective flux and is not calculated here. Third, $v_c/c_s=0.4271$, so instantaneous pressure balance is also questionable. The first two effects act in opposite directions and do not define a bracket.</span>',
    ),
    (
        "A1: the scale is confirmed",
        '<div class="keyresult"><b>A1: the pressure scale height gives the correct scale but not the measured granule size.</b> The photospheric scale height is $143$ km, while the mean granule diameter is $1050\\pm22$ km. Identifying the diameter with $2\\ell$ gives $572$ km, a $21.7\\sigma$ shortfall; identifying it with $\\ell$ changes the ratio but not the disagreement. Because $\\alpha=2$ was calibrated to the solar radius, this is not a parameter-free prediction. The robust conclusion is only that granulation occurs on a scale set by several pressure scale heights.</div>',
    ),
    (
        "A comparison that is refused.",
        '<span class="warn"><b>The lower temperature boundaries are not comparable.</b> Heiles and Troland use $500$–$5000$ K as a classification range for thermally unstable warm neutral gas. The present cooling curve gives turning points at $184$ and $5039$ K. The upper values agree within $0.8$ per cent and describe the cooling transition relevant to warm gas. The lower values have different definitions, so no quantitative comparison is made there.</span>',
    ),
    (
        "10.1 Confirmed:",
        '<h3 id="confirmed">10.1 The measured median lies inside the standard pressure window</h3>',
    ),
    (
        "10.2 How far the confirmation",
        '<h3>10.2 Sensitivity to the model parameters</h3>',
    ),
    (
        "The confirmation is not robust",
        '<div class="keyresult"><b>The comparison depends on the adopted microphysics.</b> The measured median lies inside four of the five predicted pressure windows. In two cases it sits close to the upper boundary, at $0.970$ and $0.955$ of $P_{\\max}$. For the low-$\\varphi_{\\rm PAH}$ model it exceeds $P_{\\max}=3150\\ \\mathrm{K\\,cm^{-3}}$ by a factor of $1.207$.</div>',
    ),
    (
        "The two tiers must be kept apart.",
        '<p>The source distinguishes excluded variants from merely poorer fits. Two variants are ruled out by the authors, while two others perform worse on independent diagnostics. Only the standard model is not criticised on those grounds, and its predicted interval contains the measured median.</p>',
    ),
    (
        "10.3 Refuted:",
        '<h3 id="refuted">10.3 Cold gas below $P_{\\min}$ contradicts static two-phase equilibrium</h3>',
    ),
    (
        "What is not refuted.",
        '<p>Cold gas above $P_{\\max}$ is allowed because only the warm phase becomes unstable there. The observed $28$ per cent above $P_{\\max}$ therefore does not test the two-phase prediction. The contradiction arises only below $P_{\\min}$, where the static model permits no cold phase.</p>',
    ),
    (
        "Two limits on that sweep.",
        '<span class="warn"><b>Limits of the parameter sweep.</b> Only the fitted static distribution was recomputed for all variants; the measured $29$ per cent below threshold applies to the standard $P_{\\min}$. Jenkins and Tripp also caution that their lognormal fit underestimates material outside $3.2<\\log(p/k)<4.0$. Three variants place $P_{\\min}$ below that range, so their fitted low-pressure fractions are extrapolations and probably underestimates.</span>',
    ),
    (
        "Mixing-length theory is a one-parameter closure",
        '<li>Mixing-length theory contains one calibrated parameter. The value $\\alpha=2$ is fitted to the solar radius. Problem C3 shows that the velocity scales weakly as $\\alpha^{1/3}$, while the superadiabatic excess scales more strongly as $\\alpha^{-4/3}$.</li>',
    ),
    (
        "From (3.1), $N^2",
        '<div>Equation (3.1) gives $N^2=(g/H)(\\nabla_{\\rm ad}-\\nabla)$ with $H=k_BT/(\\mu m_u g)$. Substituting $\\nabla=-(H/T)dT/dz$ and $\\nabla_{\\rm ad}=k_B/(\\mu m_u c_p)$ yields $$N^2=\\frac{g}{T}\\left(\\frac{g}{c_p}+\\frac{dT}{dz}\\right).$$ The bracket compares the dry adiabatic lapse rate with the actual lapse rate. In the isothermal lower stratosphere at $216.65$ K, $N=0.02102\\ \\mathrm{rad\\,s^{-1}}$ and the period is $4.98$ min. In the troposphere at $288.15$ K with the standard lapse rate, $N=0.01053\\ \\mathrm{rad\\,s^{-1}}$ and the period is $9.94$ min. Both layers are stable, with buoyancy periods of order ten minutes.</div>',
    ),
])

apply(7, [
    (
        "Two fluids meet at a surface.",
        '<p class="sub">An interface becomes unstable when a heavy fluid overlies a light one or when the fluids move past each other. A single dispersion relation describes both Rayleigh–Taylor and Kelvin–Helmholtz instability. Surface tension, gravity, shear, viscosity, compressibility, and magnetic tension determine which wavelengths grow. Laboratory examples establish the physical scales before the theory is applied to supernova remnants and coronal mass ejections.</p>',
    ),
    (
        "The hypotheses that will later be paid for",
        '<p>The derivation assumes incompressible, inviscid, semi-infinite fluids separated by a sharp interface. Incompressibility removes acoustic effects, while inviscid flow provides no short-wavelength dissipation. The semi-infinite geometry removes any external length scale, and the discontinuous interface neglects finite-thickness shear. Sections 4, 7, and 9 examine the consequences of these assumptions.</p>',
    ),
    (
        "Equation (3.1) will shortly",
        '<p>Before applying equation (3.1) to astronomical systems, we evaluate five cases with known limiting behaviour. These checks establish the signs, dimensions, and parameter conventions used in the later calculations.</p>',
    ),
    (
        "Proposition 3 (the viscous crossover",
        '<div class="prop"><b>Proposition 3 (viscous crossover estimate).</b> A free-surface wave of wavenumber $k$ in a fluid with kinematic viscosity $\\nu$ is damped at approximately $2\\nu k^2$. Equating this rate to the inviscid growth rate $\\sqrt{Agk}$ gives $$k_\\nu=\\left(\\frac{Ag}{4\\nu^2}\\right)^{1/3},\\qquad \\lambda_\\nu=\\frac{2\\pi}{k_\\nu}.\\tag{4.4}$$ Viscosity is a perturbation for wavelengths above $\\lambda_\\nu$ and becomes dynamically important below it. This estimate locates the crossover but does not solve the full viscous eigenvalue problem.</div>',
    ),
    (
        "What stops the small scales here",
        '<p>In the salt-water experiment, diffusion and viscosity replace capillarity as the short-wavelength regulators. Equation (4.4) gives $\\lambda_\\nu=2.08$ mm, compared with $0.467$ mm for water over air. The factor $4.45$ equals $88^{1/3}$ because $\\lambda_\\nu\\propto A^{-1/3}$. Salt diffusion also broadens the interface, an effect absent from the discontinuous model.</p>',
    ),
    (
        "Two standard cases bracket",
        '<p>Two expansion laws bracket the relevant supernova-remnant range. A Sedov–Taylor blast wave has $m=2/5$, while a young ejecta-driven remnant has $m\\simeq0.7$. Evaluating both shows that the inferred instability scale depends only weakly on this choice.</p>',
    ),
    (
        "This source is a preprint",
        '<span class="warn"><b>Source status.</b> Shimony et al. is available as arXiv:2210.06631v1 and has no journal reference or publisher DOI. The measurements used below are taken directly from that preprint. Its preprint status should be considered when assessing the reported uncertainties and interpretation.</span>',
    ),
    (
        "8.2 Confirmed:",
        '<h3 id="confirmed">8.2 Test of the quadratic mixing law</h3>',
    ),
    (
        "Confirmed. The form $h_B",
        '<div class="keyresult"><b>The experiment supports the quadratic mixing law.</b> Four initial conditions, spanning a factor of two in seed wavelength and including both two- and three-dimensional cases, give late-time widths linear in $x_{\\rm Read}$. The two seed wavelengths give coefficients that differ by $1.00\\sigma$. The experiment tests the form $h_B=\\alpha_BAgt^2$, while the coefficient $\\alpha_B$ remains empirical.</div>',
    ),
    (
        "Refuted. $\\alpha_B",
        '<div class="keyresult"><b>The reported coefficient does not resolve the earlier factor-of-two range.</b> The measurement $\\alpha_B=0.038\\pm0.008$ lies $1.50\\sigma$ below $0.050$ and $1.62\\sigma$ above the inferred simulation value $0.025$. It is statistically consistent with both ends of the range. The measurement is informative, but the claim that it closes the discrepancy is stronger than the stated uncertainty supports.</div>',
    ),
    (
        "Two values that an earlier draft",
        '<span class="warn"><b>Unsupported comparison values are omitted.</b> The preprint does not contain the values $\\alpha_B=0.060$ or $0.077$ sometimes attributed to earlier experiments. The comparison therefore uses only the values documented in the cited source.</span>',
    ),
    (
        "What this anchor does",
        '<div class="keyresult"><b>Scope of the coronal comparison.</b> The observation does not provide an independent measurement of the linear growth rate. It instead yields a magnetic-field bound and tests the consistency of the density, shear, and geometry assumptions. Section 9.5 derives the bound, while the remaining subsections quantify the assumptions that limit its interpretation.</div>',
    ),
    (
        "9.2 Reproduced, not confirmed:",
        '<h3 id="reproduced">9.2 Reproduction of the published growth-rate calculation</h3>',
    ),
    (
        "This is a check on arithmetic",
        '<span class="warn"><b>Internal calculation check.</b> The published rate $0.003$–$0.006\\ \\mathrm{s^{-1}}$ equals $\\tfrac12k\\Delta V$ evaluated with the authors\' own velocities. Reproducing it shows that Proposition 1 reduces to their equation (1) under the same assumptions. Because no growth rate was independently measured, the agreement does not test the solar model.</span>',
    ),
    (
        "One substitution in their own Section 3",
        '<p>The published calculation substitutes the vortex propagation speed, $6$–$14\\ \\mathrm{km\\,s^{-1}}$, for the velocity shear in equation (1). The shear is measured separately as approximately $20\\ \\mathrm{km\\,s^{-1}}$. These quantities differ: Proposition 8 predicts the propagation speed from the shear and density contrast. Using the measured shear instead gives</p>',
    ),
    (
        "Consistent, not discriminating",
        '<div class="keyresult"><b>The propagation-speed observation does not distinguish the density models.</b> The unequal-density prediction is $6.18\\ \\mathrm{km\\,s^{-1}}$, just inside the observed $6$–$14\\ \\mathrm{km\\,s^{-1}}$ interval. The equal-density prediction, $10.00\\ \\mathrm{km\\,s^{-1}}$, also lies inside. The observational interval is too wide to distinguish predictions that differ by a factor of $1.62$.</div>',
    ),
    (
        "9.4 Refuted:",
        '<h3 id="refuted">9.4 Effect of the measured density contrast</h3>',
    ),
    (
        "Refuted, with the paper's own inputs.",
        '<div class="keyresult"><b>The equal-density approximation overestimates the growth rate.</b> Using the reported density ratio and magnetic field reduces the rate to $0.84702$ of the published value. The equal-density estimate is therefore $18.1$ per cent larger than the value obtained from the measured contrast.</div>',
    ),
    (
        "9.6 Refuted:",
        '<h3 id="smooth">9.6 Failure of the vortex-sheet approximation</h3>',
    ),
    (
        "9.7 A counterfactual",
        '<h3 id="counterfactual">9.7 Dependence on interface orientation</h3>',
    ),
    (
        "Long waves are the stabilised ones",
        '<p>Gravity stabilises the long wavelengths in this geometry. The ratio above unity places the observed mode on the stable side by a factor of $1.37$. Because the inputs are accurate only to about a factor of two, the appropriate interpretation is that the mode lies near the cutoff rather than securely beyond it.</p>',
    ),
    (
        "This is a counterfactual",
        '<span class="warn"><b>Interpretation of the geometry test.</b> The calculation changes the observed orientation, so it does not contradict a measurement. It shows that rotating gravity across the interface would place the mode near the stability cutoff. Interface orientation is therefore a controlling physical parameter, not a minor geometrical detail.</span>',
    ),
    (
        "The error is the existence of $T_s$",
        '<div>Salt water and fresh water are miscible, so they have no equilibrium interfacial tension. The value $72.75\\ \\mathrm{dyn\\,cm^{-1}}$ applies to water against air and cannot be used for this pair. With $T_s\\simeq0$, Proposition 2 reduces to $\\sigma=\\sqrt{Agk}$ and has no capillary cutoff. Viscosity instead gives $\\lambda_\\nu=2.08$ mm, while salt diffusion further broadens the interface. For wavelengths above this crossover, the inviscid rates are $8.34\\ \\mathrm{s^{-1}}$ at $1$ cm and $2.64\\ \\mathrm{s^{-1}}$ at $10$ cm.</div>',
    ),
    (
        "Miles (1961) and Howard (1961)",
        '<div>Miles (1961) and Howard (1961) proved that $\\mathrm{Ri}>1/4$ everywhere is sufficient for stability. Its contrapositive makes $\\mathrm{Ri}<1/4$ a necessary, but not sufficient, condition for instability. At $T=220$ K with a $6.0\\ \\mathrm{K\\,km^{-1}}$ lapse rate, the threshold corresponds to a shear of $25.9\\ \\mathrm{m\\,s^{-1}}$ per kilometre. Such shears are common near jet streams, so the criterion identifies regions where turbulence is possible but does not localise individual turbulent patches.</div>',
    ),
    (
        "The derivation is the proof of Proposition 6.",
        '<div>Proposition 6 gives a gravitational cutoff only when the light fluid lies above the dense fluid. A prominence instead places dense material above tenuous corona, so it is Rayleigh–Taylor unstable at every wavelength even without shear. At $\\lambda=1000$ km, $\\sigma=0.04109\\ \\mathrm{s^{-1}}$ and the growth time is $24.3$ s. Reversing the density ordering produces a cutoff wavelength of $92$ km for a $20\\ \\mathrm{km\\,s^{-1}}$ shear. That scale lies below the $435$ km AIA pixel, so the reversed interface would appear stable at observable wavelengths.</div>',
    ),
    (
        "The ambient sound speed is $c_s",
        '<div>The ambient sound speed is $480.6\\ \\mathrm{km\\,s^{-1}}$, so a Mach-5 shear has $\\Delta U=2403\\ \\mathrm{km\\,s^{-1}}$. The incompressible relation gives $1/\\sigma=4.110\\times10^5$ yr, comparable to the $4.069\\times10^5$ yr travel time over 1 kpc. This estimate is not dynamically attainable because $M=5$ exceeds the compressible-stability threshold $2\\sqrt2$. Only sufficiently oblique modes remain, and their projected shear permits at most $0.56$ e-foldings. The example shows why an incompressible dispersion relation must be checked against the sound-speed ordering before it is applied to a supersonic jet.</div>',
    ),
])
