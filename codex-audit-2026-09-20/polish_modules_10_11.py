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


apply(10, [
    (
        "A softer count exists",
        '<p>Using the Kolmogorov turnover time $\\tau_\\eta$ gives $\\mathrm{Re}^{1/2}$ small-eddy turnovers and $\\mathrm{Re}^{11/4}$ updates. A numerical solver must instead use the advection time $\\eta/U$, which is shorter by $$\\frac{U}{u_\\eta}=\\mathrm{Re}^{1/4}.\\tag{3.6}$$ The resulting operation count scales as $\\mathrm{Re}^3$. The table prints both estimates so their different time-step assumptions remain explicit.</p>',
    ),
    (
        "Two more evaluations of (3.1)",
        '<p>Two further evaluations of equation (3.1) illustrate its range of validity. The second deliberately lies outside that range and diagnoses the failure of the cascade assumption.</p>',
    ),
    (
        "Read the second row as a refutation",
        '<div class="warn"><b>The second row has no inertial range.</b> It gives $\\eta/L=1.078$, so the nominal dissipation scale exceeds the system size. The K41 relation $\\varepsilon=U^3/L$ is then inapplicable because it assumes the cascade whose absence the calculation reveals. The same breakdown appears as $\\mathrm{Kn}=0.375$ in Section 6. With the magnetically suppressed viscosity used there, the estimate instead gives $\\eta=3.887$ au, or $3.1\\times10^{-10}$ of the system size.</div>',
    ),
    (
        "Check 2 — CONFIRMED",
        '<div class="keyresult"><b>Check 2: the Kolmogorov constant is approximately universal across the compiled flows.</b> Sreenivasan reports $C_K=0.53\\pm0.055$ for more than 100 flows, a fractional scatter of $10.4$ per cent. The data span $R_\\lambda\\simeq50$ to $10^4$, corresponding to about $4.6$ decades in Reynolds number. K41 does not predict the numerical value $0.53$; it predicts that one dimensionless value should describe many geometries at high Reynolds number. The observed scatter quantifies that universality.</div>',
    ),
    (
        "That number is quoted at second hand",
        '<div class="warn"><b>Source note.</b> The $C_K$ entry comes from Sreenivasan\'s Table IV rather than direct inspection of Grant et al. (1962). Sreenivasan averages seventeen values estimated from log–log plots and notes a possible shift exceeding ten per cent under a different reading. The quoted $R_\\lambda$ range is also his estimate. This entry illustrates the historical value but is not used in later calculations.</div>',
    ),
    (
        "The two bounds differ",
        '<div class="keyresult"><b>The local viscosity bounds span $1.59\\times10^{13}$.</b> This factor is $3.07$ times $\\lambda/r_g$ because Braginskii\'s parallel coefficient uses a different speed convention and carries the numerical factor $0.96$. Neither endpoint is a measured effective viscosity for the intracluster medium. Pressure-anisotropy microinstabilities can increase the scattering rate, so the calculation bounds $\\mathrm{Re}_\\perp$ without assigning it a unique value.</div>',
    ),
    (
        "Kinetic theory's $\\lambda\\bar v/3$",
        '<p>The estimate $\\nu=\\lambda\\bar v/3$ approximates angular transport by a factor of one third. Braginskii (1965) derives the plasma coefficients kinetically. Comparing the two requires separating the numerical transport coefficient from the different definitions of collision time and thermal speed.</p>',
    ),
    (
        "First: what Braginskii's $\\tau_i$ is.",
        '<p>Braginskii defines the ion collision time by $$\\tau_i=\\frac{3\\sqrt{m_i}T_i^{3/2}}{4\\sqrt{\\pi}\\,\\ln\\Lambda\\,e^4Z^4n_i}=4.4126\\times10^{14}\\ \\mathrm{s}.\\tag{6.5}$$ With the Spitzer mean free path, this equals $\\lambda/v_{\\rm rms}$ algebraically. The numerical equality holds to four figures after retaining the unrounded $22.5$ kpc mean free path. This identity fixes the convention; it is not an independent validation of the mean-free-path coefficient.</p>',
    ),
    (
        "Module 2 §9 printed",
        '<p>Module 2 gives $\\mathrm{Re}\\approx14$ for the solar wind at 1 au, whereas the present convention gives $12.34$. The two values use different thermal speeds and collision-time normalisations. Their ratio factorises exactly into those convention choices:</p>',
    ),
    (
        "This is the module's anchor",
        '<p>The solar-wind spectrum provides two tests from one instrument and one fitting interval. The velocity and magnetic fields yield different exponents, so the comparison can distinguish a successful scaling from an unsuccessful one under the same observational conditions.</p>',
    ),
    (
        "7.1 The refutation",
        '<h3 id="velocity-refutation">7.1 Velocity-spectrum disagreement</h3>',
    ),
    (
        "7.2 The confirmation",
        '<h3 id="magnetic-confirmation">7.2 Magnetic-spectrum agreement in the mean</h3>',
    ),
    (
        "Check 1(b) — CONFIRMED",
        '<div class="keyresult"><b>Check 1(b): the mean magnetic index agrees with $5/3$.</b> The mean is $1.6550$, compared with $1.6667$, giving a ratio of $0.9930$. A test of the four intervals gives $t=-0.41$ on three degrees of freedom and $p=0.71$. This supports the mean exponent only; individual intervals need not equal $5/3$. Against $3/2$, the magnetic mean differs by $2.50\\sigma$ while the velocity mean is consistent.</div>',
    ),
    (
        "What is confirmed is an exponent",
        '<div class="warn"><b>The exponent does not identify the cascade mechanism.</b> The observed $5/3$ belongs to a magnetic spectrum in an Alfvénic plasma, whereas Proposition 2 treats incompressible hydrodynamic turbulence. Goldreich and Sridhar obtain the same exponent from anisotropic critical balance. Distinguishing these mechanisms requires anisotropy information, developed in Module 12.</div>',
    ),
    (
        "The assumption, stated before",
        '<div class="warn"><b>Interpretive assumption.</b> A structure function measures velocity differences within one flow as a function of separation. The Solomon et al. exponent instead comes from one linewidth and one size for each of 273 clouds. Comparing it with $\\delta v(\\ell)\\propto\\ell^{1/3}$ assumes that the cloud ensemble samples one statistical cascade. Larson made this identification explicitly, but the following inference remains conditional on it.</div>',
    ),
    (
        "Check 4 — Disagreement",
        '<div class="keyresult"><b>Check 4: the molecular-cloud exponent disagrees with incompressible K41 scaling.</b> The measured exponent is $0.50$, while K41 predicts $1/3$. Their difference, $0.1667$, is $3.33$ times the stated systematic envelope of $\\pm0.05$. Burgers scaling predicts $1/2$ and matches the exponent, although the exponent alone does not select its physical mechanism.</div>',
    ),
    (
        "The exponent refutes Kolmogorov.",
        '<div class="warn"><b>The $1/2$ exponent is not unique to Burgers turbulence.</b> Virial equilibrium at constant surface density also gives $\\sigma_v\\propto S^{1/2}$ because $\\sigma^2\\sim GM/S$ and $M\\sim\\Sigma S^2$. Solomon et al. favour this interpretation using their mean surface density $170\\,M_\\odot\\,\\mathrm{pc^{-2}}$. The linewidth–size exponent therefore excludes the K41 value under the ensemble assumption but does not distinguish a compressive cascade from virial balance.</div>',
    ),
    (
        "Larger than any other row.",
        'The magnetic $5/3$ spectrum is compatible with both K41 and critically balanced MHD turbulence. The exponent agrees; the physical mechanism remains unresolved.',
    ),
    (
        "Nobody addresses it.",
        'No module assigns a unique effective intracluster-medium viscosity. The table records this as an unresolved transport problem.',
    ),
    (
        "Read as a whole",
        '<p>The comparisons reveal an instructive reversal. The magnetic spectrum of a weakly collisional, magnetised solar-wind plasma has a mean index within seven parts in a thousand of $5/3$. The molecular-cloud linewidth relation, in a system better described as a fluid, differs strongly from the K41 exponent. Module 12 explains why an MHD cascade can share the hydrodynamic spectral exponent while differing in geometry.</p>',
    ),
    (
        "The ratio of the two is the Mach number",
        '<p>The ratio of the sound-crossing time to the turnover time is the Mach number, $10.82$. The turnover time governs the cascade and rearrangement of the cloud structure. Sound crosses the region more than ten times too slowly to maintain pressure communication during one turnover.</p>',
    ),
    (
        "That answer must be rejected",
        '<p>The formal value $\\eta=64.67$ kpc exceeds the $60$ kpc system size, giving $\\eta/L=1.078$. No inertial range exists, so $\\eta$ cannot be interpreted as a dissipation scale. The independent value $\\mathrm{Kn}=0.375$ reaches the same conclusion through equation (1.2). Moreover, $\\varepsilon=U^3/L$ already assumes the cascade that this calculation shows to be absent.</p>',
    ),
    (
        "That is $2.46$ times",
        '<p>The required dispersion is $2.46$ times the measured $164\\ \\mathrm{km\\,s^{-1}}$. Because $\\alpha\\propto\\sigma_v^2$, this corresponds to a factor of $6.0$ in the pressure ratio. A twenty-per-cent hydrostatic mass bias is therefore excluded by a wide margin for this core. The result scales as $\\mu^{-1/2}$ and is independent of density.</p>',
    ),
])

apply(11, [
    (
        "the numerical calculation differentiates",
        '<div class="prov"><b>Keplerian shear check.</b> Differentiating the numerical $\\Omega(R)$ profile gives $q=1.5000000000$, compared with the analytic value $3/2$. This derives the shear parameter used in Module 12 from the Keplerian rotation law rather than assuming it.</div>',
    ),
    (
        "Three quantities in this calculation",
        '<p>Reasonable transport conventions change the molecular viscosity by less than one decade. Using the mixture mass instead of the ion mass contributes a factor $1.2957$. Doubling the Coulomb logarithm contributes $0.5$, and using $n_i=n/2$ contributes another $0.5$. Together these changes reduce the discrepancy from $12.01$ to $11.71$ decades. No convention within the molecular transport coefficient approaches the observed viscous timescale.</p>',
    ),
    (
        "The dwarf-nova parameters are a configuration",
        '<div class="prov"><b>Status of the dwarf-nova example.</b> The adopted $M=0.6\\,M_\\odot$, $R=10^{10}\\ \\mathrm{cm}$, $T=3\\times10^4$ K, $\\Sigma=100\\ \\mathrm{g\\,cm^{-2}}$, and five-day outburst are representative round values rather than a fit to one named system. Changing them within the observed class range affects the detailed ratio but not the twelve-decade failure of molecular viscosity.</div>',
    ),
    (
        "The algebra in the last two lines",
        '<div class="prov"><b>Source note.</b> Pringle (1981) gives the standard angular-momentum derivation of equation (5.1). The equation is reproduced here because the viscous timescale in Section 6 is its diffusion time. No numerical result depends on importing a value from that review.</div>',
    ),
    (
        "The argument behind the bound is short.",
        '<p>The bound follows from the size and speed of turbulent motions within a thin disc. Eddies much larger than $H$ leave the disc, while motions much faster than $c_T$ shock and dissipate. Thus $\\nu\\lesssim c_TH$ and $\\alpha\\lesssim1$. This is a dimensional bound on the prescription, not a derivation of the stress.</p>',
    ),
    (
        "Proposition 7 (what \"thin\" means",
        '<div class="prop"><b>Proposition 7 (thin-disc condition).</b> Dividing $H=c_T/\\Omega$ by $R$ gives $$\\frac{H}{R}=\\frac{c_T}{v_K}.\\tag{7.2}$$ A disc is geometrically thin when its thermal speed is small compared with its orbital speed.</div>',
    ),
    (
        "CHECK 2 — CONFIRMED",
        '<div class="keyresult"><b>Check 2: observed cataclysmic-variable discs support the $R^{-3/4}$ temperature profile.</b> The exponent contains no $\\nu$, $\\alpha$, or $\\Sigma$ because these cancel between equations (8.1) and (8.2). King, Pringle, and Livio describe reasonable agreement with continuum spectra and eclipse mapping. The numerical profile here has slope $-0.74902$ at $10^5R_g$, but the review gives no fitted exponent or uncertainty. The evidence therefore supports the radial shape rather than four-digit agreement in the slope.</div>',
    ),
    (
        "Neither number is retyped from memory",
        '<div class="prov"><b>Extreme-Kerr evaluation.</b> The efficiencies are calculated from the orbit-energy formulae of Bardeen, Press, and Teukolsky rather than quoted from their text. Their general expression becomes $0/0$ at $a=M$ and $r=M$, so the extreme limit must use their separate equation (2.14). Evaluating the generic expression exactly at that point is undefined, reflecting the singular Boyer–Lindquist-coordinate limit rather than a physical divergence.</div>',
    ),
    (
        "CHECK 3 — CONFIRMED",
        '<div class="keyresult"><b>Check 3: the calculated relativistic efficiencies agree with contemporary published estimates.</b> Shakura and Sunyaev quote $\\eta\\simeq0.06$ for a Schwarzschild black hole and up to $40$ per cent for a Kerr black hole. The values computed here from the 1972 orbit formulae differ by $4.7$ and $5.7$ per cent, respectively.</div>',
    ),
    (
        "The price of a Newtonian book",
        '<div class="warn"><b>Limit of the Newtonian efficiency.</b> At $6R_g$, the Newtonian value $1/12$ exceeds the relativistic Schwarzschild efficiency $1-\\sqrt{8/9}$ by a factor of $1.4571$. Gravitational redshift and relativistic orbital binding are already important at this radius. Equation (9.1) should therefore be treated as a Newtonian estimate rather than a black-hole efficiency.</div>',
    ),
    (
        "Everything so far has assumed",
        '<p>The preceding derivation neglects the disc\'s self-gravity. Rotation stabilises long wavelengths, while sufficiently strong disc gravity destabilises them. The next section combines these effects in the local axisymmetric dispersion relation.</p>',
    ),
    (
        "The coefficient $\\pi$ is derived",
        '<div class="warn"><b>Gas and stellar Toomre coefficients differ.</b> The gas calculation above gives the coefficient $\\pi$. Toomre (1964) analysed a collisionless stellar disc and obtained $3.36$ in his equation (65), a seven-per-cent difference. The two coefficients reflect different distribution functions and response physics. The gas criterion is conventionally called the Toomre criterion, with Safronov (1960) providing an earlier gaseous precedent.</div>',
    ),
    (
        "That radius is a LOWER BOUND",
        '<div class="warn"><b>The self-gravity radius is a lower bound.</b> In an optically thick disc, $T_{\\rm mid}^4=(3/4)\\tau T_{\\rm eff}^4$ with $\\tau=\\kappa_{\\rm op}\\Sigma/2$. Thus $T_{\\rm mid}>T_{\\rm eff}$ when $\\tau>4/3$, increasing $c_T$ and $Q$ at a given radius. The radius where $Q=1$ then moves outward. The present estimate shows only that the $10^8M_\\odot$ disc becomes self-gravitating no closer than $7\\times10^{-4}$ pc; locating the transition requires vertical radiative transfer and a self-gravitating disc model.</div>',
    ),
    (
        "The first draft of the numerical calculation",
        '<div class="prov"><b>Universality of the magnetic-stress estimate.</b> Equation (11.1) gives $1.026040$ for both illustrative discs because every disc property cancels from the ratio. It is therefore a general order-of-magnitude bound rather than a census result. The identification $B^2\\sim4\\pi\\alpha P$ is approximate; simulations commonly place the Maxwell stress near $0.3B^2/4\\pi$ rather than $B^2/4\\pi$.</div>',
    ),
    (
        "What is refuted is not the prescription.",
        '<p>Equation (6.1) defines $\\alpha$ and remains useful. The observations exclude only the interpretation of $\\alpha$ as a universal constant. Shakura and Sunyaev require $\\alpha\\lesssim1$ and note that the observable disc spectrum depends only weakly on its chosen value.</p>',
    ),
    (
        "Module 2 §11 promises",
        'Modules 2 and 9 point to two-temperature and radiatively inefficient accretion flows. Such flows are geometrically thick and require separate ion and electron energy equations. They lie outside the thin, one-temperature framework developed here.',
    ),
    (
        "Refused in print, here.",
        'Oblique magnetohydrodynamic shock conditions are outside the scope of this volume. Applying the disc or MHD results to such shocks requires the full magnetic jump conditions.',
    ),
])
